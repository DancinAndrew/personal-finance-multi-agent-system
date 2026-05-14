<template>
  <main class="app-shell">
    <section class="workspace-header">
      <div>
        <p class="eyebrow">AIASE Final Project MVP</p>
        <h1>台股多代理投資研究工作台</h1>
        <p class="subhead">以群聯電子 8299 為範例，展示資料來源、LLMWiki-lite、代理執行軌跡、研究報告與評估。</p>
      </div>
      <div class="status-strip">
        <span>本機 fixture</span>
        <span>Deterministic agents</span>
        <span>非即時行情</span>
      </div>
    </section>

    <section class="task-bar" aria-label="研究任務">
      <label>
        標的
        <input v-model="targetName" type="text" />
      </label>
      <label>
        研究問題
        <input v-model="question" type="text" />
      </label>
      <label class="price-field">
        示範股價
        <input v-model.number="price" inputmode="numeric" pattern="[0-9]*" type="text" />
      </label>
      <button type="button" :disabled="loading" @click="runResearch">
        {{ loading ? '執行中' : '啟動研究' }}
      </button>
    </section>

    <p v-if="error" class="error-message">{{ error }}</p>

    <section v-if="result" class="summary-band">
      <div>
        <span class="label">Run</span>
        <strong>{{ result.run.id }}</strong>
      </div>
      <div>
        <span class="label">Evaluation</span>
        <strong>{{ result.evaluation.total_score }} / 5</strong>
      </div>
      <div>
        <span class="label">Price fixture</span>
        <strong>{{ formatPrice(result.run.price_fixture.price) }}</strong>
      </div>
      <div>
        <span class="label">Status</span>
        <strong>{{ result.evaluation.status }}</strong>
      </div>
      <div>
        <span class="label">Health gaps</span>
        <strong>{{ healthGapSummary }}</strong>
      </div>
    </section>

    <section v-if="result" class="workspace-grid">
      <aside class="timeline-panel" aria-label="代理執行軌跡">
        <div class="panel-heading">
          <h2>Agent Trace</h2>
          <span>{{ result.steps.length }} steps</span>
        </div>
        <button
          v-for="step in result.steps"
          :key="step.id"
          class="timeline-step"
          :class="{ active: selectedStep?.id === step.id }"
          type="button"
          @click="selectedStep = step"
        >
          <span class="step-agent">{{ step.agent }}</span>
          <span class="step-summary">{{ step.output_summary }}</span>
          <span class="step-meta">{{ step.confidence }} confidence · {{ step.latency_ms }} ms</span>
        </button>
      </aside>

      <section class="report-panel" aria-label="研究報告">
        <div class="panel-heading">
          <h2>Research Report</h2>
          <span>{{ result.run.price_fixture.display_note }}</span>
        </div>
        <article class="report-content" v-html="renderMarkdown(result.report.report_markdown)"></article>
      </section>

      <aside class="detail-panel" aria-label="細節">
        <div class="tabs" role="tablist">
          <button :class="{ active: activeTab === 'step' }" type="button" @click="activeTab = 'step'">Step</button>
          <button :class="{ active: activeTab === 'sources' }" type="button" @click="activeTab = 'sources'">Sources</button>
          <button :class="{ active: activeTab === 'health' }" type="button" @click="activeTab = 'health'">Health</button>
          <button :class="{ active: activeTab === 'wiki' }" type="button" @click="activeTab = 'wiki'">Wiki</button>
          <button :class="{ active: activeTab === 'eval' }" type="button" @click="activeTab = 'eval'">Eval</button>
        </div>

        <section v-if="activeTab === 'step'" class="tab-body">
          <h3>{{ selectedStep?.agent || '選擇一個 step' }}</h3>
          <dl v-if="selectedStep" class="definition-list">
            <dt>Input</dt>
            <dd>{{ selectedStep.input_summary }}</dd>
            <dt>Output</dt>
            <dd>{{ selectedStep.output_summary }}</dd>
            <dt>Sources</dt>
            <dd>{{ selectedStep.source_ids.length ? selectedStep.source_ids.join(', ') : '無直接來源' }}</dd>
            <dt>Cost</dt>
            <dd>{{ selectedStep.cost_usd === 0 ? '0 USD（deterministic）' : selectedStep.cost_usd }}</dd>
          </dl>
        </section>

        <section v-if="activeTab === 'sources'" class="tab-body source-list">
          <h3>Source Map</h3>
          <article v-for="source in result.sources" :key="source.id" class="source-row">
            <div>
              <strong>{{ source.id }} · {{ source.title }}</strong>
              <p>{{ source.reliability_note }}</p>
            </div>
            <a :href="source.url_or_path" target="_blank" rel="noreferrer">{{ source.source_type }}</a>
          </article>
        </section>

        <section v-if="activeTab === 'health'" class="tab-body">
          <h3>Health Check</h3>
          <p class="tab-note">public fixture only · 缺資料時保留 unknown / not_available</p>
          <article v-for="check in result.analysis.health_checks.checks" :key="check.id" class="health-row">
            <div class="health-row-header">
              <strong>{{ check.name }}</strong>
              <span class="status-chip" :class="`status-${check.status}`">{{ check.status }}</span>
            </div>
            <p>{{ check.status_reason }}</p>
            <dl class="health-meta">
              <dt>Takeaway</dt>
              <dd>{{ check.report_takeaway }}</dd>
              <dt>Missing</dt>
              <dd>{{ check.missing_data.join('、') }}</dd>
              <dt>Sources</dt>
              <dd>{{ formatSourceIds(check.source_ids) }}</dd>
            </dl>
          </article>
        </section>

        <section v-if="activeTab === 'wiki'" class="tab-body">
          <h3>LLMWiki-lite</h3>
          <select v-model="selectedWikiName">
            <option v-for="page in result.wiki.pages" :key="page.name" :value="page.name">{{ page.name }}</option>
          </select>
          <article class="wiki-content" v-html="renderMarkdown(selectedWikiContent)"></article>
          <h4>Provenance</h4>
          <ul class="provenance-list">
            <li v-for="claim in result.wiki.provenance" :key="claim.claim_id">
              <strong>{{ claim.claim_id }}</strong>
              <span>{{ claim.source_ids.join(', ') }} · {{ claim.status }}</span>
            </li>
          </ul>
        </section>

        <section v-if="activeTab === 'eval'" class="tab-body">
          <h3>Evaluation</h3>
          <div class="score-box">
            <strong>{{ result.evaluation.total_score }} / 5</strong>
            <span>threshold {{ result.evaluation.threshold }}</span>
          </div>
          <article v-for="dimension in result.evaluation.dimensions" :key="dimension.id" class="dimension-row">
            <span>{{ dimension.name }}</span>
            <strong>{{ dimension.score }}</strong>
          </article>
          <h4>Notes</h4>
          <ul>
            <li v-for="note in result.evaluation.notes" :key="note">{{ note }}</li>
          </ul>
        </section>
      </aside>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { createResearchRun, fetchDefaultRun } from './api'

const defaultQuestion = '人工智慧固態硬碟成長故事是否足以支撐目前估值？'

const result = ref(null)
const selectedStep = ref(null)
const selectedWikiName = ref('')
const activeTab = ref('step')
const loading = ref(false)
const error = ref('')
const targetName = ref('群聯電子（8299）')
const question = ref(defaultQuestion)
const price = ref(2430)

const selectedWikiContent = computed(() => {
  if (!result.value) return ''
  return result.value.wiki.pages.find((page) => page.name === selectedWikiName.value)?.content || ''
})

const healthGapSummary = computed(() => {
  const summary = result.value?.analysis?.health_checks?.summary
  if (!summary) return 'N/A'
  return `${summary.unknown} unknown / ${summary.not_available} N/A`
})

watch(result, (next) => {
  if (!next) return
  selectedStep.value = next.steps[0]
  selectedWikiName.value = next.wiki.pages[0]?.name || ''
  price.value = next.run.price_fixture.price
})

onMounted(async () => {
  await loadDefaultRun()
})

async function loadDefaultRun() {
  loading.value = true
  error.value = ''
  try {
    result.value = await fetchDefaultRun()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function runResearch() {
  loading.value = true
  error.value = ''
  try {
    result.value = await createResearchRun({
      question: question.value,
      price: price.value,
      target: {
        ticker: '8299',
        name: targetName.value,
        market: 'TW_OTC'
      }
    })
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function formatPrice(value) {
  return new Intl.NumberFormat('zh-TW', {
    style: 'currency',
    currency: 'TWD',
    maximumFractionDigits: 0
  }).format(value)
}

function formatSourceIds(sourceIds) {
  return sourceIds.length ? sourceIds.join(', ') : '無直接來源'
}

function renderMarkdown(markdown) {
  return markdown
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^\|(.+)\|$/gm, '<pre class="markdown-table">|$1|</pre>')
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n{2,}/g, '</p><p>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>')
}
</script>

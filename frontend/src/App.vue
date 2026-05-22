<template>
  <main class="app-shell">
    <section class="workspace-header">
      <div>
        <p class="eyebrow">AIASE Final Project MVP</p>
        <h1>台股多代理投資研究工作台</h1>
        <p class="subhead">以群聯電子 8299 為範例，展示資料來源、evidence pack、代理執行軌跡、研究報告與評估。</p>
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
      <div>
        <span class="label">Fundamentals</span>
        <strong>{{ fundamentalCoverageSummary }}</strong>
      </div>
      <div>
        <span class="label">Valuation</span>
        <strong>{{ valuationCoverageSummary }}</strong>
      </div>
      <div>
        <span class="label">Chip</span>
        <strong>{{ chipCoverageSummary }}</strong>
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
          <button :class="{ active: activeTab === 'valuation' }" type="button" @click="activeTab = 'valuation'">Valuation</button>
          <button :class="{ active: activeTab === 'chip' }" type="button" @click="activeTab = 'chip'">Chip</button>
          <button :class="{ active: activeTab === 'health' }" type="button" @click="activeTab = 'health'">Health</button>
          <button :class="{ active: activeTab === 'fundamentals' }" type="button" @click="activeTab = 'fundamentals'">Fundamentals</button>
          <button :class="{ active: activeTab === 'evidence' }" type="button" @click="activeTab = 'evidence'">Evidence</button>
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

        <section v-if="activeTab === 'valuation'" class="tab-body">
          <h3>Valuation</h3>
          <p class="tab-note">public fixture only · 非即時行情 · 目標價與 Forward P/E 只作情境敏感度</p>
          <div class="fundamental-summary">
            <span>估值覆蓋</span>
            <strong>{{ valuationCoverageSummary }}</strong>
          </div>
          <dl class="valuation-meta">
            <dt>示範股價</dt>
            <dd>{{ formatPrice(valuationSummary.price || 0) }} · {{ valuationSummary.price_as_of_date }}</dd>
            <dt>主要缺口</dt>
            <dd>{{ valuationSummary.major_gaps?.join('、') || 'N/A' }}</dd>
          </dl>

          <h4>Forward P/E 情境</h4>
          <article v-for="scenario in valuationScenarios" :key="scenario.id" class="valuation-row">
            <div class="health-row-header">
              <strong>{{ scenario.label }}</strong>
              <span class="status-chip status-partial">{{ scenario.forward_pe }}x</span>
            </div>
            <dl class="health-meta">
              <dt>EPS</dt>
              <dd>{{ Number(scenario.eps).toFixed(2) }} 元</dd>
              <dt>Sources</dt>
              <dd>{{ formatSourceIds(scenario.source_ids) }}</dd>
              <dt>解讀</dt>
              <dd>{{ scenario.interpretation }}</dd>
            </dl>
          </article>

          <h4>券商目標價摘要</h4>
          <article v-for="target in brokerTargets" :key="target.id" class="valuation-row">
            <div class="health-row-header">
              <strong>{{ target.source_label }}</strong>
              <span class="status-chip status-partial">{{ target.date }}</span>
            </div>
            <dl class="health-meta">
              <dt>目標價</dt>
              <dd>{{ formatTargetPrice(target) }}</dd>
              <dt>敏感度</dt>
              <dd>{{ formatTargetSensitivity(target) }}</dd>
              <dt>Sources</dt>
              <dd>{{ formatSourceIds(target.source_ids) }}</dd>
              <dt>限制</dt>
              <dd>{{ target.reliability_note }}</dd>
            </dl>
          </article>

          <h4>缺口資料</h4>
          <ul class="gap-list">
            <li v-for="gap in valuationDataGaps" :key="gap">{{ gap }}</li>
          </ul>
        </section>

        <section v-if="activeTab === 'chip'" class="tab-body">
          <h3>Chip</h3>
          <p class="tab-note">public fixture only · 目前只呈現籌碼資料覆蓋與缺口，不判斷偏多偏空</p>
          <div class="fundamental-summary">
            <span>整體訊號</span>
            <strong>{{ chipSummary.overall_signal || 'N/A' }}</strong>
          </div>
          <dl class="valuation-meta">
            <dt>覆蓋狀態</dt>
            <dd>{{ chipCoverageSummary }}</dd>
            <dt>主要缺口</dt>
            <dd>{{ chipSummary.major_gaps?.join('、') || 'N/A' }}</dd>
          </dl>

          <article v-for="signal in chipSignals" :key="signal.id" class="chip-row">
            <div class="health-row-header">
              <strong>{{ signal.name }}</strong>
              <span class="status-chip" :class="`status-${signal.coverage_status}`">
                {{ signal.coverage_status }}
              </span>
            </div>
            <p>{{ signal.summary }}</p>
            <dl class="health-meta">
              <dt>Signal</dt>
              <dd>
                <span class="status-chip" :class="`status-${signal.signal_bias}`">
                  {{ signal.signal_bias }}
                </span>
              </dd>
              <dt>Window</dt>
              <dd>{{ signal.lookback_window }}</dd>
              <dt>Missing</dt>
              <dd>{{ signal.missing_data.join('、') }}</dd>
              <dt>Sources</dt>
              <dd>{{ formatSourceIds(signal.source_ids) }}</dd>
            </dl>
          </article>

          <h4>Interpretation</h4>
          <ul class="gap-list">
            <li v-for="item in chipInterpretation" :key="item">{{ item }}</li>
          </ul>
        </section>

        <section v-if="activeTab === 'fundamentals'" class="tab-body">
          <h3>Fundamentals</h3>
          <p class="tab-note">public fixture only · available / partial / missing 分開呈現</p>
          <div class="fundamental-summary">
            <span>五大面向</span>
            <strong>{{ fundamentalCoverageSummary }}</strong>
          </div>
          <article
            v-for="category in fundamentalCategories"
            :key="category.id"
            class="fundamental-row"
          >
            <div class="health-row-header">
              <strong>{{ category.name }}</strong>
              <span class="status-chip" :class="`status-${category.coverage_status}`">
                {{ category.coverage_status }}
              </span>
            </div>
            <p>{{ category.category_takeaway }}</p>
            <dl class="health-meta">
              <dt>Metrics</dt>
              <dd>
                <ul class="metric-list">
                  <li v-for="metric in category.metrics" :key="metric.id">
                    <div>
                      <strong>{{ metric.label }}</strong>
                      <span>{{ formatMetricValue(metric) }}</span>
                    </div>
                    <span class="status-chip" :class="`status-${metric.coverage_status}`">
                      {{ metric.coverage_status }}
                    </span>
                    <small>{{ formatSourceIds(metric.source_ids) }} · {{ metric.interpretation }}</small>
                  </li>
                </ul>
              </dd>
              <dt>Missing</dt>
              <dd>{{ category.missing_data.join('、') }}</dd>
            </dl>
          </article>
        </section>

        <section v-if="activeTab === 'evidence'" class="tab-body">
          <h3>Evidence Pack</h3>
          <select v-model="selectedEvidenceName">
            <option v-for="page in result.evidence.pages" :key="page.name" :value="page.name">{{ page.name }}</option>
          </select>
          <article class="evidence-content" v-html="renderMarkdown(selectedEvidenceContent)"></article>
          <h4>Provenance</h4>
          <ul class="provenance-list">
            <li v-for="claim in result.evidence.provenance" :key="claim.claim_id">
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
const selectedEvidenceName = ref('')
const activeTab = ref('step')
const loading = ref(false)
const error = ref('')
const targetName = ref('群聯電子（8299）')
const question = ref(defaultQuestion)
const price = ref(2430)

const selectedEvidenceContent = computed(() => {
  if (!result.value) return ''
  return result.value.evidence.pages.find((page) => page.name === selectedEvidenceName.value)?.content || ''
})

const healthGapSummary = computed(() => {
  const summary = result.value?.analysis?.health_checks?.summary
  if (!summary) return 'N/A'
  return `${summary.unknown} unknown / ${summary.not_available} N/A`
})

const fundamentalCategories = computed(() => {
  return result.value?.analysis?.fundamentals?.categories || []
})

const fundamentalCoverageSummary = computed(() => {
  const summary = result.value?.analysis?.fundamentals?.summary
  if (!summary) return 'N/A'
  return `${summary.partial} partial / ${summary.missing} missing`
})

const valuationSummary = computed(() => {
  return result.value?.analysis?.valuation?.summary || {}
})

const valuationCoverageSummary = computed(() => {
  const coverage = valuationSummary.value?.coverage
  if (!coverage) return 'N/A'
  return `${coverage.partial} partial / ${coverage.missing} missing`
})

const valuationScenarios = computed(() => {
  return result.value?.analysis?.valuation?.scenarios || []
})

const brokerTargets = computed(() => {
  return result.value?.analysis?.valuation?.broker_targets || []
})

const valuationDataGaps = computed(() => {
  return result.value?.analysis?.valuation?.data_gaps || []
})

const chipSummary = computed(() => {
  return result.value?.analysis?.chip?.summary || {}
})

const chipSignals = computed(() => {
  return result.value?.analysis?.chip?.signals || []
})

const chipCoverageSummary = computed(() => {
  const summary = chipSummary.value
  const coverage = summary?.coverage
  if (!coverage) return 'N/A'
  return `${summary.overall_signal} / ${coverage.missing} missing / ${coverage.not_available} N/A`
})

const chipInterpretation = computed(() => {
  return result.value?.analysis?.chip?.interpretation || []
})

watch(result, (next) => {
  if (!next) return
  selectedStep.value = next.steps[0]
  selectedEvidenceName.value = next.evidence.pages[0]?.name || ''
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
  const ids = sourceIds || []
  return ids.length ? ids.join(', ') : '無直接來源'
}

function formatMetricValue(metric) {
  if (metric.value === null || metric.value === undefined) return '缺資料'
  if (metric.unit === 'TWD_BN') return `${Number(metric.value).toFixed(2)} 十億元`
  if (metric.unit === 'TWD') return `${Number(metric.value).toFixed(2)} 元`
  if (metric.unit === 'percent') return `${Number(metric.value).toFixed(2)}%`
  return `${metric.value} ${metric.unit}`
}

function formatTargetPrice(target) {
  if (target.target_price_range) {
    return `${formatPrice(target.target_price_range.low)} 到 ${formatPrice(target.target_price_range.high)}`
  }
  return formatPrice(target.target_price)
}

function formatTargetSensitivity(target) {
  if (target.target_price_range) {
    return `${formatPercent(target.low_upside_pct)} 到 ${formatPercent(target.high_upside_pct)}`
  }
  return formatPercent(target.upside_pct)
}

function formatPercent(value) {
  if (value === null || value === undefined) return 'N/A'
  return `${Number(value) >= 0 ? '+' : ''}${Number(value).toFixed(1)}%`
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

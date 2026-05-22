import { spawn } from 'node:child_process'
import { mkdir } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

import { chromium } from 'playwright'

const __dirname = dirname(fileURLToPath(import.meta.url))
const frontendRoot = resolve(__dirname, '..')
const repoRoot = resolve(frontendRoot, '..')
const backendPort = Number(process.env.BACKEND_PORT || 8000)
const frontendPort = Number(process.env.FRONTEND_PORT || 5173)
const backendUrl = `http://127.0.0.1:${backendPort}`
const frontendUrl = `http://127.0.0.1:${frontendPort}`
const artifactsDir = resolve(frontendRoot, 'test-results', 'technical-tab')

const children = []

process.on('SIGINT', async () => {
  await stopChildren()
  process.exit(130)
})

process.on('SIGTERM', async () => {
  await stopChildren()
  process.exit(143)
})

try {
  await mkdir(artifactsDir, { recursive: true })
  await run()
} catch (error) {
  console.error(error instanceof Error ? error.message : error)
  process.exitCode = 1
} finally {
  await stopChildren()
}

async function run() {
  startProcess('backend', 'python3', ['-m', 'backend.app'], repoRoot)
  startProcess('frontend', 'npm', ['run', 'dev', '--', '--host', '127.0.0.1', '--port', String(frontendPort)], frontendRoot)

  await waitForUrl(`${backendUrl}/api/health`, 'Flask API')
  await waitForUrl(frontendUrl, 'Vue dev server')

  const browser = await chromium.launch({ headless: true })
  try {
    const results = []
    results.push(
      await verifyViewport(browser, {
        name: 'desktop',
        width: 1280,
        height: 900,
      }),
    )
    results.push(
      await verifyViewport(browser, {
        name: 'mobile',
        width: 390,
        height: 844,
      }),
    )
    console.log(JSON.stringify({ ok: true, results }, null, 2))
  } finally {
    await browser.close()
  }
}

function startProcess(label, command, args, cwd) {
  const child = spawn(command, args, {
    cwd,
    env: {
      ...process.env,
      FLASK_RUN_PORT: String(backendPort),
    },
    stdio: ['ignore', 'pipe', 'pipe'],
  })
  children.push(child)

  child.stdout.on('data', (chunk) => {
    process.stdout.write(`[${label}] ${chunk}`)
  })
  child.stderr.on('data', (chunk) => {
    process.stderr.write(`[${label}] ${chunk}`)
  })
  child.on('exit', (code, signal) => {
    if (code !== 0 && code !== null && process.exitCode !== 1) {
      console.error(`[${label}] exited with code ${code}`)
    }
    if (signal && signal !== 'SIGTERM') {
      console.error(`[${label}] exited with signal ${signal}`)
    }
  })
}

async function waitForUrl(url, label) {
  const deadline = Date.now() + 30_000
  let lastError = ''
  while (Date.now() < deadline) {
    try {
      const response = await fetch(url)
      if (response.ok) return
      lastError = `${response.status} ${response.statusText}`
    } catch (error) {
      lastError = error instanceof Error ? error.message : String(error)
    }
    await sleep(250)
  }
  throw new Error(`Timed out waiting for ${label} at ${url}: ${lastError}`)
}

async function verifyViewport(browser, viewport) {
  const page = await browser.newPage({
    viewport: {
      width: viewport.width,
      height: viewport.height,
    },
  })

  try {
    await page.goto(frontendUrl, { waitUntil: 'networkidle' })
    await page.getByRole('button', { name: 'Technical' }).click()

    const detailPanel = page.locator('.detail-panel')
    const detailText = await detailPanel.innerText()
    const summaryText = await page.locator('.summary-band').innerText()
    const rowCount = await detailPanel.locator('.chip-row').count()
    const errorCount = await page.locator('.error-message').count()

    assertIncludes(summaryText, 'Technical', `${viewport.name} summary band`)
    assertIncludes(detailText, 'Technical', `${viewport.name} detail panel`)
    assertIncludes(detailText, 'not_evaluable', `${viewport.name} overall signal`)
    assertIncludes(detailText, 'manual_public_snapshot_only', `${viewport.name} data policy`)
    for (const label of ['價格趨勢', '量能趨勢', '均線結構', '動能', '波動風險']) {
      assertIncludes(detailText, label, `${viewport.name} technical signal`)
    }
    if (rowCount !== 5) {
      throw new Error(`${viewport.name} expected 5 technical rows, got ${rowCount}`)
    }
    if (errorCount !== 0) {
      throw new Error(`${viewport.name} rendered ${errorCount} error messages`)
    }

    const overflow = await page.evaluate(() => {
      const root = document.querySelector('.detail-panel')
      if (!root) return [{ selector: '.detail-panel', text: 'missing detail panel' }]

      return Array.from(root.querySelectorAll('*'))
        .filter((element) => {
          const style = window.getComputedStyle(element)
          const scrollable = ['auto', 'scroll'].includes(style.overflowX)
          return !scrollable && element.scrollWidth > element.clientWidth + 1
        })
        .map((element) => ({
          selector: element.className ? `.${String(element.className).trim().replaceAll(' ', '.')}` : element.tagName.toLowerCase(),
          text: (element.textContent || '').trim().slice(0, 80),
          scrollWidth: element.scrollWidth,
          clientWidth: element.clientWidth,
        }))
    })
    if (overflow.length > 0) {
      throw new Error(`${viewport.name} has horizontal overflow: ${JSON.stringify(overflow, null, 2)}`)
    }

    const screenshotPath = resolve(artifactsDir, `${viewport.name}.png`)
    await page.screenshot({ path: screenshotPath, fullPage: true })

    return {
      viewport: viewport.name,
      size: `${viewport.width}x${viewport.height}`,
      technicalRows: rowCount,
      overflowCount: overflow.length,
      screenshot: screenshotPath,
    }
  } finally {
    await page.close()
  }
}

function assertIncludes(text, expected, context) {
  if (!text.includes(expected)) {
    throw new Error(`${context} missing expected text: ${expected}`)
  }
}

function sleep(ms) {
  return new Promise((resolveSleep) => {
    setTimeout(resolveSleep, ms)
  })
}

async function stopChildren() {
  for (const child of children.toReversed()) {
    if (!child.killed) {
      child.kill('SIGTERM')
    }
  }
  await sleep(300)
}

"""Deterministic agents for the MVP demo."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable


EPS_ASSUMPTIONS = [
    {
        "id": "factset_low",
        "label": "FactSet low",
        "eps": 134.78,
        "source_ids": ["S5"],
        "interpretation": "若市場採低標，估值壓力最大。",
    },
    {
        "id": "factset_median",
        "label": "FactSet median",
        "eps": 184.73,
        "source_ids": ["S5"],
        "interpretation": "較保守的市場共識中樞。",
    },
    {
        "id": "factset_average",
        "label": "FactSet average",
        "eps": 192.4,
        "source_ids": ["S5"],
        "interpretation": "適合和新聞中的整體共識比較。",
    },
    {
        "id": "factset_high",
        "label": "FactSet high",
        "eps": 276.05,
        "source_ids": ["S5"],
        "interpretation": "高標仍低於群益 05/07 摘要。",
    },
    {
        "id": "capital_aggressive",
        "label": "Capital 2026-05-07",
        "eps": 307.99,
        "source_ids": ["S4"],
        "interpretation": "需要 AI SSD 與 NAND 價格循環持續兌現。",
    },
    {
        "id": "q1_naive_annualized",
        "label": "Q1 naive annualized",
        "eps": 275.2,
        "source_ids": ["S3"],
        "interpretation": "只能當粗略 sanity check，不得直接當全年預估。",
    },
]


@dataclass(frozen=True)
class AgentResult:
    """Single deterministic agent result."""

    step: dict[str, Any]
    payload: dict[str, Any]


def timed_step(
    *,
    agent: str,
    run_id: str,
    input_summary: str,
    source_ids: list[str],
    confidence: float,
    work: Callable[[], tuple[str, dict[str, Any]]],
) -> AgentResult:
    """Run deterministic work and wrap it in a trace step."""

    started = perf_counter()
    output_summary, payload = work()
    latency_ms = max(1, round((perf_counter() - started) * 1000))
    return AgentResult(
        step={
            "id": f"step_{agent}",
            "run_id": run_id,
            "agent": agent,
            "status": "completed",
            "input_summary": input_summary,
            "output_summary": output_summary,
            "source_ids": source_ids,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "cost_usd": 0,
        },
        payload=payload,
    )


class IntentRouter:
    """Route a request into the Taiwan-equity research workflow."""

    def run(self, run_id: str, question: str, target: dict[str, Any]) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            in_scope = target.get("ticker") == "8299" or "群聯" in question
            route = "taiwan_equity_research" if in_scope else "out_of_scope"
            return (
                "辨識為台股單一個股研究任務，啟動群聯 deterministic research pipeline。",
                {"route": route, "in_scope": in_scope},
            )

        return timed_step(
            agent="intent_router",
            run_id=run_id,
            input_summary=f"question={question}; target={target.get('ticker')}",
            source_ids=[],
            confidence=0.96,
            work=work,
        )


class SourceRetrieval:
    """Return curated sources and research wiki context."""

    def run(
        self,
        run_id: str,
        sources: list[dict[str, Any]],
        wiki_pages: list[dict[str, str]],
        provenance: list[dict[str, Any]],
    ) -> AgentResult:
        source_ids = [source["id"] for source in sources]

        def work() -> tuple[str, dict[str, Any]]:
            return (
                f"載入 {len(sources)} 筆 curated sources、{len(wiki_pages)} 個 wiki pages 與 {len(provenance)} 筆 provenance。",
                {
                    "source_count": len(sources),
                    "wiki_page_count": len(wiki_pages),
                    "provenance_count": len(provenance),
                },
            )

        return timed_step(
            agent="source_retrieval",
            run_id=run_id,
            input_summary="讀取 source catalog、source excerpts、wiki pages、provenance 與 contradiction log。",
            source_ids=source_ids,
            confidence=0.92,
            work=work,
        )


class NewsSectorAgent:
    """Summarize the AI SSD and NAND sector narrative."""

    def run(self, run_id: str) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            thesis = [
                "AI inference、資料中心與 enterprise SSD 需求是群聯估值重估的主要敘事。",
                "2026 年 4 月營收與 Q1 財報新聞顯示成長故事已反映到營運數字。",
                "NAND 上行循環可能推升營收、毛利率與庫存利益，但也會帶來反轉風險。",
            ]
            return (
                "整理出 AI SSD / enterprise SSD 成長與 NAND 上行循環兩條主要敘事。",
                {"thesis": thesis},
            )

        return timed_step(
            agent="news_sector_agent",
            run_id=run_id,
            input_summary="使用官方營收、財報新聞與券商新聞摘要建立產業敘事。",
            source_ids=["S1", "S2", "S3", "S4", "S6"],
            confidence=0.82,
            work=work,
        )


class FundamentalAgent:
    """Build EPS scenarios and valuation sensitivity."""

    def run(self, run_id: str, price: float, price_date: str) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            scenarios = []
            for assumption in EPS_ASSUMPTIONS:
                pe = round(price / assumption["eps"], 1)
                scenarios.append(
                    {
                        **assumption,
                        "price": price,
                        "price_date": price_date,
                        "forward_pe": pe,
                    }
                )
            return (
                "建立 6 個 2026 EPS 情境；估值結論對 FactSet 中位數與群益高標差異高度敏感。",
                {"valuation_scenarios": scenarios},
            )

        return timed_step(
            agent="fundamental_agent",
            run_id=run_id,
            input_summary=f"使用示範股價 {price} 元（{price_date}，非即時行情）計算 Forward P/E。",
            source_ids=["S3", "S4", "S5"],
            confidence=0.8,
            work=work,
        )


class HealthCheckAgent:
    """Summarize conservative StatementDog-style health checks."""

    def run(
        self,
        run_id: str,
        checks: list[dict[str, Any]],
    ) -> AgentResult:
        source_ids = sorted({source_id for check in checks for source_id in check["source_ids"]})

        def work() -> tuple[str, dict[str, Any]]:
            summary = {
                "total": len(checks),
                "pass": _count_status(checks, "pass"),
                "fail": _count_status(checks, "fail"),
                "unknown": _count_status(checks, "unknown"),
                "not_available": _count_status(checks, "not_available"),
                "data_policy": "public_fixture_only",
                "major_gaps": _major_health_gaps(checks),
            }
            return (
                "完成 7 種股票健診框架，"
                f"{summary['pass']} pass、{summary['fail']} fail、"
                f"{summary['unknown']} unknown、{summary['not_available']} not_available；"
                f"主要缺口為{'、'.join(summary['major_gaps'])}。",
                {"summary": summary, "checks": checks},
            )

        return timed_step(
            agent="health_check_agent",
            run_id=run_id,
            input_summary="使用 public fixture 將財報狗式七種股票健診轉成保守狀態與資料缺口。",
            source_ids=source_ids,
            confidence=0.78,
            work=work,
        )


class RiskAgent:
    """Generate risks and opposing views."""

    def run(self, run_id: str) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            risks = [
                "NAND 報價反轉或漲幅放緩，會壓縮毛利率與庫存利益。",
                "Q1 EPS 不應無條件年化，需補正式財報與季節性檢查。",
                "券商摘要與 FactSet 共識差距大，代表估值結論對 EPS 假設高度敏感。",
                "CMoney 與新聞摘要不能替代完整券商研報。",
                "營運現金流、庫存週轉與應收帳款仍需後續補資料。",
            ]
            return (
                "列出 NAND 循環、Q1 年化、來源層級與現金流等主要反方風險。",
                {"risks": risks},
            )

        return timed_step(
            agent="risk_agent",
            run_id=run_id,
            input_summary="檢查 golden sample 反幻覺清單與 Risk_Register wiki page。",
            source_ids=["S3", "S4", "S5", "S6", "S8"],
            confidence=0.86,
            work=work,
        )


class ReportGenerator:
    """Generate a source-backed deterministic report."""

    def run(
        self,
        run_id: str,
        question: str,
        target: dict[str, Any],
        narrative: dict[str, Any],
        fundamentals: dict[str, Any],
        health_checks: dict[str, Any],
        risks: dict[str, Any],
        price_note: str,
    ) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            scenarios = fundamentals["valuation_scenarios"]
            report = _build_report(
                question=question,
                target=target,
                thesis=narrative["thesis"],
                scenarios=scenarios,
                health_checks=health_checks,
                risks=risks["risks"],
                price_note=price_note,
            )
            claims = [
                {
                    "claim": "AI SSD / enterprise SSD 是群聯目前估值重估的主要敘事之一。",
                    "source_ids": ["S4", "S6"],
                    "wiki_page": "Theme_AI_SSD.md",
                },
                {
                    "claim": "2026 EPS 假設分散，估值支撐程度取決於採用哪個 EPS 情境。",
                    "source_ids": ["S4", "S5"],
                    "wiki_page": "Valuation_EPS_Assumptions.md",
                },
                {
                    "claim": "CMoney 與新聞摘要不是完整券商研報。",
                    "source_ids": ["S4", "S6", "S8"],
                    "wiki_page": "Brokerage_View_Summary.md",
                },
            ]
            return (
                "產生一份偏中性偏多、含股票健診摘要、來源與風險邊界的研究輔助報告。",
                {"report_markdown": report, "claims": claims},
            )

        return timed_step(
            agent="report_generator",
            run_id=run_id,
            input_summary="整合產業敘事、估值情境、風險與 source hierarchy。",
            source_ids=["S1", "S3", "S4", "S5", "S6", "S8"],
            confidence=0.84,
            work=work,
        )


class EvaluationAgent:
    """Score the generated report with a deterministic rubric."""

    def run(
        self,
        run_id: str,
        report_markdown: str,
        rubric: dict[str, Any],
        provenance_count: int,
        health_checks: dict[str, Any] | None = None,
    ) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            hard_fail_hits = [
                rule for rule in rubric["hard_fail_rules"] if _rule_is_hit(rule, report_markdown)
            ]
            if _health_check_hallucination_is_hit(report_markdown):
                hard_fail_hits.append("health_check_hallucination")
            health_summary_missing = not _has_health_check_summary(report_markdown, health_checks)
            dimensions = [
                {"id": "source_grounding", "name": "來源 grounding", "score": 4.5},
                {"id": "valuation_rigor", "name": "財務與估值嚴謹度", "score": 4.4},
                {"id": "industry_narrative", "name": "產業敘事品質", "score": 4.1},
                {"id": "risk_coverage", "name": "風險與反方觀點", "score": 4.4},
                {"id": "health_check_honesty", "name": "健診與資料缺口誠實度", "score": 4.3},
                {"id": "user_usefulness", "name": "使用者可用性", "score": 4.5},
            ]
            total = round(sum(item["score"] for item in dimensions) / len(dimensions), 2)
            if health_summary_missing:
                total = min(total, 3.5)
            if hard_fail_hits:
                total = min(total, 2.5)
            status = "passed" if total >= rubric["threshold"] and not hard_fail_hits else "needs_revision"
            notes = [
                "有標示公開來源 proxy golden sample，不宣稱完整券商研報。",
                f"已有 {provenance_count} 筆 wiki provenance 可追溯重要 claim。",
                "股票健診採 public fixture 保守輸出，缺資料時標示 unknown / not_available。",
                "仍需後續補正式 Q1 財報、現金流、股利、籌碼與長期估值區間。",
            ]
            if health_summary_missing:
                notes.append("報告缺少完整股票健診摘要或未呈現七種健診，需補強。")
            payload = {
                "total_score": total,
                "threshold": rubric["threshold"],
                "status": status,
                "dimensions": dimensions,
                "hard_fail_hits": hard_fail_hits,
                "notes": notes,
            }
            return (f"Evaluation score {total} / 5，狀態：{status}。", payload)

        return timed_step(
            agent="evaluation_agent",
            run_id=run_id,
            input_summary="依 rubric、hard fail rules 與 wiki provenance 檢查報告品質。",
            source_ids=[],
            confidence=0.88,
            work=work,
        )


def _build_report(
    *,
    question: str,
    target: dict[str, Any],
    thesis: list[str],
    scenarios: list[dict[str, Any]],
    health_checks: dict[str, Any],
    risks: list[str],
    price_note: str,
) -> str:
    target_display_name = _target_display_name(target)
    scenario_rows = "\n".join(
        f"| {item['label']} | {item['eps']:.2f} | {item['forward_pe']:.1f}x | {', '.join(item['source_ids'])} | {item['interpretation']} |"
        for item in scenarios
    )
    thesis_rows = "\n".join(f"- {item}" for item in thesis)
    health_rows = _build_health_check_rows(health_checks["checks"])
    health_gaps = "、".join(health_checks["summary"]["major_gaps"])
    risk_rows = "\n".join(f"- {item}" for item in risks)
    return f"""# {target_display_name}研究輔助報告

研究問題：{question}

> 這是研究輔助輸出，不是買賣建議。使用的股價資料為示範 fixture，{price_note}

## 一句話結論

公開來源支持「AI SSD / enterprise SSD + NAND 上行循環」正在改善群聯的成長敘事，但估值是否被支撐高度取決於 2026 EPS 假設。若採 FactSet 中位數，市場已反映相當多期待；若採群益 05/07 摘要的高標 EPS，估值壓力相對降低。因此目前結論是中性偏多，但需要持續驗證 EPS、毛利率、現金流與 NAND 循環。

## 成長敘事

{thesis_rows}

## EPS 與 Forward P/E 情境

| 情境 | 2026 EPS | Forward P/E | Sources | 解讀 |
|---|---:|---:|---|---|
{scenario_rows}

## 股票健診摘要

本段是 public fixture / public_fixture_only 的保守框架化輸出，不是財報狗登入或付費資料結果。`unknown` 代表資料不足，`not_available` 代表目前 MVP 沒有資料入口或權限。

| 健診 | 狀態 | 保守解讀 | 主要缺口 | Sources |
|---|---|---|---|---|
{health_rows}

主要缺口：{health_gaps}。

## 反方與風險

{risk_rows}

## 來源邊界

- S1 是公司官方月營收，可作營收硬數據。
- S3 是財報新聞，正式研究需回到 MOPS 或公司財報補驗。
- S4、S7、S8、S10 是 CMoney 券商摘要，不是完整券商研報。
- S5 是 FactSet 共識經新聞平台轉載，不是單一券商模型。
- S8 沒有揭露完整 10 家券商名單，系統不得自行補齊。
"""


def _target_display_name(target: dict[str, Any]) -> str:
    name = str(target.get("name") or "群聯電子").strip()
    ticker = str(target.get("ticker") or "8299").strip()
    if ticker and ticker not in name:
        return f"{name}（{ticker}）"
    return name


def _count_status(checks: list[dict[str, Any]], status: str) -> int:
    return sum(1 for check in checks if check["status"] == status)


def _major_health_gaps(checks: list[dict[str, Any]]) -> list[str]:
    gap_keywords = [
        ("現金流", "現金流"),
        ("股利", "股利"),
        ("殖利率", "股利"),
        ("籌碼", "籌碼"),
        ("董監", "籌碼"),
        ("P/B", "P/B"),
        ("F-score", "F-score"),
        ("P/E", "長期估值區間"),
        ("估值", "長期估值區間"),
    ]
    gaps: list[str] = []
    for check in checks:
        for missing in check["missing_data"]:
            label = next((value for needle, value in gap_keywords if needle in missing), missing)
            if label not in gaps:
                gaps.append(label)
    return gaps[:5]


def _build_health_check_rows(checks: list[dict[str, Any]]) -> str:
    rows = []
    for check in checks:
        sources = ", ".join(check["source_ids"]) if check["source_ids"] else "無直接來源"
        missing = "、".join(check["missing_data"][:3])
        rows.append(
            f"| {check['name']} | {check['status']} | {check['report_takeaway']} | {missing} | {sources} |"
        )
    return "\n".join(rows)


def _has_health_check_summary(
    report_markdown: str,
    health_checks: dict[str, Any] | None,
) -> bool:
    if not health_checks:
        return False
    if "股票健診摘要" not in report_markdown:
        return False
    checks = health_checks.get("checks", [])
    if len(checks) != 7:
        return False
    return all(check["name"] in report_markdown for check in checks)


def _health_check_hallucination_is_hit(report_markdown: str) -> bool:
    risky_phrases = [
        "已使用財報狗付費資料",
        "已使用財報狗登入資料",
        "籌碼健診通過",
        "not_available 通過",
        "unknown 通過",
        "完整驗證",
    ]
    return any(phrase in report_markdown for phrase in risky_phrases)


def _rule_is_hit(rule: str, report_markdown: str) -> bool:
    """Very small deterministic hard-fail scanner."""

    if "宣稱已閱讀完整券商研報" in rule:
        return "已閱讀完整券商研報" in report_markdown
    if "補齊未揭露" in rule:
        return "完整 10 家券商名單如下" in report_markdown
    if "現在買" in rule:
        return "現在買" in report_markdown or "一定會漲" in report_markdown
    if "單一目標價" in rule:
        return "3,080 元就是合理價" in report_markdown
    if "過期股價" in rule:
        claims_live_price = "即時行情" in report_markdown and "不是即時行情" not in report_markdown
        lacks_date = "日期" not in report_markdown
        return claims_live_price or lacks_date
    return False

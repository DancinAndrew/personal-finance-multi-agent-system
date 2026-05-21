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
    """Return curated sources and research evidence context."""

    def run(
        self,
        run_id: str,
        sources: list[dict[str, Any]],
        evidence_pages: list[dict[str, str]],
        provenance: list[dict[str, Any]],
    ) -> AgentResult:
        source_ids = [source["id"] for source in sources]

        def work() -> tuple[str, dict[str, Any]]:
            return (
                f"載入 {len(sources)} 筆 curated sources、{len(evidence_pages)} 個 evidence pages 與 {len(provenance)} 筆 provenance。",
                {
                    "source_count": len(sources),
                    "evidence_page_count": len(evidence_pages),
                    "provenance_count": len(provenance),
                },
            )

        return timed_step(
            agent="source_retrieval",
            run_id=run_id,
            input_summary="讀取 source catalog、source excerpts、evidence pages、provenance 與 contradiction log。",
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
    """Build EPS scenarios plus a conservative fundamental snapshot."""

    def run(
        self,
        run_id: str,
        price: float,
        price_date: str,
        metrics_snapshot: dict[str, Any],
        source_catalog: list[dict[str, Any]],
    ) -> AgentResult:
        catalog_ids = {source["id"] for source in source_catalog}
        source_ids = _unique_source_ids(
            [source_id for assumption in EPS_ASSUMPTIONS for source_id in assumption["source_ids"]]
            + _source_ids_from_fundamentals(metrics_snapshot)
        )
        invalid_source_ids = set(source_ids).difference(catalog_ids)
        if invalid_source_ids:
            raise ValueError(f"Unknown fundamental source ids: {sorted(invalid_source_ids)}")

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
            categories = metrics_snapshot["categories"]
            summary = _build_fundamental_summary(metrics_snapshot)
            key_findings = _build_fundamental_key_findings(categories)
            data_gaps = _major_fundamental_gaps(categories)
            return (
                "建立 6 個 2026 EPS/P/E 情境，並整理五大基本面面向："
                f"{summary['partial']} partial、{summary['missing']} missing；"
                f"主要缺口為{'、'.join(summary['major_gaps'])}。",
                {
                    "valuation_scenarios": scenarios,
                    "summary": summary,
                    "categories": categories,
                    "key_findings": key_findings,
                    "data_gaps": data_gaps,
                },
            )

        return timed_step(
            agent="fundamental_agent",
            run_id=run_id,
            input_summary=f"使用示範股價 {price} 元（{price_date}，非即時行情）計算 Forward P/E。",
            source_ids=source_ids,
            confidence=0.8,
            work=work,
        )


class ValuationAgent:
    """Build a conservative valuation snapshot separate from fundamentals."""

    def run(
        self,
        run_id: str,
        price: float,
        price_date: str,
        valuation_fixture: dict[str, Any],
        fundamentals: dict[str, Any],
        source_catalog: list[dict[str, Any]],
    ) -> AgentResult:
        catalog_ids = {source["id"] for source in source_catalog}
        source_ids = _unique_source_ids(
            _source_ids_from_valuation_fixture(valuation_fixture)
            + [
                source_id
                for assumption in EPS_ASSUMPTIONS
                for source_id in assumption["source_ids"]
            ]
        )
        invalid_source_ids = set(source_ids).difference(catalog_ids)
        if invalid_source_ids:
            raise ValueError(f"Unknown valuation source ids: {sorted(invalid_source_ids)}")

        def work() -> tuple[str, dict[str, Any]]:
            scenarios = _build_valuation_scenarios(price, price_date)
            multiples = _build_valuation_multiples(
                valuation_fixture["multiples"],
                scenarios,
                price,
                price_date,
            )
            broker_targets = _build_broker_targets(
                valuation_fixture["broker_targets"],
                price,
                price_date,
            )
            data_gaps = _valuation_data_gaps(valuation_fixture, multiples)
            coverage = _build_valuation_coverage(multiples, broker_targets)
            summary = {
                "data_policy": valuation_fixture["data_policy"],
                "as_of_date": valuation_fixture["as_of_date"],
                "price": price,
                "price_as_of_date": price_date,
                "is_live_market_data": False,
                "coverage": coverage,
                "major_gaps": data_gaps[:6],
            }
            interpretation = _build_valuation_interpretation(
                scenarios,
                broker_targets,
                fundamentals,
            )
            return (
                "建立 Forward P/E 與券商目標價敏感度，"
                f"{coverage['partial']} partial、{coverage['missing']} missing；"
                f"主要缺口為{'、'.join(summary['major_gaps'])}。",
                {
                    "summary": summary,
                    "scenarios": scenarios,
                    "multiples": multiples,
                    "broker_targets": broker_targets,
                    "data_gaps": data_gaps,
                    "interpretation": interpretation,
                },
            )

        return timed_step(
            agent="valuation_agent",
            run_id=run_id,
            input_summary=(
                f"使用示範股價 {price} 元（{price_date}，非即時行情）、"
                "EPS assumptions 與公開券商摘要建立估值拆解。"
            ),
            source_ids=source_ids,
            confidence=0.79,
            work=work,
        )


class HealthCheckAgent:
    """Summarize conservative StatementDog-style health checks."""

    def run(
        self,
        run_id: str,
        checks: list[dict[str, Any]],
        fundamentals: dict[str, Any] | None = None,
        valuation: dict[str, Any] | None = None,
    ) -> AgentResult:
        source_ids = sorted({source_id for check in checks for source_id in check["source_ids"]})

        def work() -> tuple[str, dict[str, Any]]:
            fundamental_alignment = _build_health_fundamental_alignment(fundamentals, valuation)
            summary = {
                "total": len(checks),
                "pass": _count_status(checks, "pass"),
                "fail": _count_status(checks, "fail"),
                "unknown": _count_status(checks, "unknown"),
                "not_available": _count_status(checks, "not_available"),
                "data_policy": "public_fixture_only",
                "major_gaps": _major_health_gaps(checks),
                "fundamental_alignment": fundamental_alignment,
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
            input_summary="使用 public fixture 將財報狗式七種股票健診轉成保守狀態與資料缺口；可讀取 fundamentals payload 但不重新計算 metrics。",
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
            input_summary="檢查 golden sample 反幻覺清單與 Risk_Register evidence page。",
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
        valuation: dict[str, Any],
        health_checks: dict[str, Any],
        risks: dict[str, Any],
        price_note: str,
    ) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            report = _build_report(
                question=question,
                target=target,
                thesis=narrative["thesis"],
                fundamentals=fundamentals,
                valuation=valuation,
                health_checks=health_checks,
                risks=risks["risks"],
                price_note=price_note,
            )
            claims = [
                {
                    "claim": "AI SSD / enterprise SSD 是群聯目前估值重估的主要敘事之一。",
                    "source_ids": ["S4", "S6"],
                    "evidence_page": "Theme_AI_SSD.md",
                },
                {
                    "claim": "2026 EPS 假設分散，估值支撐程度取決於採用哪個 EPS 情境。",
                    "source_ids": ["S4", "S5"],
                    "evidence_page": "Valuation_EPS_Assumptions.md",
                },
                {
                    "claim": "估值支撐需要同時觀察 EPS 敏感度、券商目標價區間與 P/B、殖利率、歷史估值缺口。",
                    "source_ids": ["S4", "S5", "S6", "S8", "S10"],
                    "evidence_page": "Valuation_EPS_Assumptions.md",
                },
                {
                    "claim": "CMoney 與新聞摘要不是完整券商研報。",
                    "source_ids": ["S4", "S6", "S8"],
                    "evidence_page": "Brokerage_View_Summary.md",
                },
            ]
            return (
                "產生一份偏中性偏多、含估值拆解、股票健診摘要、來源與風險邊界的研究輔助報告。",
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
        fundamentals: dict[str, Any] | None = None,
        valuation: dict[str, Any] | None = None,
    ) -> AgentResult:
        def work() -> tuple[str, dict[str, Any]]:
            hard_fail_hits = [
                rule for rule in rubric["hard_fail_rules"] if _rule_is_hit(rule, report_markdown)
            ]
            if _health_check_hallucination_is_hit(report_markdown):
                hard_fail_hits.append("health_check_hallucination")
            if _fundamental_overclaim_is_hit(report_markdown):
                hard_fail_hits.append("fundamental_overclaim")
            if _valuation_overclaim_is_hit(report_markdown):
                hard_fail_hits.append("valuation_overclaim")
            health_summary_missing = not _has_health_check_summary(report_markdown, health_checks)
            fundamental_breakdown_missing = not _has_fundamental_breakdown(
                report_markdown,
                fundamentals,
            )
            valuation_breakdown_missing = valuation is not None and not _has_valuation_breakdown(
                report_markdown,
                valuation,
            )
            dimensions = [
                {"id": "source_grounding", "name": "來源 grounding", "score": 4.5},
                {"id": "valuation_rigor", "name": "財務與估值嚴謹度", "score": 4.4},
                {"id": "fundamental_coverage", "name": "基本面覆蓋與缺口誠實度", "score": 4.2},
                {"id": "industry_narrative", "name": "產業敘事品質", "score": 4.1},
                {"id": "risk_coverage", "name": "風險與反方觀點", "score": 4.4},
                {"id": "health_check_honesty", "name": "健診與資料缺口誠實度", "score": 4.3},
                {"id": "user_usefulness", "name": "使用者可用性", "score": 4.5},
            ]
            total = round(sum(item["score"] for item in dimensions) / len(dimensions), 2)
            if health_summary_missing or fundamental_breakdown_missing or valuation_breakdown_missing:
                total = min(total, 3.5)
            if hard_fail_hits:
                total = min(total, 2.5)
            status = "passed" if total >= rubric["threshold"] and not hard_fail_hits else "needs_revision"
            notes = [
                "有標示公開來源 proxy golden sample，不宣稱完整券商研報。",
                f"已有 {provenance_count} 筆 evidence provenance 可追溯重要 claim。",
                "股票健診採 public fixture 保守輸出，缺資料時標示 unknown / not_available。",
                "基本面拆解採五大面向 coverage，營收 / EPS 是 partial evidence，安全性與現金流仍缺資料。",
                "估值拆解採 public fixture，目標價與 Forward P/E 只作敏感度，仍缺 P/B、殖利率、歷史估值與同業估值。",
                "仍需後續補正式 Q1 財報、現金流、股利、籌碼、P/B、殖利率與長期估值區間。",
            ]
            if health_summary_missing:
                notes.append("報告缺少完整股票健診摘要或未呈現七種健診，需補強。")
            if fundamental_breakdown_missing:
                notes.append("報告缺少完整五大面向基本面拆解，需補營收、獲利、安全性、成長力與現金流品質。")
            if valuation_breakdown_missing:
                notes.append("報告缺少估值拆解，需補示範股價日期、Forward P/E 情境、券商目標價區間與估值缺口。")
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
            input_summary="依 rubric、hard fail rules 與 evidence provenance 檢查報告品質。",
            source_ids=[],
            confidence=0.88,
            work=work,
        )


def _build_report(
    *,
    question: str,
    target: dict[str, Any],
    thesis: list[str],
    fundamentals: dict[str, Any],
    valuation: dict[str, Any],
    health_checks: dict[str, Any],
    risks: list[str],
    price_note: str,
) -> str:
    target_display_name = _target_display_name(target)
    scenarios = fundamentals["valuation_scenarios"]
    scenario_rows = "\n".join(
        f"| {item['label']} | {item['eps']:.2f} | {item['forward_pe']:.1f}x | {', '.join(item['source_ids'])} | {item['interpretation']} |"
        for item in scenarios
    )
    valuation_scenario_rows = _build_valuation_scenario_rows(valuation["scenarios"])
    broker_target_rows = _build_broker_target_rows(valuation["broker_targets"])
    valuation_gap_text = "、".join(valuation["summary"]["major_gaps"])
    valuation_interpretation_rows = "\n".join(
        f"- {item}" for item in valuation["interpretation"]
    )
    thesis_rows = "\n".join(f"- {item}" for item in thesis)
    fundamental_rows = _build_fundamental_rows(fundamentals["categories"])
    fundamental_gaps = "、".join(fundamentals["summary"]["major_gaps"])
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

## 基本面拆解

本段把基本面品質與估值敏感度分開看。EPS / Forward P/E 是估值敏感度，不等同完整基本面品質；`partial` 代表有方向性線索但不足以做完整判斷，`missing` 代表本機 fixture 尚未納入必要資料。

| 面向 | Coverage | 保守解讀 | 主要指標 | 主要缺口 | Sources |
|---|---|---|---|---|---|
{fundamental_rows}

基本面主要缺口：{fundamental_gaps}。

## EPS 與 Forward P/E 情境

下表只呈現 2026 EPS 假設對 Forward P/E 的敏感度；它不能替代營收、獲利、安全性、成長力與現金流品質的完整基本面判斷。

| 情境 | 2026 EPS | Forward P/E | Sources | 解讀 |
|---|---:|---:|---|---|
{scenario_rows}

## 估值拆解

示範股價日期：{valuation['summary']['price_as_of_date']}；股價 {valuation['summary']['price']:.0f} 元，非即時行情。以下內容只做情境敏感度與資料缺口整理，不是合理價、目標價承諾或買賣建議。

### Forward P/E 情境敏感度

| 情境 | 2026 EPS | Forward P/E | Sources | 解讀 |
|---|---:|---:|---|---|
{valuation_scenario_rows}

### 券商目標價區間

| 來源 | 日期 | 目標價 / 區間 | 相對示範股價 | Sources | 可靠度限制 |
|---|---|---|---|---|---|
{broker_target_rows}

估值缺口：{valuation_gap_text}。

{valuation_interpretation_rows}

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


def _source_ids_from_fundamentals(snapshot: dict[str, Any]) -> list[str]:
    return [
        source_id
        for category in snapshot["categories"]
        for metric in category["metrics"]
        for source_id in metric["source_ids"]
    ]


def _source_ids_from_valuation_fixture(snapshot: dict[str, Any]) -> list[str]:
    return (
        list(snapshot["price"].get("source_ids", []))
        + [
            source_id
            for multiple in snapshot["multiples"]
            for source_id in multiple["source_ids"]
        ]
        + [
            source_id
            for target in snapshot["broker_targets"]
            for source_id in target["source_ids"]
        ]
    )


def _unique_source_ids(source_ids: list[str]) -> list[str]:
    return sorted(set(source_ids), key=_source_sort_key)


def _source_sort_key(source_id: str) -> tuple[int, str]:
    if source_id.startswith("S") and source_id[1:].isdigit():
        return (int(source_id[1:]), source_id)
    return (999, source_id)


def _build_fundamental_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    categories = snapshot["categories"]
    return {
        "categories_total": len(categories),
        "available": _count_category_status(categories, "available"),
        "partial": _count_category_status(categories, "partial"),
        "missing": _count_category_status(categories, "missing"),
        "not_available": _count_category_status(categories, "not_available"),
        "data_policy": snapshot["data_policy"],
        "as_of_date": snapshot["as_of_date"],
        "major_gaps": _major_fundamental_gaps(categories)[:6],
    }


def _count_category_status(categories: list[dict[str, Any]], status: str) -> int:
    return sum(1 for category in categories if category["coverage_status"] == status)


def _build_fundamental_key_findings(categories: list[dict[str, Any]]) -> list[str]:
    by_id = {category["id"]: category for category in categories}
    return [
        f"{by_id['revenue']['name']}：{by_id['revenue']['category_takeaway']}",
        f"{by_id['profitability']['name']}：{by_id['profitability']['category_takeaway']}",
        "安全性與現金流品質目前標為 missing，不能用 EPS 或營收新聞替代資產負債表與現金流檢查。",
    ]


def _major_fundamental_gaps(categories: list[dict[str, Any]]) -> list[str]:
    gap_keywords = [
        ("毛利", "毛利率"),
        ("現金流", "現金流"),
        ("負債", "負債比"),
        ("流動比", "流動比"),
        ("速動比", "速動比"),
        ("週轉", "週轉天數"),
        ("ROE", "ROE / ROA"),
        ("產品別", "產品別營收"),
        ("YoY", "月營收 YoY 序列"),
    ]
    gaps: list[str] = []
    for category in categories:
        for missing in category["missing_data"]:
            label = next((value for needle, value in gap_keywords if needle in missing), missing)
            if label not in gaps:
                gaps.append(label)
    return gaps


def _build_health_fundamental_alignment(
    fundamentals: dict[str, Any] | None,
    valuation: dict[str, Any] | None = None,
) -> dict[str, str]:
    if not fundamentals:
        return {}
    by_id = {category["id"]: category for category in fundamentals.get("categories", [])}
    alignment: dict[str, str] = {}
    growth = by_id.get("growth")
    if growth:
        alignment["growth_stock"] = (
            f"Fundamental growth coverage is {growth['coverage_status']}；"
            f"{growth['category_takeaway']}"
        )
    cash_flow = by_id.get("cash_flow_quality")
    if cash_flow:
        alignment["landmine_risk"] = (
            f"Cash-flow quality coverage is {cash_flow['coverage_status']}；"
            "地雷股健診仍需現金流與週轉資料。"
        )
    if valuation:
        gaps = "、".join(valuation.get("summary", {}).get("major_gaps", []))
        alignment["value_stock"] = (
            "Valuation Agent 已提供情境敏感度，但便宜股健診仍維持 unknown；"
            f"主要缺口為{gaps}。"
        )
    else:
        alignment["value_stock"] = "Forward P/E 情境只作敏感度，不作便宜股健診通過判定。"
    return alignment


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


def _build_fundamental_rows(categories: list[dict[str, Any]]) -> str:
    rows = []
    for category in categories:
        metrics = _build_fundamental_metric_summary(category["metrics"])
        missing = "、".join(category["missing_data"][:4])
        sources = _format_metric_sources(category["metrics"])
        rows.append(
            f"| {category['name']} | {category['coverage_status']} | "
            f"{category['category_takeaway']} | {metrics} | {missing} | {sources} |"
        )
    return "\n".join(rows)


def _build_fundamental_metric_summary(metrics: list[dict[str, Any]]) -> str:
    items = []
    for metric in metrics[:3]:
        items.append(
            f"{metric['label']}={_format_metric_value(metric)} ({metric['coverage_status']})"
        )
    return "；".join(items)


def _format_metric_value(metric: dict[str, Any]) -> str:
    value = metric["value"]
    if value is None:
        return "缺資料"
    unit = metric["unit"]
    if unit == "TWD_BN":
        return f"{float(value):.2f} 十億元"
    if unit == "TWD":
        return f"{float(value):.2f} 元"
    if unit == "percent":
        return f"{float(value):.2f}%"
    return f"{value} {unit}"


def _format_metric_sources(metrics: list[dict[str, Any]]) -> str:
    source_ids = _unique_source_ids(
        [source_id for metric in metrics for source_id in metric["source_ids"]]
    )
    return ", ".join(source_ids) if source_ids else "無直接來源"


def _build_valuation_scenarios(price: float, price_date: str) -> list[dict[str, Any]]:
    scenarios = []
    for assumption in EPS_ASSUMPTIONS:
        scenarios.append(
            {
                **assumption,
                "price": price,
                "price_date": price_date,
                "forward_pe": round(price / assumption["eps"], 1),
                "coverage_status": "partial",
            }
        )
    return scenarios


def _build_valuation_multiples(
    fixture_multiples: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    price: float,
    price_date: str,
) -> list[dict[str, Any]]:
    median_scenario = next(
        scenario for scenario in scenarios if scenario["id"] == "factset_median"
    )
    multiples = []
    for multiple in fixture_multiples:
        item = dict(multiple)
        if item["id"] == "forward_pe_factset_median":
            item["value"] = median_scenario["forward_pe"]
            item["price"] = price
            item["price_date"] = price_date
        multiples.append(item)
    return multiples


def _build_broker_targets(
    fixture_targets: list[dict[str, Any]],
    price: float,
    price_date: str,
) -> list[dict[str, Any]]:
    targets = []
    for target in fixture_targets:
        item = dict(target)
        item["price"] = price
        item["price_date"] = price_date
        item["coverage_status"] = "partial"
        if "target_price" in item:
            item["upside_pct"] = _pct_change(item["target_price"], price)
        else:
            price_range = item["target_price_range"]
            item["low_upside_pct"] = _pct_change(price_range["low"], price)
            item["high_upside_pct"] = _pct_change(price_range["high"], price)
        targets.append(item)
    return targets


def _pct_change(target_price: float, price: float) -> float:
    return round(((float(target_price) - price) / price) * 100, 1)


def _valuation_data_gaps(
    valuation_fixture: dict[str, Any],
    multiples: list[dict[str, Any]],
) -> list[str]:
    gaps = list(valuation_fixture["missing_data"])
    for multiple in multiples:
        if multiple["coverage_status"] == "missing":
            for missing in multiple["missing_data"]:
                if missing not in gaps:
                    gaps.append(missing)
    return gaps


def _build_valuation_coverage(
    multiples: list[dict[str, Any]],
    broker_targets: list[dict[str, Any]],
) -> dict[str, int]:
    statuses = ["available", "partial", "missing", "not_available"]
    coverage = {status: 0 for status in statuses}
    for multiple in multiples:
        coverage[multiple["coverage_status"]] += 1
    if broker_targets:
        coverage["partial"] += 1
    return coverage


def _build_valuation_interpretation(
    scenarios: list[dict[str, Any]],
    broker_targets: list[dict[str, Any]],
    fundamentals: dict[str, Any],
) -> list[str]:
    by_id = {scenario["id"]: scenario for scenario in scenarios}
    target_prices = _target_price_values(broker_targets)
    low_target = min(target_prices)
    high_target = max(target_prices)
    fundamental_gaps = "、".join(fundamentals["summary"]["major_gaps"][:4])
    return [
        "AI SSD 成長故事若要支撐目前估值，需要 EPS 接近 FactSet high 或群益 05/07 摘要高標，且毛利率與 NAND cycle 持續兌現。",
        (
            f"以示範股價計算，FactSet median EPS 對應 Forward P/E 約 "
            f"{by_id['factset_median']['forward_pe']:.1f}x；群益高標摘要對應約 "
            f"{by_id['capital_aggressive']['forward_pe']:.1f}x，兩者代表不同信心門檻。"
        ),
        (
            f"公開摘要目標價大致落在 {low_target:.0f} 到 {high_target:.0f} 元區間；"
            "這只能作市場預期參考，不是合理價或買賣建議。"
        ),
        f"估值判斷仍需補 {fundamental_gaps}，以及 P/B、殖利率、歷史估值與同業比較。",
    ]


def _target_price_values(broker_targets: list[dict[str, Any]]) -> list[float]:
    values: list[float] = []
    for target in broker_targets:
        if "target_price" in target:
            values.append(float(target["target_price"]))
        else:
            values.append(float(target["target_price_range"]["low"]))
            values.append(float(target["target_price_range"]["high"]))
    return values


def _build_valuation_scenario_rows(scenarios: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"| {item['label']} | {item['eps']:.2f} | {item['forward_pe']:.1f}x | "
        f"{', '.join(item['source_ids'])} | {item['interpretation']} |"
        for item in scenarios
    )


def _build_broker_target_rows(broker_targets: list[dict[str, Any]]) -> str:
    rows = []
    for target in broker_targets:
        if "target_price" in target:
            target_display = f"{target['target_price']:.0f} 元"
            sensitivity = f"{target['upside_pct']:+.1f}%"
        else:
            price_range = target["target_price_range"]
            target_display = f"{price_range['low']:.0f} 到 {price_range['high']:.0f} 元"
            sensitivity = f"{target['low_upside_pct']:+.1f}% 到 {target['high_upside_pct']:+.1f}%"
        rows.append(
            f"| {target['source_label']} | {target['date']} | {target_display} | "
            f"{sensitivity} | {', '.join(target['source_ids'])} | {target['reliability_note']} |"
        )
    return "\n".join(rows)


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


def _has_fundamental_breakdown(
    report_markdown: str,
    fundamentals: dict[str, Any] | None,
) -> bool:
    if not fundamentals:
        return False
    if "基本面拆解" not in report_markdown:
        return False
    categories = fundamentals.get("categories", [])
    if len(categories) != 5:
        return False
    return all(
        category["name"] in report_markdown
        and category["coverage_status"] in report_markdown
        for category in categories
    )


def _has_valuation_breakdown(
    report_markdown: str,
    valuation: dict[str, Any] | None,
) -> bool:
    if not valuation:
        return False
    if "估值拆解" not in report_markdown:
        return False
    required_phrases = ["示範股價日期", "非即時行情", "券商目標價區間"]
    if not all(phrase in report_markdown for phrase in required_phrases):
        return False
    gaps = valuation.get("summary", {}).get("major_gaps", [])
    return all(gap in report_markdown for gap in gaps[:3])


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


def _fundamental_overclaim_is_hit(report_markdown: str) -> bool:
    risky_phrases = [
        "Q1 EPS 年化為正式全年預估",
        "現金流品質已確認改善",
        "安全性已確認健康",
        "獲利能力全面改善",
        "Forward P/E 證明便宜",
        "基本面已完整驗證",
        "partial 已完整驗證",
        "missing 已完整驗證",
    ]
    return any(phrase in report_markdown for phrase in risky_phrases)


def _valuation_overclaim_is_hit(report_markdown: str) -> bool:
    risky_phrases = [
        "3,080 元就是合理價",
        "目標價就是買進理由",
        "Forward P/E 證明便宜",
        "CMoney 完整券商模型",
        "估值已完整驗證",
        "target upside 是買進理由",
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
        return _valuation_overclaim_is_hit(report_markdown)
    if "過期股價" in rule:
        claims_live_price = "即時行情" in report_markdown and "不是即時行情" not in report_markdown
        lacks_date = "日期" not in report_markdown
        return claims_live_price or lacks_date
    if "partial" in rule or "missing" in rule or "Q1 EPS" in rule:
        return _fundamental_overclaim_is_hit(report_markdown) or _valuation_overclaim_is_hit(
            report_markdown
        )
    return False

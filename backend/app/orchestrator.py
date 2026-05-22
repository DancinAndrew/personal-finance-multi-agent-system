"""Research orchestration for the deterministic MVP."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .agents import (
    ChipAgent,
    EvaluationAgent,
    FundamentalAgent,
    HealthCheckAgent,
    IntentRouter,
    NewsSectorAgent,
    ReportGenerator,
    RiskAgent,
    SourceRetrieval,
    TechnicalAgent,
    ValuationAgent,
)
from .store import FileStore


class ResearchOrchestrator:
    """Run the deterministic multi-agent research workflow."""

    def __init__(self, store: FileStore) -> None:
        self.store = store
        self.intent_router = IntentRouter()
        self.source_retrieval = SourceRetrieval()
        self.news_sector_agent = NewsSectorAgent()
        self.fundamental_agent = FundamentalAgent()
        self.valuation_agent = ValuationAgent()
        self.chip_agent = ChipAgent()
        self.technical_agent = TechnicalAgent()
        self.health_check_agent = HealthCheckAgent()
        self.risk_agent = RiskAgent()
        self.report_generator = ReportGenerator()
        self.evaluation_agent = EvaluationAgent()

    def run_default(self) -> dict[str, Any]:
        """Run the default Phison research task."""

        return self.run({})

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Run the deterministic workflow and return a JSON-ready result."""

        demo = self.store.load_demo_run()
        price_fixture = self.store.load_price_fixture()
        target = payload.get("target") or demo["target"]
        question = payload.get("question") or demo["question"]
        price = float(payload.get("price") or price_fixture["price"])
        price_date = str(payload.get("price_date") or price_fixture["as_of_date"])
        price_note = (
            f"{price:.0f} 元，日期 {price_date}，不是即時行情；正式使用前必須重新確認。"
        )
        run_id = str(payload.get("id") or demo["id"])
        now = datetime.now(timezone.utc).isoformat()

        sources = self.store.load_source_catalog()
        evidence_pages = self.store.load_evidence_pages()
        provenance = self.store.load_provenance()
        rubric = self.store.load_rubric()
        health_check_fixture = self.store.load_health_checks()
        fundamental_metrics = self.store.load_fundamental_metrics()
        valuation_fixture = self.store.load_valuation_fixture()
        chip_fixture = self.store.load_chip_fixture()
        technical_fixture = self.store.load_technical_fixture()

        steps: list[dict[str, Any]] = []

        route = self.intent_router.run(run_id, question, target)
        steps.append(route.step)
        retrieval = self.source_retrieval.run(run_id, sources, evidence_pages, provenance)
        steps.append(retrieval.step)
        narrative = self.news_sector_agent.run(run_id)
        steps.append(narrative.step)
        fundamentals = self.fundamental_agent.run(
            run_id,
            price,
            price_date,
            fundamental_metrics,
            sources,
        )
        steps.append(fundamentals.step)
        valuation = self.valuation_agent.run(
            run_id,
            price,
            price_date,
            valuation_fixture,
            fundamentals.payload,
            sources,
        )
        steps.append(valuation.step)
        chip = self.chip_agent.run(run_id, chip_fixture, sources)
        steps.append(chip.step)
        technical = self.technical_agent.run(run_id, technical_fixture, sources)
        steps.append(technical.step)
        health_checks = self.health_check_agent.run(
            run_id,
            health_check_fixture,
            fundamentals.payload,
            valuation.payload,
            chip.payload,
            technical.payload,
        )
        steps.append(health_checks.step)
        risks = self.risk_agent.run(run_id, chip.payload, technical.payload)
        steps.append(risks.step)
        report = self.report_generator.run(
            run_id,
            question,
            target,
            narrative.payload,
            fundamentals.payload,
            valuation.payload,
            chip.payload,
            technical.payload,
            health_checks.payload,
            risks.payload,
            price_note,
        )
        steps.append(report.step)
        evaluation = self.evaluation_agent.run(
            run_id,
            report.payload["report_markdown"],
            rubric,
            len(provenance),
            health_checks.payload,
            fundamentals.payload,
            valuation.payload,
            chip.payload,
            technical.payload,
        )
        steps.append(evaluation.step)

        return {
            "run": {
                "id": run_id,
                "target": target,
                "question": question,
                "status": "completed",
                "mode": "deterministic_demo",
                "created_at": now,
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "evaluation_score": evaluation.payload["total_score"],
                "price_fixture": {
                    "price": price,
                    "as_of_date": price_date,
                    "is_live_market_data": False,
                    "display_note": price_note,
                },
            },
            "steps": steps,
            "sources": sources,
            "evidence": {
                "pages": evidence_pages,
                "provenance": provenance,
            },
            "analysis": {
                "route": route.payload,
                "retrieval": retrieval.payload,
                "narrative": narrative.payload,
                "fundamentals": fundamentals.payload,
                "valuation": valuation.payload,
                "chip": chip.payload,
                "technical": technical.payload,
                "health_checks": health_checks.payload,
                "risks": risks.payload,
            },
            "report": report.payload,
            "evaluation": evaluation.payload,
            "disclaimer": "本系統只提供研究輔助，不提供買賣建議或交易執行。",
        }

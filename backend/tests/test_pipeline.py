from __future__ import annotations

import unittest
from pathlib import Path

from backend.app.agents import EvaluationAgent
from backend.app.orchestrator import ResearchOrchestrator
from backend.app.store import FileStore


REPO_ROOT = Path(__file__).resolve().parents[2]


class FileStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = FileStore(REPO_ROOT)

    def test_source_catalog_has_required_fields(self) -> None:
        sources = self.store.load_source_catalog()
        self.assertGreaterEqual(len(sources), 8)
        required = {"id", "title", "source", "source_type", "date", "url_or_path", "reliability_note"}
        for source in sources:
            self.assertTrue(required.issubset(source.keys()))

    def test_wiki_pages_and_provenance_load(self) -> None:
        pages = self.store.load_wiki_pages()
        provenance = self.store.load_provenance()
        self.assertEqual(len(pages), 7)
        self.assertGreaterEqual(len(provenance), 5)


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.orchestrator = ResearchOrchestrator(FileStore(REPO_ROOT))

    def test_default_run_contains_trace_report_and_evaluation(self) -> None:
        result = self.orchestrator.run_default()
        self.assertEqual(result["run"]["status"], "completed")
        self.assertEqual(len(result["steps"]), 7)
        self.assertIn("report_markdown", result["report"])
        self.assertGreaterEqual(result["evaluation"]["total_score"], 4.0)
        for step in result["steps"]:
            self.assertIn("input_summary", step)
            self.assertIn("output_summary", step)
            self.assertIn("source_ids", step)
            self.assertIn("latency_ms", step)

    def test_price_override_changes_forward_pe(self) -> None:
        default = self.orchestrator.run_default()
        overridden = self.orchestrator.run({"price": 3000})
        default_pe = default["analysis"]["fundamentals"]["valuation_scenarios"][1]["forward_pe"]
        override_pe = overridden["analysis"]["fundamentals"]["valuation_scenarios"][1]["forward_pe"]
        self.assertNotEqual(default_pe, override_pe)
        self.assertGreater(override_pe, default_pe)

    def test_report_title_does_not_duplicate_ticker(self) -> None:
        report = self.orchestrator.run(
            {
                "target": {
                    "ticker": "8299",
                    "name": "群聯電子（8299）",
                    "market": "TWSE",
                }
            }
        )["report"]["report_markdown"]
        self.assertIn("# 群聯電子（8299）研究輔助報告", report)
        self.assertNotIn("（8299）（8299）", report)

    def test_report_avoids_hard_fail_phrases(self) -> None:
        report = self.orchestrator.run_default()["report"]["report_markdown"]
        forbidden = [
            "已閱讀完整券商研報",
            "完整 10 家券商名單如下",
            "現在買",
            "一定會漲",
            "3,080 元就是合理價",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, report)
        self.assertIn("不是買賣建議", report)

    def test_evaluation_flags_hard_fail_report(self) -> None:
        store = FileStore(REPO_ROOT)
        rubric = store.load_rubric()
        result = EvaluationAgent().run(
            "run_bad",
            "我已閱讀完整券商研報，完整 10 家券商名單如下，現在買。",
            rubric,
            provenance_count=0,
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertEqual(result.payload["status"], "needs_revision")


class FlaskApiTests(unittest.TestCase):
    def test_health_endpoint_when_flask_is_available(self) -> None:
        try:
            from backend.app import create_app
        except ModuleNotFoundError as exc:
            if exc.name == "flask":
                self.skipTest("Flask is not installed in this environment")
            raise

        app = create_app(REPO_ROOT)
        client = app.test_client()
        response = client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_default_run_endpoint_when_flask_is_available(self) -> None:
        try:
            from backend.app import create_app
        except ModuleNotFoundError as exc:
            if exc.name == "flask":
                self.skipTest("Flask is not installed in this environment")
            raise

        app = create_app(REPO_ROOT)
        client = app.test_client()
        response = client.get("/api/demo/default-run")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["run"]["status"], "completed")
        self.assertGreaterEqual(data["evaluation"]["total_score"], 4.0)

    def test_missing_run_returns_404_when_flask_is_available(self) -> None:
        try:
            from backend.app import create_app
        except ModuleNotFoundError as exc:
            if exc.name == "flask":
                self.skipTest("Flask is not installed in this environment")
            raise

        app = create_app(REPO_ROOT)
        client = app.test_client()
        response = client.get("/api/research-runs/missing")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "research_run_not_found")


if __name__ == "__main__":
    unittest.main()

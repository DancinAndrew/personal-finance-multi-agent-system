from __future__ import annotations

import unittest
from pathlib import Path

from backend.app.agents import EvaluationAgent
from backend.app.orchestrator import ResearchOrchestrator
from backend.app.store import FileStore


REPO_ROOT = Path(__file__).resolve().parents[2]
VALID_HEALTH_STATUSES = {"pass", "fail", "unknown", "not_available"}
VALID_FUNDAMENTAL_STATUSES = {"available", "partial", "missing", "not_available"}
EXPECTED_FUNDAMENTAL_CATEGORY_IDS = {
    "revenue",
    "profitability",
    "safety",
    "growth",
    "cash_flow_quality",
}


class FileStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = FileStore(REPO_ROOT)

    def test_source_catalog_has_required_fields(self) -> None:
        sources = self.store.load_source_catalog()
        self.assertGreaterEqual(len(sources), 8)
        required = {"id", "title", "source", "source_type", "date", "url_or_path", "reliability_note"}
        for source in sources:
            self.assertTrue(required.issubset(source.keys()))

    def test_evidence_pages_and_provenance_load(self) -> None:
        pages = self.store.load_evidence_pages()
        provenance = self.store.load_provenance()
        self.assertEqual(len(pages), 7)
        self.assertGreaterEqual(len(provenance), 5)

    def test_health_check_fixture_has_required_shape(self) -> None:
        checks = self.store.load_health_checks()
        self.assertEqual(len(checks), 7)

        required = {
            "id",
            "name",
            "status",
            "status_reason",
            "criteria",
            "source_ids",
            "missing_data",
            "report_takeaway",
            "data_policy",
        }
        for check in checks:
            self.assertTrue(required.issubset(check.keys()))
            self.assertIn(check["status"], VALID_HEALTH_STATUSES)
            self.assertEqual(check["data_policy"], "public_fixture_only")

    def test_health_check_source_ids_reference_catalog(self) -> None:
        source_ids = {source["id"] for source in self.store.load_source_catalog()}
        for check in self.store.load_health_checks():
            self.assertTrue(set(check["source_ids"]).issubset(source_ids))
            for criterion in check["criteria"]:
                self.assertIn(criterion["status"], VALID_HEALTH_STATUSES)
                self.assertTrue(set(criterion["source_ids"]).issubset(source_ids))

    def test_fundamental_metrics_fixture_has_required_shape(self) -> None:
        snapshot = self.store.load_fundamental_metrics()
        self.assertEqual(snapshot["data_policy"], "public_fixture_only")
        self.assertEqual(
            {category["id"] for category in snapshot["categories"]},
            EXPECTED_FUNDAMENTAL_CATEGORY_IDS,
        )

        category_required = {
            "id",
            "name",
            "coverage_status",
            "category_takeaway",
            "metrics",
            "missing_data",
        }
        metric_required = {
            "id",
            "label",
            "period",
            "value",
            "unit",
            "coverage_status",
            "source_ids",
            "interpretation",
            "missing_data",
        }
        for category in snapshot["categories"]:
            self.assertTrue(category_required.issubset(category.keys()))
            self.assertIn(category["coverage_status"], VALID_FUNDAMENTAL_STATUSES)
            self.assertIsInstance(category["metrics"], list)
            self.assertGreaterEqual(len(category["metrics"]), 1)
            for metric in category["metrics"]:
                self.assertTrue(metric_required.issubset(metric.keys()))
                self.assertIn(metric["coverage_status"], VALID_FUNDAMENTAL_STATUSES)
                if metric["value"] is None:
                    self.assertNotEqual(metric["coverage_status"], "available")
                    self.assertGreater(len(metric["missing_data"]), 0)

    def test_fundamental_metric_source_ids_reference_catalog(self) -> None:
        source_ids = {source["id"] for source in self.store.load_source_catalog()}
        for category in self.store.load_fundamental_metrics()["categories"]:
            for metric in category["metrics"]:
                self.assertTrue(set(metric["source_ids"]).issubset(source_ids))


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.orchestrator = ResearchOrchestrator(FileStore(REPO_ROOT))

    def test_default_run_contains_trace_report_and_evaluation(self) -> None:
        result = self.orchestrator.run_default()
        self.assertEqual(result["run"]["status"], "completed")
        self.assertEqual(len(result["steps"]), 8)
        self.assertIn("health_check_agent", [step["agent"] for step in result["steps"]])
        self.assertIn("evidence", result)
        self.assertNotIn("wiki", result)
        self.assertIn("report_markdown", result["report"])
        self.assertGreaterEqual(result["evaluation"]["total_score"], 4.0)
        for step in result["steps"]:
            self.assertIn("input_summary", step)
            self.assertIn("output_summary", step)
            self.assertIn("source_ids", step)
            self.assertIn("latency_ms", step)

    def test_default_run_contains_health_check_analysis(self) -> None:
        result = self.orchestrator.run_default()
        health_checks = result["analysis"]["health_checks"]
        self.assertEqual(health_checks["summary"]["total"], 7)
        self.assertEqual(health_checks["summary"]["unknown"], 6)
        self.assertEqual(health_checks["summary"]["not_available"], 1)
        self.assertEqual(len(health_checks["checks"]), 7)
        self.assertEqual(health_checks["summary"]["data_policy"], "public_fixture_only")

    def test_default_run_contains_expanded_fundamentals(self) -> None:
        result = self.orchestrator.run_default()
        fundamentals = result["analysis"]["fundamentals"]
        self.assertEqual(len(fundamentals["valuation_scenarios"]), 6)
        self.assertEqual(fundamentals["summary"]["categories_total"], 5)
        self.assertEqual(fundamentals["summary"]["partial"], 3)
        self.assertEqual(fundamentals["summary"]["missing"], 2)
        self.assertEqual(fundamentals["summary"]["data_policy"], "public_fixture_only")
        self.assertEqual(
            {category["id"] for category in fundamentals["categories"]},
            EXPECTED_FUNDAMENTAL_CATEGORY_IDS,
        )
        self.assertGreaterEqual(len(fundamentals["key_findings"]), 2)
        self.assertIn("現金流", "、".join(fundamentals["data_gaps"]))

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
            "已使用財報狗付費資料",
            "籌碼健診通過",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, report)
        self.assertIn("不是買賣建議", report)

    def test_report_contains_health_check_summary(self) -> None:
        report = self.orchestrator.run_default()["report"]["report_markdown"]
        self.assertIn("股票健診摘要", report)
        self.assertIn("public fixture", report)
        self.assertIn("排除地雷股", report)
        self.assertIn("籌碼", report)
        self.assertIn("not_available", report)

    def test_report_contains_fundamental_breakdown(self) -> None:
        report = self.orchestrator.run_default()["report"]["report_markdown"]
        self.assertIn("基本面拆解", report)
        for label in ["營收", "獲利能力", "安全性", "成長力", "現金流品質"]:
            self.assertIn(label, report)
        self.assertIn("partial", report)
        self.assertIn("missing", report)
        self.assertIn("EPS / Forward P/E 是估值敏感度", report)
        forbidden = [
            "獲利能力全面改善",
            "現金流品質已確認改善",
            "Forward P/E 證明便宜",
            "Q1 EPS 年化為正式全年預估",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, report)

    def test_evaluation_flags_hard_fail_report(self) -> None:
        store = FileStore(REPO_ROOT)
        rubric = store.load_rubric()
        result = EvaluationAgent().run(
            "run_bad",
            "我已閱讀完整券商研報，完整 10 家券商名單如下，現在買。",
            rubric,
            provenance_count=0,
            health_checks={"summary": {"total": 0}, "checks": []},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertEqual(result.payload["status"], "needs_revision")

    def test_evaluation_flags_missing_health_check_summary(self) -> None:
        store = FileStore(REPO_ROOT)
        rubric = store.load_rubric()
        result = EvaluationAgent().run(
            "run_missing_health",
            "# 群聯電子（8299）研究輔助報告\n\n## 一句話結論\n\n這是研究輔助，不是買賣建議。",
            rubric,
            provenance_count=5,
            health_checks={"summary": {"total": 7}, "checks": store.load_health_checks()},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertEqual(result.payload["status"], "needs_revision")

    def test_evaluation_flags_health_check_hallucination(self) -> None:
        store = FileStore(REPO_ROOT)
        rubric = store.load_rubric()
        result = EvaluationAgent().run(
            "run_bad_health",
            "股票健診摘要：籌碼健診通過，已使用財報狗付費資料完整驗證。",
            rubric,
            provenance_count=5,
            health_checks={"summary": {"total": 7}, "checks": store.load_health_checks()},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertIn("health_check_hallucination", result.payload["hard_fail_hits"])

    def test_evaluation_flags_missing_fundamental_breakdown(self) -> None:
        store = FileStore(REPO_ROOT)
        health_checks = {"summary": {"total": 7}, "checks": store.load_health_checks()}
        health_names = "\n".join(f"- {check['name']}" for check in health_checks["checks"])
        result = EvaluationAgent().run(
            "run_missing_fundamentals",
            (
                "# 群聯電子（8299）研究輔助報告\n\n"
                "## 股票健診摘要\n\n"
                f"{health_names}\n\n"
                "這是研究輔助，不是買賣建議。"
            ),
            store.load_rubric(),
            provenance_count=5,
            health_checks=health_checks,
            fundamentals={"categories": store.load_fundamental_metrics()["categories"]},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertEqual(result.payload["status"], "needs_revision")

    def test_evaluation_flags_fundamental_overclaim(self) -> None:
        store = FileStore(REPO_ROOT)
        result = EvaluationAgent().run(
            "run_bad_fundamentals",
            "基本面拆解：Q1 EPS 年化為正式全年預估，現金流品質已確認改善。",
            store.load_rubric(),
            provenance_count=5,
            health_checks={"summary": {"total": 7}, "checks": store.load_health_checks()},
            fundamentals={"categories": store.load_fundamental_metrics()["categories"]},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertIn("fundamental_overclaim", result.payload["hard_fail_hits"])


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
        self.assertEqual(len(data["analysis"]["health_checks"]["checks"]), 7)
        self.assertEqual(data["analysis"]["fundamentals"]["summary"]["categories_total"], 5)
        self.assertEqual(len(data["analysis"]["fundamentals"]["categories"]), 5)

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

    def test_evidence_endpoint_when_flask_is_available(self) -> None:
        try:
            from backend.app import create_app
        except ModuleNotFoundError as exc:
            if exc.name == "flask":
                self.skipTest("Flask is not installed in this environment")
            raise

        app = create_app(REPO_ROOT)
        client = app.test_client()
        response = client.get("/api/research-runs/run_demo_phison_ai_ssd/evidence")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["run_id"], "run_demo_phison_ai_ssd")
        self.assertEqual(len(data["evidence"]["pages"]), 7)
        self.assertGreaterEqual(len(data["evidence"]["provenance"]), 5)
        self.assertNotIn("wiki", data)


if __name__ == "__main__":
    unittest.main()

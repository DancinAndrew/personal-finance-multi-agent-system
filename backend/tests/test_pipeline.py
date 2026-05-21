from __future__ import annotations

import unittest
from pathlib import Path

from backend.app.agents import EvaluationAgent
from backend.app.orchestrator import ResearchOrchestrator
from backend.app.store import FileStore


REPO_ROOT = Path(__file__).resolve().parents[2]
VALID_HEALTH_STATUSES = {"pass", "fail", "unknown", "not_available"}
VALID_FUNDAMENTAL_STATUSES = {"available", "partial", "missing", "not_available"}
VALID_VALUATION_STATUSES = {"available", "partial", "missing", "not_available"}
VALID_CHIP_COVERAGE_STATUSES = {"available", "partial", "missing", "not_available"}
VALID_CHIP_SIGNAL_BIASES = {
    "bullish",
    "bearish",
    "neutral",
    "mixed",
    "unknown",
    "not_available",
}
EXPECTED_FUNDAMENTAL_CATEGORY_IDS = {
    "revenue",
    "profitability",
    "safety",
    "growth",
    "cash_flow_quality",
}
EXPECTED_CHIP_SIGNAL_IDS = {
    "broker_branch_flow",
    "major_shareholders",
    "director_holdings",
    "director_pledges",
    "shareholder_count",
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
        self.assertEqual(len(snapshot["categories"]), 5)
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

    def test_valuation_fixture_has_required_shape(self) -> None:
        snapshot = self.store.load_valuation_fixture()
        self.assertEqual(snapshot["data_policy"], "public_fixture_only")
        self.assertFalse(snapshot["price"]["is_live_market_data"])
        self.assertEqual(snapshot["price"]["unit"], "TWD")

        required_top_level = {
            "as_of_date",
            "data_policy",
            "price",
            "multiples",
            "broker_targets",
            "missing_data",
        }
        self.assertTrue(required_top_level.issubset(snapshot.keys()))
        self.assertGreaterEqual(len(snapshot["multiples"]), 5)
        self.assertGreaterEqual(len(snapshot["broker_targets"]), 4)

        multiple_required = {
            "id",
            "label",
            "value",
            "unit",
            "coverage_status",
            "source_ids",
            "interpretation",
            "missing_data",
        }
        for multiple in snapshot["multiples"]:
            self.assertTrue(multiple_required.issubset(multiple.keys()))
            self.assertIn(multiple["coverage_status"], VALID_VALUATION_STATUSES)
            if multiple["value"] is None:
                self.assertNotEqual(multiple["coverage_status"], "available")
                self.assertGreater(len(multiple["missing_data"]), 0)

        broker_target_required = {
            "id",
            "source_label",
            "date",
            "source_ids",
            "reliability_note",
        }
        for target in snapshot["broker_targets"]:
            self.assertTrue(broker_target_required.issubset(target.keys()))
            self.assertTrue("target_price" in target or "target_price_range" in target)

    def test_valuation_fixture_source_ids_reference_catalog(self) -> None:
        source_ids = {source["id"] for source in self.store.load_source_catalog()}
        snapshot = self.store.load_valuation_fixture()
        self.assertTrue(set(snapshot["price"]["source_ids"]).issubset(source_ids))
        for multiple in snapshot["multiples"]:
            self.assertTrue(set(multiple["source_ids"]).issubset(source_ids))
        for target in snapshot["broker_targets"]:
            self.assertTrue(set(target["source_ids"]).issubset(source_ids))

    def test_chip_fixture_has_required_shape(self) -> None:
        snapshot = self.store.load_chip_fixture()
        self.assertEqual(snapshot["data_policy"], "public_fixture_only")
        self.assertEqual(len(snapshot["signals"]), 5)
        self.assertEqual(
            {signal["id"] for signal in snapshot["signals"]},
            EXPECTED_CHIP_SIGNAL_IDS,
        )

        required_top_level = {"as_of_date", "data_policy", "signals", "missing_data"}
        self.assertTrue(required_top_level.issubset(snapshot.keys()))
        signal_required = {
            "id",
            "name",
            "coverage_status",
            "signal_bias",
            "source_ids",
            "lookback_window",
            "summary",
            "missing_data",
            "data_policy",
        }
        for signal in snapshot["signals"]:
            self.assertTrue(signal_required.issubset(signal.keys()))
            self.assertIn(signal["coverage_status"], VALID_CHIP_COVERAGE_STATUSES)
            self.assertIn(signal["signal_bias"], VALID_CHIP_SIGNAL_BIASES)
            self.assertIsInstance(signal["source_ids"], list)
            self.assertIsInstance(signal["missing_data"], list)
            if signal["coverage_status"] == "missing":
                self.assertEqual(signal["signal_bias"], "unknown")
                self.assertGreater(len(signal["missing_data"]), 0)
            if signal["coverage_status"] == "not_available":
                self.assertEqual(signal["signal_bias"], "not_available")
                self.assertGreater(len(signal["missing_data"]), 0)

    def test_chip_fixture_source_ids_reference_catalog(self) -> None:
        source_ids = {source["id"] for source in self.store.load_source_catalog()}
        for signal in self.store.load_chip_fixture()["signals"]:
            self.assertTrue(set(signal["source_ids"]).issubset(source_ids))


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.orchestrator = ResearchOrchestrator(FileStore(REPO_ROOT))

    def test_default_run_contains_trace_report_and_evaluation(self) -> None:
        result = self.orchestrator.run_default()
        self.assertEqual(result["run"]["status"], "completed")
        self.assertEqual(len(result["steps"]), 10)
        self.assertIn("health_check_agent", [step["agent"] for step in result["steps"]])
        self.assertIn("valuation_agent", [step["agent"] for step in result["steps"]])
        self.assertIn("chip_agent", [step["agent"] for step in result["steps"]])
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
        self.assertEqual(len(fundamentals["categories"]), 5)
        self.assertEqual(fundamentals["summary"]["partial"], 3)
        self.assertEqual(fundamentals["summary"]["missing"], 2)
        self.assertEqual(fundamentals["summary"]["data_policy"], "public_fixture_only")
        self.assertEqual(
            {category["id"] for category in fundamentals["categories"]},
            EXPECTED_FUNDAMENTAL_CATEGORY_IDS,
        )
        self.assertGreaterEqual(len(fundamentals["key_findings"]), 2)
        self.assertIn("現金流", "、".join(fundamentals["data_gaps"]))

    def test_default_run_contains_valuation_analysis(self) -> None:
        result = self.orchestrator.run_default()
        valuation = result["analysis"]["valuation"]
        self.assertEqual(valuation["summary"]["data_policy"], "public_fixture_only")
        self.assertFalse(valuation["summary"]["is_live_market_data"])
        self.assertEqual(valuation["summary"]["price_as_of_date"], "2026-05-10")
        self.assertEqual(valuation["summary"]["coverage"]["partial"], 2)
        self.assertEqual(valuation["summary"]["coverage"]["missing"], 4)
        self.assertEqual(len(valuation["scenarios"]), 6)
        self.assertGreaterEqual(len(valuation["multiples"]), 5)
        self.assertGreaterEqual(len(valuation["broker_targets"]), 4)
        self.assertIn("歷史 P/E percentile", "、".join(valuation["data_gaps"]))
        self.assertTrue(
            any("AI SSD" in item and "支撐目前估值" in item for item in valuation["interpretation"])
        )

    def test_default_run_contains_chip_analysis(self) -> None:
        result = self.orchestrator.run_default()
        chip = result["analysis"]["chip"]
        self.assertEqual(chip["summary"]["data_policy"], "public_fixture_only")
        self.assertEqual(chip["summary"]["signals_total"], 5)
        self.assertEqual(chip["summary"]["coverage"]["missing"], 4)
        self.assertEqual(chip["summary"]["coverage"]["not_available"], 1)
        self.assertEqual(chip["summary"]["overall_signal"], "not_evaluable")
        self.assertEqual(len(chip["signals"]), 5)
        self.assertEqual({signal["id"] for signal in chip["signals"]}, EXPECTED_CHIP_SIGNAL_IDS)
        self.assertIn("分點買賣超", "、".join(chip["data_gaps"]))
        self.assertIn("董監質押", "、".join(chip["data_gaps"]))
        self.assertIn("股東人數", "、".join(chip["data_gaps"]))
        self.assertTrue(
            any("不能用籌碼面支持或反駁" in item for item in chip["interpretation"])
        )

    def test_health_check_consumes_chip_without_passing_chip_signal(self) -> None:
        result = self.orchestrator.run_default()
        health_checks = result["analysis"]["health_checks"]
        chip_check = next(check for check in health_checks["checks"] if check["id"] == "chip_signal")
        self.assertEqual(chip_check["status"], "not_available")
        self.assertIn("chip_signal", health_checks["summary"]["chip_alignment"])
        self.assertIn("not_evaluable", health_checks["summary"]["chip_alignment"]["chip_signal"])

    def test_price_override_changes_valuation_scenarios(self) -> None:
        default = self.orchestrator.run_default()
        overridden = self.orchestrator.run({"price": 3000})
        default_pe = default["analysis"]["valuation"]["scenarios"][1]["forward_pe"]
        override_pe = overridden["analysis"]["valuation"]["scenarios"][1]["forward_pe"]
        self.assertNotEqual(default_pe, override_pe)
        self.assertGreater(override_pe, default_pe)
        self.assertEqual(overridden["analysis"]["valuation"]["summary"]["price"], 3000)

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

    def test_report_contains_valuation_breakdown(self) -> None:
        report = self.orchestrator.run_default()["report"]["report_markdown"]
        self.assertIn("估值拆解", report)
        self.assertIn("示範股價日期", report)
        self.assertIn("非即時行情", report)
        self.assertIn("券商目標價區間", report)
        self.assertIn("P/B", report)
        self.assertIn("殖利率", report)
        self.assertIn("歷史 P/E percentile", report)
        forbidden = [
            "3,080 元就是合理價",
            "目標價就是買進理由",
            "Forward P/E 證明便宜",
            "CMoney 完整券商模型",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, report)

    def test_report_contains_chip_summary(self) -> None:
        report = self.orchestrator.run_default()["report"]["report_markdown"]
        self.assertIn("籌碼面摘要", report)
        for label in ["分點籌碼", "大股東持股", "董監持股", "董監質押", "股東人數"]:
            self.assertIn(label, report)
        self.assertIn("not_evaluable", report)
        self.assertIn("不是財報狗登入", report)
        self.assertIn("不是財報狗登入 / 付費資料、券商分點資料或即時籌碼 API", report)
        forbidden = ["籌碼轉強", "主力進場", "大股東增加", "散戶下降"]
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

    def test_evaluation_flags_missing_valuation_breakdown(self) -> None:
        store = FileStore(REPO_ROOT)
        health_checks = {"summary": {"total": 7}, "checks": store.load_health_checks()}
        fundamentals = {"categories": store.load_fundamental_metrics()["categories"]}
        result = EvaluationAgent().run(
            "run_missing_valuation",
            (
                "# 群聯電子（8299）研究輔助報告\n\n"
                "## 基本面拆解\n\n"
                "營收 partial；獲利能力 partial；安全性 missing；成長力 partial；現金流品質 missing。\n\n"
                "## 股票健診摘要\n\n"
                + "\n".join(f"- {check['name']}" for check in health_checks["checks"])
                + "\n\n這是研究輔助，不是買賣建議。"
            ),
            store.load_rubric(),
            provenance_count=5,
            health_checks=health_checks,
            fundamentals=fundamentals,
            valuation={"summary": {"coverage": {"partial": 2, "missing": 4}}},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertEqual(result.payload["status"], "needs_revision")

    def test_evaluation_flags_valuation_overclaim(self) -> None:
        store = FileStore(REPO_ROOT)
        result = EvaluationAgent().run(
            "run_bad_valuation",
            "估值拆解：3,080 元就是合理價，Forward P/E 證明便宜，目標價就是買進理由。",
            store.load_rubric(),
            provenance_count=5,
            health_checks={"summary": {"total": 7}, "checks": store.load_health_checks()},
            fundamentals={"categories": store.load_fundamental_metrics()["categories"]},
            valuation={"summary": {"coverage": {"partial": 2, "missing": 4}}},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertIn("valuation_overclaim", result.payload["hard_fail_hits"])

    def test_evaluation_flags_missing_chip_summary(self) -> None:
        store = FileStore(REPO_ROOT)
        result = EvaluationAgent().run(
            "run_missing_chip",
            (
                "# 群聯電子（8299）研究輔助報告\n\n"
                "## 估值拆解\n\n"
                "示範股價日期：2026-05-10；非即時行情；券商目標價區間。"
                "\n\n## 股票健診摘要\n\n"
                + "\n".join(f"- {check['name']}" for check in store.load_health_checks())
                + "\n\n## 基本面拆解\n\n"
                "營收 partial；獲利能力 partial；安全性 missing；成長力 partial；現金流品質 missing。"
            ),
            store.load_rubric(),
            provenance_count=5,
            health_checks={"summary": {"total": 7}, "checks": store.load_health_checks()},
            fundamentals={"categories": store.load_fundamental_metrics()["categories"]},
            valuation={"summary": {"major_gaps": ["P/B", "殖利率", "歷史 P/E percentile"]}},
            chip={"summary": {"signals_total": 5}, "signals": store.load_chip_fixture()["signals"]},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertEqual(result.payload["status"], "needs_revision")

    def test_evaluation_flags_chip_overclaim(self) -> None:
        store = FileStore(REPO_ROOT)
        result = EvaluationAgent().run(
            "run_bad_chip",
            "籌碼面摘要：主力進場，分點買超，大股東增加，籌碼轉強。",
            store.load_rubric(),
            provenance_count=5,
            health_checks={"summary": {"total": 7}, "checks": store.load_health_checks()},
            fundamentals={"categories": store.load_fundamental_metrics()["categories"]},
            valuation={"summary": {"coverage": {"partial": 2, "missing": 4}}},
            chip={"summary": {"signals_total": 5}, "signals": store.load_chip_fixture()["signals"]},
        )
        self.assertLess(result.payload["total_score"], 4.0)
        self.assertIn("chip_overclaim", result.payload["hard_fail_hits"])


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
        self.assertIn("valuation", data["analysis"])
        self.assertEqual(len(data["analysis"]["valuation"]["scenarios"]), 6)
        self.assertFalse(data["analysis"]["valuation"]["summary"]["is_live_market_data"])
        self.assertIn("chip", data["analysis"])
        self.assertEqual(len(data["analysis"]["chip"]["signals"]), 5)
        self.assertEqual(data["analysis"]["chip"]["summary"]["overall_signal"], "not_evaluable")

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

"""Local Markdown / JSON fixture store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FixtureNotFoundError(FileNotFoundError):
    """Raised when a required local fixture is missing."""


class FileStore:
    """Read local fixtures for the deterministic MVP."""

    HEALTH_STATUSES = {"pass", "fail", "unknown", "not_available"}
    FUNDAMENTAL_STATUSES = {"available", "partial", "missing", "not_available"}
    VALUATION_STATUSES = {"available", "partial", "missing", "not_available"}
    CHIP_COVERAGE_STATUSES = {"available", "partial", "missing", "not_available"}
    CHIP_SIGNAL_BIASES = {
        "bullish",
        "bearish",
        "neutral",
        "mixed",
        "unknown",
        "not_available",
    }
    TECHNICAL_COVERAGE_STATUSES = {"available", "partial", "missing", "not_available"}
    TECHNICAL_BIASES = {
        "bullish",
        "bearish",
        "neutral",
        "mixed",
        "unknown",
        "not_available",
    }
    FUNDAMENTAL_CATEGORY_IDS = {
        "revenue",
        "profitability",
        "safety",
        "growth",
        "cash_flow_quality",
    }
    CHIP_SIGNAL_IDS = {
        "broker_branch_flow",
        "major_shareholders",
        "director_holdings",
        "director_pledges",
        "shareholder_count",
    }
    TECHNICAL_SIGNAL_IDS = {
        "price_trend",
        "volume_trend",
        "moving_average_structure",
        "momentum",
        "volatility_risk",
    }

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def load_demo_run(self) -> dict[str, Any]:
        return self._load_json("data/phison/demo_run.json")

    def load_price_fixture(self) -> dict[str, Any]:
        return self._load_json("data/phison/price_fixture.json")

    def load_source_catalog(self) -> list[dict[str, Any]]:
        data = self._load_json("data/phison/source_catalog.json")
        if not isinstance(data, list):
            raise ValueError("source_catalog.json must contain a list")
        return data

    def load_rubric(self) -> dict[str, Any]:
        return self._load_json("data/evaluation/rubric.json")

    def load_health_checks(self) -> list[dict[str, Any]]:
        data = self._load_json("data/phison/health_check_fixture.json")
        if not isinstance(data, list):
            raise ValueError("health_check_fixture.json must contain a list")

        source_ids = {source["id"] for source in self.load_source_catalog()}
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
        for check in data:
            missing = required.difference(check)
            if missing:
                raise ValueError(f"Health check fixture missing fields: {sorted(missing)}")
            self._validate_health_status(check["status"])
            self._validate_source_ids(check["source_ids"], source_ids, check["id"])
            if not isinstance(check["criteria"], list):
                raise ValueError(f"Health check criteria must be a list: {check['id']}")
            for criterion in check["criteria"]:
                self._validate_health_status(criterion.get("status"))
                self._validate_source_ids(criterion.get("source_ids", []), source_ids, criterion["id"])
        return data

    def load_fundamental_metrics(self) -> dict[str, Any]:
        data = self._load_json("data/phison/fundamental_metrics_fixture.json")
        if not isinstance(data, dict):
            raise ValueError("fundamental_metrics_fixture.json must contain an object")

        required_top_level = {"as_of_date", "data_policy", "categories"}
        missing_top_level = required_top_level.difference(data)
        if missing_top_level:
            raise ValueError(
                f"Fundamental metrics fixture missing fields: {sorted(missing_top_level)}"
            )
        if data["data_policy"] != "public_fixture_only":
            raise ValueError("Fundamental metrics fixture must use public_fixture_only")
        categories = data["categories"]
        if not isinstance(categories, list):
            raise ValueError("fundamental metrics categories must be a list")
        if len(categories) != len(self.FUNDAMENTAL_CATEGORY_IDS):
            raise ValueError(
                "Fundamental metrics categories must contain exactly "
                f"{len(self.FUNDAMENTAL_CATEGORY_IDS)} items"
            )
        category_ids = {category.get("id") for category in categories}
        if category_ids != self.FUNDAMENTAL_CATEGORY_IDS:
            raise ValueError(
                "Fundamental metrics categories must be exactly "
                f"{sorted(self.FUNDAMENTAL_CATEGORY_IDS)}"
            )

        source_ids = {source["id"] for source in self.load_source_catalog()}
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
        for category in categories:
            category_id = category["id"]
            missing = category_required.difference(category)
            if missing:
                raise ValueError(
                    f"Fundamental category {category_id} missing fields: {sorted(missing)}"
                )
            self._validate_fundamental_status(category["coverage_status"])
            if not isinstance(category["metrics"], list) or not category["metrics"]:
                raise ValueError(f"Fundamental category {category_id} must contain metrics")
            if not isinstance(category["missing_data"], list):
                raise ValueError(f"Fundamental category {category_id} missing_data must be a list")
            for metric in category["metrics"]:
                metric_id = metric.get("id", "<missing>")
                missing_metric_fields = metric_required.difference(metric)
                if missing_metric_fields:
                    raise ValueError(
                        f"Fundamental metric {metric_id} missing fields: "
                        f"{sorted(missing_metric_fields)}"
                    )
                self._validate_fundamental_status(metric["coverage_status"])
                self._validate_source_ids(metric["source_ids"], source_ids, metric_id)
                if metric["coverage_status"] == "available" and not metric["source_ids"]:
                    raise ValueError(f"Available fundamental metric needs source_ids: {metric_id}")
                if metric["value"] is None:
                    if metric["coverage_status"] == "available":
                        raise ValueError(
                            f"Fundamental metric with null value cannot be available: {metric_id}"
                        )
                    if not metric["missing_data"]:
                        raise ValueError(
                            f"Fundamental metric with null value needs missing_data: {metric_id}"
                        )
        return data

    def load_valuation_fixture(self) -> dict[str, Any]:
        data = self._load_json("data/phison/valuation_fixture.json")
        if not isinstance(data, dict):
            raise ValueError("valuation_fixture.json must contain an object")

        required_top_level = {
            "as_of_date",
            "data_policy",
            "price",
            "multiples",
            "broker_targets",
            "missing_data",
        }
        missing_top_level = required_top_level.difference(data)
        if missing_top_level:
            raise ValueError(f"Valuation fixture missing fields: {sorted(missing_top_level)}")
        if data["data_policy"] != "public_fixture_only":
            raise ValueError("Valuation fixture must use public_fixture_only")
        if not isinstance(data["missing_data"], list):
            raise ValueError("Valuation fixture missing_data must be a list")

        source_ids = {source["id"] for source in self.load_source_catalog()}
        self._validate_valuation_price(data["price"], source_ids)
        self._validate_valuation_multiples(data["multiples"], source_ids)
        self._validate_broker_targets(data["broker_targets"], source_ids)
        return data

    def load_chip_fixture(self) -> dict[str, Any]:
        data = self._load_json("data/phison/chip_fixture.json")
        if not isinstance(data, dict):
            raise ValueError("chip_fixture.json must contain an object")

        required_top_level = {"as_of_date", "data_policy", "signals", "missing_data"}
        missing_top_level = required_top_level.difference(data)
        if missing_top_level:
            raise ValueError(f"Chip fixture missing fields: {sorted(missing_top_level)}")
        if data["data_policy"] != "public_fixture_only":
            raise ValueError("Chip fixture must use public_fixture_only")
        if not isinstance(data["missing_data"], list):
            raise ValueError("Chip fixture missing_data must be a list")
        signals = data["signals"]
        if not isinstance(signals, list):
            raise ValueError("Chip fixture signals must be a list")
        if len(signals) != len(self.CHIP_SIGNAL_IDS):
            raise ValueError(
                f"Chip fixture must contain exactly {len(self.CHIP_SIGNAL_IDS)} signals"
            )
        signal_ids = {signal.get("id") for signal in signals}
        if signal_ids != self.CHIP_SIGNAL_IDS:
            raise ValueError(f"Chip fixture signals must be exactly {sorted(self.CHIP_SIGNAL_IDS)}")

        source_ids = {source["id"] for source in self.load_source_catalog()}
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
        for signal in signals:
            signal_id = signal.get("id", "<missing>")
            missing = signal_required.difference(signal)
            if missing:
                raise ValueError(f"Chip signal {signal_id} missing fields: {sorted(missing)}")
            self._validate_chip_coverage_status(signal["coverage_status"])
            self._validate_chip_signal_bias(signal["signal_bias"])
            if not isinstance(signal["source_ids"], list):
                raise ValueError(f"Chip signal {signal_id} source_ids must be a list")
            if not isinstance(signal["missing_data"], list):
                raise ValueError(f"Chip signal {signal_id} missing_data must be a list")
            self._validate_source_ids(signal["source_ids"], source_ids, signal_id)
            if signal["coverage_status"] == "missing" and signal["signal_bias"] != "unknown":
                raise ValueError(f"Missing chip signal must have unknown bias: {signal_id}")
            if (
                signal["coverage_status"] == "not_available"
                and signal["signal_bias"] != "not_available"
            ):
                raise ValueError(
                    f"Not-available chip signal must have not_available bias: {signal_id}"
                )
            if signal["coverage_status"] in {"missing", "not_available"} and not signal[
                "missing_data"
            ]:
                raise ValueError(f"Unavailable chip signal needs missing_data: {signal_id}")
        return data

    def load_technical_fixture(self) -> dict[str, Any]:
        data = self._load_json("data/phison/technical_fixture.json")
        if not isinstance(data, dict):
            raise ValueError("technical_fixture.json must contain an object")

        required_top_level = {
            "as_of_date",
            "data_policy",
            "price_data_policy",
            "signals",
            "missing_data",
        }
        missing_top_level = required_top_level.difference(data)
        if missing_top_level:
            raise ValueError(f"Technical fixture missing fields: {sorted(missing_top_level)}")
        if data["data_policy"] != "public_fixture_only":
            raise ValueError("Technical fixture must use public_fixture_only")
        if data["price_data_policy"] != "manual_public_snapshot_only":
            raise ValueError("Technical fixture must use manual_public_snapshot_only")
        if not isinstance(data["missing_data"], list):
            raise ValueError("Technical fixture missing_data must be a list")
        signals = data["signals"]
        if not isinstance(signals, list):
            raise ValueError("Technical fixture signals must be a list")
        if len(signals) != len(self.TECHNICAL_SIGNAL_IDS):
            raise ValueError(
                f"Technical fixture must contain exactly {len(self.TECHNICAL_SIGNAL_IDS)} signals"
            )
        signal_ids = {signal.get("id") for signal in signals}
        if signal_ids != self.TECHNICAL_SIGNAL_IDS:
            raise ValueError(
                f"Technical fixture signals must be exactly {sorted(self.TECHNICAL_SIGNAL_IDS)}"
            )

        source_ids = {source["id"] for source in self.load_source_catalog()}
        signal_required = {
            "id",
            "name",
            "coverage_status",
            "technical_bias",
            "source_ids",
            "lookback_window",
            "metric_values",
            "summary",
            "missing_data",
            "data_policy",
        }
        for signal in signals:
            signal_id = signal.get("id", "<missing>")
            missing = signal_required.difference(signal)
            if missing:
                raise ValueError(f"Technical signal {signal_id} missing fields: {sorted(missing)}")
            self._validate_technical_coverage_status(signal["coverage_status"])
            self._validate_technical_bias(signal["technical_bias"])
            if not isinstance(signal["source_ids"], list):
                raise ValueError(f"Technical signal {signal_id} source_ids must be a list")
            if not isinstance(signal["metric_values"], dict):
                raise ValueError(f"Technical signal {signal_id} metric_values must be an object")
            if not isinstance(signal["missing_data"], list):
                raise ValueError(f"Technical signal {signal_id} missing_data must be a list")
            self._validate_source_ids(signal["source_ids"], source_ids, signal_id)
            if signal["coverage_status"] == "missing" and signal["technical_bias"] != "unknown":
                raise ValueError(f"Missing technical signal must have unknown bias: {signal_id}")
            if (
                signal["coverage_status"] == "not_available"
                and signal["technical_bias"] != "not_available"
            ):
                raise ValueError(
                    f"Not-available technical signal must have not_available bias: {signal_id}"
                )
            if signal["coverage_status"] in {"missing", "not_available"} and not signal[
                "missing_data"
            ]:
                raise ValueError(f"Unavailable technical signal needs missing_data: {signal_id}")
        return data

    def load_provenance(self) -> list[dict[str, Any]]:
        data = self._load_json("knowledge/phison/provenance.json")
        if not isinstance(data, list):
            raise ValueError("provenance.json must contain a list")
        return data

    def load_source_excerpts(self, source_ids: list[str] | None = None) -> dict[str, str]:
        catalog = self.load_source_catalog()
        selected_ids = set(source_ids or [source["id"] for source in catalog])
        excerpts: dict[str, str] = {}
        for source in catalog:
            if source["id"] not in selected_ids:
                continue
            excerpt_path = source.get("excerpt_path")
            if not excerpt_path:
                continue
            excerpts[source["id"]] = self._load_text(excerpt_path)
        return excerpts

    def load_evidence_pages(self) -> list[dict[str, str]]:
        pages_dir = self.repo_root / "knowledge/phison/pages"
        if not pages_dir.exists():
            raise FixtureNotFoundError(f"Missing evidence directory: {pages_dir}")

        pages = [
            {"name": path.name, "content": path.read_text(encoding="utf-8")}
            for path in sorted(pages_dir.glob("*.md"))
        ]
        contradiction_log = self.repo_root / "knowledge/phison/Contradiction_Log.md"
        pages.append(
            {
                "name": "Contradiction_Log.md",
                "content": contradiction_log.read_text(encoding="utf-8"),
            }
        )
        return pages

    def _load_json(self, relative_path: str) -> Any:
        path = self.repo_root / relative_path
        if not path.exists():
            raise FixtureNotFoundError(f"Missing fixture: {path}")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON fixture: {path}") from exc

    def _load_text(self, relative_path: str) -> str:
        path = self.repo_root / relative_path
        if not path.exists():
            raise FixtureNotFoundError(f"Missing fixture: {path}")
        return path.read_text(encoding="utf-8")

    def _validate_health_status(self, status: Any) -> None:
        if status not in self.HEALTH_STATUSES:
            raise ValueError(f"Invalid health check status: {status}")

    def _validate_fundamental_status(self, status: Any) -> None:
        if status not in self.FUNDAMENTAL_STATUSES:
            raise ValueError(f"Invalid fundamental coverage status: {status}")

    def _validate_valuation_status(self, status: Any) -> None:
        if status not in self.VALUATION_STATUSES:
            raise ValueError(f"Invalid valuation coverage status: {status}")

    def _validate_chip_coverage_status(self, status: Any) -> None:
        if status not in self.CHIP_COVERAGE_STATUSES:
            raise ValueError(f"Invalid chip coverage status: {status}")

    def _validate_chip_signal_bias(self, bias: Any) -> None:
        if bias not in self.CHIP_SIGNAL_BIASES:
            raise ValueError(f"Invalid chip signal bias: {bias}")

    def _validate_technical_coverage_status(self, status: Any) -> None:
        if status not in self.TECHNICAL_COVERAGE_STATUSES:
            raise ValueError(f"Invalid technical coverage status: {status}")

    def _validate_technical_bias(self, bias: Any) -> None:
        if bias not in self.TECHNICAL_BIASES:
            raise ValueError(f"Invalid technical bias: {bias}")

    def _validate_source_ids(
        self,
        ids: list[str],
        valid_source_ids: set[str],
        owner_id: str,
    ) -> None:
        invalid = set(ids).difference(valid_source_ids)
        if invalid:
            raise ValueError(f"Unknown source ids for {owner_id}: {sorted(invalid)}")

    def _validate_valuation_price(
        self,
        price: Any,
        valid_source_ids: set[str],
    ) -> None:
        if not isinstance(price, dict):
            raise ValueError("Valuation price must be an object")
        required = {"value", "unit", "as_of_date", "is_live_market_data", "source_ids"}
        missing = required.difference(price)
        if missing:
            raise ValueError(f"Valuation price missing fields: {sorted(missing)}")
        if price["unit"] != "TWD":
            raise ValueError("Valuation price unit must be TWD")
        if price["is_live_market_data"] is not False:
            raise ValueError("Valuation fixture price must not be live market data")
        if not isinstance(price["source_ids"], list):
            raise ValueError("Valuation price source_ids must be a list")
        self._validate_source_ids(price["source_ids"], valid_source_ids, "valuation_price")

    def _validate_valuation_multiples(
        self,
        multiples: Any,
        valid_source_ids: set[str],
    ) -> None:
        if not isinstance(multiples, list) or not multiples:
            raise ValueError("Valuation multiples must be a non-empty list")
        required = {
            "id",
            "label",
            "value",
            "unit",
            "coverage_status",
            "source_ids",
            "interpretation",
            "missing_data",
        }
        for multiple in multiples:
            multiple_id = multiple.get("id", "<missing>")
            missing = required.difference(multiple)
            if missing:
                raise ValueError(f"Valuation multiple {multiple_id} missing fields: {sorted(missing)}")
            self._validate_valuation_status(multiple["coverage_status"])
            if not isinstance(multiple["missing_data"], list):
                raise ValueError(f"Valuation multiple {multiple_id} missing_data must be a list")
            self._validate_source_ids(multiple["source_ids"], valid_source_ids, multiple_id)
            if multiple["value"] is None:
                if multiple["coverage_status"] == "available":
                    raise ValueError(
                        f"Valuation multiple with null value cannot be available: {multiple_id}"
                    )
                if not multiple["missing_data"]:
                    raise ValueError(
                        f"Valuation multiple with null value needs missing_data: {multiple_id}"
                    )

    def _validate_broker_targets(
        self,
        broker_targets: Any,
        valid_source_ids: set[str],
    ) -> None:
        if not isinstance(broker_targets, list) or not broker_targets:
            raise ValueError("Valuation broker_targets must be a non-empty list")
        required = {"id", "source_label", "date", "source_ids", "reliability_note"}
        for target in broker_targets:
            target_id = target.get("id", "<missing>")
            missing = required.difference(target)
            if missing:
                raise ValueError(f"Broker target {target_id} missing fields: {sorted(missing)}")
            if "target_price" not in target and "target_price_range" not in target:
                raise ValueError(f"Broker target {target_id} needs target_price or target_price_range")
            if "target_price_range" in target:
                price_range = target["target_price_range"]
                if not isinstance(price_range, dict) or {"low", "high"}.difference(price_range):
                    raise ValueError(f"Broker target {target_id} has invalid target_price_range")
            self._validate_source_ids(target["source_ids"], valid_source_ids, target_id)

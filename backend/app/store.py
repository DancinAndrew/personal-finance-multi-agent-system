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
    FUNDAMENTAL_CATEGORY_IDS = {
        "revenue",
        "profitability",
        "safety",
        "growth",
        "cash_flow_quality",
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

    def _validate_source_ids(
        self,
        ids: list[str],
        valid_source_ids: set[str],
        owner_id: str,
    ) -> None:
        invalid = set(ids).difference(valid_source_ids)
        if invalid:
            raise ValueError(f"Unknown source ids for {owner_id}: {sorted(invalid)}")

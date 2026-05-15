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

    def _validate_source_ids(
        self,
        ids: list[str],
        valid_source_ids: set[str],
        owner_id: str,
    ) -> None:
        invalid = set(ids).difference(valid_source_ids)
        if invalid:
            raise ValueError(f"Unknown source ids for {owner_id}: {sorted(invalid)}")

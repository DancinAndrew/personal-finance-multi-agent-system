"""Flask application factory."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def create_app(repo_root: Path | None = None) -> Any:
    """Create the Flask app.

    Flask is imported inside the factory so core pipeline tests can run without
    requiring web dependencies to be installed.
    """

    from flask import Flask, jsonify, request

    from .orchestrator import ResearchOrchestrator
    from .store import FileStore

    root = repo_root or Path(__file__).resolve().parents[2]
    store = FileStore(root)
    orchestrator = ResearchOrchestrator(store)
    runs: dict[str, dict[str, Any]] = {}

    app = Flask(__name__)

    @app.after_request
    def add_cors_headers(response: Any) -> Any:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    @app.get("/api/health")
    def health() -> Any:
        return jsonify({"status": "ok", "mode": "deterministic_demo"})

    @app.get("/api/demo/default-run")
    def default_run() -> Any:
        result = orchestrator.run_default()
        runs[result["run"]["id"]] = result
        return jsonify(result)

    @app.post("/api/research-runs")
    def create_research_run() -> Any:
        payload = request.get_json(silent=True) or {}
        result = orchestrator.run(payload)
        runs[result["run"]["id"]] = result
        return jsonify(result), 201

    @app.get("/api/research-runs/<run_id>")
    def get_research_run(run_id: str) -> Any:
        result = _get_or_create_run(run_id)
        if result is None:
            return jsonify({"error": "research_run_not_found", "run_id": run_id}), 404
        return jsonify(result)

    @app.get("/api/research-runs/<run_id>/steps")
    def get_research_steps(run_id: str) -> Any:
        result = _get_or_create_run(run_id)
        if result is None:
            return jsonify({"error": "research_run_not_found", "run_id": run_id}), 404
        return jsonify({"run_id": run_id, "steps": result["steps"]})

    @app.get("/api/research-runs/<run_id>/sources")
    def get_research_sources(run_id: str) -> Any:
        result = _get_or_create_run(run_id)
        if result is None:
            return jsonify({"error": "research_run_not_found", "run_id": run_id}), 404
        return jsonify({"run_id": run_id, "sources": result["sources"]})

    @app.get("/api/research-runs/<run_id>/evaluation")
    def get_research_evaluation(run_id: str) -> Any:
        result = _get_or_create_run(run_id)
        if result is None:
            return jsonify({"error": "research_run_not_found", "run_id": run_id}), 404
        return jsonify({"run_id": run_id, "evaluation": result["evaluation"]})

    @app.get("/api/research-runs/<run_id>/evidence")
    def get_research_evidence(run_id: str) -> Any:
        result = _get_or_create_run(run_id)
        if result is None:
            return jsonify({"error": "research_run_not_found", "run_id": run_id}), 404
        return jsonify({"run_id": run_id, "evidence": result["evidence"]})

    def _get_or_create_run(run_id: str) -> dict[str, Any] | None:
        if run_id in runs:
            return runs[run_id]
        if run_id == store.load_demo_run()["id"]:
            result = orchestrator.run_default()
            runs[run_id] = result
            return result
        return None

    return app

"""Run the Flask app with `python -m backend.app`."""

from __future__ import annotations

from . import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)

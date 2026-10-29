"""CLI: genera 05-core-middleware/openapi.yaml."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.export_openapi import export_openapi  # noqa: E402

if __name__ == "__main__":
    print(export_openapi())

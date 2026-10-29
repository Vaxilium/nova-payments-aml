"""Exporta el contrato OpenAPI a YAML."""

from __future__ import annotations

from pathlib import Path

import yaml

from .api import create_app
from .config import OPENAPI_PATH


def export_openapi(output: str | Path | None = None) -> Path:
    destination = Path(output) if output is not None else OPENAPI_PATH
    spec = create_app().openapi()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        yaml.safe_dump(spec, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return destination


if __name__ == "__main__":
    print(export_openapi())

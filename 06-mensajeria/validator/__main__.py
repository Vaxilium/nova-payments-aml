"""CLI mínima: ``python -m validator --message archivo.xml``."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .mapping import mt103_to_pacs008_fields
from .mt103 import parse_mt103, validate_mt103
from .xml_messages import validate_message, validate_pacs008_international


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida mensajes ISO 20022 y MT103 del caso NovaBank")
    parser.add_argument("--message", type=Path, help="Archivo XML ISO 20022")
    parser.add_argument("--international-pacs008", action="store_true", help="Exige IBAN y BIC en pacs.008")
    parser.add_argument("--mt103", type=Path, help="Archivo MT103")
    parser.add_argument("--map", action="store_true", help="Muestra el mapeo MT103 → pacs.008")
    args = parser.parse_args()
    if not args.message and not args.mt103:
        parser.print_help()
        return 2
    if args.message:
        text = _read(args.message)
        result = (
            validate_pacs008_international(text)
            if args.international_pacs008
            else validate_message(text)
        )
        print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
        return 0 if result.valid else 1
    text = _read(args.mt103)
    result = validate_mt103(text)
    payload: dict[str, object] = {"validation": result.as_dict()}
    if result.valid and args.map:
        payload["mapping"] = mt103_to_pacs008_fields(parse_mt103(text))
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

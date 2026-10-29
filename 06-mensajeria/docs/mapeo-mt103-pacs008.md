# Mapeo funcional MT103 ↔ pacs.008

**Propósito:** documentar las equivalencias usadas por el caso para migrar instrucciones MT103 al perfil ISO 20022. No es una traducción certificada por SWIFT.

> **Supuesto:** el mapeo es una propuesta funcional del caso (S-064, SNV-09). La conformidad con las reglas CBPR+ y con un motor de traducción real debe verificarse antes de usarlo en producción.

## Tabla de equivalencias

| MT103 | ISO 20022 (`pacs.008`) | Dirección | Regla del caso |
|---|---|---|---|
| `20` | `PmtId/InstrId` y `PmtId/EndToEndId` | MT103 → pacs.008 | La referencia del ordenante se reutiliza si no hay otro identificador |
| `23B` | `PmtTpInf` (informativo) | MT103 → pacs.008 | Sin equivalencia ISO única en este perfil |
| `32A` | `IntrBkSttlmAmt/@Ccy` + `IntrBkSttlmDt` | MT103 → pacs.008 | Fecha valor → fecha de liquidación; moneda/importe → importe interbancario |
| `33B` | `InstdAmt/@Ccy` | MT103 → pacs.008 | Opcional si coincide con `32A` |
| `50K` | `Dbtr/Nm` + `Dbtr/Acct/Id/Othr/Id` | MT103 → pacs.008 | Cuenta local como `Othr/Id` |
| `52A` | `DbtrAgt/FinInstnId/BICFI` | MT103 → pacs.008 | BIC del banco ordenante |
| `57A` | `CdtrAgt/FinInstnId/BICFI` | MT103 → pacs.008 | BIC del banco beneficiario |
| `59` | `Cdtr/Nm` + `Cdtr/Acct` + `Cdtr/Agt` | MT103 → pacs.008 | Beneficiario, cuenta/IBAN y BIC si existe |
| `70` | `RmtInf/Ustrd` | MT103 → pacs.008 | Remesa no estructurada |
| `71A` | `ChrgBr` | MT103 → pacs.008 | `OUR→DEBT`, `SHA→SHAR`, `BEN→CRED` |
| `72` | `RmtInf` o datos suplementarios | MT103 → pacs.008 | No se usa en el flujo principal |
| `PmtId/EndToEndId` | `20` | pacs.008 → MT103 | Se conserva como referencia del mensaje |
| `IntrBkSttlmAmt` + `IntrBkSttlmDt` | `32A` | pacs.008 → MT103 | Se compone fecha valor + moneda + importe |
| `ChrgBr` | `71A` | pacs.008 → MT103 | `DEBT→OUR`, `SHAR→SHA`, `CRED→BEN` |

La misma tabla está disponible para importación en [`mapping/mt103-pacs008.csv`](../mapping/mt103-pacs008.csv).

## Reglas de transformación

1. **Referencias:** `20` se recorta a 35 caracteres para cumplir Max35Text. Si no hay `EndToEndId`, se usa como referencia extremo a extremo.
2. **Importes:** se respeta la escala de la moneda. PYG se expresa sin decimales; USD con dos decimales (`S-066`, ISO 4217 F-13).
3. **Fecha valor:** `32A` aporta `YYMMDD`; se convierte a `YYYY-MM-DD`.
4. **Cargos:** el mapeo es biyectivo para `OUR/SHA/BEN` ↔ `DEBT/SHAR/CRED`.
5. **Cuentas:** `50K` y `59` pueden incluir `/cuenta` seguido del nombre. El parser separa la cuenta de las líneas de nombre.
6. **BIC:** se aceptan 8 u 11 caracteres (ISO 9362, F-15/F-16).
7. **Montos PYG:** no se agregan decimales artificiales al generar `32A`.

## Ejemplo

MT103 de entrada: [`examples/mt/mt103-international-transfer.txt`](../examples/mt/mt103-international-transfer.txt).

```text
20  → INV-2026-0001
32A → 261028USD1250,00
50K → /00000000000001 / ANA DEMO
59  → /DE89370400440532013000 / JOHN DEMO
71A → SHA → SHAR
```

## Uso del CLI

```powershell
cd 06-mensajeria
..\.venv\Scripts\python.exe -m validator --mt103 examples\mt\mt103-international-transfer.txt
```

El comando devuelve el resultado de validación del MT103. El mapeo a campos `pacs.008` se obtiene desde Python:

```python
from validator.mt103 import parse_mt103
from validator.mapping import mt103_to_pacs008_fields

message = parse_mt103(open("examples/mt/mt103-international-transfer.txt", encoding="utf-8").read())
fields = mt103_to_pacs008_fields(message)
```

## Limitaciones

- No se modelan mensajes de cobertura, instrucciones de banco corresponsal ni redes SWIFT reales.
- `23B` y `72` no tienen una equivalencia ISO 20022 única en este perfil.
- La tabla no reemplaza las reglas de validación de un proveedor CBPR+ certificado.

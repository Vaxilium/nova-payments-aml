# Validador de mensajes

**Propósito:** validar identificadores, monedas, importes, campos obligatorios y estados de los mensajes usados en el caso, sin depender de conectividad externa.

## Componentes

| Archivo | Responsabilidad |
|---|---|
| `validator/validation.py` | `ValidationIssue`, `ValidationResult` y `MessageValidationError` |
| `validator/iso4217.py` | Tabla estática ISO 4217 generada desde el XML de SIX (F-13) |
| `validator/identifiers.py` | IBAN (MOD 97-10), BIC (ISO 9362), Max35Text y UETR |
| `validator/amounts.py` | Importes decimales, escala por moneda y conversión a unidades menores |
| `validator/xml_messages.py` | Validación estructural de pain.001, pacs.008, pacs.002 y camt.053 |
| `validator/mt103.py` | Parser y validación de MT103 |
| `validator/mapping.py` | Equivalencias MT103 ↔ pacs.008 |
| `validator/__main__.py` | CLI para XML, MT103 y mapeo |

## Capas de validación

1. **XML:** documento bien formado, raíz `Document` y tipo de mensaje reconocido.
2. **Cabecera:** `MsgId`, `CreDtTm`, `NbOfTxs` y, en pain.001, `CtrlSum`.
3. **Identificadores:** IBAN con longitud de país y checksum; BIC de 8/11; referencias Max35Text; UETR UUID v4.
4. **Moneda e importe:** código ISO 4217 activo, importe numérico no negativo y escala correcta (PYG 0; USD 2).
5. **Reglas de negocio del perfil:** cuentas, agentes, estados, motivos de rechazo y coherencia de cantidad de transacciones.

`validate_pacs008_international` agrega dos reglas: el beneficiario debe usar IBAN y ambos agentes (`DbtrAgt` y `CdtrAgt`) deben informar BIC.

## Uso

Desde `06-mensajeria`:

```powershell
# Mensaje local o genérico
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pacs.008-customer-credit-transfer.xml

# Perfil internacional (IBAN + agentes BIC)
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pacs.008-customer-credit-transfer.xml --international-pacs008

# MT103
..\.venv\Scripts\python.exe -m validator --mt103 examples\mt\mt103-international-transfer.txt

# MT103 + mapeo a pacs.008
..\.venv\Scripts\python.exe -m validator --mt103 examples\mt\mt103-international-transfer.txt --map
```

La salida es JSON con `valid` y la lista de `issues`. El código de salida es `0` si el mensaje es válido y `1` si tiene errores.

## Códigos de error principales

| Código | Causa |
|---|---|
| `XML_PARSE` | XML mal formado o archivo ilegible |
| `XML_ROOT` / `XML_BODY` / `MESSAGE_TYPE` | Raíz, cuerpo o tipo no soportado |
| `IBAN_FORMAT`, `IBAN_LENGTH`, `IBAN_CHECKSUM` | IBAN inválido |
| `IBAN_COUNTRY_UNSUPPORTED` | País fuera de la tabla IBAN del validador |
| `BIC_FORMAT` | BIC distinto de 8/11 caracteres |
| `CURRENCY_UNKNOWN` | Código fuera de ISO 4217 |
| `AMOUNT_FORMAT`, `AMOUNT_PRECISION`, `AMOUNT_NEGATIVE` | Importe inválido |
| `FIELD_REQUIRED`, `ACCOUNT_REQUIRED`, `PARTY_REQUIRED` | Campo obligatorio ausente |
| `STATUS_INVALID`, `REJECT_REASON_REQUIRED` | Estado o motivo inválido en pacs.002 |

## Límites

- No valida contra XSD oficiales ni aplica todas las reglas CBPR+ (S-056).
- La tabla IBAN cubre 77 países y territorios; no es el registro completo.
- La tabla ISO 4217 es estática: no se actualiza en tiempo de ejecución.
- No valida firmas, cifrado ni conectividad.

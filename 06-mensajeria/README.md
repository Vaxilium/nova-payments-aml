# 06 — Mensajería financiera

Modelado, validación y simulación de pagos locales e internacionales para NovaBank. Todo el contenido es ficticio y reproducible.

## Contenido

| Artefacto | Ubicación |
|---|---|
| Catálogo ISO 20022 y reglas usadas | [`docs/catalogo-iso20022.md`](docs/catalogo-iso20022.md) |
| Mapeo funcional MT103 ↔ pacs.008 | [`docs/mapeo-mt103-pacs008.md`](docs/mapeo-mt103-pacs008.md) |
| Validador | [`docs/validador.md`](docs/validador.md) y `validator/` |
| Simuladores local e internacional | [`docs/simuladores.md`](docs/simuladores.md) y `simulator/` |
| Ejemplos XML y MT103 | [`examples/`](examples/) |
| Tabla importable de mapeo | [`mapping/mt103-pacs008.csv`](mapping/mt103-pacs008.csv) |
| Diagramas Mermaid | [`diagrams/`](diagrams/) |
| Pruebas | [`tests/`](tests/) |

## Alcance

- **Local:** pago instantáneo PYG inspirado en el SPI del BCP, con tope de ₲10.000.000, alias/cuenta y máquina de estados.
- **Internacional:** transferencia saliente con IBAN/BIC, mensaje `pacs.008`, comisión configurable y liquidación USD en el core.
- **Validación:** IBAN (MOD 97-10), BIC (ISO 9362), ISO 4217, importes, Max35Text, UETR y campos obligatorios.
- **Mensajes:** `pain.001.001.09`, `pacs.008.001.08`, `pacs.002.001.10` y `camt.053.001.08` como versiones de ejemplo.

Fuera de alcance: conectividad real con SWIFT/BCP, XSD oficiales, firma/cifrado y traducción MT103 certificada. Ver supuestos S-056 a S-066 en [`docs/SUPUESTOS.md`](../docs/SUPUESTOS.md).

## Inicio rápido

```powershell
# Desde la raíz del repositorio
.\.venv\Scripts\Activate.ps1

# Validar los ejemplos
cd 06-mensajeria
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pacs.008-customer-credit-transfer.xml --international-pacs008
..\.venv\Scripts\python.exe -m validator --mt103 examples\mt\mt103-international-transfer.txt --map

# Pruebas de todo el repositorio
cd ..
.\.venv\Scripts\python.exe -m pytest -q
```

## Resultado verificado

- `pytest -q`: **158 pruebas aprobadas** (69 del core + 89 de mensajería), 0 fallos.
- Los cinco ejemplos ISO 20022 y el MT103 publicado se validan sin errores.
- El simulador internacional balancea el asiento: débito `2102` por importe + comisión; crédito `1102` por importe; crédito `4102` por comisión.

## Integración con el core

| Punto | Uso |
|---|---|
| `app.service.BankingService` | Cuentas, transferencias internas y débitos |
| `app.ledger.post_entry` | Asiento de partida doble |
| `app.db.connect` | Lectura de saldos y auditoría |
| `simulator.core_bridge.CoreLedgerBridge` | Posteo internacional con comisión |

El core usa unidades menores enteras (`PYG` 0 decimales, `USD` 2). La mensajería convierte con `validator.amounts.to_minor` antes de postear.

## Regla de fuentes

Toda referencia a estándares se registra en [`docs/FUENTES.md`](../docs/FUENTES.md). Las definiciones no verificables están marcadas como `SUPUESTO NO VERIFICADO` y registradas en [`docs/PENDIENTES.md`](../docs/PENDIENTES.md).

# Catálogo ISO 20022 del caso

**Alcance:** campos y reglas que usa NovaBank para los mensajes de pago del caso. No es el catálogo completo de ISO 20022 ni una declaración de conformidad XSD.

**Versiones de ejemplo:** `pain.001.001.09`, `pacs.008.001.08`, `pacs.002.001.10` y `camt.053.001.08`, alineadas al baseline CBPR+ vigente al cierre de la coexistencia MT/ISO 20022 (F-18, S-057).

> El validador aplica reglas estructurales y de negocio sobre estos campos (S-056). Los XSD oficiales no se descargaron por bloqueo de acceso automatizado (P-008).

## Cabecera común

| Campo | Uso en el caso | Regla aplicada |
|---|---|---|
| `GrpHdr/MsgId` | Identificador del mensaje | Obligatorio; hasta 35 caracteres |
| `GrpHdr/CreDtTm` | Fecha y hora de creación | Obligatorio; ISO 8601 |
| `GrpHdr/NbOfTxs` | Cantidad de transacciones | Obligatorio; entero positivo y coherente con el cuerpo |
| `GrpHdr/CtrlSum` | Suma de control | Solo `pain.001`; numérico no negativo |

## pain.001 — Customer Credit Transfer Initiation

**Uso:** orden de transferencia iniciada por el cliente (corporativo o persona) hacia NovaBank.

| Ruta | Uso | Regla |
|---|---|---|
| `PmtInf/PmtInfId` | Identificador del bloque de pago | Obligatorio; Max35Text |
| `PmtInf/PmtMtd` | Método de pago | `TRF` o `TRA` |
| `PmtInf/ReqdExctnDt/Dt` | Fecha de ejecución solicitada | ISO 8601 (`YYYY-MM-DD`) |
| `PmtInf/Dbtr/Nm` | Nombre del ordenante | Obligatorio; hasta 140 caracteres |
| `PmtInf/Dbtr/Acct/Id` | Cuenta del ordenante | `IBAN` u `Othr/Id` local |
| `CdtTrfTxInf/PmtId/EndToEndId` | Referencia extremo a extremo | Obligatoria; Max35Text |
| `CdtTrfTxInf/Amt/InstdAmt/@Ccy` | Importe instruido y moneda | ISO 4217; escala de la moneda |
| `CdtTrfTxInf/Cdtr/Nm` | Nombre del beneficiario | Obligatorio; hasta 140 caracteres |
| `CdtTrfTxInf/Cdtr/Acct/Id` | Cuenta del beneficiario | `IBAN` u `Othr/Id` |
| `CdtTrfTxInf/CdtrAgt/FinInstnId/BICFI` | BIC del banco del beneficiario | Opcional; ISO 9362 si se informa |
| `CdtTrfTxInf/RmtInf/Ustrd` | Remesa no estructurada | Hasta 140 caracteres |

Ejemplo: [`examples/iso20022/pain.001-customer-credit-transfer.xml`](../examples/iso20022/pain.001-customer-credit-transfer.xml).

## pacs.008 — FI to FI Customer Credit Transfer

**Uso:** transferencia interbancaria, tanto en el tramo local como en el internacional.

| Ruta | Uso | Regla |
|---|---|---|
| `SttlmInf/SttlmMtd` | Método de liquidación | El ejemplo usa `CLRG` |
| `PmtId/InstrId` | Identificador de la instrucción | Obligatorio; Max35Text |
| `PmtId/EndToEndId` | Referencia extremo a extremo | Obligatoria; Max35Text |
| `PmtId/UETR` | Identificador único de transacción | Opcional; UUID v4 canónico |
| `IntrBkSttlmAmt/@Ccy` | Importe interbancario y moneda | Obligatorio; ISO 4217 y escala |
| `IntrBkSttlmDt` | Fecha de liquidación | ISO 8601 si se informa |
| `ChrgBr` | Responsable de cargos | `DEBT`, `CRED`, `SHAR` o `SLEV` |
| `Dbtr/Nm`, `Dbtr/Acct` | Ordenante y cuenta | Obligatorios; cuenta local como `Othr/Id` |
| `Cdtr/Nm`, `Cdtr/Acct` | Beneficiario y cuenta | Obligatorios; internacional exige `IBAN` |
| `DbtrAgt/FinInstnId/BICFI` | Banco del ordenante | Obligatorio en el perfil internacional |
| `CdtrAgt/FinInstnId/BICFI` | Banco del beneficiario | Obligatorio en el perfil internacional |
| `RmtInf/Ustrd` | Remesa | Hasta 140 caracteres |

Ejemplo: [`examples/iso20022/pacs.008-customer-credit-transfer.xml`](../examples/iso20022/pacs.008-customer-credit-transfer.xml).

### Perfil local e internacional

| Regla | Local (SPI-like) | Internacional (SWIFT/ISO 20022) |
|---|---|---|
| Moneda | PYG | USD en liquidación del core; EUR solo validación/mapeo (S-061) |
| Cuenta del beneficiario | Alias, número local o cuenta interna | IBAN obligatorio |
| Agentes | No exigidos por el simulador local | `DbtrAgt` y `CdtrAgt` obligatorios |
| ChrgBr | `SLEV` | `DEBT`, `SHAR` o `CRED` |
| Tope | ₲10.000.000 por operación | Sin tope específico; valida saldo y comisión |

> Paraguay no figura en el registro IBAN consultado (F-14). Por eso el tramo local usa cuenta/alias y el internacional IBAN/BIC (S-058).

## pacs.002 — FI to FI Payment Status Report

**Uso:** informe de estado de un `pacs.008`. El simulador emite `ACSC` al liquidar, `PDNG` al retener por AML y `RJCT` ante rechazo o timeout.

| Ruta | Uso | Regla |
|---|---|---|
| `OrgnlGrpInfAndSts/OrgnlMsgId` | Mensaje original | Obligatorio |
| `OrgnlGrpInfAndSts/OrgnlMsgNmId` | Tipo del mensaje original | Debe comenzar con `pacs.008.` |
| `OrgnlInstrId` | Instrucción original | Informativo |
| `OrgnlEndToEndId` | Referencia extremo a extremo original | Obligatoria |
| `OrgnlUETR` | UETR original | Opcional; UUID v4 |
| `TxSts` | Estado | `ACSC`, `ACSP`, `ACCP`, `RJCT`, `PDNG` o `RCVD` |
| `StsRsnInf/Rsn/Cd` | Motivo ISO | Hasta 4 caracteres cuando se usa código |
| `StsRsnInf/Rsn/Prtry` | Motivo propietario | Se usa para `TIMEOUT`, `AMLHOLD` o `AMLREJECT` |

Ejemplos: [`ACSC`](../examples/iso20022/pacs.002-payment-status-report-acsc.xml) y [`RJCT`](../examples/iso20022/pacs.002-payment-status-report-rjct.xml).

### Estados y motivos usados

| Valor | Tipo | Significado en el caso |
|---|---|---|
| `ACSC` | ISO | Liquidación completada |
| `PDNG` | ISO | Pago retenido, pendiente de resolución |
| `RJCT` | ISO | Pago rechazado |
| `AM04` | ISO | Saldo insuficiente |
| `AC01` | ISO | Cuenta inexistente o no válida |
| `FF01` | ISO | Error de formato o rechazo funcional |
| `TIMEOUT` | Propietario | Sin respuesta dentro de los reintentos |
| `AMLHOLD` | Propietario | Retenido por screening AML simulado |
| `AMLREJECT` | Propietario | Rechazado por screening AML simulado |

Los códigos ISO se usan como referencia funcional; el caso no certifica su interpretación ante SWIFT ni ante el BCP (S-065).

## camt.053 — Bank to Customer Statement

**Uso:** extracto de cuenta para conciliación y reporting.

| Ruta | Uso | Regla |
|---|---|---|
| `Stmt/Id` | Identificador del extracto | Obligatorio |
| `Stmt/Acct/Id/IBAN` | Cuenta del extracto | IBAN u `Othr/Id` |
| `Stmt/Bal` | Saldo inicial o final | Al menos uno |
| `Bal/Tp/CdOrPrtry/Cd` | Tipo de saldo | El ejemplo usa `OPBD` |
| `Bal/Amt/@Ccy` | Importe y moneda del saldo | ISO 4217; numérico |
| `Bal/CdtDbtInd` | Naturaleza del saldo | `CRDT` o `DBIT` |
| `Ntry/Amt/@Ccy` | Importe del asiento | ISO 4217 y escala |
| `Ntry/CdtDbtInd` | Naturaleza del asiento | `CRDT` o `DBIT` |
| `Ntry/Sts` | Estado del asiento | `BOOK` o `PDNG` en el validador |
| `Ntry/BookgDt/Dt` | Fecha contable | ISO 8601 |
| `Ntry/NtryDtls/TxDtls` | Detalle y referencias | Opcional |

Ejemplo: [`examples/iso20022/camt.053-bank-to-customer-statement.xml`](../examples/iso20022/camt.053-bank-to-customer-statement.xml).

## Fuera de alcance

- Validación contra XSD oficiales y reglas de red SWIFT/BCP.
- Mensajes de investigación (`camt.056`, `camt.029`), cartas de crédito, cheques o pagos masivos.
- Firma, cifrado, non-repudiation y conectividad real.
- Conversión certificada MT103 ↔ ISO 20022.

**Fuentes:** F-12, F-13, F-14, F-15, F-16, F-17 y F-18 en [`docs/FUENTES.md`](../../docs/FUENTES.md).

# Ejemplos de mensajería

Todos los mensajes usan datos ficticios y versiones ISO 20022 de ejemplo. No son mensajes de producción ni una declaración de conformidad XSD.

## ISO 20022

| Archivo | Tipo | Escenario |
|---|---|---|
| `iso20022/pain.001-customer-credit-transfer.xml` | pain.001.001.09 | Orden de transferencia internacional iniciada por el cliente |
| `iso20022/pacs.008-customer-credit-transfer.xml` | pacs.008.001.08 | Transferencia interbancaria internacional USD |
| `iso20022/pacs.002-payment-status-report-acsc.xml` | pacs.002.001.10 | Estado de liquidación completada |
| `iso20022/pacs.002-payment-status-report-rjct.xml` | pacs.002.001.10 | Rechazo por saldo insuficiente (`AM04`) |
| `iso20022/camt.053-bank-to-customer-statement.xml` | camt.053.001.08 | Extracto con un asiento contable |

## MT103

| Archivo | Escenario |
|---|---|
| `mt/mt103-international-transfer.txt` | Transferencia internacional USD con cargos compartidos (`SHA`) |

## Verificación

```powershell
cd 06-mensajeria
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pacs.008-customer-credit-transfer.xml --international-pacs008
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\camt.053-bank-to-customer-statement.xml
..\.venv\Scripts\python.exe -m validator --mt103 examples\mt\mt103-international-transfer.txt --map
```

Los ejemplos también se validan automáticamente en `tests/test_examples.py`.

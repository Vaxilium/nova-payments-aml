# Screening de sanciones y PEP

## 1. Alcance

El screening de NovaBank es una demostración funcional con **listas ficticias**. No usa listas reales, no consulta directorios oficiales y no emite juicios sobre personas reales. Los nombres, alias, países y programas son inventados.

Archivos:

- `07-aml-compliance/data/lista_sanciones_pep.csv`: 20 registros ficticios (10 SANCTIONS, 8 PEP, 2 INTERNAL).
- `07-aml-compliance/data/high_risk_countries.csv`: 8 países de una lista interna ficticia.
- Tablas: `aml_watchlist` y `aml_high_risk_countries`.
- Implementación: `07-aml-compliance/aml/screening.py`.

## 2. Algoritmo

1. **Normalización:** mayúsculas, remoción de diacríticos, reemplazo de caracteres no alfanuméricos y eliminación de sufijos societarios (`S.A.`, `SRL`, `LTDA`, `SOCIEDAD`, `ANONIMA`).
2. **Comparación:** se calcula Jaro-Winkler y similitud de tokens ordenados (`difflib.SequenceMatcher`); se toma el mayor valor.
3. **Umbrales:**
   - `≥ 0,95`: `BLOCK` (coincidencia fuerte).
   - `≥ 0,88` y `< 0,95`: `REVIEW` (revisión manual).
   - `≥ 0,80` y `< 0,88`: candidato mínimo, se conserva para revisión.
   - `< 0,80`: `NO_MATCH`.
4. **Registro:** cada evaluación se guarda en `aml_screening_results` con nombre normalizado, lista, coincidencia, score, umbral, decisión y referencia de pago.

La comparación es explicable y reproducible, pero no sustituye un motor certificado de screening.

## 3. Decisiones operativas

| Resultado | Acción en el hook de pagos |
|---|---|
| `BLOCK` | Rechazo del pago (`REJECT`) antes de enviarlo al corredor. |
| `REVIEW` | Retención (`HOLD`) para revisión manual. |
| `NO_MATCH` | Continúa el flujo normal, sujeto a KYC, monto y país. |

El hook evalúa tanto al beneficiario como al ordenante. Si cualquiera coincide, se aplica la decisión más restrictiva.

## 4. Falsos positivos y calidad

- Los umbrales priorizan sensibilidad; un nombre similar puede generar `REVIEW`.
- La lista es pequeña y ficticia; no se reportan tasas de falsos positivos de producción.
- Todo match conserva el nombre que coincidió y el score para auditoría.
- Las listas deben actualizarse con un proceso formal, versionado y aprobado por Cumplimiento en un escenario real.

## 5. Pruebas

`07-aml-compliance/tests/test_screening.py` cubre:

- Normalización de tildes y sufijos.
- Coincidencia exacta que bloquea.
- Variante parcial que revisa o bloquea.
- Nombre normal sin coincidencia.
- Persistencia del resultado del screening.

## 6. Referencias

- SEPRELAD, Preguntas Frecuentes (F-03): PEP y debida diligencia.
- FATF, Recomendación 10 (CDD) y Recomendación 12 (PEP), según F-04 y fuentes oficiales registradas.
- Las listas utilizadas son ficticias (`S-018`, `SNV-03`).

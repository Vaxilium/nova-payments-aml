# Enfoque basado en riesgo (EBR) de NovaBank

**Fase:** 5 — AML/compliance  
**Naturaleza:** caso 100 % ficticio. Los umbrales, roles y listas son parámetros de diseño, no disposiciones legales.

## 1. Principio de diseño

NovaBank aplica un enfoque basado en riesgo: la intensidad del KYC, la debida diligencia ampliada (EDD) y el monitoreo dependen del riesgo del cliente, del producto, del canal y de la contraparte. El modelo no clasifica personas reales ni usa listas reales.

El diseño se apoya en tres capas:

1. **Onboarding y KYC:** identificación, beneficiario final, origen de fondos, PEP, noticias negativas y propósito de la relación.
2. **Monitoreo transaccional:** reglas SQL sobre el dataset del core, con parámetros versionados.
3. **Investigación y reporte:** alertas priorizadas, casos, SLA, ROS y trazabilidad de decisiones.

## 2. Factores y pesos del scoring

El score va de 0 a 100 y se calcula por suma de puntos. La clasificación es:

| Categoría | Rango | Consecuencia |
|---|---:|---|
| LOW | 0–39 | CDD estándar y monitoreo ordinario. |
| MEDIUM | 40–69 | Revisión periódica y controles adicionales. |
| HIGH | 70–100 | EDD obligatoria y revisión del oficial de cumplimiento. |

| Factor | Valores | Puntos |
|---|---|---:|
| Tipo de cliente | INDIVIDUAL / BUSINESS | 4 / 8 |
| Segmento | RETAIL / PREMIUM / SME / CORPORATE | 4 / 6 / 8 / 10 |
| País del cliente | LOW / MEDIUM / HIGH | 0 / 8 / 20 |
| Riesgo de actividad | LOW / MEDIUM / HIGH | 0 / 8 / 15 |
| Canal de alta | BRANCH / WEB / MOBILE / API | 0 / 2 / 4 / 6 |
| PEP | No / Sí | 0 / 35 |
| Beneficiario final | Identificado / No identificado | 0 / 10 |
| Origen de fondos | Verificado / No verificado | 0 / 8 |
| Noticias negativas | No / Sí | 0 / 10 |
| Complejidad del producto | BASIC / MEDIUM / COMPLEX | 0 / 4 / 8 |
| Volumen mensual esperado | LOW / MEDIUM / HIGH / VERY_HIGH | 0 / 3 / 6 / 8 |
| Antigüedad | >24 meses / 6–24 / <6 | 0 / 2 / 4 |

La suma se limita a 100. Los pesos son parámetros internos del caso y deben validarse con Cumplimiento antes de un uso real.

## 3. Disparadores de EDD

Se exige EDD cuando ocurre al menos uno de estos eventos:

- Clasificación HIGH.
- Cliente PEP.
- País de alto riesgo según la lista interna ficticia.
- Beneficiario final no identificado.
- Origen de fondos no verificado.
- Noticias negativas.
- Producto o canal de complejidad alta combinado con volumen relevante.

La EDD incluye revisión de fuente de fondos, fuente de patrimonio, propósito de la relación, aprobación de un nivel superior y monitoreo reforzado.

## 4. Perfiles sintéticos

Los perfiles se generan de forma determinística a partir de `SHA-256(customer_id)` para que el dataset sea reproducible:

- PEP si `digest % 37 == 0`.
- UBO faltante en clientes BUSINESS si `digest % 5 == 0`.
- Origen de fondos no verificado si `digest % 7 == 0`.
- Noticias negativas si `digest % 53 == 0`.
- Canal y complejidad según el digest y el segmento.

No se usan nombres, documentos, cuentas ni direcciones reales.

## 5. Monitoreo continuo

El motor evalúa 12 reglas SQL (ver `reglas-monitoreo.md`) y convierte las coincidencias en alertas deduplicadas por regla, cliente, cuenta y día. La prioridad se asigna por score:

| Score | Prioridad | SLA de asignación | SLA de cierre |
|---:|---|---:|---:|
| ≥ 80 | P1 | 15 minutos | 10 días hábiles |
| 50–79 | P2 | 240 minutos | 15 días hábiles |
| < 50 | P3 | 1.440 minutos | 20 días hábiles |

Los SLA son parámetros internos (`SUPUESTO NO VERIFICADO`, SNV-08) y no plazos regulatorios.

## 6. Gobierno y limitaciones

- Las listas de sanciones, PEP y países de alto riesgo son ficticias y están versionadas en `07-aml-compliance/data/`.
- La evaluación contra la verdad sintética se documenta en `evaluacion-verdad.md`; la muestra NORMAL de Fase 3 es una muestra, no el universo de operaciones normales.
- El indicador de dormancia no existe en el core; R06 usa un proxy (cuenta antigua, inactividad y depósito relevante) y se registra en P-015.
- El screening es difuso y explicable, pero no sustituye una herramienta certificada ni listas oficiales.
- Los textos normativos se citan en `docs/FUENTES.md`; lo no verificable se marca `SUPUESTO NO VERIFICADO`.

## 7. Referencias internas

- Esquema: `07-aml-compliance/aml/schema_aml.sql`.
- Configuración: `07-aml-compliance/aml/config.py`.
- Scoring: `07-aml-compliance/aml/kyc.py`.
- Screening: `07-aml-compliance/aml/screening.py`.
- Reglas: `07-aml-compliance/sql/rules/`.
- Evaluación: `07-aml-compliance/docs/evaluacion-verdad.md`.

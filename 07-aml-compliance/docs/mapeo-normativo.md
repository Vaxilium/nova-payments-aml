# Mapeo normativo AML

**Alcance:** matriz de correspondencia entre obligaciones y controles del caso NovaBank. No es una opinión legal. Las referencias se parafrasean y las fuentes se registran en `docs/FUENTES.md`.

## 1. Advertencia de aplicabilidad

NovaBank es un banco ficticio. La resolución de SEPRELAD aplicable específicamente a bancos supervisados por la SIB no fue verificada en texto completo (`SUPUESTO NO VERIFICADO`, SNV-02 / P-009). Por eso la matriz usa obligaciones generales de la Ley N° 1015/1997, la Resolución SEPRELAD N° 70/2019 y la Resolución N° 214/2019 como marco de referencia, sin afirmar que sean la norma exacta aplicable a la entidad.

## 2. Matriz de correspondencia

| Obligación / expectativa | Referencia | Control en NovaBank | Evidencia |
|---|---|---|---|
| Enfoque basado en riesgo | GAFI R.1; guía de RBA para banca (F-21) | Scoring KYC 0–100; EDD por riesgo alto; monitoreo proporcional. | `aml/kyc.py`, `docs/enfoque-riesgo.md` |
| Debida diligencia del cliente | GAFI R.10; SEPRELAD Res. 70/2019 (F-19) | Identificación, perfil, propósito, UBO, PEP, SOF y noticias negativas. | `aml/kyc.py`, `aml/schema_aml.sql` |
| Identificación del beneficiario final | SEPRELAD Res. 70/2019, Anexo A4 (F-19) | Campo `ubo_identified`; penalización si falta y EDD. | `aml/kyc.py` |
| Personas expuestas políticamente | GAFI R.12; SEPRELAD Res. 50/2019, referenciada en F-03 | Factor PEP con 35 puntos y EDD. | `aml/kyc.py` |
| Screening de sanciones | GAFI R.10/R.12; listas ficticias (S-018) | Screening difuso de ordenante y beneficiario; decisión BLOCK/REVIEW. | `aml/screening.py`, `docs/screening.md` |
| Monitoreo continuo | SEPRELAD Res. 214/2019 (F-20); GAFI R.10 | 12 reglas SQL, parámetros versionados y ejecución periódica. | `sql/rules/`, `docs/reglas-monitoreo.md` |
| Alertas y priorización | SEPRELAD Res. 214/2019 (F-20) | Alertas deduplicadas, score, prioridad P1/P2/P3 y SLA interno. | `aml/alerts.py`, `docs/alertas-casos-sla.md` |
| Investigación y escalamiento | GAFI R.20; SEPRELAD Res. 70/2019 | Casos, transiciones auditables y asignación de analista. | `aml/workflow.py` |
| Reporte de operación sospechosa | GAFI R.20; Ley N° 1015/1997 (F-03) | ROS con narrativa, operaciones y estado; dos casos ficticios. | `aml/schema_aml.sql`, `docs/ros.md` |
| Reserva y no divulgación | Ley N° 1015/1997; SEPRELAD F-03 | El caso no publica ROS reales ni datos de personas; todo es sintético. | `docs/ros.md` |
| Transparencia de transferencias | GAFI R.16 | Campos de ordenante/beneficiario en mensajes ISO 20022 y hook AML. | `06-mensajeria/`, `aml/hook.py` |
| Conservación de registros | GAFI R.11; política interna `SUPUESTO NO VERIFICADO` | Auditoría y transiciones con fecha; retención de 5 años como parámetro (P-012). | `aml/schema_aml.sql`, `aml/workflow.py` |
| Actualización de la norma | Res. SEPRELAD N° 254/2020, que modifica arts. 26–28 de la Res. 70/2019 (F-19) | Los parámetros y textos se versionan; se registra la necesidad de revisión legal. | `docs/FUENTES.md`, `docs/PENDIENTES.md` |

## 3. Controles del caso y límites

- **KYC:** el score es determinístico y explicable; no reemplaza un modelo validado por Cumplimiento.
- **Screening:** listas ficticias y comparación difusa; no sustituye listas oficiales ni un motor certificado.
- **Monitoreo:** 12 reglas SQL; los umbrales son parámetros de diseño (`SNV-04`, `SNV-08`).
- **Alertas:** la deduplicación es diaria por regla, cliente y cuenta; un caso real puede requerir otra ventana.
- **ROS:** los dos documentos son borradores ficticios; no se presentó ningún reporte ante una autoridad.
- **Datos:** no se usan nombres, documentos, cuentas ni operaciones reales.

## 4. Fuentes

| ID | Fuente | Uso |
|---|---|---|
| F-03 | SEPRELAD, Preguntas Frecuentes | Rol de la UIF, Ley 1015/1997, ROS, PEP y beneficiario final. |
| F-04 | GAFI/FATF, The FATF Recommendations | R.1, R.10, R.12, R.16, R.20 y R.21. |
| F-19 | SEPRELAD, Resolución N° 70/2019 | Debida diligencia, UBO, conservación y ROS. |
| F-20 | SEPRELAD, Resolución N° 214/2019 | Monitoreo, alertas y metodología. |
| F-21 | GAFI/FATF, Risk-based approach — banking sector | Enfoque basado en riesgo para banca. |

Las notas de acceso, bloqueos y verificaciones pendientes están en `docs/FUENTES.md` y `docs/PENDIENTES.md`.

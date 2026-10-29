# BRD resumido — NovaPay

**Página:** BRD resumido  
**Documento fuente:** `01-negocio/BRD.md` (BRD-NB-001)  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Dueño:** Producto — Pagos  
**Estado:** Aprobado para Fase 2 (validación funcional ficticia pendiente)

> Resumen listo para Confluence. El BRD completo, con anexos y referencias, está en el repositorio. Todo el caso es ficticio.

---

## 1. Problema

NovaBank no puede competir en pagos instantáneos ni cross-border con la velocidad, disponibilidad y trazabilidad que el mercado exige. La operación está fragmentada entre canales, core, mensajería y cumplimiento; esto impide confirmar en segundos, operar 24/7, detectar riesgo en tiempo real y demostrar control ante el regulador.

---

## 2. Objetivos medibles

| ID | Objetivo | Métrica | Meta | Fecha |
|---|---|---|---|---|
| O-01 | Lanzar transferencias instantáneas locales. | p95 acreditación; disponibilidad | ≤ 5 s; ≥ 99,9 % | 2027-06-30 |
| O-02 | Habilitar cross-border saliente ISO 20022. | % validados; STP | 100 %; ≥ 90 % | 2027-09-30 |
| O-03 | Integrar screening y scoring en el pago. | % evaluados; p95 scoring | 100 %; ≤ 2 s | 2027-06-30 |
| O-04 | Reducir gestión manual. | Reducción de intervención; P1 a tiempo | −40 %; ≥ 95 % | 2027-12-31 |
| O-05 | Mejorar experiencia y transparencia. | CSAT; reclamos | ≥ 4,3/5; < 0,5 % | 2027-12-31 |
| O-06 | Asegurar trazabilidad y evidencia. | Traza completa | ≥ 99,5 % | 2027-12-31 |

> Metas de planificación del caso; no son resultados medidos.

---

## 3. Alcance

### 3.1 Incluido

- Transferencia instantánea local P2P/P2B en PYG, 24/7, hasta ₲10.000.000.
- Alias/cuenta, confirmación, estado y devoluciones.
- Transferencia internacional saliente USD/EUR con ISO 20022.
- Onboarding y KYC, screening, monitoreo transaccional, alertas y ROS ficticio.
- Partida doble, conciliación, auditoría y reporting operativo.

### 3.2 Excluido

- Cross-border entrante, FX, QR, tarjetas y adquirencia.
- Desarrollo de app móvil/home banking.
- Conectividad SWIFT real y certificación CBPR+.
- Envío real de ROS a SEPRELAD.
- Listas reales de sanciones/PEP.
- Sustitución del core bancario.

---

## 4. Requerimientos de negocio

| ID | Requerimiento | Prioridad |
|---|---|---|
| BR-01 | Transferencias locales PYG 24/7 hasta ₲10.000.000. | Must |
| BR-02 | Identificación del beneficiario por alias o cuenta. | Must |
| BR-03 | Estado del pago en tiempo real. | Must |
| BR-04 | Devoluciones y reclamos. | Should |
| BR-05 | Cross-border saliente USD/EUR con ISO 20022. | Must |
| BR-06 | Validación de IBAN, BIC, moneda, importe y campos. | Must |
| BR-07 | Screening y riesgo antes de liberar fondos. | Must |
| BR-08 | Monitoreo transaccional por reglas. | Must |
| BR-09 | Gestión de alertas con prioridad, SLA y evidencia. | Must |
| BR-10 | KYC/CDD, beneficiario final y PEP. | Must |
| BR-11 | Partida doble y conciliación. | Must |
| BR-12 | Trazabilidad de auditoría. | Must |
| BR-13 | KPIs operativos y de cumplimiento. | Should |
| BR-14 | Configuración de límites y reglas. | Should |
| BR-15 | Idempotencia y reintentos sin duplicar. | Must |
| BR-16 | Consultas y reclamos con estado del pago. | Should |

---

## 5. KPIs principales

| KPI | Meta | Dueño |
|---|---|---|
| K-01 p95 acreditación local | ≤ 5 s | Operaciones |
| K-02 Disponibilidad | ≥ 99,9 % | TI |
| K-03 STP local | ≥ 95 % | Operaciones |
| K-05 STP internacional | ≥ 90 % | Operaciones Intl. |
| K-07 Cobertura de screening | 100 % | Cumplimiento |
| K-09 Alertas P1 a tiempo | ≥ 95 % | Monitoreo AML |
| K-12 ROS en plazo | 100 % | Cumplimiento |
| K-16 Traza completa | ≥ 99,5 % | Auditoría/TI |
| K-17 Conciliación | ≥ 99,5 % | Contraloría |

La ficha completa está en `01-negocio/kpis.md`.

---

## 6. Supuestos y restricciones clave

- El SPI opera 24/7, en PYG, con tope de ₲10.000.000 y acreditación ≤ 5 s (verificado con F-01 el 2026-10-29; SNV-01 cerrado).
- NovaBank ya tiene core, libro mayor y canal digital; el programa integra, no reemplaza.
- La conexión SWIFT se simula; no hay certificación real.
- Las listas de sanciones/PEP y países de alto riesgo son ficticias.
- Los umbrales de los DMN son parámetros de diseño (`SUPUESTO NO VERIFICADO`, SNV-04).
- El caso es ficticio y no usa datos reales.
- La validación legal es responsabilidad de Cumplimiento y Legal.

---

## 7. Riesgos prioritarios

| ID | Riesgo | Nivel |
|---|---|---|
| R-01 | Interpretación errónea de SPI/SEPRELAD. | Crítico |
| R-02 | Fraude o suplantación en pagos instantáneos. | Crítico |
| R-04 | Indisponibilidad de SPI/SWIFT/core. | Alto |
| R-05 | Duplicidad por reintentos sin idempotencia. | Alto |
| R-12 | Backlog de alertas AML. | Alto |
| R-17 | Evidencia incompleta. | Alto |

El registro completo está en `01-negocio/riesgos.md` y el RAID log en `05-raid-log.md`.

---

## 8. Trazabilidad hacia el backlog

| Requerimiento | Épica | Historias |
|---|---|---|
| BR-01, BR-02, BR-03, BR-04 | EP-01 Pagos locales | US-001 a US-005 |
| BR-03, BR-05, BR-06, BR-15 | EP-02 Cross-border | US-006 a US-010 |
| BR-07, BR-10 | EP-03 Onboarding/KYC | US-011 a US-015 |
| BR-07, BR-08, BR-09 | EP-04 Monitoreo/alertas | US-016 a US-020 |
| BR-09, BR-12 | EP-05 Investigación/ROS | US-021 a US-023 |
| BR-11, BR-12 | EP-06 Contabilidad/auditoría | US-024 a US-027 |
| BR-13 | EP-07 Reporting | US-028 a US-030 |
| BR-03, BR-04, BR-16 | EP-08 Experiencia | US-031 a US-033 |
| BR-14 | EP-09 Parametrización | US-034 a US-036 |
| BR-12, BR-15 | EP-10 Plataforma | US-037 a US-040 |

La matriz completa está en `matriz-trazabilidad.csv`.

---

## 9. Referencias

- `01-negocio/BRD.md` — documento completo.
- `01-negocio/kpis.md` — fichas de KPIs.
- `01-negocio/riesgos.md` — registro de riesgos.
- `02-procesos/mapa-procesos.md` — procesos.
- `docs/FUENTES.md` — fuentes normativas y técnicas.
- `docs/SUPUESTOS.md` — supuestos.
- `docs/PENDIENTES.md` — brechas.

**Fin de la página.**

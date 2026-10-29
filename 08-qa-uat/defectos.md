# Registro de defectos — UAT NovaBank

**Fecha de registro:** 2026-10-29
**Ambiente:** Prototipo local (Windows, Python 3.15, SQLite, pytest 9.2.0)
**Alcance:** Defectos de ejemplo observados al preparar y ejecutar la UAT. No son
incidentes de producción y no se declaran corregidos.

| ID | Título | Severidad | Prioridad | Estado | Caso |
|---|---|---|---|---|---|
| DEF-001 | El canal no resuelve alias de beneficiario ni devuelve titular enmascarado | Alta | P1 | Abierto | TC-002 |
| DEF-002 | No existe flujo de devolución de pagos locales ni devolución internacional | Alta | P1 | Abierto | TC-004; TC-010 |
| DEF-003 | La API no implementa autenticación ni autorización por rol | Crítica | P1 | Abierto - brecha de alcance conocida | TC-037 |
| DEF-004 | Discrepancia entre el corte de alertas de Fase 5 y el dataset analítico | Media | P2 | Abierto | TC-029 |
| DEF-005 | El límite diario agregado de pagos locales no se valida | Media | P2 | Abierto - aceptado como alcance del prototipo | TC-005; TC-034 |

---

## DEF-001 — Alias de beneficiario no resuelto

- **Severidad:** Alta
- **Prioridad:** P1
- **Estado:** Abierto
- **Historia:** US-002
- **Caso:** TC-002
- **Ambiente:** Prototipo local — API `/v1` y simulador instantáneo
- **Componente:** `06-mensajeria/simulator/instant.py`, canal de transferencias

**Descripción:** El simulador acepta un alias como referencia del acreedor, pero
no existe un directorio de alias ni una operación que devuelva el titular y la
cuenta enmascarados. Tampoco se rechaza un alias inexistente con
`ALIAS_NO_ENCONTRADO`.

**Pasos para reproducir:**

1. Abrir el flujo de transferencia local.
2. Ingresar el alias `BENEFICIARIO-INEXISTENTE`.
3. Confirmar la búsqueda.

**Resultado esperado:** el sistema devuelve `ALIAS_NO_ENCONTRADO` y no crea el pago.

**Resultado obtenido:** no hay endpoint de resolución; el alias solo se
transporta como texto y el pago puede continuar con datos no verificados.

**Evidencia:** `08-qa-uat/casos-prueba.csv` (TC-002);
`06-mensajeria/simulator/instant.py`; `04-diseno-ux/especificacion-pantallas.md`.

**Impacto:** el cliente no puede verificar al beneficiario antes de confirmar.

**Responsable sugerido:** Product Owner / Desarrollo de canales.

---

## DEF-002 — Sin flujo de devolución local ni internacional

- **Severidad:** Alta
- **Prioridad:** P1
- **Estado:** Abierto
- **Historia:** US-004; US-010
- **Caso:** TC-004; TC-010
- **Ambiente:** Prototipo local — procesos BPMN y simuladores
- **Componente:** `02-procesos/bpmn/transferencia-instantanea-to-be.bpmn`,
  `06-mensajeria/simulator/`

**Descripción:** Los procesos de devolución están modelados en BPMN, pero no hay
endpoint, máquina de estados ni asiento de reverso para devolver un pago local
o internacional. El simulador solo cubre rechazo y timeout.

**Pasos para reproducir:**

1. Tomar un pago en estado `ACREDITADO`.
2. Solicitar la devolución dentro del plazo configurado.
3. Confirmar la solicitud.

**Resultado esperado:** se crea un caso de devolución con número, dueño y SLA, y
se registra el asiento de reverso.

**Resultado obtenido:** no existe operación de devolución; el flujo queda en el
modelo de procesos y no en el código.

**Evidencia:** `08-qa-uat/casos-prueba.csv` (TC-004, TC-010);
`02-procesos/bpmn/transferencia-instantanea-to-be.bpmn`;
`06-mensajeria/docs/simuladores.md`.

**Impacto:** un cliente no puede recuperar fondos por el canal digital.

**Responsable sugerido:** Desarrollo Core / Operaciones.

---

## DEF-003 — API sin autenticación ni autorización por rol

- **Severidad:** Crítica
- **Prioridad:** P1
- **Estado:** Abierto - brecha de alcance conocida
- **Historia:** US-037
- **Caso:** TC-037
- **Ambiente:** Prototipo local — FastAPI `/v1`
- **Componente:** `05-core-middleware/app/api.py`, `docs/SUPUESTOS.md` (S-055)

**Descripción:** Cualquier cliente puede invocar los endpoints de crédito, débito
y transferencia sin autenticarse. No hay validación de rol ni segregación de
funciones. La limitación está registrada como supuesto de alcance, pero sigue
siendo un defecto para cualquier uso fuera del entorno controlado.

**Pasos para reproducir:**

1. Invocar `POST /v1/transfers` sin credenciales.
2. Repetir la operación con un usuario de solo lectura.

**Resultado esperado:** sin credenciales se responde `401`; con rol `LECTURA` se
responde `403`.

**Resultado obtenido:** la operación se ejecuta porque el prototipo no tiene capa
de identidad ni autorización.

**Evidencia:** `08-qa-uat/casos-prueba.csv` (TC-037);
`05-core-middleware/app/api.py`; `docs/SUPUESTOS.md` (S-055).

**Impacto:** el prototipo no es apto para exposición fuera de un entorno
controlado. Es la brecha más importante para un piloto productivo.

**Responsable sugerido:** Arquitectura / Seguridad.

---

## DEF-004 — Discrepancia de cortes de alertas

- **Severidad:** Media
- **Prioridad:** P2
- **Estado:** Abierto
- **Historia:** US-029
- **Caso:** TC-029
- **Ambiente:** Dataset analítico y documentación de evidencias
- **Componente:** `07-aml-compliance/scripts/evaluate_rules.py`,
  `09-analitica/scripts/export_analytics.py`

**Descripción:** La evidencia de Fase 5 documenta 775 alertas deduplicadas
(1.326 coincidencias), mientras que el corte reproducible de Fase 6 genera 377
alertas (786 coincidencias). La diferencia proviene de ejecutar las reglas sobre
la base actual y no sobre el snapshot original. Está registrada como P-018.

**Pasos para reproducir:**

1. Ejecutar `07-aml-compliance/scripts/evaluate_rules.py` sobre la base actual.
2. Ejecutar `09-analitica/scripts/export_analytics.py`.
3. Comparar el conteo de alertas con `docs/EVIDENCIAS.md` de Fase 5.

**Resultado esperado:** un único corte documentado y trazable para todas las fases.

**Resultado obtenido:** dos cortes con conteos distintos y sin reconciliación
automática.

**Evidencia:** `docs/PENDIENTES.md` (P-018);
`09-analitica/data/export_report.json`; `docs/EVIDENCIAS.md` (Fase 5).

**Impacto:** riesgo de inconsistencia en tableros y en la narrativa del portafolio.

**Responsable sugerido:** BA / Analítica.

---

## DEF-005 — Límite diario agregado no validado

- **Severidad:** Media
- **Prioridad:** P2
- **Estado:** Abierto - aceptado como alcance del prototipo
- **Historia:** US-005; US-034
- **Caso:** TC-005; TC-034
- **Ambiente:** Prototipo local — simulador instantáneo
- **Componente:** `06-mensajeria/simulator/instant.py`

**Descripción:** El simulador aplica el tope por operación de 10.000.000 PYG,
pero no acumula el importe diario por cliente. Un cliente podría realizar varias
operaciones por debajo del tope y superar el límite diario definido en el BRD.

**Pasos para reproducir:**

1. Enviar dos pagos de 9.000.000 PYG el mismo día.
2. Revisar el total acumulado del cliente.

**Resultado esperado:** el segundo pago se rechaza por límite diario.

**Resultado obtenido:** ambos pagos se aceptan porque solo se evalúa el tope por
operación.

**Evidencia:** `08-qa-uat/casos-prueba.csv` (TC-005, TC-034);
`06-mensajeria/simulator/instant.py`; `01-negocio/BRD.md`.

**Impacto:** el control de límites no cubre el riesgo de fragmentación diaria.

**Responsable sugerido:** Desarrollo Core / Riesgos.

---

## Convenciones de cierre

- Un defecto pasa a **Resuelto** solo con una corrección y una prueba que lo
  demuestre.
- Un defecto pasa a **Cerrado** cuando la corrección se verificó en la suite y
  en el caso UAT asociado.
- Un defecto puede quedar **Aceptado como limitación** solo con aprobación
  explícita del Product Owner y registro en `docs/PENDIENTES.md`.
- Ningún defecto de este registro se declara corregido en la fecha de cierre.

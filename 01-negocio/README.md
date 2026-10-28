# 01 — Negocio

Propósito: capturar el problema, el contexto, las reglas de negocio y los criterios de éxito de NovaBank antes de especificar soluciones.

## Contenidos

| Documento | Descripción | Estado |
|---|---|---|
| `BRD.md` | Contexto, objetivos, alcance, requerimientos, beneficios y restricciones. | Completado |
| `stakeholders.md` | Mapa de actores, poder/interés, RACI, comunicación y escalamiento. | Completado |
| `riesgos.md` | Registro de riesgos con probabilidad, impacto, respuesta y riesgo residual. | Completado |
| `glosario.md` | Glosario bilingüe de pagos, mensajería, AML y gobernanza. | Completado |
| `kpis.md` | Fichas de indicadores, metas, fuentes y gobierno del dato. | Completado |
| `contexto-regulatorio.md` | Marco público citado, controles derivados y supuestos no verificados. | Completado |

## Decisiones clave

- El alcance internacional es **saliente** (outbound), en USD y EUR.
- El canal local opera 24/7, en PYG, con tope de ₲10.000.000 y acreditación objetivo ≤ 5 s, con base en la información pública del BCP.
- Las listas de sanciones, PEP y países de alto riesgo son **ficticias**.
- Las metas y umbrales son **parámetros de diseño**, no resultados ni límites regulatorios.
- Las referencias normativas se citan desde `docs/FUENTES.md`; las brechas se marcan como `SUPUESTO NO VERIFICADO` y se registran en `docs/PENDIENTES.md`.

## Verificación

- Contenido revisado para coherencia con el BRD, los procesos, los riesgos y los KPIs.
- Sin secretos, credenciales ni datos personales reales.
- Fechas en formato `YYYY-MM-DD`.

## Pendientes

- Validación legal de normativa y umbrales (P-006, P-009, P-011).
- Evidencias visuales de herramientas externas (`docs/EVIDENCIAS.md`).

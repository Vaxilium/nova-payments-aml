# SUPUESTOS Y DECISIONES

Registro de toda decisión o supuesto tomado sin consulta al autor, según las reglas de autonomía de `AGENTS.md`.

**Convenciones**
- **Decisión:** elección operativa tomada por el agente.
- **Supuesto:** condición asumida como verdadera a falta de información.
- **`SUPUESTO NO VERIFICADO`:** afirmación que depende de normativa o estándar real y aún no fue contrastada con fuente oficial. Debe aparecer marcada también en el documento donde se use.
- Fechas en formato `YYYY-MM-DD`. Estado: `activo`, `reemplazado`, `cerrado`.

| ID | Fecha | Tipo | Decisión / supuesto | Motivo | Impacto | Estado |
|---|---|---|---|---|---|---|
| S-001 | 2026-10-27 | Decisión | El repositorio de trabajo es `C:\Users\User\Documents\nova-payments-aml`, no el cwd por defecto `C:\Users\User`. | Es el clon con el remoto `origin` correcto. | Bajo | Activo |
| S-002 | 2026-10-27 | Supuesto | Todo nombre, cuenta, BIC, IBAN, cliente y transacción es ficticio, aunque con formato válido. | Regla de honestidad y privacidad del portafolio. | Alto | Activo |
| S-003 | 2026-10-27 | Decisión | El stack objetivo es Python 3.12, pero el equipo solo tiene Python 3.15. Se crea `.venv` con 3.15 y el código se mantiene compatible con 3.12+. | Único intérprete disponible. | Medio | Activo |
| S-004 | 2026-10-27 | Decisión | Se ignoran `*.db`, `*.sqlite` y `*.sqlite3`; la base se regenera con el script de seed (semilla fija). | Evitar binarios y datos volátiles en git; garantizar reproducibilidad. | Bajo | Activo |
| S-005 | 2026-10-27 | Decisión | Carpetas en español con prefijo numérico; código e identificadores en inglés. | Orden narrativo del portafolio y convención de código. | Bajo | Activo |
| S-006 | 2026-10-27 | Decisión | Documentación en español; `README.md` con resumen ejecutivo en inglés al inicio. | Requisito del autor y alcance internacional del portafolio. | Bajo | Activo |
| S-007 | 2026-10-27 | Decisión | En Fase 0 no se escribe contenido normativo; las fuentes oficiales se verificarán al inicio de las fases 1, 4 y 5. | Evitar citas inventadas. | Medio | Activo |
| S-008 | 2026-10-27 | Decisión | No se publican enlaces a Jira, Confluence, Azure DevOps, Figma, Power BI ni similares hasta que existan y el autor los cree. `EVIDENCIAS.md` solo contiene placeholders. | No inventar enlaces ni afirmar uso de herramientas. | Alto | Activo |
| S-009 | 2026-10-27 | Decisión | Una sola rama `main`; commits convencionales; push al cierre de cada fase; prohibido `--force`. | Simplicidad y trazabilidad del portafolio. | Bajo | Activo |
| S-010 | 2026-10-27 | Decisión | Los datos sintéticos se generan con semilla fija (`NOVABANK_SEED=20261027`) y se documentan en el diccionario de datos. | Reproducibilidad y pruebas deterministas. | Medio | Activo |
| S-011 | 2026-10-27 | Decisión | Lo no verificable se marca `SUPUESTO NO VERIFICADO` inline y se lista en `PENDIENTES.md`. | Transparencia. | Alto | Activo |
| S-012 | 2026-10-27 | Decisión | Se incluye `opencode.json` en el repositorio como configuración de la sesión de trabajo. | Facilitar futuras sesiones del agente. | Bajo | Activo |
| S-013 | 2026-10-27 | Decisión | No se crea `LICENSE` en Fase 0; la licencia se decide antes de difundir el repositorio (Fase 7). | Evitar otorgar licencia sin decisión explícita del autor. | Medio | Activo |

## Supuestos no verificados vigentes

Ninguno. No se ha incorporado contenido normativo en esta fase.

## Historial de cambios

| Fecha | Cambio |
|---|---|
| 2026-10-27 | Creación del registro con S-001 a S-013. |

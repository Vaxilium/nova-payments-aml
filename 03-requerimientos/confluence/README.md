# Kit Confluence — estructura del espacio NovaBank

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** CON-NB-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Artefacto:** páginas Markdown listas para copiar a Confluence

> El agente no opera Confluence. Estas páginas son artefactos de diseño para que el autor cree el espacio, pegue el contenido y registre la evidencia en `docs/EVIDENCIAS.md` (EV-002). No se declara que el espacio exista.

---

## 1. Estructura propuesta del espacio

```text
NovaBank — Payments & AML
├─ Inicio
├─ 01 Negocio
│  ├─ BRD resumido
│  ├─ Objetivos y KPIs
│  ├─ Alcance y exclusiones
│  └─ Glosario
├─ 02 Requerimientos
│  ├─ Épicas
│  ├─ Historias y criterios de aceptación
│  ├─ Requerimientos no funcionales
│  └─ Planificación de sprints
├─ 03 Decisiones
│  ├─ Índice de ADR
│  ├─ ADR-001 Orquestación de pagos
│  ├─ ADR-002 Idempotencia y estados
│  ├─ ADR-003 Modelo ISO 20022
│  ├─ ADR-004 Motor de decisiones de riesgo
│  ├─ ADR-005 Auditoría y correlación
│  └─ ADR-006 Datos sintéticos y simulación
├─ 04 Operación y control
│  ├─ RAID log
│  ├─ Runbook operativo (Fase 7)
│  └─ Evidencias y enlaces
└─ 05 Actas
   ├─ Acta 2026-10-20 — Kickoff
   ├─ Acta 2026-10-22 — Taller de requerimientos
   └─ Acta 2026-10-27 — Refinamiento y cierre de Fase 2
```

---

## 2. Orden de creación recomendado

1. Crear el espacio `NovaBank` (clave sugerida: `NOVA`).
2. Crear la página **Inicio** y pegar `00-inicio.md`.
3. Crear la sección **01 Negocio** y pegar `01-brd-resumido.md` y `03-glosario.md`.
4. Crear la sección **03 Decisiones** y pegar cada ADR de `02-decisiones/`.
5. Crear la sección **05 Actas** y pegar las actas de `04-actas/`.
6. Crear la página **RAID log** y pegar `05-raid-log.md`.
7. Crear las páginas de requerimientos enlazando o pegando los documentos del repositorio (`epicas.md`, `historias-usuario.md`, `requerimientos-no-funcionales.md`, `planificacion-sprints.md`).
8. Verificar la jerarquía, los enlaces internos y los permisos de lectura.
9. Registrar el enlace del espacio y una captura en `docs/EVIDENCIAS.md` (EV-002).

---

## 3. Convenciones de contenido

- **Idioma:** español; términos técnicos en inglés cuando el estándar lo exige.
- **Fechas:** `YYYY-MM-DD`.
- **Estados:** `Borrador`, `En revisión`, `Aprobado`, `Reemplazado`.
- **Decisiones:** toda decisión relevante se registra como ADR con contexto, decisión, consecuencias y alternativas.
- **Actas:** solo roles, no nombres de personas reales; el caso es ficticio.
- **Datos:** sin PII real, sin secretos, sin enlaces inventados.
- **Macros:** evitar macros que requieran apps de pago. Las páginas usan Markdown compatible con el editor de Confluence; si una tabla o bloque no se pega bien, recrearlo con el editor.
- **Enlaces:** no publicar enlaces a Jira, Azure DevOps, Figma, Power BI o similares hasta que existan y el autor los cree.

---

## 4. Etiquetas sugeridas

| Página | Labels |
|---|---|
| Inicio | `novabank`, `pagos`, `aml`, `indice` |
| BRD resumido | `brd`, `negocio`, `alcance` |
| Glosario | `glosario`, `pagos`, `aml` |
| ADR | `adr`, `arquitectura`, `decision` |
| Actas | `acta`, `gobernanza` |
| RAID log | `raid`, `riesgos`, `supuestos`, `dependencias` |
| Requerimientos | `backlog`, `historias`, `gherkin` |

---

## 5. Verificación de la importación manual

- [ ] Espacio creado con la jerarquía propuesta.
- [ ] Página de inicio con navegación y estado.
- [ ] BRD resumido y glosario visibles.
- [ ] Seis ADR creados y enlazados desde el índice.
- [ ] Tres actas creadas y etiquetadas como simuladas.
- [ ] RAID log con riesgos, supuestos, issues y dependencias.
- [ ] Permisos de lectura para la audiencia prevista.
- [ ] Enlace y captura registrados en `docs/EVIDENCIAS.md` (EV-002).

---

## 6. Referencias

- `00-inicio.md` — página de inicio.
- `01-brd-resumido.md` — BRD para Confluence.
- `02-decisiones/` — ADR.
- `03-glosario.md` — glosario.
- `04-actas/` — actas simuladas.
- `05-raid-log.md` — RAID log.
- `../epicas.md`, `../historias-usuario.md`, `../requerimientos-no-funcionales.md`, `../planificacion-sprints.md` — documentos fuente.
- `../../docs/EVIDENCIAS.md` — EV-002.

**Fin del documento.**

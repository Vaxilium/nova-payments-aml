# PENDIENTES

Bloqueos, deuda técnica y acciones que requieren intervención del autor (herramientas externas, credenciales, decisiones de negocio).

**Regla:** un problema se registra aquí después de **3 intentos fallidos** de resolución autónoma, o cuando depende de una acción que el agente no puede ejecutar.

| ID | Fase | Descripción | Impacto | Intentos | Próximo paso | Estado |
|---|---|---|---|---|---|---|
| P-001 | 3 | Python 3.12 no está instalado (solo 3.15). El código se mantiene compatible con 3.12+, pero el entorno no reproduce exactamente la versión objetivo. | Bajo | 1 | Instalar Python 3.12 y recrear `.venv` si se requiere reproducibilidad exacta. | Abierto |
| P-002 | 1–7 | Evidencias de herramientas no operables (Jira, Confluence, Azure DevOps, Bizagi/Camunda, Figma/Balsamiq, Power BI/Tableau, Lucidchart/Visio/Miro): requieren que el autor importe los artefactos y capture pantallas. | Medio | 0 | Seguir los pasos de `docs/EVIDENCIAS.md` al cerrar cada fase. Para Fase 1: EV-004 y EV-005. | Abierto |
| P-003 | 1 | Registro de fuentes oficiales iniciado y con 11 fuentes (F-01 a F-11), pero faltan textos normativos primarios del SIPAP y de SEPRELAD aplicables a bancos. | Medio | 1 | Completar en Fase 4/5 con el Reglamento del SIPAP y la resolución SEPRELAD aplicable a bancos. | Parcial |
| P-004 | 7 | Enlace público de LinkedIn no disponible; el README usa un placeholder. | Bajo | 0 | Agregar la URL real antes de difundir el repositorio. | Abierto |
| P-005 | 7 | Licencia del repositorio sin definir. | Medio | 0 | Decidir licencia (por ejemplo, MIT) y agregar `LICENSE` antes de publicar. | Abierto |
| P-006 | 1 | El BCP presenta dos descripciones distintas del SPI: F-01 (consultas frecuentes) indica operación 24/7, mientras que la tabla resumen de F-02 indica “días hábiles”. El caso adopta F-01 y lo marca `SUPUESTO NO VERIFICADO` (SNV-01). | Alto | 1 | Contrastar con el Reglamento General del SIPAP vigente antes de Fase 4. | Abierto |
| P-007 | 1 | El sitio oficial de FATF devolvió HTTP 403 a la descarga automatizada. Las Recomendaciones 10, 16 y 20 se corroboraron por fragmentos indexados y copias espejo, pero no se descargó el PDF oficial completo. | Medio | 1 | Descargar el PDF oficial desde una sesión con acceso y archivar la fecha/versión. | Abierto |
| P-008 | 1, 4 | Los sitios de ISO 20022 y SWIFT bloquearon parte de las consultas automatizadas (HTTP 403). Las definiciones de pacs.008/pacs.002 y el fin de coexistencia CBPR+ se corroboraron por resultados indexados y documentos públicos de SWIFT. | Medio | 2 | Verificar en el portal de ISO 20022/SWIFT con acceso manual y registrar captura en Fase 4. | Abierto |
| P-009 | 1, 5 | No se verificó el número y texto de la resolución SEPRELAD aplicable específicamente a bancos supervisados por la SIB. El caso usa obligaciones generales de la Ley 1015/97 según F-03 y lo marca `SUPUESTO NO VERIFICADO` (SNV-02, SNV-05). | Alto | 1 | Validar con Cumplimiento y citar la norma exacta en Fase 5. | Abierto |
| P-010 | 1 | La lista de países de alto riesgo del DMN es ficticia y no reproduce una lista oficial del GAFI. Marcada `SUPUESTO NO VERIFICADO` (SNV-03). | Medio | 0 | Sustituir por la lista interna aprobada por Cumplimiento en Fase 5. | Abierto |
| P-011 | 1 | Los umbrales de los DMN (montos, SLA y aprobaciones) son parámetros de diseño sin validación del negocio. Marcados `SUPUESTO NO VERIFICADO` (SNV-04). | Medio | 0 | Validar con Riesgos, Operaciones y Cumplimiento antes de Fase 2. | Abierto |

## Cómo cerrar un pendiente

1. Ejecutar la acción indicada.
2. Verificar el resultado.
3. Actualizar `docs/EVIDENCIAS.md` o el documento afectado.
4. Cambiar el estado a `Cerrado` con fecha y nota.

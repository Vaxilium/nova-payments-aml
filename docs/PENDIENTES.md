# PENDIENTES

Bloqueos, deuda técnica y acciones que requieren intervención del autor (herramientas externas, credenciales, decisiones de negocio).

**Regla:** un problema se registra aquí después de **3 intentos fallidos** de resolución autónoma, o cuando depende de una acción que el agente no puede ejecutar.

| ID | Fase | Descripción | Impacto | Intentos | Próximo paso | Estado |
|---|---|---|---|---|---|---|
| P-001 | 3 | Python 3.12 no está instalado (solo 3.15). El código se mantiene compatible con 3.12+, pero el entorno no reproduce exactamente la versión objetivo. | Bajo | 1 | Instalar Python 3.12 y recrear `.venv` si se requiere reproducibilidad exacta. | Abierto |
| P-002 | 1–7 | Evidencias de herramientas no operables (Jira, Confluence, Azure DevOps, Bizagi/Camunda, Figma/Balsamiq, Power BI/Tableau, Lucidchart/Visio/Miro): requieren que el autor importe los artefactos y capture pantallas. | Medio | 0 | Seguir los pasos de `docs/EVIDENCIAS.md` al cerrar cada fase. | Abierto |
| P-003 | 1 | Registro de fuentes oficiales (BCP/SPI, SEPRELAD, GAFI, ISO 20022, SWIFT) aún vacío. No se ha escrito contenido normativo. | Medio | 0 | Verificar y citar antes de redactar el BRD y las reglas AML. | Abierto |
| P-004 | 7 | Enlace público de LinkedIn no disponible; el README usa un placeholder. | Bajo | 0 | Agregar la URL real antes de difundir el repositorio. | Abierto |
| P-005 | 7 | Licencia del repositorio sin definir. | Medio | 0 | Decidir licencia (por ejemplo, MIT) y agregar `LICENSE` antes de publicar. | Abierto |

## Cómo cerrar un pendiente

1. Ejecutar la acción indicada.
2. Verificar el resultado.
3. Actualizar `docs/EVIDENCIAS.md` o el documento afectado.
4. Cambiar el estado a `Cerrado` con fecha y nota.

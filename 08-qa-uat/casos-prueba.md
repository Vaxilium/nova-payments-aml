# Casos de prueba y UAT

Catálogo generado desde `08-qa-uat/uat/cases.py`. No se declaran resultados
hasta ejecutar `08-qa-uat/scripts/run_uat.py`.

- Casos totales: **65**
- Automatizados: **51**
- Manuales pendientes: **6**
- No implementados en el prototipo: **8**

| ID | Tipo | Historia | Título | Prioridad | Automatización |
|---|---|---|---|---|---|
| TC-001 | Positivo | US-001 | Transferencia local PYG entre cuentas activas | Alta | Automatizado |
| TC-002 | Negativo | US-002 | Resolver alias de beneficiario inexistente | Alta | No implementado |
| TC-003 | Positivo | US-003 | Consultar estado y asientos de una operación | Alta | Automatizado |
| TC-004 | Negativo | US-004 | Solicitar devolución fuera de plazo | Media | No implementado |
| TC-005 | Límite | US-005 | Rechazar transferencia local por encima del tope y por saldo insuficiente | Alta | Automatizado |
| TC-006 | Negativo | US-006 | Rechazar IBAN con checksum inválido y BIC mal formado | Alta | Automatizado |
| TC-007 | Positivo | US-007 | Generar y validar pacs.008 internacional | Alta | Automatizado |
| TC-008 | Positivo | US-008 | Procesar pacs.002 aceptado y rechazado | Alta | Automatizado |
| TC-009 | Positivo | US-009 | Reintentar envío internacional sin duplicar | Alta | Automatizado |
| TC-010 | Negativo | US-010 | Gestionar rechazo y timeout internacional | Media | Automatizado (parcial) |
| TC-011 | Positivo | US-011 | Alta digital de cliente con datos mínimos | Alta | No implementado |
| TC-012 | Negativo | US-012 | Verificación de identidad con documento vencido | Alta | No implementado |
| TC-013 | Positivo | US-013 | Screening de sanciones con coincidencia exacta y nombre normal | Alta | Automatizado |
| TC-014 | Límite | US-014 | Scoring KYC bajo y cliente PEP con EDD | Alta | Automatizado |
| TC-015 | Negativo | US-015 | Bloqueo por revisión periódica vencida | Media | No implementado |
| TC-016 | Negativo | US-016 | Retener o rechazar pago por screening previo | Alta | Automatizado |
| TC-017 | Positivo | US-017 | Ejecutar las 12 reglas de monitoreo y detectar patrones | Alta | Automatizado |
| TC-018 | Límite | US-018 | Asignar prioridad P1 y SLA a una alerta de alto riesgo | Alta | Automatizado |
| TC-019 | Positivo | US-019 | Listar alertas distintas y filtrar por prioridad | Alta | Automatizado |
| TC-020 | Positivo | US-020 | Investigar y cerrar una alerta | Alta | Automatizado |
| TC-021 | Positivo | US-021 | Escalar alerta a caso de investigación y cerrarlo | Media | Automatizado |
| TC-022 | Positivo | US-022 | Preparar borrador de ROS con campos obligatorios | Alta | Manual |
| TC-023 | Negativo | US-023 | Aprobar ROS sin evidencia adjunta | Alta | Manual |
| TC-024 | Positivo | US-024 | Registrar asiento de partida doble balanceado | Alta | Automatizado |
| TC-025 | Positivo | US-025 | Conciliar saldo operativo contra libro mayor | Alta | Automatizado |
| TC-026 | Límite | US-026 | Cierre diario contra el libro mayor | Media | Automatizado (parcial) |
| TC-027 | Positivo | US-027 | Consultar bitácora de auditoría por correlación | Alta | Manual |
| TC-028 | Positivo | US-028 | Validar KPIs de pagos en el dataset analítico | Media | Automatizado |
| TC-029 | Positivo | US-029 | Validar KPIs AML y referencias de alertas | Media | Automatizado |
| TC-030 | Positivo | US-030 | Exportar reporte operativo y verificar integridad | Baja | Automatizado |
| TC-031 | Positivo | US-031 | Consultar estado desde autoservicio | Media | Manual |
| TC-032 | Negativo | US-032 | Registrar reclamo de pago sin comprobante | Media | No implementado |
| TC-033 | Positivo | US-033 | Notificar evento de estado final | Media | No implementado |
| TC-034 | Límite | US-034 | Configurar tope local y validar su aplicación | Media | Automatizado (parcial) |
| TC-035 | Negativo | US-035 | Aprobar cambio de regla sin segundo aprobador | Media | Manual |
| TC-036 | Positivo | US-036 | Simular impacto de un cambio de umbral | Baja | Manual |
| TC-037 | Negativo | US-037 | Acceso a operación sin rol autorizado | Alta | No implementado |
| TC-038 | Positivo | US-038 | Propagar identificador de correlación en la API | Alta | Automatizado |
| TC-039 | Negativo | US-039 | Repetir solicitud idempotente y detectar conflicto | Alta | Automatizado |
| TC-040 | Positivo | US-040 | Monitorear salud del core | Alta | Automatizado |
| TC-041 | Límite | US-005 | Aceptar pago local exactamente en el tope de 10.000.000 PYG | Alta | Automatizado |
| TC-042 | Límite | US-005 | Rechazar pago local un peso por encima del tope | Alta | Automatizado |
| TC-043 | Negativo | US-005 | Rechazar importe cero | Alta | Automatizado |
| TC-044 | Negativo | US-005 | Rechazar importe negativo | Alta | Automatizado |
| TC-045 | Negativo | US-006 | Rechazar moneda desconocida | Alta | Automatizado |
| TC-046 | Límite | US-006 | Rechazar decimales en guaraníes | Alta | Automatizado |
| TC-047 | Negativo | US-006 | Rechazar IBAN con dígito de control incorrecto | Alta | Automatizado |
| TC-048 | Negativo | US-006 | Rechazar IBAN de país no soportado | Media | Automatizado |
| TC-049 | Negativo | US-006 | Rechazar BIC con longitud inválida | Alta | Automatizado |
| TC-050 | Negativo | US-007 | Rechazar UETR inválido | Media | Automatizado |
| TC-051 | Negativo | US-007 | Rechazar pacs.008 internacional sin agente acreedor | Alta | Automatizado |
| TC-052 | Negativo | US-008 | Rechazar pacs.002 RJCT sin motivo | Alta | Automatizado |
| TC-053 | Negativo | US-007 | Rechazar XML mal formado | Alta | Automatizado |
| TC-054 | Negativo | US-008 | Rechazar camt.053 con estado inválido | Media | Automatizado |
| TC-055 | Negativo | US-010 | Rechazar MT103 sin campo obligatorio | Alta | Automatizado |
| TC-056 | Negativo | US-010 | Rechazar MT103 con charge bearer inválido | Media | Automatizado |
| TC-057 | Negativo | US-006 | Rechazar liquidación internacional en EUR | Media | Automatizado |
| TC-058 | Negativo | US-010 | Rechazar pago internacional por saldo insuficiente | Alta | Automatizado |
| TC-059 | Negativo | US-009 | Detectar conflicto de idempotencia internacional | Alta | Automatizado |
| TC-060 | Positivo | US-017 | Detectar estructuración por debajo del umbral | Alta | Automatizado |
| TC-061 | Negativo | US-016 | Permitir pago normal sin alerta AML | Alta | Automatizado |
| TC-062 | Positivo | US-017 | Detectar jurisdicción de alto riesgo | Media | Automatizado |
| TC-063 | Negativo | US-024 | Rechazar asiento contable desbalanceado | Alta | Automatizado |
| TC-064 | Negativo | US-024 | Impedir modificación de un asiento posteado | Alta | Automatizado |
| TC-065 | Negativo | US-024 | Impedir sobregiro por encima del límite | Alta | Automatizado |

## Cobertura por tipo

| Tipo | Casos |
|---|---|
| Positivo | 25 |
| Negativo | 32 |
| Límite | 8 |

## Artefactos

- `casos-prueba.csv`: catálogo completo con pasos, datos y resultado esperado.
- `casos-prueba-ado-testplans.csv`: importación en Azure Test Plans (una fila por paso).
- `matriz-cobertura.csv`: cobertura por historia y estado de automatización.
- `matriz-ejecucion.xlsx`: workbook con resumen, casos, ejecución, cobertura y defectos.
- `resultados/resultados-uat.json`: resultados reales de la última ejecución.

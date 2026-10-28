# Historias de usuario

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** HUS-NB-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Fase:** 2 — Requerimientos

> Caso 100 % ficticio. Cada historia sigue el formato «Como… quiero… para…», tiene criterios de aceptación en Gherkin, prioridad MoSCoW, story points y dependencias.

---

## 1. Convenciones

- **ID:** `US-###` estable; se usa en Jira, Azure DevOps, trazabilidad y pruebas.
- **Prioridad MoSCoW:** `Must` (MVP), `Should` (importante, no bloquea MVP), `Could` (deseable).
- **Story points:** escala Fibonacci; miden complejidad relativa, no horas.
- **Dependencias:** historias que deben estar terminadas o suficientemente resueltas antes de iniciar.
- **Gherkin:** `Dado` (contexto), `Cuando` (acción), `Entonces` (resultado observable), `Y` (conjunción).
- **Criterio de aceptación:** cada escenario debe poder verificarse con una prueba funcional o UAT.

### 1.1 Índice por épica

| Épica | Nombre | Historias |
|---|---|---|
| EP-01 | Pagos locales instantáneos | US-001, US-002, US-003, US-004, US-005 |
| EP-02 | Cross-border ISO 20022 | US-006, US-007, US-008, US-009, US-010 |
| EP-03 | Onboarding y KYC digital | US-011, US-012, US-013, US-014, US-015 |
| EP-04 | Monitoreo AML y gestión de alertas | US-016, US-017, US-018, US-019, US-020 |
| EP-05 | Investigación y ROS | US-021, US-022, US-023 |
| EP-06 | Contabilidad, conciliación y auditoría | US-024, US-025, US-026, US-027 |
| EP-07 | Reporting y analítica | US-028, US-029, US-030 |
| EP-08 | Experiencia de cliente y autoservicio | US-031, US-032, US-033 |
| EP-09 | Parametrización y gobierno de reglas | US-034, US-035, US-036 |
| EP-10 | Plataforma, seguridad e idempotencia | US-037, US-038, US-039, US-040 |

### 1.2 Resumen de estimación

| Prioridad | Historias | Story points |
|---|---:|---:|
| Must | 26 | 135 |
| Should | 12 | 52 |
| Could | 2 | 11 |
| **Total** | **40** | **198** |

---

## 2. Historias

### US-001 — Crear transferencia local P2P

| Campo | Valor |
|---|---|
| Épica | EP-01 — Pagos locales instantáneos |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-011, US-037 |
| Requerimientos | BR-01, BR-02 |
| Proceso | PR-02 — Transferencia instantánea local |
| Sprint propuesto | Sprint 1 |

**Historia:** Como cliente persona, quiero iniciar una transferencia local en PYG indicando cuenta destino o alias, para enviar dinero al instante sin acudir a una sucursal.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Pago local válido
  Dado que el cliente está autenticado y tiene una cuenta origen con saldo suficiente
  Cuando ingresa un alias o cuenta destino válidos, un importe menor o igual a ₲10.000.000 y confirma la operación
  Entonces el sistema crea un pago con identificador único y estado RECIBIDO
  Y muestra un comprobante preliminar con beneficiario enmascarado e importe

Escenario: Importe por encima del límite
  Dado que el límite por operación configurado es ₲10.000.000
  Cuando el cliente intenta transferir un importe mayor
  Entonces el sistema rechaza la solicitud con el motivo LIMITE_EXCEDIDO
  Y no debita la cuenta origen
```

**Notas:** El tope de ₲10.000.000 y la operación 24/7 son parámetros del caso alineados a F-01 y marcados SUPUESTO NO VERIFICADO (SNV-01).

### US-002 — Resolver alias o cuenta destino

| Campo | Valor |
|---|---|
| Épica | EP-01 — Pagos locales instantáneos |
| Prioridad MoSCoW | Must |
| Story Points | 3 |
| Dependencias | US-001 |
| Requerimientos | BR-02 |
| Proceso | PR-02 — Transferencia instantánea local |
| Sprint propuesto | Sprint 1 |

**Historia:** Como cliente persona, quiero resolver el alias o la cuenta del beneficiario antes de confirmar, para verificar que el dinero llegará a la persona correcta.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Alias vigente
  Dado que existe un alias vigente asociado a una cuenta activa
  Cuando el cliente lo ingresa en el formulario de pago
  Entonces el sistema devuelve el titular enmascarado y la cuenta destino enmascarada
  Y permite continuar con la confirmación

Escenario: Alias inexistente
  Dado que el alias ingresado no existe o está inactivo
  Cuando el cliente intenta continuar
  Entonces el sistema muestra ALIAS_NO_ENCONTRADO
  Y no crea el pago
```

**Notas:** La resolución de alias es interna y no consulta directorios reales; el alias es un dato sintético.

### US-003 — Confirmar y consultar el estado del pago

| Campo | Valor |
|---|---|
| Épica | EP-01 — Pagos locales instantáneos |
| Prioridad MoSCoW | Must |
| Story Points | 3 |
| Dependencias | US-001 |
| Requerimientos | BR-03 |
| Proceso | PR-02 — Transferencia instantánea local |
| Sprint propuesto | Sprint 1 |

**Historia:** Como cliente persona, quiero consultar el estado del pago en tiempo real, para saber si el dinero fue acreditado, rechazado o devuelto sin llamar al banco.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Consulta de estado exitosa
  Dado que existe un pago del cliente con identificador único
  Cuando el cliente consulta el estado
  Entonces el sistema devuelve uno de los estados RECIBIDO, VALIDADO, ENVIADO, ACREDITADO, RECHAZADO o DEVUELTO
  Y muestra la marca de tiempo y el próximo paso cuando corresponda

Escenario: Estado final notificado
  Dado que el pago alcanzó un estado final
  Cuando el motor registra la transición
  Entonces se emite un evento de estado final con el identificador de correlación
  Y el cliente recibe una notificación con datos enmascarados
```

**Notas:** La máquina de estados es la fuente única de verdad para canal, atención y auditoría.

### US-004 — Solicitar devolución de un pago local

| Campo | Valor |
|---|---|
| Épica | EP-01 — Pagos locales instantáneos |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-003 |
| Requerimientos | BR-04 |
| Proceso | PR-07 — Devoluciones y reclamos |
| Sprint propuesto | Backlog |

**Historia:** Como cliente persona, quiero solicitar la devolución de un pago local dentro del plazo permitido, para recuperar el dinero cuando el pago no correspondía.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Solicitud dentro de plazo
  Dado que el pago está en estado ACREDITADO y dentro del plazo de solicitud
  Cuando el cliente registra el motivo y confirma la solicitud
  Entonces el sistema crea un caso de devolución con número, dueño y SLA
  Y muestra el estado SOLICITADA al cliente

Escenario: Solicitud fuera de plazo
  Dado que el pago superó el plazo configurado para solicitar devolución
  Cuando el cliente intenta registrar la solicitud
  Entonces el sistema rechaza la devolución automática con el motivo FUERA_DE_PLAZO
  Y ofrece el canal de reclamo formal
```

**Notas:** El plazo de devolución es un parámetro del caso y debe validarse con Operaciones y Cumplimiento.

### US-005 — Validar límites y saldo disponible

| Campo | Valor |
|---|---|
| Épica | EP-01 — Pagos locales instantáneos |
| Prioridad MoSCoW | Must |
| Story Points | 3 |
| Dependencias | US-001 |
| Requerimientos | BR-01 |
| Proceso | PR-02 — Transferencia instantánea local |
| Sprint propuesto | Sprint 1 |

**Historia:** Como cliente persona, quiero que el sistema valide límites y saldo antes de enviar el pago, para evitar rechazos tardíos y débitos inconsistentes.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Saldo y límites suficientes
  Dado que el cliente tiene saldo disponible y no supera el límite por operación ni el límite diario
  Cuando solicita el pago
  Entonces el sistema marca la validación como APTA
  Y continúa con la evaluación de riesgo

Escenario: Saldo insuficiente
  Dado que el cliente no tiene saldo suficiente en la cuenta origen
  Cuando solicita el pago
  Entonces el sistema rechaza la operación con el motivo SALDO_INSUFICIENTE
  Y no genera orden al riel
```

**Notas:** Los límites por cliente y por día son configurables; los valores concretos son parámetros de diseño.

### US-006 — Validar IBAN, BIC, moneda e importe internacional

| Campo | Valor |
|---|---|
| Épica | EP-02 — Cross-border ISO 20022 |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-037 |
| Requerimientos | BR-05, BR-06 |
| Proceso | PR-03 — Transferencia internacional saliente |
| Sprint propuesto | Sprint 2 |

**Historia:** Como cliente empresa, quiero que el sistema valide los datos del pago internacional antes de enviarlo, para evitar rechazos del corresponsal y reprocesos.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Datos internacionales válidos
  Dado que el cliente ingresa un IBAN con checksum válido, un BIC de 8 u 11 caracteres y una moneda USD o EUR
  Cuando solicita validar la instrucción
  Entonces el sistema devuelve el resultado VÁLIDO con los campos normalizados
  Y habilita la generación del mensaje ISO 20022

Escenario: IBAN con checksum inválido
  Dado que el IBAN ingresado no supera la validación de estructura o checksum
  Cuando el cliente solicita validar la instrucción
  Entonces el sistema rechaza con el campo IBAN y el motivo CHECKSUM_INVALIDO
  Y no genera ningún mensaje

Escenario: Moneda no soportada
  Dado que el cliente selecciona una moneda distinta de USD o EUR
  Cuando solicita validar la instrucción
  Entonces el sistema rechaza con el motivo MONEDA_NO_SOPORTADA
  Y muestra las monedas disponibles
```

**Notas:** La validación usa formato y checksum; no consulta directorios reales de IBAN/BIC (S-026).

### US-007 — Generar y validar mensaje pacs.008

| Campo | Valor |
|---|---|
| Épica | EP-02 — Cross-border ISO 20022 |
| Prioridad MoSCoW | Must |
| Story Points | 8 |
| Dependencias | US-006 |
| Requerimientos | BR-05, BR-06 |
| Proceso | PR-03 — Transferencia internacional saliente |
| Sprint propuesto | Sprint 2 |

**Historia:** Como sistema de mensajería, quiero generar un pacs.008 válido a partir de la instrucción, para enviar el pago internacional con la estructura ISO 20022 correcta.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Generación de pacs.008
  Dado que la instrucción internacional fue validada
  Cuando el sistema genera el mensaje
  Entonces crea un pacs.008 con UETR, importe, moneda, ordenante, beneficiario y referencias
  Y valida el mensaje contra el esquema antes de enviarlo

Escenario: Campo obligatorio faltante
  Dado que la instrucción carece de un campo obligatorio del mensaje
  Cuando el sistema intenta generar el pacs.008
  Entonces bloquea el envío y reporta el campo faltante
  Y deja el pago en estado REQUIERE_CORRECCION
```

**Notas:** El catálogo de campos y el mapeo MT103 ↔ ISO 20022 se completan en Fase 4.

### US-008 — Procesar pacs.002 y actualizar el estado

| Campo | Valor |
|---|---|
| Épica | EP-02 — Cross-border ISO 20022 |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-007 |
| Requerimientos | BR-03, BR-05 |
| Proceso | PR-03 — Transferencia internacional saliente |
| Sprint propuesto | Sprint 2 |

**Historia:** Como sistema de mensajería, quiero procesar el reporte de estado pacs.002 y actualizar el pago, para conocer si el corresponsal aceptó, rechazó o devolvió la operación.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Pacs.002 aceptado
  Dado que el corresponsal responde con un pacs.002 de aceptación
  Cuando el adaptador procesa el mensaje y correlaciona el UETR
  Entonces el pago pasa a estado ACEPTADO_CORRESPONSAL o ACREDITADO según la etapa
  Y se registra el evento con el identificador de correlación

Escenario: Pacs.002 rechazado
  Dado que el corresponsal responde con un rechazo
  Cuando el adaptador procesa el mensaje
  Entonces el pago pasa a estado RECHAZADO con el motivo informado
  Y se crea un caso para Operaciones Internacionales
```

**Notas:** Los códigos de rechazo se mapean a un catálogo funcional en Fase 4.

### US-009 — Reintentar envío internacional sin duplicar

| Campo | Valor |
|---|---|
| Épica | EP-02 — Cross-border ISO 20022 |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-007, US-039 |
| Requerimientos | BR-15 |
| Proceso | PR-03 — Transferencia internacional saliente |
| Sprint propuesto | Backlog |

**Historia:** Como sistema de mensajería, quiero reintentar un envío internacional usando la misma clave de idempotencia, para recuperar timeouts sin generar un segundo pago.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Reintento con la misma clave
  Dado que el primer envío terminó en timeout sin respuesta confirmada
  Cuando el sistema reintenta con la misma clave de idempotencia y el mismo payload
  Entonces reutiliza el resultado del intento original o consulta el estado
  Y no genera un segundo pacs.008

Escenario: Clave reutilizada con otro payload
  Dado que existe una clave de idempotencia asociada a un pago distinto
  Cuando se intenta usarla con otro importe o beneficiario
  Entonces el sistema rechaza con el motivo IDEMPOTENCY_KEY_CONFLICT
  Y no envía el mensaje
```

**Notas:** La clave de idempotencia se conserva al menos durante la ventana de reintentos definida por Operaciones.

### US-010 — Gestionar rechazo o devolución internacional

| Campo | Valor |
|---|---|
| Épica | EP-02 — Cross-border ISO 20022 |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-008 |
| Requerimientos | BR-04, BR-05 |
| Proceso | PR-03 — Transferencia internacional saliente |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Operaciones Internacionales, quiero gestionar el rechazo o la devolución de un pago internacional, para resolver la excepción con evidencia y notificar al cliente.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Rechazo del corresponsal
  Dado que el corresponsal rechazó el pago y existe un pacs.002 de rechazo
  Cuando el analista revisa el caso
  Entonces el sistema muestra el motivo, el mensaje y la traza completa
  Y permite notificar al cliente con una explicación accionable

Escenario: Devolución de fondos
  Dado que el corresponsal devolvió los fondos
  Cuando Operaciones registra la devolución
  Entonces el pago pasa a estado DEVUELTO y se genera el asiento de reversa
  Y se cierra el caso con evidencia
```

**Notas:** La devolución internacional se concilia con el asiento de reversa en Fase 3.

### US-011 — Iniciar alta digital de cliente

| Campo | Valor |
|---|---|
| Épica | EP-03 — Onboarding y KYC digital |
| Prioridad MoSCoW | Must |
| Story Points | 8 |
| Dependencias | Ninguna |
| Requerimientos | BR-10 |
| Proceso | PR-01 — Onboarding y KYC |
| Sprint propuesto | Sprint 1 |

**Historia:** Como cliente persona, quiero completar el alta digital con mis datos y aceptar los términos, para abrir una cuenta sin ir a una sucursal.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Solicitud de alta completa
  Dado que el cliente completa los datos obligatorios y acepta los términos
  Cuando envía la solicitud
  Entonces el sistema crea una solicitud en estado PENDIENTE_VERIFICACION con identificador
  Y muestra los siguientes pasos y el plazo estimado

Escenario: Datos obligatorios incompletos
  Dado que falta un dato obligatorio o el formato es inválido
  Cuando el cliente intenta enviar la solicitud
  Entonces el sistema marca los campos faltantes y no avanza
  Y conserva lo ingresado para reintentar
```

**Notas:** El alta digital es parte del TO-BE de PR-01; no se desarrolla la app móvil (E-04).

### US-012 — Verificar identidad y documentación

| Campo | Valor |
|---|---|
| Épica | EP-03 — Onboarding y KYC digital |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-011 |
| Requerimientos | BR-10 |
| Proceso | PR-01 — Onboarding y KYC |
| Sprint propuesto | Sprint 1 |

**Historia:** Como analista de Cumplimiento, quiero verificar la identidad y la documentación del cliente, para asegurar que la persona es quien dice ser.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Identidad verificada
  Dado que el documento es válido, está vigente y coincide con los datos declarados
  Cuando el servicio de identidad completa la verificación
  Entonces la solicitud pasa a identidad VERIFICADA
  Y se adjunta la evidencia al expediente

Escenario: Documento vencido
  Dado que el documento presentado está vencido o ilegible
  Cuando se ejecuta la verificación
  Entonces la solicitud queda PENDIENTE_DOCUMENTO con el motivo
  Y se solicita al cliente un documento válido
```

**Notas:** La verificación es simulada; no se integra un proveedor real de identidad.

### US-013 — Ejecutar screening de sanciones y PEP

| Campo | Valor |
|---|---|
| Épica | EP-03 — Onboarding y KYC digital |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-012 |
| Requerimientos | BR-07, BR-10 |
| Proceso | PR-01 — Onboarding y KYC |
| Sprint propuesto | Sprint 1 |

**Historia:** Como analista de Cumplimiento, quiero ejecutar el screening del cliente contra listas ficticias, para detectar coincidencias antes de aprobar el alta o un pago.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Sin coincidencias
  Dado que el cliente no presenta coincidencias en las listas ficticias
  Cuando se ejecuta el screening
  Entonces el resultado es LIMPIO y se registra la versión de la lista consultada
  Y el expediente queda listo para scoring de riesgo

Escenario: Coincidencia crítica
  Dado que el cliente coincide con una entrada crítica de la lista ficticia
  Cuando se ejecuta el screening
  Entonces el sistema bloquea el alta y genera una alerta P1
  Y deriva el caso a revisión de Cumplimiento

Escenario: Coincidencia parcial
  Dado que el screening devuelve una coincidencia parcial o de baja confianza
  Cuando se registra el resultado
  Entonces el caso pasa a revisión manual con la evidencia de la coincidencia
  Y no se aprueba el alta hasta la decisión del analista
```

**Notas:** Las listas son ficticias (S-018); no se usan listas reales de sanciones o PEP.

### US-014 — Calcular scoring de riesgo y aplicar EDD

| Campo | Valor |
|---|---|
| Épica | EP-03 — Onboarding y KYC digital |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-013 |
| Requerimientos | BR-10 |
| Proceso | PR-01 — Onboarding y KYC |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Cumplimiento, quiero calcular el riesgo del cliente y aplicar debida diligencia proporcional, para asignar controles adecuados a cada perfil.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Riesgo bajo
  Dado que el cliente obtiene un score de riesgo bajo
  Cuando el motor de decisión clasifica el perfil
  Entonces se aplica CDD estándar y el alta queda apta para aprobación
  Y se registra el score y sus factores

Escenario: Riesgo alto o PEP
  Dado que el cliente es PEP o su score es alto
  Cuando el motor de decisión clasifica el perfil
  Entonces se exige EDD y aprobación del Oficial de Cumplimiento
  Y no se habilita el alta hasta completar la evidencia adicional
```

**Notas:** El scoring usa el DMN de Fase 1; los umbrales son parámetros configurables (SNV-04).

### US-015 — Programar revisión periódica y bloqueo

| Campo | Valor |
|---|---|
| Épica | EP-03 — Onboarding y KYC digital |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-014 |
| Requerimientos | BR-10 |
| Proceso | PR-14 — Revisión periódica de cliente |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Cumplimiento, quiero programar la revisión periódica del cliente y bloquearlo si el riesgo lo exige, para mantener actualizado el perfil y evitar operar con clientes de riesgo no atendido.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Revisión vencida
  Dado que la fecha de revisión periódica de un cliente venció
  Cuando el job diario evalúa los vencimientos
  Entonces crea una tarea de revisión con dueño y plazo
  Y notifica al analista asignado

Escenario: Bloqueo por riesgo alto
  Dado que la revisión detecta un riesgo alto no aceptado
  Cuando Cumplimiento aprueba el bloqueo
  Entonces el cliente pasa a estado BLOQUEADO y se impiden nuevos pagos
  Y se registra el motivo y la evidencia
```

**Notas:** La periodicidad por nivel de riesgo es un parámetro de diseño pendiente de validación.

### US-016 — Evaluar screening y riesgo antes de liberar el pago

| Campo | Valor |
|---|---|
| Épica | EP-04 — Monitoreo AML y gestión de alertas |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-013, US-001 |
| Requerimientos | BR-07 |
| Proceso | PR-04 — Monitoreo transaccional |
| Sprint propuesto | Sprint 1 |

**Historia:** Como sistema de riesgo, quiero evaluar screening y riesgo de cada pago antes de liberar fondos, para evitar que una operación riesgosa salga sin control.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Pago sin coincidencia
  Dado que el ordenante y el beneficiario no presentan coincidencias
  Cuando el motor evalúa el pago
  Entonces registra la decisión LIBERAR con la evidencia y la versión de reglas
  Y el pago continúa al riel

Escenario: Coincidencia en lista
  Dado que el screening detecta una coincidencia crítica en el beneficiario
  Cuando el motor evalúa el pago
  Entonces bloquea la liberación y genera una alerta P1
  Y el pago queda en estado BLOQUEADO_POR_RIESGO
```

**Notas:** La cobertura de screening debe ser 100 % de los pagos liberados (K-07).

### US-017 — Ejecutar reglas de monitoreo transaccional

| Campo | Valor |
|---|---|
| Épica | EP-04 — Monitoreo AML y gestión de alertas |
| Prioridad MoSCoW | Must |
| Story Points | 8 |
| Dependencias | US-016 |
| Requerimientos | BR-08 |
| Proceso | PR-04 — Monitoreo transaccional |
| Sprint propuesto | Sprint 2 |

**Historia:** Como analista de Monitoreo AML, quiero ejecutar reglas de umbral, velocidad, geografía, contraparte y estructuración, para detectar operaciones inusuales de forma consistente.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Regla de umbral
  Dado que un pago supera el umbral configurado para la regla RULE-01
  Cuando se ejecuta el monitoreo
  Entonces se genera una alerta con la regla, el importe y el contexto del cliente
  Y se registra la evidencia de la evaluación

Escenario: Regla de velocidad
  Dado que un cliente supera la cantidad de operaciones permitidas en la ventana de tiempo
  Cuando se ejecuta la regla RULE-02
  Entonces se genera una alerta de velocidad con las operaciones que la activaron
  Y se prioriza según el DMN de prioridad

Escenario: Regla de estructuración
  Dado que se detectan varias operaciones por debajo del umbral con patrón repetido
  Cuando se ejecuta la regla RULE-04
  Entonces se genera una alerta de estructuración con la secuencia detectada
  Y se conserva la traza de las operaciones relacionadas
```

**Notas:** Las reglas y umbrales son parámetros del caso (SNV-04); se implementan en SQL en Fase 5.

### US-018 — Priorizar alertas P1, P2 y P3

| Campo | Valor |
|---|---|
| Épica | EP-04 — Monitoreo AML y gestión de alertas |
| Prioridad MoSCoW | Must |
| Story Points | 3 |
| Dependencias | US-017 |
| Requerimientos | BR-09 |
| Proceso | PR-05 — Gestión de alertas AML |
| Sprint propuesto | Sprint 2 |

**Historia:** Como supervisor de Monitoreo AML, quiero priorizar automáticamente las alertas según el riesgo, para atender primero los casos más críticos.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Alerta crítica
  Dado que una alerta involucra una coincidencia de sanciones o un importe crítico
  Cuando se evalúa la prioridad
  Entonces se clasifica como P1 con SLA de asignación de 15 minutos
  Y se muestra en la parte superior de la bandeja

Escenario: Alerta de bajo riesgo
  Dado que una alerta corresponde a un umbral menor sin otros factores
  Cuando se evalúa la prioridad
  Entonces se clasifica como P3 con el SLA correspondiente
  Y se encola para atención según capacidad
```

**Notas:** El DMN de prioridad de Fase 1 define la lógica; los SLA son parámetros del caso.

### US-019 — Asignar y gestionar la bandeja de alertas

| Campo | Valor |
|---|---|
| Épica | EP-04 — Monitoreo AML y gestión de alertas |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-018 |
| Requerimientos | BR-09 |
| Proceso | PR-05 — Gestión de alertas AML |
| Sprint propuesto | Sprint 2 |

**Historia:** Como supervisor de Monitoreo AML, quiero asignar alertas a analistas y controlar su SLA, para garantizar que ninguna alerta quede sin dueño.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Asignación manual
  Dado que existe una alerta sin asignar
  Cuando el supervisor la asigna a un analista
  Entonces la alerta pasa a estado ASIGNADA con dueño, prioridad y vencimiento
  Y el analista la ve en su bandeja

Escenario: P1 sin asignar
  Dado que una alerta P1 lleva 15 minutos sin asignación
  Cuando el job de SLA evalúa la bandeja
  Entonces escala la alerta al supervisor y registra el incumplimiento
  Y muestra la alerta como SLA_EN_RIESGO
```

**Notas:** La bandeja es el punto único de gestión; no se usan correos ni hojas de cálculo.

### US-020 — Investigar y cerrar una alerta

| Campo | Valor |
|---|---|
| Épica | EP-04 — Monitoreo AML y gestión de alertas |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-019 |
| Requerimientos | BR-09 |
| Proceso | PR-05 — Gestión de alertas AML |
| Sprint propuesto | Sprint 2 |

**Historia:** Como analista de Monitoreo AML, quiero documentar la investigación y cerrar la alerta con evidencia, para demostrar que el caso fue analizado y justificar la decisión.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Cierre no sospechoso
  Dado que el analista revisó la evidencia y no encontró indicios de sospecha
  Cuando registra el análisis y confirma el cierre
  Entonces la alerta pasa a CERRADA con motivo NO_SOSPECHOSA
  Y se conserva el expediente y la marca de tiempo

Escenario: Evidencia insuficiente
  Dado que el analista no adjuntó evidencia suficiente
  Cuando intenta cerrar la alerta
  Entonces el sistema bloquea el cierre y solicita completar el expediente
  Y mantiene la alerta en estado EN_INVESTIGACION
```

**Notas:** El cierre requiere motivo y evidencia; el caso queda disponible para auditoría.

### US-021 — Escalar un caso a investigación

| Campo | Valor |
|---|---|
| Épica | EP-05 — Investigación y ROS |
| Prioridad MoSCoW | Should |
| Story Points | 3 |
| Dependencias | US-020 |
| Requerimientos | BR-09 |
| Proceso | PR-06 — Investigación y ROS |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Monitoreo AML, quiero escalar una alerta a investigación cuando existen indicios de sospecha, para profundizar el análisis con el expediente completo.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Escalamiento aprobado
  Dado que el analista documenta indicios de sospecha
  Cuando el supervisor aprueba el escalamiento
  Entonces se crea un caso de investigación con el expediente vinculado
  Y se asigna al analista de investigación

Escenario: Escalamiento sin aprobación
  Dado que el supervisor no aprueba el escalamiento
  Cuando revisa la solicitud
  Entonces el caso vuelve a la bandeja de alertas con el comentario
  Y no se crea un caso de investigación
```

**Notas:** La segregación entre monitoreo e investigación evita conflicto de interés.

### US-022 — Preparar el borrador de ROS

| Campo | Valor |
|---|---|
| Épica | EP-05 — Investigación y ROS |
| Prioridad MoSCoW | Must |
| Story Points | 8 |
| Dependencias | US-021 |
| Requerimientos | BR-09, BR-12 |
| Proceso | PR-06 — Investigación y ROS |
| Sprint propuesto | Backlog |

**Historia:** Como analista de investigación, quiero preparar un borrador de ROS con los campos obligatorios y la narrativa, para documentar la sospecha de forma completa y consistente.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Borrador completo
  Dado que el caso de investigación tiene evidencia y análisis
  Cuando el analista genera el borrador
  Entonces el sistema completa los campos obligatorios y la narrativa
  Y deja el ROS en estado BORRADOR para revisión

Escenario: Campo obligatorio faltante
  Dado que falta un campo obligatorio del ROS
  Cuando el analista intenta enviarlo a revisión
  Entonces el sistema bloquea el envío y marca el campo faltante
  Y conserva el borrador para completarlo
```

**Notas:** El formato y los campos del ROS son ficticios y se detallan en Fase 5.

### US-023 — Aprobar y registrar el ROS ficticio

| Campo | Valor |
|---|---|
| Épica | EP-05 — Investigación y ROS |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-022 |
| Requerimientos | BR-09, BR-12 |
| Proceso | PR-06 — Investigación y ROS |
| Sprint propuesto | Backlog |

**Historia:** Como Oficial de Cumplimiento, quiero aprobar y registrar el ROS ficticio con control de reserva, para dejar evidencia de la decisión sin enviar información real.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Aprobación del ROS
  Dado que el borrador está completo y revisado
  Cuando el Oficial de Cumplimiento aprueba
  Entonces el ROS pasa a estado APROBADO con hash, fecha y responsable
  Y se registra como ficticio, sin envío a SEPRELAD

Escenario: Rechazo del borrador
  Dado que el Oficial de Cumplimiento detecta información insuficiente
  Cuando rechaza el borrador
  Entonces el ROS vuelve a BORRADOR con el comentario
  Y se notifica al analista
```

**Notas:** El envío real a SEPRELAD está fuera de alcance (E-06); el ROS es un artefacto de diseño.

### US-024 — Registrar asiento de partida doble

| Campo | Valor |
|---|---|
| Épica | EP-06 — Contabilidad, conciliación y auditoría |
| Prioridad MoSCoW | Must |
| Story Points | 8 |
| Dependencias | US-001, US-008 |
| Requerimientos | BR-11 |
| Proceso | PR-08 — Conciliación y contabilidad |
| Sprint propuesto | Sprint 2 |

**Historia:** Como sistema contable, quiero registrar cada movimiento con débito y crédito balanceados, para mantener el libro mayor íntegro y auditable.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Asiento balanceado
  Dado que un pago fue aceptado y tiene importe, cuentas y referencias
  Cuando el sistema registra el asiento
  Entonces crea débito y crédito de igual importe vinculados al pago
  Y valida que la suma de débitos sea igual a la suma de créditos

Escenario: Asiento desbalanceado
  Dado que el importe del débito no coincide con el crédito
  Cuando el sistema intenta registrar el asiento
  Entonces rechaza el registro y genera una alerta contable
  Y no altera el libro mayor
```

**Notas:** La invariante de partida doble se verifica con tests en Fase 3.

### US-025 — Conciliar contra el riel y el core

| Campo | Valor |
|---|---|
| Épica | EP-06 — Contabilidad, conciliación y auditoría |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-024 |
| Requerimientos | BR-11 |
| Proceso | PR-08 — Conciliación y contabilidad |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Contraloría, quiero conciliar diariamente los asientos contra el riel y el core, para detectar diferencias antes del cierre.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Cierre sin diferencias
  Dado que los registros del libro mayor, el riel y el core coinciden
  Cuando se ejecuta la conciliación diaria
  Entonces el sistema marca el cierre como CONCILIADO
  Y publica el porcentaje de conciliación del día

Escenario: Diferencia detectada
  Dado que existe un asiento sin contraparte en el riel o el core
  Cuando se ejecuta la conciliación
  Entonces se crea una diferencia con dueño, importe y referencia
  Y se excluye del cierre automático
```

**Notas:** La conciliación se implementa en Fase 3 con datos sintéticos.

### US-026 — Gestionar diferencias de conciliación

| Campo | Valor |
|---|---|
| Épica | EP-06 — Contabilidad, conciliación y auditoría |
| Prioridad MoSCoW | Should |
| Story Points | 3 |
| Dependencias | US-025 |
| Requerimientos | BR-11 |
| Proceso | PR-08 — Conciliación y contabilidad |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Contraloría, quiero gestionar las diferencias de conciliación hasta su resolución, para evitar ajustes manuales sin trazabilidad.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Diferencia asignada
  Dado que existe una diferencia de conciliación
  Cuando Contraloría la asigna a un responsable
  Entonces la diferencia pasa a estado ABIERTA con plazo y evidencia
  Y se muestra en el tablero de cierre

Escenario: Ajuste aprobado
  Dado que la diferencia fue investigada y requiere ajuste
  Cuando el supervisor aprueba el asiento de ajuste
  Entonces se registra el ajuste con referencia a la diferencia
  Y la diferencia pasa a CERRADA
```

**Notas:** Todo ajuste requiere aprobación y queda en la bitácora de auditoría.

### US-027 — Consultar la bitácora de auditoría

| Campo | Valor |
|---|---|
| Épica | EP-06 — Contabilidad, conciliación y auditoría |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-038 |
| Requerimientos | BR-12 |
| Proceso | PR-13 — Auditoría y evidencia |
| Sprint propuesto | Backlog |

**Historia:** Como auditor interno, quiero consultar la bitácora de una operación por identificador, para reconstruir la historia completa y demostrar el control.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Consulta por operación
  Dado que el auditor tiene permiso de consulta
  Cuando busca una operación por su identificador de correlación
  Entonces el sistema devuelve los eventos ordenados con actor, timestamp y resultado
  Y permite exportar la traza para evidencia

Escenario: Intento de modificación
  Dado que la bitácora es de solo agregado
  Cuando un usuario intenta modificar o borrar un evento
  Entonces el sistema rechaza la operación y registra el intento
  Y notifica a Seguridad
```

**Notas:** La retención y el acceso se definen con Cumplimiento y Seguridad.

### US-028 — Tablero de KPIs de pagos

| Campo | Valor |
|---|---|
| Épica | EP-07 — Reporting y analítica |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-024, US-025 |
| Requerimientos | BR-13 |
| Proceso | PR-09 — Reporting operativo y AML |
| Sprint propuesto | Backlog |

**Historia:** Como gerente de Operaciones, quiero ver un tablero con los KPIs de pagos locales e internacionales, para detectar desvíos de SLA y volumen a tiempo.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Tablero con datos
  Dado que existen datos del periodo seleccionado
  Cuando el gerente abre el tablero
  Entonces ve K-01 a K-06 con fórmula, periodo, fuente y dueño
  Y puede filtrar por canal, moneda y tipo de pago

Escenario: Dato faltante
  Dado que una fuente no reportó datos para el periodo
  Cuando se carga el tablero
  Entonces el KPI se muestra como SIN_DATOS
  Y no se infiere ni se completa el valor
```

**Notas:** El tablero se construye en Fase 6; esta historia define el contrato funcional.

### US-029 — Tablero de KPIs AML

| Campo | Valor |
|---|---|
| Épica | EP-07 — Reporting y analítica |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-020, US-023 |
| Requerimientos | BR-13 |
| Proceso | PR-09 — Reporting operativo y AML |
| Sprint propuesto | Backlog |

**Historia:** Como Jefe de Monitoreo AML, quiero ver un tablero con los KPIs de alertas, investigación y ROS, para gestionar capacidad, SLA y calidad de las reglas.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Tablero AML
  Dado que existen alertas y casos del periodo
  Cuando el jefe abre el tablero
  Entonces ve K-07 a K-12 con filtros por prioridad, analista y regla
  Y puede identificar la regla con mayor tasa de falsos positivos

Escenario: Filtro por analista
  Dado que el jefe selecciona un analista
  Cuando aplica el filtro
  Entonces el tablero muestra solo los casos asignados a ese analista
  Y conserva el periodo y la definición del KPI
```

**Notas:** Los datos son sintéticos y agregados; no se exponen datos personales.

### US-030 — Exportar reporte operativo

| Campo | Valor |
|---|---|
| Épica | EP-07 — Reporting y analítica |
| Prioridad MoSCoW | Could |
| Story Points | 3 |
| Dependencias | US-028 |
| Requerimientos | BR-13 |
| Proceso | PR-09 — Reporting operativo y AML |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Operaciones, quiero exportar un reporte operativo filtrado a CSV, para compartir el análisis con áreas que no acceden al tablero.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Exportación con filtros
  Dado que el analista aplicó filtros válidos
  Cuando solicita exportar
  Entonces el sistema genera un CSV con los filtros, la fecha y la fuente
  Y registra la exportación en la bitácora

Escenario: Exportación sin permiso
  Dado que el usuario no tiene permiso de exportación
  Cuando intenta exportar
  Entonces el sistema deniega la operación con 403
  Y registra el intento
```

**Notas:** La exportación debe respetar minimización y enmascaramiento de datos.

### US-031 — Consultar estado desde autoservicio

| Campo | Valor |
|---|---|
| Épica | EP-08 — Experiencia de cliente y autoservicio |
| Prioridad MoSCoW | Should |
| Story Points | 3 |
| Dependencias | US-003 |
| Requerimientos | BR-03, BR-16 |
| Proceso | PR-07 — Devoluciones y reclamos |
| Sprint propuesto | Backlog |

**Historia:** Como cliente persona, quiero consultar el estado y el próximo paso de mi pago desde autoservicio, para resolver la duda sin contactar al banco.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Consulta del propio pago
  Dado que el cliente está autenticado y el pago le pertenece
  Cuando abre el detalle del pago
  Entonces ve estado, importe, beneficiario enmascarado y próximo paso
  Y ve el canal de reclamo cuando el estado es final

Escenario: Acceso a pago ajeno
  Dado que el pago pertenece a otro cliente
  Cuando el cliente intenta consultarlo
  Entonces el sistema deniega el acceso
  Y no revela información del pago
```

**Notas:** La pantalla se especifica en Fase 6; el contrato de estado es el de US-003.

### US-032 — Registrar reclamo de pago

| Campo | Valor |
|---|---|
| Épica | EP-08 — Experiencia de cliente y autoservicio |
| Prioridad MoSCoW | Should |
| Story Points | 3 |
| Dependencias | US-031 |
| Requerimientos | BR-04, BR-16 |
| Proceso | PR-07 — Devoluciones y reclamos |
| Sprint propuesto | Backlog |

**Historia:** Como cliente persona, quiero registrar un reclamo asociado a un pago, para dejar constancia y recibir seguimiento.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Reclamo nuevo
  Dado que el cliente selecciona un pago propio y un motivo válido
  Cuando envía el reclamo
  Entonces el sistema crea un caso con número y plazo visible
  Y muestra el estado REGISTRADO

Escenario: Reclamo duplicado
  Dado que ya existe un reclamo abierto para el mismo pago y motivo
  Cuando el cliente intenta registrar otro
  Entonces el sistema vincula la solicitud al caso existente
  Y evita duplicar el expediente
```

**Notas:** El CRM es simulado; el caso se integra con la trazabilidad del pago.

### US-033 — Notificar eventos del pago al cliente

| Campo | Valor |
|---|---|
| Épica | EP-08 — Experiencia de cliente y autoservicio |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-003 |
| Requerimientos | BR-03 |
| Proceso | PR-07 — Devoluciones y reclamos |
| Sprint propuesto | Backlog |

**Historia:** Como sistema de notificaciones, quiero enviar notificaciones claras cuando cambia el estado del pago, para el cliente sepa qué pasó sin consultar manualmente.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Notificación de acreditación
  Dado que el pago pasó a estado ACREDITADO
  Cuando se procesa el evento
  Entonces el sistema envía una notificación con importe y beneficiario enmascarado
  Y registra el envío y la respuesta del canal

Escenario: Fallo de notificación
  Dado que el canal de notificación no responde
  Cuando se intenta enviar el mensaje
  Entonces el sistema programa reintentos y registra el fallo
  Y no bloquea ni revierte el pago
```

**Notas:** La notificación es un efecto secundario: nunca condiciona la liquidación del pago.

### US-034 — Configurar límites y umbrales

| Campo | Valor |
|---|---|
| Épica | EP-09 — Parametrización y gobierno de reglas |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-037 |
| Requerimientos | BR-14 |
| Proceso | PR-10 — Gestión de reglas y parámetros |
| Sprint propuesto | Backlog |

**Historia:** Como administrador de Riesgos, quiero configurar límites y umbrales sin desplegar código, para ajustar el control al apetito de riesgo vigente.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Nuevo umbral
  Dado que el administrador tiene permiso de configuración
  Cuando crea un cambio de umbral dentro del rango permitido
  Entonces el sistema crea una versión en estado BORRADOR con autor y fecha
  Y no afecta la operación hasta su aprobación

Escenario: Valor fuera de rango
  Dado que el valor propuesto está fuera del rango permitido
  Cuando el administrador intenta guardarlo
  Entonces el sistema rechaza el cambio con el rango válido
  Y no crea la versión
```

**Notas:** Los rangos y valores son parámetros del caso; requieren aprobación de Riesgos y Cumplimiento.

### US-035 — Versionar y aprobar cambios de reglas

| Campo | Valor |
|---|---|
| Épica | EP-09 — Parametrización y gobierno de reglas |
| Prioridad MoSCoW | Should |
| Story Points | 5 |
| Dependencias | US-034 |
| Requerimientos | BR-14 |
| Proceso | PR-10 — Gestión de reglas y parámetros |
| Sprint propuesto | Backlog |

**Historia:** Como Oficial de Cumplimiento, quiero aprobar y activar versiones de reglas con vigencia, para todo cambio tenga control, evidencia y posibilidad de reversa.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Cambio aprobado
  Dado que existe una versión BORRADOR revisada
  Cuando Riesgos y Cumplimiento aprueban
  Entonces la versión pasa a ACTIVA con fecha de vigencia
  Y la versión anterior queda histórica

Escenario: Cambio sin aprobación
  Dado que falta una de las aprobaciones requeridas
  Cuando se intenta activar la versión
  Entonces el sistema bloquea la activación
  Y muestra las aprobaciones pendientes
```

**Notas:** El gobierno de cambios se audita con la bitácora de US-027.

### US-036 — Simular impacto de reglas

| Campo | Valor |
|---|---|
| Épica | EP-09 — Parametrización y gobierno de reglas |
| Prioridad MoSCoW | Could |
| Story Points | 8 |
| Dependencias | US-034 |
| Requerimientos | BR-14 |
| Proceso | PR-10 — Gestión de reglas y parámetros |
| Sprint propuesto | Backlog |

**Historia:** Como analista de Riesgos, quiero simular el impacto de una regla sobre datos sintéticos, para estimar alertas y falsos positivos antes de activarla.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Simulación disponible
  Dado que existe un dataset sintético versionado
  Cuando el analista ejecuta la simulación de una regla
  Entonces el sistema muestra operaciones afectadas, alertas estimadas y tasa de falsos positivos
  Y conserva el resultado con la versión simulada

Escenario: Dataset no disponible
  Dado que el dataset requerido no está disponible
  Cuando el analista intenta simular
  Entonces el sistema muestra DATASET_NO_DISPONIBLE
  Y no genera resultados parciales
```

**Notas:** La simulación se apoya en el dataset sintético de Fase 3; no usa datos reales.

### US-037 — Autenticación y autorización por rol

| Campo | Valor |
|---|---|
| Épica | EP-10 — Plataforma, seguridad e idempotencia |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | Ninguna |
| Requerimientos | BR-12, NFR-03 |
| Proceso | PR-11 — Gestión de incidentes |
| Sprint propuesto | Sprint 1 |

**Historia:** Como usuario interno, quiero acceder solo a las funciones permitidas por mi rol, para segregar funciones y proteger la información.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Acceso permitido
  Dado que un usuario tiene el rol ANALISTA_AML
  Cuando accede a la bandeja de alertas
  Entonces el sistema permite la operación
  Y registra el acceso en la bitácora

Escenario: Acceso denegado
  Dado que un usuario con rol ANALISTA_AML intenta acceder a configuración de reglas
  Cuando realiza la solicitud
  Entonces el sistema responde 403 y no muestra la función
  Y registra el intento denegado
```

**Notas:** Los roles se definen con Seguridad y Cumplimiento; el detalle técnico se implementa en Fase 3.

### US-038 — Registrar eventos con correlación

| Campo | Valor |
|---|---|
| Épica | EP-10 — Plataforma, seguridad e idempotencia |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-037 |
| Requerimientos | BR-12 |
| Proceso | PR-13 — Auditoría y evidencia |
| Sprint propuesto | Sprint 1 |

**Historia:** Como sistema de auditoría, quiero registrar cada evento con identificador de correlación, actor y resultado, para reconstruir cualquier operación de extremo a extremo.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Evento correlacionado
  Dado que ocurre un evento de pago, riesgo o alerta
  Cuando se persiste el evento
  Entonces incluye correlation_id, actor, timestamp, tipo y resultado
  Y queda disponible para consulta

Escenario: Evento sin correlación
  Dado que un evento no tiene correlation_id
  Cuando se intenta persistir
  Entonces el sistema lo rechaza y registra el error
  Y no contamina la traza
```

**Notas:** La bitácora es append-only y se implementa en Fase 3.

### US-039 — Garantizar idempotencia de API

| Campo | Valor |
|---|---|
| Épica | EP-10 — Plataforma, seguridad e idempotencia |
| Prioridad MoSCoW | Must |
| Story Points | 5 |
| Dependencias | US-037 |
| Requerimientos | BR-15 |
| Proceso | PR-11 — Gestión de incidentes |
| Sprint propuesto | Sprint 2 |

**Historia:** Como sistema cliente, quiero reintentar una solicitud sin duplicar el efecto, para tolerar timeouts y fallos de red de forma segura.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Reintento idempotente
  Dado que se envió una solicitud con una Idempotency-Key y se recibió timeout
  Cuando se repite la solicitud con la misma clave y payload
  Entonces el sistema devuelve la misma respuesta sin crear otro recurso
  Y mantiene el estado original

Escenario: Conflicto de clave
  Dado que la Idempotency-Key ya fue usada con otro payload
  Cuando se envía la nueva solicitud
  Entonces el sistema responde 409 IDEMPOTENCY_KEY_CONFLICT
  Y no procesa la nueva solicitud
```

**Notas:** La clave se conserva durante la ventana de reintentos; el detalle se implementa en Fase 3.

### US-040 — Monitorear salud y SLA

| Campo | Valor |
|---|---|
| Épica | EP-10 — Plataforma, seguridad e idempotencia |
| Prioridad MoSCoW | Must |
| Story Points | 3 |
| Dependencias | US-038 |
| Requerimientos | BR-13, NFR-06 |
| Proceso | PR-11 — Gestión de incidentes |
| Sprint propuesto | Backlog |

**Historia:** Como operador de TI, quiero monitorear la salud de los componentes y el cumplimiento de SLA, para detectar degradaciones antes de que afecten a los clientes.

**Criterios de aceptación (Gherkin):**

```gherkin
Escenario: Chequeo de salud
  Dado que el operador consulta el endpoint de salud
  Cuando el sistema evalúa las dependencias
  Entonces devuelve el estado de core, riel, screening y base de datos
  Y marca DEGRADADO cuando una dependencia no responde

Escenario: Latencia fuera de umbral
  Dado que el p95 de un componente supera el umbral configurado
  Cuando se evalúa la regla de monitoreo
  Entonces se genera una alerta operativa con el componente y la ventana
  Y se registra el evento en la bitácora
```

**Notas:** El stack de observabilidad se especifica en Fase 3/7; aquí se define el comportamiento funcional.

---

## 3. Historias excluidas de los dos primeros sprints

Las historias no listadas en `planificacion-sprints.md` permanecen en el backlog priorizado. No se eliminan: se reevalúan al cierre de cada sprint según valor, dependencia y capacidad.

## 4. Referencias

- `epicas.md` — agrupación y resultados esperados.
- `planificacion-sprints.md` — asignación a Sprint 1 y Sprint 2.
- `matriz-trazabilidad.csv` — trazabilidad completa.
- `../01-negocio/BRD.md` — requerimientos de negocio.

**Fin del documento.**

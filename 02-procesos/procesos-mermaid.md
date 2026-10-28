# Procesos en Mermaid

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub
**Documento:** MMD-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-27

> Diagramas complementarios a los BPMN. Se pueden visualizar en GitHub, GitLab, VS Code o en la herramienta de diagramación preferida. Los BPMN son la fuente principal para importar en Bizagi/Camunda/Signavio; Mermaid es una vista rápida y portable.

---

## 1. Leyenda

| Forma | Uso |
|---|---|
| Rectángulo | Actividad o paso |
| Rombo | Decisión |
| Óvalo / estadio | Inicio o fin |
| Flecha | Flujo de secuencia |
| Flecha punteada | Mensaje o dependencia |
| Nota | Aclaración |

---

## 2. Transferencia local AS-IS

```mermaid
flowchart LR
    A([Cliente solicita transferencia]) --> B[Recibir formulario y documentos]
    B --> C[Validar datos manualmente]
    C --> D{¿Datos completos?}
    D -- No --> E[Solicitar corrección]
    E --> B
    D -- Sí --> F[Autorizar supervisor]
    F --> G[Cargar en lote]
    G --> H[Esperar ventana de proceso]
    H --> I[Procesar ACH/LBTR]
    I --> J[Conciliar y registrar]
    J --> K[Notificar al cliente]
    K --> L([Transferencia completada])
```

**Problemas visibles:** validación manual, autorización separada, proceso por lote, espera de ventana y conciliación posterior.

---

## 3. Transferencia local TO-BE

```mermaid
flowchart LR
    A([Cliente inicia pago]) --> B[Capturar alias/cuenta, importe y motivo]
    B --> C[Resolver alias y validar datos]
    C --> D{¿Datos y límite válidos?}
    D -- No --> E[Corregir datos]
    E --> B
    D -- Sí --> F[Verificar saldo y límite]
    F --> G{¿Saldo suficiente?}
    G -- No --> H([Pago rechazado por datos])
    G -- Sí --> I[Screening y scoring de riesgo]
    I --> J{¿Pago aprobado?}
    J -- No --> K([Pago retenido para revisión])
    J -- Sí --> L[Enviar orden al SPI]
    L --> M[Esperar confirmación del SPI]
    M --> N{¿Confirmado?}
    N -- No --> O[Gestionar rechazo o devolución]
    O --> P([Pago rechazado o devuelto])
    N -- Sí --> Q[Acreditar y registrar asiento]
    Q --> R[Registrar partida doble]
    R --> S[Notificar estado al cliente]
    S --> T([Pago completado])
```

**Controles:** idempotencia por identificador, scoring antes de liberar, confirmación del SPI, asiento contable y notificación.

---

## 4. Transferencia internacional TO-BE

```mermaid
flowchart LR
    A([Cliente solicita pago internacional]) --> B[Capturar IBAN/BIC, moneda e importe]
    B --> C[Validar IBAN, BIC e ISO 4217]
    C --> D{¿Datos válidos?}
    D -- No --> E[Corregir instrucción]
    E --> B
    D -- Sí --> F[Screening y scoring de riesgo]
    F --> G{¿Aprobado?}
    G -- No --> H([Pago en revisión])
    G -- Sí --> I[Generar pacs.008]
    I --> J[Validar esquema ISO 20022]
    J --> K{¿Mensaje válido?}
    K -- No --> L[Reparar mensaje]
    L --> I
    K -- Sí --> M[Enviar pacs.008 a SWIFT]
    M --> N[Esperar pacs.002]
    N --> O{¿Aceptado?}
    O -- No --> P[Gestionar rechazo o devolución]
    P --> Q([Pago rechazado o devuelto])
    O -- Sí --> R[Conciliar y registrar asiento]
    R --> S[Notificar estado al cliente]
    S --> T([Pago enviado])
```

**Controles:** validación de IBAN/BIC/ISO 4217, screening previo, validación del esquema, correlación `pacs.008`/`pacs.002` y conciliación.

---

## 5. Onboarding y KYC

```mermaid
flowchart TD
    A([Persona solicita alta]) --> B[Capturar datos y documentos]
    B --> C[Validar identidad]
    C --> D{¿Identidad verificada?}
    D -- No --> E[Solicitar documentación adicional]
    E --> B
    D -- Sí --> F[Screening de sanciones y PEP]
    F --> G{¿Coincidencia crítica?}
    G -- Sí --> H[Bloquear y rechazar]
    H --> I([Alta rechazada])
    G -- No --> J[Evaluar riesgo con DMN]
    J --> K{¿Requiere EDD?}
    K -- Sí --> L[Solicitar evidencia adicional]
    L --> M[Revisar y aprobar EDD]
    K -- No --> N[Aprobar cliente]
    M --> O[Crear cliente y cuenta]
    N --> O
    O --> P[Notificar alta y condiciones]
    P --> Q([Cliente activo])
```

**Excepciones:** identidad no verificable, coincidencia en listas, PEP, beneficiario final incompleto y rechazo por riesgo.

---

## 6. Gestión de alerta AML

```mermaid
flowchart TD
    A([Transacción registrada]) --> B[Evaluar reglas de monitoreo]
    B --> C{¿Genera alerta?}
    C -- No --> D([Sin alerta])
    C -- Sí --> E[Crear alerta con contexto]
    E --> F[Priorizar con DMN]
    F --> G[Asignar analista y SLA]
    G --> H[Investigar y reunir evidencia]
    H --> I{¿Requiere EDD?}
    I -- Sí --> J[Solicitar información adicional]
    J --> H
    I -- No --> K[Documentar decisión]
    K --> L{¿Existe sospecha?}
    L -- Sí --> M[Escalar a investigación/ROS]
    M --> N([Caso escalado a ROS])
    L -- No --> O[Cerrar caso con evidencia]
    O --> P([Caso cerrado])
```

**SLA del caso:** P1 = 15 min para asignación; P2 = 60 min; P3 = 4 h. Son parámetros de diseño.

---

## 7. Investigación y ROS

```mermaid
flowchart TD
    A([Caso escalado recibido]) --> B[Reunir y analizar evidencia]
    B --> C[Redactar narrativa y hallazgos]
    C --> D{¿Existe sospecha?}
    D -- No --> E[Cerrar caso y documentar]
    E --> F([Caso cerrado sin ROS])
    D -- Sí --> G[Preparar borrador de ROS]
    G --> H[Revisar ROS]
    H --> I{¿ROS aprobado?}
    I -- No --> J[Devolver a análisis]
    J --> C
    I -- Sí --> K[Aprobar y registrar ROS]
    K --> L[Aplicar reserva y control de acceso]
    L --> M[Notificar a UIF simulado]
    M --> N([ROS reportado])
```

**Control clave:** la reserva impide revelar al cliente que se reportó la operación.

---

## 8. Máquina de estados del pago

```mermaid
stateDiagram-v2
    [*] --> RECIBIDO
    RECIBIDO --> VALIDADO: datos OK
    RECIBIDO --> RECHAZADO: datos inválidos
    VALIDADO --> EN_EVALUACION: scoring
    EN_EVALUACION --> RETENIDO: riesgo no aprobado
    EN_EVALUACION --> ENVIADO: riesgo aprobado
    ENVIADO --> ACREDITADO: confirmación
    ENVIADO --> RECHAZADO: rechazo del riel
    ENVIADO --> DEVUELTO: devolución
    RETENIDO --> ENVIADO: aprobación manual
    RETENIDO --> RECHAZADO: rechazo manual
    ACREDITADO --> [*]
    RECHAZADO --> [*]
    DEVUELTO --> [*]
```

**Invariante:** un pago no puede pasar de `ACREDITADO` a `ENVIADO`; toda transición queda registrada.

---

## 9. Secuencia local TO-BE

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente
    participant NB as NovaBank
    participant AML as Riesgo/AML
    participant SPI as SPI
    participant CT as Contabilidad

    C->>NB: Solicita transferencia
    NB->>NB: Valida alias, límite y saldo
    NB->>AML: Evalúa screening y scoring
    AML-->>NB: Decisión
    alt Aprobado
        NB->>SPI: Envía orden
        SPI-->>NB: Confirma acreditación
        NB->>CT: Registra asiento
        NB-->>C: Notifica pago completado
    else Retenido o rechazado
        NB-->>C: Notifica estado y motivo
    end
```

---

## 10. Secuencia internacional TO-BE

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente
    participant NB as NovaBank
    participant VAL as Validador ISO 20022
    participant SW as SWIFT
    participant CO as Corresponsal
    participant BC as Banco beneficiario

    C->>NB: Solicita pago internacional
    NB->>NB: Valida IBAN/BIC/moneda y riesgo
    NB->>VAL: Genera y valida pacs.008
    VAL-->>NB: Resultado
    NB->>SW: Envía pacs.008
    SW->>CO: Entrega mensaje
    CO->>BC: Acredita/procesa
    BC-->>CO: Estado
    CO-->>SW: pacs.002
    SW-->>NB: pacs.002
    NB-->>C: Notifica estado
```

---

## 11. Estado de una alerta AML

```mermaid
stateDiagram-v2
    [*] --> NUEVA
    NUEVA --> ASIGNADA: prioridad y analista
    ASIGNADA --> EN_INVESTIGACION: inicio de análisis
    EN_INVESTIGACION --> PENDIENTE_INFO: falta evidencia
    PENDIENTE_INFO --> EN_INVESTIGACION: evidencia recibida
    EN_INVESTIGACION --> ESCALADA: sospecha
    EN_INVESTIGACION --> CERRADA: no sospecha
    ESCALADA --> ROS: se prepara reporte
    ROS --> CERRADA: reporte registrado
    CERRADA --> [*]
```

---

## 12. Notas de uso

- Los diagramas no reemplazan los BPMN; son vistas para comunicación.
- Si se edita un proceso, actualizar BPMN, Mermaid y `mapa-procesos.md`.
- Las etiquetas con acentos y signos de interrogación se muestran correctamente en UTF-8.
- Para exportar a PNG/SVG, usar la extensión Mermaid de VS Code o la vista de GitHub.
- No se declara que los diagramas hayan sido renderizados en una herramienta específica; la verificación visual es manual.

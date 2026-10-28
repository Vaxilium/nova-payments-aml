# Diagramas de sistema, datos y experiencia

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub
**Documento:** DIA-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-27

> Arquitectura conceptual y preliminar. No representa la arquitectura real de ninguna entidad. El detalle de implementación se define en Fase 3.

---

## 1. Contexto (C4 nivel 1)

```mermaid
flowchart LR
    Cliente[Cliente persona o empresa]
    Canal[Canal digital / API]
    NB[NovaBank<br/>Pagos + AML Hub]
    Core[Core bancario]
    SPI[SPI / BCP]
    SWIFT[SWIFT / Red internacional]
    Corresponsal[Banco corresponsal]
    SEPRELAD[SEPRELAD]
    Screening[Proveedor de screening]
    BI[Tableros y reporting]

    Cliente --> Canal
    Canal --> NB
    NB <--> Core
    NB <--> SPI
    NB <--> SWIFT
    SWIFT <--> Corresponsal
    NB --> SEPRELAD
    NB <--> Screening
    NB --> BI
```

**Fronteras:** NovaBank controla canal, orquestación, riesgo, contabilidad y reporting. SPI, SWIFT, corresponsal y proveedor de screening son externos.

---

## 2. Contenedores (C4 nivel 2)

```mermaid
flowchart TB
    subgraph Canales
        WEB[Home banking]
        APP[App móvil]
        API[API para empresas]
    end

    subgraph NovaBank
        GW[API Gateway / BFF]
        ORQ[Orquestador de Pagos]
        RIESGO[Motor de Riesgo y Scoring]
        SCREEN[Motor de Screening]
        CASOS[Case Management AML]
        MENSA[Mensajería ISO 20022 / SWIFT]
        COREINT[Adaptador Core]
        LEDGER[Libro Mayor]
        CONC[Motor de Conciliación]
        EVENTOS[Bus de Eventos]
        DATOS[Plataforma de Datos]
        OBS[Observabilidad]
        IAM[Identidad y Accesos]
    end

    subgraph Externos
        SPI[SPI / BCP]
        SWIFT[SWIFT]
        PROV[Proveedor de listas]
        CORR[Corresponsal]
    end

    WEB --> GW
    APP --> GW
    API --> GW
    GW --> ORQ
    ORQ --> RIESGO
    RIESGO --> SCREEN
    SCREEN --> PROV
    ORQ --> MENSA
    MENSA --> SWIFT
    SWIFT --> CORR
    ORQ --> COREINT
    COREINT --> CORE[(Core bancario)]
    ORQ --> LEDGER
    ORQ --> CONC
    CONC --> LEDGER
    ORQ --> EVENTOS
    EVENTOS --> DATOS
    EVENTOS --> CASOS
    CASOS --> DATOS
    ORQ --> SPI
    GW --> IAM
    ORQ --> OBS
    DATOS --> BI[Reporting]
```

**Notas:**
- El orquestador es el dueño de la máquina de estados del pago.
- El motor de riesgo decide; el screening aporta coincidencias.
- El case management es el sistema de registro de alertas y ROS.
- El bus de eventos alimenta datos, auditoría y tableros.

---

## 3. Componentes del orquestador

```mermaid
flowchart LR
    API[API de pagos] --> VAL[Validador de entrada]
    VAL --> LIM[Límites y reglas]
    LIM --> ROUTER[Router local/internacional]
    ROUTER --> STATE[Máquina de estados]
    STATE --> RISK[Cliente de riesgo]
    STATE --> MSG[Cliente de mensajería]
    STATE --> CORE[Cliente de core]
    STATE --> ACC[Cliente de contabilidad]
    STATE --> NOTIF[Notificador]
    STATE --> AUD[Auditoría]
    RISK --> DEC[Decisión]
    MSG --> ISO[ISO 20022]
    MSG --> SPI[SPI]
    CORE --> SALDO[Saldo y cuenta]
    ACC --> ASIENTO[Asiento]
    STATE --> OUTBOX[Outbox / eventos]
```

**Patrones:** outbox transaccional, idempotencia, saga para pasos distribuidos, reintentos con backoff y dead-letter queue.

---

## 4. Integraciones

| Integración | Dirección | Protocolo | Datos | Riesgo | Control |
|---|---|---|---|---|---|
| Canal → API Gateway | Entrada | HTTPS/JSON | Intención de pago | Suplantación | OAuth2, mTLS, rate limit |
| Orquestador → Core | Bidireccional | API | Cuenta, saldo, débito/crédito | Consistencia | Idempotencia, timeout, compensación |
| Orquestador → SPI | Bidireccional | Adaptador/ISO | Orden y estado | Indisponibilidad | Reintentos, conciliación |
| Orquestador → SWIFT | Bidireccional | ISO 20022 | pacs.008/pacs.002 | Rechazo | Validador, correlación |
| Orquestador → Screening | Salida | API | Persona/operación | Falso positivo | Listas versionadas, revisión |
| Orquestador → Ledger | Salida | API/evento | Asiento | Diferencia | Partida doble, conciliación |
| Case Management → UIF | Salida | Canal oficial simulado | ROS | Reserva | Control de acceso |
| Bus → Data Platform | Salida | Eventos | Métricas y casos | PII | Enmascaramiento |

---

## 5. Flujo de datos de un pago local

```mermaid
flowchart LR
    A[Intención de pago] --> B[Validación]
    B --> C[Resolución de alias]
    C --> D[Scoring]
    D --> E[Orden SPI]
    E --> F[Confirmación]
    F --> G[Asiento]
    G --> H[Evento de pago]
    H --> I[Notificación]
    H --> J[KPIs]
    H --> K[Auditoría]
```

**Datos mínimos:** `payment_id`, `idempotency_key`, `cliente_id`, `cuenta_origen`, `cuenta_destino`, `alias`, `monto`, `moneda`, `estado`, `motivo`, `timestamp`, `regla_version`, `score`, `uetr` (internacional).

---

## 6. Modelo entidad-relación preliminar

```mermaid
erDiagram
    CLIENTE ||--o{ CUENTA : posee
    CLIENTE ||--|| PERFIL_RIESGO : tiene
    CLIENTE ||--o{ DOCUMENTO_KYC : presenta
    CLIENTE ||--o{ BENEFICIARIO_FINAL : declara
    CLIENTE ||--o{ TRANSFERENCIA : origina
    CUENTA ||--o{ TRANSFERENCIA : debita
    TRANSFERENCIA ||--o{ EVENTO_PAGO : genera
    TRANSFERENCIA ||--o{ ASIENTO : contabiliza
    TRANSFERENCIA ||--o{ ALERTA : dispara
    ALERTA }o--|| CASO : agrupa
    CASO ||--o| ROS : culmina
    REGLA ||--o{ ALERTA : genera
    LISTA ||--o{ SCREENING : alimenta
    TRANSFERENCIA ||--o{ SCREENING : evalua

    CLIENTE {
        string cliente_id PK
        string tipo_cliente
        string nombre
        string pais_residencia
        string estado
        datetime alta
    }
    CUENTA {
        string cuenta_id PK
        string cliente_id FK
        string numero
        string moneda
        decimal saldo
        string estado
    }
    PERFIL_RIESGO {
        string perfil_id PK
        string cliente_id FK
        int score
        string nivel
        boolean es_pep
        boolean requiere_edd
        date proxima_revision
    }
    DOCUMENTO_KYC {
        string documento_id PK
        string cliente_id FK
        string tipo
        string estado
        date vencimiento
    }
    BENEFICIARIO_FINAL {
        string beneficiario_id PK
        string cliente_id FK
        string nombre
        decimal porcentaje
        string tipo_control
    }
    TRANSFERENCIA {
        string payment_id PK
        string cliente_id FK
        string cuenta_origen FK
        string cuenta_destino
        decimal monto
        string moneda
        string tipo
        string estado
        string idempotency_key
        string uetr
        datetime creada
    }
    EVENTO_PAGO {
        string evento_id PK
        string payment_id FK
        string tipo
        string estado_anterior
        string estado_nuevo
        datetime ocurrido
    }
    ASIENTO {
        string asiento_id PK
        string payment_id FK
        string cuenta_contable
        decimal debito
        decimal credito
        string moneda
        date fecha
    }
    ALERTA {
        string alerta_id PK
        string payment_id FK
        string regla_id FK
        string prioridad
        string estado
        decimal score
        datetime creada
    }
    CASO {
        string caso_id PK
        string alerta_id FK
        string analista_id
        string estado
        string decision
        datetime cierre
    }
    ROS {
        string ros_id PK
        string caso_id FK
        string estado
        date fecha_reporte
        string narrativa
    }
    REGLA {
        string regla_id PK
        string nombre
        string version
        boolean activa
        string tipo
    }
    LISTA {
        string lista_id PK
        string nombre
        string version
        date vigencia
    }
    SCREENING {
        string screening_id PK
        string payment_id FK
        string lista_id FK
        string resultado
        decimal coincidencia
        datetime evaluado
    }
```

> Modelo conceptual. El DDL, índices, constraints y tipos definitivos se definen en Fase 3.

---

## 7. Event storming

```mermaid
flowchart LR
    subgraph Comandos
        C1[Iniciar transferencia]
        C2[Evaluar riesgo]
        C3[Enviar pago]
        C4[Investigar alerta]
    end
    subgraph Eventos
        E1[PagoRecibido]
        E2[DatosValidados]
        E3[RiesgoEvaluado]
        E4[PagoEnviado]
        E5[PagoAcreditado]
        E6[AlertaCreada]
        E7[CasoEscalado]
        E8[ROSAprobado]
    end
    subgraph Politicas
        P1[Si riesgo alto, retener]
        P2[Si confirmado, contabilizar]
        P3[Si sospecha, escalar]
        P4[Si ROS aprobado, reportar]
    end
    C1 --> E1 --> E2
    E2 --> C2 --> E3
    E3 --> P1
    E3 --> C3 --> E4 --> E5
    E5 --> P2
    E3 --> E6 --> C4
    C4 --> E7 --> P3
    E7 --> E8 --> P4
```

---

## 8. Journey — pago local P2P

```mermaid
journey
    title Cliente persona — pago local
    section Iniciar
      Abre la app: 5: Cliente
      Elige beneficiario: 5: Cliente
      Ingresa importe y motivo: 4: Cliente
    section Confirmar
      Revisa alias y titular: 5: Cliente
      Confirma irrevocabilidad: 4: Cliente
    section Esperar
      Ve estado en tiempo real: 4: Cliente
      Recibe confirmación: 5: Cliente
    section Resolver
      Consulta comprobante: 5: Cliente
      Reclama si hay error: 2: Cliente
```

**Puntos de dolor:** confirmación de titular, claridad de irrevocabilidad y tiempos de respuesta.

---

## 9. Journey — pago internacional

```mermaid
journey
    title Cliente empresa — pago internacional
    section Preparar
      Selecciona beneficiario: 4: Cliente
      Ingresa IBAN/BIC: 3: Cliente
      Adjunta documentación: 3: Cliente
    section Validar
      Confirma moneda e importe: 4: Cliente
      Espera screening: 3: Cliente
    section Seguir
      Consulta estado: 4: Cliente
      Recibe comprobante: 5: Cliente
    section Resolver
      Atiende requerimiento EDD: 2: Cliente
      Consulta devolución: 2: Cliente
```

**Puntos de dolor:** errores de IBAN/BIC, solicitudes EDD y falta de visibilidad del estado.

---

## 10. Despliegue conceptual

```mermaid
flowchart TB
    subgraph Zona_DMZ
        WAF[WAF / API Gateway]
    end
    subgraph Zona_Aplicaciones
        ORQ[Orquestador]
        RIESGO[Motor de riesgo]
        CASOS[Case management]
        MENSA[Mensajería]
    end
    subgraph Zona_Datos
        DB[(Base transaccional)]
        LEDGER[(Libro mayor)]
        DWH[(Data warehouse)]
    end
    subgraph Zona_Externa
        SPI[SPI]
        SWIFT[SWIFT]
        PROV[Screening]
    end
    WAF --> ORQ
    ORQ --> RIESGO
    ORQ --> MENSA
    ORQ --> CASOS
    ORQ --> DB
    ORQ --> LEDGER
    ORQ --> DWH
    MENSA --> SPI
    MENSA --> SWIFT
    RIESGO --> PROV
```

**Zonas de seguridad:** DMZ para exposición, aplicaciones con mínimo privilegio, datos cifrados y externos con mTLS.

---

## 11. Decisiones de arquitectura preliminares

| ID | Decisión | Motivo | Consecuencia |
|---|---|---|---|
| ADR-01 | Orquestador con máquina de estados explícita. | Evitar estados ambiguos y duplicados. | Más complejidad inicial, mejor control. |
| ADR-02 | Idempotencia por `idempotency_key` y `payment_id`. | Reintentos seguros. | Requiere unicidad y retención. |
| ADR-03 | Outbox transaccional para eventos. | Consistencia entre pago y evento. | Necesita relay y monitoreo. |
| ADR-04 | Screening síncrono antes de liberar. | Control AML oportuno. | Latencia y dependencia del proveedor. |
| ADR-05 | Case management como sistema de registro AML. | Evidencia y auditoría. | Integración y gobierno de datos. |
| ADR-06 | Ledger separado del core para conciliación. | Trazabilidad contable. | Doble registro y conciliación. |
| ADR-07 | ISO 20022 como contrato canónico internacional. | Estándar y futuro. | Mapeo y validación. |
| ADR-08 | Bus de eventos para analítica y auditoría. | Desacoplar reporting. | Gobierno de esquemas. |

---

## 12. Atributos de calidad y controles

| Atributo | Escenario | Control |
|---|---|---|
| Disponibilidad | Caída de un nodo sin afectar pagos. | Réplicas, balanceo, health checks. |
| Rendimiento | p95 de scoring ≤ 2 s. | Caché, reglas optimizadas, índices. |
| Consistencia | No duplicar pagos. | Idempotencia y saga. |
| Auditabilidad | Reconstruir un pago. | Eventos correlacionados y retención. |
| Seguridad | Acceso no autorizado. | IAM, mTLS, cifrado, mínimo privilegio. |
| Observabilidad | Detectar falla en < 5 min. | Métricas, trazas, alertas. |
| Recuperación | Restablecer en RTO definido. | Backups, DR, pruebas. |
| Privacidad | Evitar PII innecesaria. | Minimización y enmascaramiento. |

---

## 13. Trazabilidad de diagramas

| Diagrama | Requerimientos | Procesos |
|---|---|---|
| Contexto | BR-01, BR-05, BR-07 | PR-01 a PR-06 |
| Contenedores | NFR-01 a NFR-10 | Transversal |
| Componentes | BR-15, NFR-02 | PR-02, PR-03 |
| ER | BR-10, BR-11, BR-12 | PR-01, PR-05, PR-06 |
| Event storming | BR-07, BR-08, BR-09 | PR-04, PR-05 |
| Journeys | BR-03, BR-16 | PR-02, PR-03 |
| Despliegue | NFR-01, NFR-03, NFR-07 | Transversal |

---

## 14. Referencias

- `mapa-procesos.md` — procesos y controles.
- `bpmn/` — modelos BPMN.
- `dmn/` — decisiones.
- `../01-negocio/BRD.md` — requerimientos y NFR.
- `../01-negocio/contexto-regulatorio.md` — restricciones.

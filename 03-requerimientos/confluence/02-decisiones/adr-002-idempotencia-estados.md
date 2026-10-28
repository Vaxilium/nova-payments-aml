# ADR-002 — Idempotencia y máquina de estados para pagos reintentables

**Estado:** Aceptada  
**Fecha:** 2026-10-20  
**Decisores:** TI — Arquitectura, Operaciones, Riesgos  
**Impacto:** Alto  
**Relacionado:** BR-03, BR-15, NFR-05, R-05

---

## 1. Contexto

Los pagos instantáneos y los envíos internacionales pueden sufrir timeouts, cortes de red o respuestas desconocidas. Si el cliente o el sistema reintenta sin control, se puede debitar dos veces, enviar dos mensajes o acreditar dos veces. El SPI es irreversible una vez aceptado y el corresponsal puede responder tarde.

La operación necesita una forma determinista de saber **qué pasó** y **qué hacer** ante un reintento, sin depender de la memoria del operador.

---

## 2. Decisión

Se adopta una **máquina de estados explícita** y una **clave de idempotencia** por operación.

### 2.1 Estados del pago local

```text
RECIBIDO → VALIDADO → ENVIADO → ACREDITADO
                    ↘ RECHAZADO
                    ↘ DEVUELTO
```

### 2.2 Estados del pago internacional

```text
RECIBIDO → VALIDADO → MENSAJE_GENERADO → ENVIADO → ACEPTADO_CORRESPONSAL → ACREDITADO
                                              ↘ RECHAZADO
                                              ↘ DEVUELTO
```

### 2.3 Reglas

1. Toda transición se registra con timestamp, actor, motivo y `correlation_id`.
2. Un estado final no se reabre; se crea un caso de excepción o una reversa.
3. La `Idempotency-Key` se persiste con el hash del payload, el `payment_id` y la respuesta.
4. Misma clave + mismo payload → misma respuesta; no se crea otro pago.
5. Misma clave + payload distinto → `409 IDEMPOTENCY_KEY_CONFLICT`.
6. La ventana mínima de retención de la clave es 24 h (parámetro configurable).
7. Los reintentos usan la misma clave y consultan el estado antes de reenviar.

---

## 3. Consecuencias

### Positivas

- Elimina duplicados por reintento y facilita la conciliación.
- Da una respuesta consistente al cliente y a operaciones.
- Permite auditoría y compensación con evidencia.
- Habilita pruebas deterministas de timeout y reintento.

### Negativas / deuda asumida

- Requiere almacenamiento de claves y respuestas.
- Obliga a definir compensaciones para estados inciertos.
- Aumenta la complejidad de los adaptadores y de las pruebas.
- La ventana de idempotencia debe coordinarse con la política de reintentos.

### Riesgos asociados

- R-05 (duplicidad), R-11 (diferencias de conciliación), R-17 (evidencia incompleta).

---

## 4. Alternativas evaluadas

| Alternativa | Por qué no se eligió |
|---|---|
| Reintento manual sin clave | Depende de la memoria del operador y no escala. |
| Bloquear el pago hasta tener respuesta | Aumenta la latencia y no resuelve timeouts. |
| Usar solo el ID del mensaje | No cubre la creación del pago ni la devolución. |
| Reversa automática ante cualquier timeout | Puede revertir un pago que sí se acreditó; genera nuevas diferencias. |

---

## 5. Criterios de aceptación

- Un reintento con la misma clave y payload devuelve la misma respuesta.
- Un reintento con payload distinto devuelve 409.
- No existe más de un pago o mensaje por clave.
- Toda transición de estado tiene evento de auditoría.
- La conciliación puede explicar cada estado final.

---

## 6. Referencias

- `../../historias-usuario.md` — US-003, US-009, US-039.
- `../../requerimientos-no-funcionales.md` — NFR-05, NFR-06.
- `../../../02-procesos/bpmn/transferencia-instantanea-to-be.bpmn`
- `../../../02-procesos/bpmn/transferencia-internacional-to-be.bpmn`
- `../../../01-negocio/riesgos.md` — R-05.

**Fin de la ADR.**

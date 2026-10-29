# Especificación de pantallas — NovaBank Payments & AML Hub

**Documento:** UX-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-29
**Autor:** Franco Tillería Centurión — Business Analyst
**Alcance:** aplicación de transferencias (cliente) y consola de cumplimiento (analista AML).

> Caso 100 % ficticio. Los textos, cuentas, importes y nombres son de ejemplo y no representan datos reales.
> Los wireframes de `wireframes/` son bocetos de baja fidelidad para recrear en Figma o Balsamiq; no son un diseño visual final.

---

## 1. Principios de diseño

1. **Una decisión por pantalla.** Cada paso pide lo mínimo para avanzar y muestra el contexto necesario.
2. **Estado siempre visible.** El usuario sabe dónde está, qué ocurrió y qué puede hacer a continuación.
3. **Errores accionables.** El mensaje explica el problema, el campo afectado y la corrección esperada.
4. **Riesgo sin fricción innecesaria.** Las validaciones AML no exponen reglas internas; se informa el estado y el plazo.
5. **Accesibilidad desde el boceto.** Contraste, foco visible, etiquetas persistentes y navegación por teclado se especifican antes de la construcción.
6. **Trazabilidad.** Las acciones del analista dejan rastro (analista, fecha, motivo) y no permiten estados terminales sin justificación.

## 2. Inventario y mapa de navegación

| ID | Pantalla | Audiencia | Tipo | Archivo de wireframe |
|---|---|---|---|---|
| APP-01 | Inicio | Cliente | Mobile web / responsive | `wireframes/APP-01-inicio.svg` |
| APP-02 | Nueva transferencia local | Cliente | Formulario por pasos | `wireframes/APP-02-transferencia-local.svg` |
| APP-03 | Nueva transferencia internacional | Cliente | Formulario por pasos | `wireframes/APP-03-transferencia-internacional.svg` |
| APP-04 | Confirmación | Cliente | Revisión y autorización | `wireframes/APP-04-confirmacion.svg` |
| APP-05 | Comprobante | Cliente | Resultado exitoso | `wireframes/APP-05-comprobante.svg` |
| APP-06 | Error | Cliente | Resultado no exitoso | `wireframes/APP-06-error.svg` |
| AML-01 | Bandeja de alertas | Analista | Desktop | `wireframes/AML-01-bandeja-alertas.svg` |
| AML-02 | Detalle de caso | Analista | Desktop | `wireframes/AML-02-detalle-caso.svg` |
| AML-03 | Historial del cliente | Analista | Desktop | `wireframes/AML-03-historial-cliente.svg` |
| AML-04 | Cierre del caso | Analista | Desktop (modal/página) | `wireframes/AML-04-cierre-caso.svg` |

Flujo completo en `flujo-prototipo.md` (Mermaid) y galería navegable en `wireframes/index.html`.

---

## 3. Reglas transversales

### 3.1 Formato y localización

- Idioma: español (Paraguay). Importes con separador de miles y decimales según moneda.
- PYG: sin decimales, prefijo `₲` y espacio fino. USD/EUR: dos decimales, código ISO visible (`USD`, `EUR`).
- Fechas: `dd/mm/aaaa`; horas: 24 h; zona horaria `America/Asuncion`.
- Identificadores visibles: `TX-...`, `ALT-...`, `CASE-...`. Nunca mostrar claves internas de base.
- Enmascarar datos sensibles: documento `••••1234`, cuenta `•••• •••• 5678`, nombre completo solo si el analista tiene permiso.

### 3.2 Validaciones comunes

| Regla | Mensaje | Momento |
|---|---|---|
| Campo obligatorio vacío | “Completá este campo para continuar.” | Al salir del campo y al enviar |
| Formato inválido | “El formato de {campo} no es válido. Ejemplo: {ejemplo}.” | Al salir del campo |
| Importe ≤ 0 | “El importe debe ser mayor que cero.” | Al salir del campo |
| Importe con más decimales de los permitidos | “Usá como máximo {n} decimales para {moneda}.” | Al salir del campo |
| Error de red | “No pudimos conectar. Revisá tu conexión e intentá de nuevo.” | Al enviar |
| Sesión expirada | “Tu sesión venció por seguridad. Volvé a ingresar.” | Al enviar |
| Operación en revisión AML | “Tu transferencia quedó en revisión. Te avisaremos cuando finalice.” | Al confirmar |
| Límite excedido | “El importe supera el límite de {importe} por operación.” | Al salir del campo |

### 3.3 Estados de interfaz

Toda pantalla que consulta o envía datos debe cubrir: `cargando` (skeleton o spinner con texto), `vacío` (explicación y acción), `error recuperable` (reintentar), `error no recuperable` (contacto), `éxito` y `sin permiso`.

### 3.4 Navegación y foco

- Orden de tabulación: encabezado → contenido → acción primaria → ayuda.
- El foco se mueve al primer campo con error al enviar.
- Los modales atrapan el foco, cierran con `Esc` y devuelven el foco al disparador.
- El botón primario nunca se deshabilita sin explicar el motivo; si se deshabilita, se muestra texto de ayuda.
- No usar solo color para comunicar estado: ícono + texto.

---

## 4. APP-01 — Inicio

**Objetivo:** dar acceso rápido al saldo, a las acciones de pago y al historial reciente, sin exponer datos innecesarios.

**Componentes**

1. Barra superior: logo NovaBank, saludo, ícono de notificaciones con contador, menú de perfil.
2. Tarjeta de saldo: saldo disponible, moneda, cuenta enmascarada, botón “Ver detalle”.
3. Acciones rápidas: “Transferir”, “Pagar servicio”, “Últimos movimientos”.
4. Aviso contextual: revisión AML pendiente, si existe.
5. Lista “Últimas operaciones” (máximo 5): tipo, contraparte, fecha, importe, estado.
6. Barra inferior (mobile): Inicio, Transferir, Movimientos, Perfil.

**Campos:** ninguno editable.

**Validaciones:** ninguna; la sesión debe estar activa.

**Estados**

- `cargando`: skeleton en saldo y lista.
- `vacío`: “Todavía no tenés movimientos. Hacé tu primera transferencia.”
- `error`: tarjeta con “No pudimos cargar tu saldo” + botón “Reintentar”.
- `revisión AML`: banner informativo “Tenés una operación en revisión. Plazo estimado: 1 día hábil.”

**Textos clave**

- Título: “Hola, {nombre}”.
- Saldo: “Disponible”.
- Acción primaria: “Transferir”.
- Botón secundario: “Ver todos los movimientos”.

**Navegación:** “Transferir” → APP-02; “Transferencia internacional” (desde menú de acciones) → APP-03; operación → APP-05 si está completada, o estado de revisión; “Perfil” → menú de cuenta.

---

## 5. APP-02 — Nueva transferencia local

**Objetivo:** iniciar una transferencia instantánea en guaraníes a otra cuenta NovaBank o a un alias.

**Componentes**

1. Encabezado con “Volver” y título “Nueva transferencia”.
2. Selector de tipo: “Local (SPI)” seleccionado; enlace “Transferencia internacional”.
3. Formulario: cuenta origen, destinatario (alias o cuenta), nombre del destinatario (solo lectura si el alias resuelve), importe, motivo/concepto, switch “Guardar destinatario”.
4. Panel de ayuda: tope por operación, disponibilidad 24/7, tiempo objetivo.
5. Barra fija inferior: resumen del importe y botón “Continuar”.

**Campos**

| Campo | Tipo | Obligatorio | Validación |
|---|---|---|---|
| Cuenta origen | Selector | Sí | Debe estar `ACTIVE`, con saldo suficiente y moneda PYG |
| Destinatario | Texto con búsqueda | Sí | Alias `nombre.apellido` o cuenta numérica de 14 dígitos; no puede ser la misma cuenta |
| Nombre destinatario | Texto de solo lectura | — | Se completa al resolver el alias/cuenta |
| Importe | Moneda | Sí | > 0; ≤ saldo disponible; ≤ ₲10.000.000 por operación; sin decimales |
| Concepto | Selector + texto libre | Sí | Máximo 80 caracteres; catálogo permitido |
| Guardar destinatario | Checkbox | No | Solo si el destinatario es válido |

**Validaciones específicas**

- Alias inexistente: “No encontramos ese alias. Verificá el dato o ingresá la cuenta.”
- Cuenta destino bloqueada: “La cuenta de destino no está disponible para recibir transferencias.”
- Saldo insuficiente: “Tu saldo disponible es ₲{saldo}. Ingresá un importe menor.”
- Tope: “El límite por operación es ₲10.000.000.”
- Misma cuenta: “Elegí una cuenta de destino diferente.”

**Estados**

- `cargando` al resolver destinatario (spinner dentro del campo).
- `destinatario válido` con nombre y banco.
- `destinatario inválido` con borde y mensaje de error.
- `formulario incompleto` con botón “Continuar” deshabilitado y texto “Completá los datos para continuar.”
- `sin cuentas activas`: “No tenés cuentas disponibles para transferir.”

**Textos clave**

- Título: “Nueva transferencia local”.
- Ayuda: “Las transferencias locales se acreditan en segundos, todos los días.”
- CTA: “Continuar”.

**Navegación:** “Volver” → APP-01; “Continuar” con datos válidos → APP-04; enlace internacional → APP-03. No se envía nada en esta pantalla.

---

## 6. APP-03 — Nueva transferencia internacional

**Objetivo:** capturar una transferencia saliente en USD o EUR con datos SWIFT/ISO 20022 suficientes para validar y enviar.

**Componentes**

1. Encabezado “Nueva transferencia internacional” con “Volver”.
2. Aviso: “Las transferencias internacionales pueden demorar hasta 2 días hábiles.”
3. Formulario en dos bloques: origen y destino; importe y propósito; datos del beneficiario.
4. Panel de costos: comisión estimada, moneda, tipo de cambio referencial y total a debitar.
5. Barra inferior: total estimado y botón “Continuar”.

**Campos**

| Campo | Tipo | Obligatorio | Validación |
|---|---|---|---|
| Cuenta origen | Selector | Sí | `ACTIVE`; moneda USD/EUR; saldo suficiente para importe + comisión |
| País del beneficiario | Selector | Sí | Código ISO 3166-1 alfa-3 de la lista permitida |
| BIC/SWIFT | Texto | Sí | 8 u 11 caracteres, formato `[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?` |
| IBAN / cuenta | Texto | Sí | Formato del país; checksum cuando aplique |
| Nombre del beneficiario | Texto | Sí | 2–70 caracteres; sin caracteres de control |
| Dirección del beneficiario | Texto | Sí | 5–140 caracteres |
| Importe | Moneda | Sí | > 0; ≤ saldo − comisión; dos decimales |
| Moneda | Selector | Sí | USD o EUR (según cuenta y corresponsalía) |
| Propósito | Selector | Sí | Catálogo ISO/SWIFT simplificado |
| Referencia | Texto | No | Máximo 35 caracteres; no incluir datos sensibles |
| Aceptar costos | Checkbox | Sí | Debe marcarse para continuar |

**Validaciones específicas**

- BIC inválido: “El BIC debe tener 8 u 11 caracteres. Ejemplo: NVBKPYPA.”
- IBAN inválido: “El IBAN no supera la validación de formato y dígito de control.”
- Moneda no soportada: “Operamos transferencias internacionales en USD y EUR.”
- Saldo insuficiente para comisión: “Necesitás USD {importe+comisión} para cubrir la transferencia y la comisión.”
- País restringido: “Por ahora no podemos enviar transferencias a este país.”
- Sanción/PEP en beneficiario: mensaje neutro “La operación requiere una verificación adicional. Podés continuar; el área de Cumplimiento la revisará.”

**Estados**

- `cargando` catálogo de países y tipos de cambio.
- `tipo de cambio no disponible`: “No pudimos obtener el tipo de cambio. Reintentá en unos minutos.”
- `validación AML`: banner “Verificación adicional en curso”.
- `formulario válido` con resumen de costos.

**Textos clave**

- Comisión: “Comisión estimada: USD 25,00”.
- Total: “Total a debitar: USD {importe + comisión}”.
- CTA: “Continuar”.

**Navegación:** “Volver” → APP-01 o APP-02; “Continuar” → APP-04. Si el país es restringido, se bloquea el avance y se ofrece “Cancelar”.

---

## 7. APP-04 — Confirmación

**Objetivo:** permitir que el cliente revise todos los datos y autorice la operación antes de enviarla.

**Componentes**

1. Encabezado “Confirmá tu transferencia”.
2. Tarjeta resumen: tipo (local/internacional), cuenta origen, destinatario, importe, comisión, total, fecha estimada.
3. Bloque de advertencia AML si aplica.
4. Método de autorización: biometría, PIN o token (según canal).
5. Enlaces “Editar datos” y “Cancelar”.
6. Botón primario “Confirmar transferencia”; estado de procesamiento bloquea doble envío.

**Campos**

| Campo | Tipo | Obligatorio | Validación |
|---|---|---|---|
| Código de autorización | PIN/token | Sí | 6–8 dígitos; intentos limitados |
| Aceptar términos | Checkbox | Solo primera operación | Debe estar marcado |

**Validaciones específicas**

- PIN incorrecto: “El código no es correcto. Te quedan {n} intentos.”
- Operación duplicada: “Ya estamos procesando esta transferencia. No la envíes de nuevo.”
- Sesión expirada: “Tu sesión venció. Volvé a iniciar sesión para confirmar.”
- Timeout del riel: no mostrar error definitivo; pasar a estado “Procesando” y luego a APP-06 con reintento seguro.

**Estados**

- `listo para confirmar`.
- `autorizando`: botón con spinner y texto “Confirmando…”; se bloquean campos y navegación.
- `éxito`: transición a APP-05.
- `en revisión`: pantalla de estado con número de operación y plazo.
- `rechazo AML`: APP-06 con motivo genérico y canal de contacto.
- `error técnico`: APP-06 con opción “Reintentar de forma segura”.

**Textos clave**

- Título: “Revisá y confirmá”.
- Aviso: “Una vez confirmada, la operación no se puede cancelar.”
- CTA: “Confirmar transferencia”.
- Estado: “Estamos procesando tu transferencia. No cierres esta pantalla.”

**Navegación:** “Editar” → APP-02/APP-03 conservando datos; “Cancelar” → APP-01 con confirmación; éxito → APP-05; fallo → APP-06.

---

## 8. APP-05 — Comprobante

**Objetivo:** confirmar el resultado exitoso y entregar un comprobante verificable.

**Componentes**

1. Ícono y título “Transferencia realizada”.
2. Importe destacado y estado “Acreditada” o “Enviada”.
3. Datos: número de operación, fecha/hora, cuenta origen, destinatario, concepto, comisión, total.
4. Línea de tiempo: Recibida → Validada → Enviada → Acreditada.
5. Acciones: “Descargar comprobante” (PDF), “Compartir”, “Hacer otra transferencia”, “Volver al inicio”.

**Campos:** ninguno editable.

**Validaciones:** ninguna.

**Estados**

- `acreditada`: mensaje “El dinero ya está disponible para el destinatario.”
- `enviada`: “La transferencia fue enviada. La acreditación puede demorar hasta 2 días hábiles.”
- `comprobante no disponible`: “Estamos generando el comprobante. Reintentá en unos segundos.”
- `sin conexión al descargar`: “No pudimos descargar el PDF. Revisá tu conexión.”

**Textos clave**

- Título: “Transferencia realizada”.
- Número: “Comprobante N.º {id}”.
- Ayuda: “Guardá este comprobante para tus registros.”

**Navegación:** “Hacer otra transferencia” → APP-02; “Volver al inicio” → APP-01; “Ver estado” → detalle de operación (fuera de alcance de este prototipo).

---

## 9. APP-06 — Error

**Objetivo:** explicar un resultado no exitoso, evitar reintentos inseguros y ofrecer una salida clara.

**Componentes**

1. Ícono de estado y título según causa.
2. Mensaje principal en lenguaje simple.
3. Código de referencia y número de operación (si existe).
4. Acciones: “Reintentar”, “Volver al inicio”, “Contactar soporte”.
5. Bloque de ayuda con horarios y canales.

**Campos:** ninguno.

**Validaciones:** ninguna; el botón “Reintentar” solo aparece si la operación es reintentable.

**Estados y variantes**

| Variante | Título | Mensaje | Acción |
|---|---|---|---|
| Validación | “Revisá los datos” | “El alias o la cuenta no son válidos.” | “Corregir datos” |
| Saldo | “Saldo insuficiente” | “Tu saldo no alcanza para cubrir el importe y la comisión.” | “Cambiar importe” |
| Riel no disponible | “El servicio no está disponible” | “No pudimos enviar la transferencia. No se debitó tu cuenta.” | “Reintentar” |
| Timeout | “Estamos verificando tu operación” | “No sabemos aún si la transferencia se completó. No la repitas.” | “Ver estado” |
| AML | “Operación no autorizada” | “La operación no pudo completarse. Contactá a tu oficial de cuenta.” | “Contactar soporte” |
| Técnico | “Algo salió mal” | “Estamos trabajando para resolverlo. Tu dinero está seguro.” | “Volver al inicio” |

**Textos clave**

- Código: “Referencia: {código}”.
- Soporte: “Atención al cliente: 24/7 desde la app.”

**Navegación:** “Reintentar” → APP-04 solo si es seguro; “Corregir” → APP-02/APP-03; “Ver estado” → detalle; “Volver” → APP-01.

---

## 10. AML-01 — Bandeja de alertas

**Objetivo:** priorizar el trabajo del analista y permitir triage rápido de alertas por riesgo, SLA y estado.

**Componentes**

1. Barra superior: búsqueda global, nombre del analista, cambio de rol, notificaciones.
2. Navegación lateral: Bandeja, Casos, Clientes, Reglas, Reportes.
3. Filtros: prioridad, estado, regla, segmento, riesgo KYC, rango de fechas, “solo vencidas”.
4. Contadores: nuevas, P1, vencidas, en análisis.
5. Tabla de alertas: prioridad, alerta, cliente, regla, score, estado, asignada a, vence, acciones.
6. Selección múltiple y acciones masivas limitadas (asignar, cambiar prioridad) con confirmación.
7. Paginación y contador de resultados.
8. Estado vacío con explicación.

**Campos**

| Campo | Tipo | Validación |
|---|---|---|
| Búsqueda | Texto | Mínimo 3 caracteres; busca por ID, cliente o regla |
| Prioridad | Multiselect | P1/P2/P3 |
| Estado | Multiselect | Estados de alerta |
| Regla | Selector | R01–R12 |
| Rango de fechas | Date range | Desde ≤ hasta; máximo 12 meses |
| Solo vencidas | Checkbox | `due_at < ahora` |

**Validaciones específicas**

- Rango inválido: “La fecha desde no puede ser posterior a la fecha hasta.”
- Sin resultados: “No hay alertas con estos filtros. Probá ampliar el rango.”
- Error de carga: “No pudimos cargar la bandeja. Reintentar.”
- Acción masiva sin selección: “Seleccioná al menos una alerta.”

**Estados**

- `cargando` con skeleton de filas.
- `vacío` con CTA “Limpiar filtros”.
- `error` con reintento.
- `selección activa` con barra de acciones y contador.
- `alerta vencida` resaltada con etiqueta “SLA vencido”.

**Textos clave**

- Título: “Bandeja de alertas”.
- Contador: “{n} alertas · {p1} P1 · {vencidas} vencidas”.
- Acción: “Abrir caso”.

**Navegación:** fila → AML-02; cliente → AML-03; filtros se reflejan en la URL (compartible); “Casos” → lista filtrada de casos.

---

## 11. AML-02 — Detalle de caso

**Objetivo:** reunir evidencia, alertas, operaciones y decisiones para investigar un caso sin cambiar de pantalla.

**Componentes**

1. Encabezado del caso: ID, título, estado, prioridad, score, SLA y analista asignado.
2. Acciones: “Asignarme”, “Escalar”, “Cerrar caso”, “Generar ROS” (solo si cumple condiciones).
3. Resumen del cliente: nombre enmascarado, segmento, país, riesgo KYC, PEP, EDD.
4. Pestañas: Alertas, Operaciones, KYC y perfil, Historial, Documentos.
5. Lista de alertas vinculadas con regla, score, fecha y estado.
6. Tabla de operaciones con fecha, tipo, importe, contraparte y canal.
7. Panel de notas de investigación con autor y fecha; las notas son inmutables salvo adenda.
8. Línea de tiempo de transiciones.
9. Panel de decisión con motivo obligatorio y checklist de cierre.

**Campos**

| Campo | Tipo | Obligatorio | Validación |
|---|---|---|---|
| Nota de investigación | Texto largo | No | 10–2.000 caracteres; sin datos sensibles innecesarios |
| Decisión | Selector | Sí al cerrar | Falso positivo / Escalar / Reportar |
| Motivo | Texto | Sí al cerrar | 20–1.000 caracteres |
| Checklist | Checkboxes | Sí al cerrar | Todas obligatorias según decisión |
| ROS | Texto/adjunto | Si reporta | Narrativa mínima y operaciones incluidas |

**Validaciones específicas**

- Cierre sin motivo: “El motivo es obligatorio para cerrar el caso.”
- Cierre con alertas sin revisar: “Quedan {n} alertas sin revisar. Confirmá que querés cerrar igual.”
- Escalar sin analista: “Asigná el caso antes de escalarlo.”
- ROS sin operaciones: “Seleccioná al menos una operación para el reporte.”
- Conflicto de versión: “Otra persona actualizó el caso. Recargá para ver los cambios.”

**Estados**

- `ABIERTO`, `EN_ANALISIS`, `ESCALADO`, `CERRADO`, `REPORTADO`.
- `solo lectura` cuando el caso está cerrado o el usuario no es el asignado.
- `cargando`, `error`, `sin alertas vinculadas`.
- `SLA vencido` visible en el encabezado.

**Textos clave**

- Título: “Caso {case_id} · {título}”.
- SLA: “Vence en {tiempo} · {fecha}”.
- CTA: “Cerrar caso”.
- Aviso: “Las acciones quedan registradas en la auditoría.”

**Navegación:** pestañas internas; cliente → AML-03; “Cerrar caso” → AML-04; “Generar ROS” → editor de ROS; “Volver” → AML-01.

---

## 12. AML-03 — Historial del cliente

**Objetivo:** dar contexto longitudinal del cliente para decidir si el patrón es inusual o esperado.

**Componentes**

1. Encabezado con nombre enmascarado, ID, segmento, país, estado KYC y riesgo.
2. Tarjetas: score KYC, operaciones 90 días, alertas abiertas, casos cerrados, PEP/EDD.
3. Filtros de período y tipo de operación.
4. Gráfico de volumen mensual y gráfico de alertas por regla (placeholder en wireframe).
5. Tabla de operaciones con contraparte, canal, importe y estado.
6. Lista de alertas y casos previos con enlaces.
7. Notas de KYC y última revisión.
8. Acciones: “Abrir caso”, “Exportar historial” (con registro de auditoría).

**Campos**

| Campo | Tipo | Validación |
|---|---|---|
| Período | Selector | Máximo 24 meses |
| Tipo | Multiselect | Depósito, retiro, transferencia, comisión, FX |
| Moneda | Selector | PYG, USD |
| Buscar contraparte | Texto | Mínimo 3 caracteres |

**Validaciones específicas**

- Período inválido: “El período máximo es de 24 meses.”
- Cliente sin operaciones: “El cliente no registra operaciones en el período.”
- Sin permiso: “No tenés permiso para ver el historial completo de este cliente.”

**Estados**

- `cargando`, `vacío`, `error`, `solo lectura`.
- `cliente PEP` con etiqueta visible y aviso de EDD.

**Textos clave**

- Título: “Historial del cliente”.
- Ayuda: “Los datos personales se muestran enmascarados según tu rol.”
- Exportar: “La exportación queda registrada en la auditoría.”

**Navegación:** operación → detalle de operación; alerta → AML-02; caso → AML-02; “Volver” → AML-01 o AML-02.

---

## 13. AML-04 — Cierre del caso

**Objetivo:** registrar una decisión de cierre consistente, auditables y con la evidencia mínima requerida.

**Componentes**

1. Modal o página de dos columnas: resumen del caso y formulario de cierre.
2. Resumen: cliente, alertas, operaciones, score, analista, SLA.
3. Selector de decisión: “Falso positivo”, “Escalar a caso”, “Reportar ROS”.
4. Motivo obligatorio con contador de caracteres y plantillas de texto.
5. Checklist dinámico según decisión.
6. Adjuntos opcionales (máximo 5, PDF/PNG, 10 MB cada uno).
7. Aviso de irreversibilidad y de auditoría.
8. Botones “Cancelar” y “Confirmar cierre”.

**Campos**

| Campo | Tipo | Obligatorio | Validación |
|---|---|---|---|
| Decisión | Radio | Sí | Una opción |
| Motivo | Texto largo | Sí | 20–1.000 caracteres |
| Checklist | Checkboxes | Sí | Todas las requeridas |
| Analista responsable | Solo lectura | — | Usuario autenticado |
| ROS | Texto/adjunto | Si “Reportar” | Narrativa y operaciones |
| Adjuntos | Archivos | No | Tipo y tamaño permitidos |

**Validaciones específicas**

- Confirmación sin checklist: “Completá el checklist antes de confirmar.”
- Decisión “Reportar” sin ROS: “El ROS es obligatorio para reportar.”
- Error de guardado: “No pudimos guardar el cierre. No se aplicó ningún cambio.”
- Conflicto: “El caso cambió mientras lo revisabas. Recargá y volvé a intentar.”

**Estados**

- `formulario inicial`.
- `validando`.
- `guardando`: botones bloqueados, texto “Guardando cierre…”.
- `cerrado`: confirmación con ID de transición y enlace al caso.
- `error recuperable` conserva los datos ingresados.
- `sin permiso`: el formulario no se muestra.

**Textos clave**

- Título: “Cerrar caso {id}”.
- Aviso: “El cierre es definitivo y queda registrado con tu usuario, fecha y motivo.”
- CTA: “Confirmar cierre”.

**Navegación:** “Cancelar” → AML-02 sin cambios; éxito → AML-02 en estado cerrado con banner “Caso cerrado”; error → permanece con datos.

---

## 14. Contenido de los wireframes

Cada SVG incluye:

- Nombre de la pantalla y audiencia.
- Zonas de navegación y contenido.
- Campos con etiquetas y placeholders.
- Mensajes de validación o estados representativos.
- Acciones primaria y secundaria.
- Nota de alcance: “Boceto de baja fidelidad”.

Los textos largos se representan con líneas de marcador para no confundir el wireframe con el copy final. El copy definitivo es el de este documento.

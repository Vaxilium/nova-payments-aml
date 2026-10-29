# Checklist de accesibilidad — NovaBank Payments & AML Hub

**Documento:** UX-NB-004
**Versión:** 1.0
**Fecha:** 2026-10-29
**Referencia de trabajo:** WCAG 2.2, niveles A y AA.

> Esta checklist es una guía de diseño y verificación del caso ficticio. No constituye una certificación de accesibilidad ni una auditoría formal.

---

## 1. Cómo usar la checklist

- Marcar cada criterio por pantalla y por componente.
- Un criterio no se considera cumplido si solo se verificó visualmente.
- Registrar la evidencia (captura, prueba de teclado, resultado de herramienta) en `docs/EVIDENCIAS.md`.
- Los criterios marcados `N/A` requieren justificación.

## 2. Checklist transversal

### 2.1 Estructura y semántica

- [ ] La página tiene un `h1` único y la jerarquía de encabezados no salta niveles.
- [ ] Las regiones principales usan `header`, `nav`, `main`, `aside`, `footer`.
- [ ] Las tablas tienen `caption`, `th` con `scope` y no se usan para maquetar.
- [ ] Los formularios agrupan campos relacionados con `fieldset` y `legend`.
- [ ] Los enlaces tienen texto descriptivo; no se usa “clic aquí” ni “más”.
- [ ] El idioma del documento está declarado (`lang="es-PY"`).
- [ ] Los títulos de página son únicos y describen la tarea.

### 2.2 Teclado y foco

- [ ] Todo elemento interactivo es alcanzable con `Tab` y operable con `Enter`/`Espacio`.
- [ ] El orden de foco sigue el orden visual y lógico.
- [ ] El foco es visible en todos los componentes (contraste ≥ 3:1).
- [ ] No hay trampas de foco; los modales se pueden cerrar con `Esc`.
- [ ] Al abrir un modal, el foco se mueve al primer elemento y vuelve al disparador al cerrar.
- [ ] Los enlaces “saltar al contenido” están disponibles en desktop y mobile.
- [ ] Las acciones destructivas requieren confirmación y no se activan por foco accidental.

### 2.3 Formularios

- [ ] Cada campo tiene etiqueta persistente asociada con `for`/`id`.
- [ ] Los campos obligatorios se indican en texto, no solo con asterisco o color.
- [ ] Los errores se anuncian y se vinculan con el campo mediante `aria-describedby`.
- [ ] El foco se mueve al primer error al enviar.
- [ ] Los mensajes de error explican cómo corregir.
- [ ] Los campos de importe usan `inputmode="decimal"` y aceptan separadores locales.
- [ ] No se borra lo ingresado ante un error recuperable.
- [ ] El autocompletado usa tokens válidos cuando aplica (`name`, `tel`, `email`, `one-time-code`).

### 2.4 Color y contraste

- [ ] Texto normal ≥ 4,5:1; texto grande ≥ 3:1.
- [ ] Componentes de interfaz y bordes de foco ≥ 3:1.
- [ ] El estado no depende solo del color: hay texto e ícono.
- [ ] Los gráficos tienen etiquetas o tabla alternativa.
- [ ] Los enlaces se distinguen del texto por algo más que el color (subrayado o peso).

### 2.5 Contenido y lenguaje

- [ ] El lenguaje es claro y evita abreviaturas no explicadas.
- [ ] Los mensajes de AML no estigmatizan ni revelan reglas internas.
- [ ] Las fechas, importes y monedas se leen correctamente con lector de pantalla.
- [ ] Los textos alternativos describen la función de la imagen, no “imagen”.
- [ ] Los íconos decorativos usan `aria-hidden="true"`.

### 2.6 Movimiento y tiempo

- [ ] Se respeta `prefers-reduced-motion`.
- [ ] No hay contenido que parpadee más de tres veces por segundo.
- [ ] Las sesiones con expiración avisan antes de cerrar y permiten extenderla.
- [ ] Los mensajes temporales (toasts) se pueden leer o repetir; no desaparecen antes de 5 s.
- [ ] Los contadores de SLA no actualizan el foco ni interrumpen la lectura.

### 2.7 Tablas y datos

- [ ] Las tablas largas permiten navegación por teclado y encabezados sticky.
- [ ] Los importes se alinean a la derecha con cifras tabulares.
- [ ] Los estados tienen texto, no solo un punto de color.
- [ ] La paginación anuncia el rango y el total.
- [ ] Las acciones masivas indican cuántos elementos se seleccionaron.
- [ ] Los gráficos tienen resumen textual y datos descargables.

### 2.8 Responsive y zoom

- [ ] El contenido funciona a 320 px de ancho sin scroll horizontal.
- [ ] Con zoom al 200 % no se pierde contenido ni funcionalidad.
- [ ] Los objetivos táctiles miden al menos 24 × 24 px (recomendado 44 × 44 px).
- [ ] El texto se puede ampliar sin romper el layout.
- [ ] Las tablas se adaptan a tarjetas o scroll con encabezado visible.

## 3. Checklist por pantalla

| Pantalla | Teclado | Foco | Errores | Contraste | Lector | Responsive | Evidencia |
|---|---|---|---|---|---|---|---|
| APP-01 Inicio | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| APP-02 Local | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| APP-03 Internacional | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| APP-04 Confirmación | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| APP-05 Comprobante | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| APP-06 Error | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| AML-01 Bandeja | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| AML-02 Detalle | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| AML-03 Historial | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |
| AML-04 Cierre | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | _pendiente_ |

## 4. Pruebas mínimas antes de publicar el prototipo

1. Recorrer cada flujo completo solo con teclado.
2. Verificar el orden y la visibilidad del foco en Figma/Balsamiq y en el HTML de wireframes.
3. Probar con un lector de pantalla (NVDA en Windows o VoiceOver en macOS).
4. Simular daltonismo y verificar que los estados se entiendan sin color.
5. Probar zoom al 200 % y ancho de 320 px.
6. Revisar contraste con una herramienta y registrar los valores.
7. Verificar que los mensajes de error no dependan de un `toast` efímero.
8. Documentar hallazgos y correcciones en `docs/EVIDENCIAS.md`.

## 5. Criterios de aceptación de accesibilidad

- Ningún flujo crítico queda bloqueado por teclado.
- Todos los campos tienen etiqueta y mensaje de error asociado.
- El contraste de texto cumple AA en las pantallas principales.
- Los estados de alerta y SLA se entienden sin distinguir color.
- El prototipo es usable a 320 px y con zoom al 200 %.
- Las pruebas manuales quedan registradas con fecha y responsable.

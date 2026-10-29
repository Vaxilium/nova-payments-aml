# 04 — Diseño UX

Propósito: especificar la experiencia de usuario de los flujos críticos del producto.

## Contenido

| Archivo | Descripción |
|---|---|
| `especificacion-pantallas.md` | Especificación funcional de 10 pantallas: objetivo, componentes, campos, validaciones, estados, textos y navegación. |
| `flujo-prototipo.md` | Flujo Mermaid de la app y de la consola AML, matriz de navegación y componentes reutilizables. |
| `guia-estilo.md` | Paleta, tipografía, espaciado y componentes base propuestos. |
| `accesibilidad.md` | Checklist WCAG 2.2 A/AA aplicada al caso y por pantalla. |
| `wireframes/` | Diez wireframes SVG de baja fidelidad y galería HTML. |

## Wireframes

Abrir [`wireframes/index.html`](wireframes/index.html) o cada SVG individual:

- App cliente: `APP-01-inicio.svg`, `APP-02-transferencia-local.svg`, `APP-03-transferencia-internacional.svg`, `APP-04-confirmacion.svg`, `APP-05-comprobante.svg`, `APP-06-error.svg`.
- Consola AML: `AML-01-bandeja-alertas.svg`, `AML-02-detalle-caso.svg`, `AML-03-historial-cliente.svg`, `AML-04-cierre-caso.svg`.

Los SVG se regeneran con:

```powershell
.\.venv\Scripts\python.exe 04-diseno-ux\wireframes\generar_wireframes.py
```

## Estado

Fase 6: especificación, flujo, estilo, accesibilidad y wireframes creados. La recreación en Figma/Balsamiq y las capturas quedan como evidencia manual **EV-006** en `docs/EVIDENCIAS.md`.

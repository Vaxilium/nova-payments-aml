# Wireframes de baja fidelidad

Cada SVG representa una pantalla del caso NovaBank. Son bocetos para recrear en Figma o Balsamiq, no un diseño visual final.

| Archivo | Pantalla | Lienzo |
|---|---|---|
| `APP-01-inicio.svg` | Inicio | 390 × 844 |
| `APP-02-transferencia-local.svg` | Nueva transferencia local | 390 × 844 |
| `APP-03-transferencia-internacional.svg` | Nueva transferencia internacional | 390 × 844 |
| `APP-04-confirmacion.svg` | Confirmación | 390 × 844 |
| `APP-05-comprobante.svg` | Comprobante | 390 × 844 |
| `APP-06-error.svg` | Error | 390 × 844 |
| `AML-01-bandeja-alertas.svg` | Bandeja de alertas | 1440 × 900 |
| `AML-02-detalle-caso.svg` | Detalle de caso | 1440 × 900 |
| `AML-03-historial-cliente.svg` | Historial del cliente | 1440 × 900 |
| `AML-04-cierre-caso.svg` | Cierre del caso | 1440 × 900 |

## Uso

1. Abrir `index.html` en un navegador para ver la galería.
2. Abrir un SVG directamente para inspeccionarlo o exportarlo.
3. Recrear en Figma/Balsamiq usando los IDs y la especificación de `../especificacion-pantallas.md`.
4. No agregar datos reales ni presentar estos bocetos como capturas de una herramienta operada.

Regenerar:

```powershell
.\.venv\Scripts\python.exe 04-diseno-ux\wireframes\generar_wireframes.py
```

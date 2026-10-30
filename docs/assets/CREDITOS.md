# Créditos y autoría de los activos visuales

Todos los activos de `docs/assets/` fueron creados para este portafolio y se
generan con código propio. No se usaron fotos, ilustraciones ni imágenes
generadas por modelos de IA.

## Autoría

- **Autor del caso y del código:** Franco Tillería Centurión.
- **Marca NovaBank:** identidad ficticia creada para el caso. No representa a
  ninguna entidad financiera real.
- **Datos:** sintéticos y reproducibles con semilla fija. No contienen PII ni
  información de empleadores reales.

## Cómo se generan

| Activo | Script | Tecnología |
|---|---|---|
| Marca, isotipo, favicon | `scripts/brand.py` | SVG generado por código |
| Banners y social preview | `scripts/covers.py` | HTML/CSS + Playwright |
| Gráficos | `scripts/charts.py` | Matplotlib |
| Arquitectura y secuencias | `scripts/diagrams.py` | Mermaid + Playwright |
| BPMN | `scripts/diagrams.py` | BPMN 2.0 + bpmn-js |
| Dashboard | `scripts/dashboard.py` | HTML/CSS + Playwright |
| Wireframes | `scripts/ux.py` | SVG propios + Playwright |
| Demo GIF | `scripts/demo.py` | SQLite temporal + Playwright + Pillow |
| Carrusel LinkedIn | `scripts/carousel.py` | HTML/CSS + Playwright + img2pdf |

Comando único:

```powershell
python -m scripts.make_assets --all
```

Las dependencias Python están en `requirements-assets.txt`. Mermaid y bpmn-js se
instalan con npm en una carpeta temporal o local; no se versionan en el
repositorio. Chromium se instala con `python -m playwright install chromium`.

## Fuentes y límites

- No se descargaron imágenes de terceros.
- Los diagramas Mermaid y BPMN son artefactos propios; su render es una preview,
  no una captura de Bizagi, Camunda, Signavio, Lucidchart, Visio o Miro.
- El dashboard es una visualización HTML; no es un archivo `.pbix` de Power BI ni
  un workbook de Tableau.
- Las capturas de wireframes son PNG de los SVG del repositorio; no son capturas
  de Balsamiq o Figma.
- Las referencias a BCP, SWIFT, GAFI, SEPRELAD e ISO 20022 son contexto público,
  no una afiliación ni un respaldo.

## Licencia

El arte y el código se distribuyen bajo la licencia MIT del repositorio. Las
marcas de terceros mencionadas pertenecen a sus titulares y se usan solo como
referencia pública.

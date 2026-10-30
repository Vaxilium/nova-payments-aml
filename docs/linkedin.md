# LinkedIn — textos de difusión

> Borradores para revisión y publicación manual del autor. No se declara ningún
> post publicado. Reemplazar `_pendiente_` solo con enlaces reales y verificados.
> El caso NovaBank es 100 % ficticio.

## Carrusel 2026 — Pagos, riesgo y decisiones

**Archivo:** `docs/assets/linkedin/carousel-novabank.pdf` · 10 slides · 1080 × 1350
**Portada:** `docs/assets/linkedin/carousel/01-portada.png`
**Formato:** subir el PDF como documento en LinkedIn y usar el texto de abajo.

### Texto sugerido para el post

¿Cómo se ve un proyecto de pagos y AML desde Business Analysis?

Armé NovaBank, un caso ficticio de un banco paraguayo que lanza transferencias
instantáneas, pagos internacionales y monitoreo AML. El repositorio cubre el ciclo
completo, no solo la etapa de documentación:

- 10 épicas, 40 historias con Gherkin y 198 story points.
- 6 procesos BPMN y 4 tablas DMN.
- Core SQLite con partida doble y API FastAPI con idempotencia.
- Mensajería ISO 20022/MT103 y 12 reglas AML.
- 204 pruebas automatizadas y 51/51 casos UAT automatizados.
- Dashboard, 10 wireframes, demo GIF y este carrusel.

Lo más valioso fue la trazabilidad: cada historia tiene al menos un caso de
prueba. Lo más incómodo fue aceptar lo que el prototipo no hace: no se conecta a
SPI/SWIFT, no tiene autenticación y no es una certificación ISO 20022. Eso también
queda documentado.

Caso 100 % ficticio, datos sintéticos y resultados reproducibles.

Repo: https://github.com/Vaxilium/nova-payments-aml

#BusinessAnalysis #Pagos #AML #ISO20022 #SQL #UAT

### Guion del carrusel

1. Portada: pagos instantáneos, cross-border y AML.
2. El reto: una sola experiencia, tres tensiones.
3. Rol: BA end-to-end.
4. Arquitectura: del canal al libro mayor.
5. Diseño funcional: BPMN, DMN y criterios de aceptación.
6. Datos y AML: 494 transacciones → 377 alertas → 59 casos.
7. Calidad: 100 % recall; 99,13 % y 69,03 % de precisión.
8. Producto: wireframes, dashboard y demo.
9. Límites: lo implementado, lo manual y lo pendiente.
10. Cierre y contacto.

### Publicación

1. Revisar los 10 PNG y el PDF.
2. Subir `carousel-novabank.pdf` como documento.
3. Pegar el texto, revisar el enlace y publicar.
4. Guardar URL y captura en `docs/EVIDENCIAS.md` (EV-011).
5. No afirmar uso operativo de Jira, Figma, Power BI, Tableau, Camunda, Bizagi,
   Signavio, Lucidchart, Visio o Miro.

---

## Sección Destacados

**NovaBank — Pagos instantáneos, cross-border y AML (caso ficticio)**

Caso de negocio end-to-end de un banco paraguayo ficticio: 10 épicas, 40
historias, 6 procesos BPMN, 4 tableros DMN, core SQLite con partida doble, API
FastAPI, mensajería ISO 20022/MT103, 12 reglas AML, UAT con 65 casos y tableros
en Excel/Power BI/Tableau.

Repositorio: https://github.com/Vaxilium/nova-payments-aml

---

## Post 1 — Vista general del caso

¿Cómo se ve un proyecto de pagos y AML desde el rol de Business Analyst, sin
acceso a un core bancario real?

Armé NovaBank, un caso ficticio de un banco paraguayo que lanza transferencias
instantáneas, pagos internacionales y monitoreo AML. El repositorio cubre el
ciclo completo:

- Negocio: BRD, stakeholders, riesgos, KPIs y contexto regulatorio.
- Procesos: 6 BPMN y 4 DMN, con AS-IS y TO-BE.
- Requerimientos: 10 épicas, 40 historias con Gherkin, 16 NFR y trazabilidad.
- Core: SQLite con partida doble, 49.582 movimientos y 104.966 líneas de libro
  mayor.
- Mensajería: ISO 20022, MT103, validador y simuladores.
- AML: KYC, screening, 12 reglas SQL, alertas, casos y ROS ficticios.
- Analítica: 12 CSV, Excel de 11 hojas, 36 medidas DAX y guía de Tableau.
- QA/UAT: 65 casos, 51 automatizados aprobados y 204 pruebas pytest.

Lo más valioso no fue la cantidad de artefactos, sino la trazabilidad: cada
historia tiene al menos un caso de prueba y cada resultado se puede reproducir
con una semilla fija.

También dejé explícito lo que el prototipo no hace: no se conecta a SPI/SWIFT,
no tiene autenticación y no reemplaza una certificación real.

Repositorio: https://github.com/Vaxilium/nova-payments-aml

#BusinessAnalysis #Pagos #AML #ISO20022 #SQL #PowerBI

---

## Post 2 — Monitoreo AML con datos sintéticos

Una de las partes más interesantes del caso NovaBank fue diseñar monitoreo AML
sin usar datos reales.

El dataset tiene 500 clientes, 800 cuentas y 49.582 movimientos sintéticos, con
341 operaciones sospechosas etiquetadas. Sobre esa base corren 12 reglas SQL:
estructuración, alta velocidad, pass-through, round mule, activación de cuentas
dormidas, país de riesgo, monto inusual, entre otras.

Resultados del corte de evaluación:

- 494 transacciones alertadas.
- 341 verdaderos positivos etiquetados.
- 3 falsos positivos etiquetados.
- 150 alertas sin etiqueta.
- Recall: 100 % sobre las sospechosas conocidas.
- Precisión sobre etiquetadas: 99,13 %.
- Precisión conservadora: 69,03 %.

La diferencia entre 99,13 % y 69,03 % es importante: la segunda cuenta como
error todas las alertas no etiquetadas. Con datos sintéticos no se puede afirmar
que sean falsos positivos; simplemente no hay ground truth.

Ese matiz es el tipo de cosa que un tablero bonito puede esconder. Por eso el
repositorio documenta la métrica conservadora y la limitación, en lugar de
publicar solo el número más favorable.

Repositorio: https://github.com/Vaxilium/nova-payments-aml

#AML #Compliance #SQL #BusinessAnalysis #Riesgo

---

## Post 3 — Lo que la UAT me mostró sobre el alcance

Cerré la fase de QA/UAT de NovaBank con un resultado cómodo y otro incómodo.

El cómodo: 204 pruebas pytest aprobadas, 51/51 casos automatizados aprobados y
23/23 consultas SQL de control OK.

El incómodo: de 65 casos de prueba, 8 corresponden a funcionalidades que están
especificadas pero no implementadas, y 6 dependen de pantallas o flujos que el
prototipo no tiene. Además quedaron 5 defectos abiertos, incluido uno crítico:
la API no tiene autenticación ni autorización por rol.

Podría haber omitido esos casos para mostrar un 100 % limpio. Pero un UAT que
solo mide lo que ya funciona no sirve para decidir si algo está listo.

La trazabilidad historia → caso → evidencia hizo visible el hueco. Eso me dejó
tres aprendizajes:

1. Cubrir 40/40 historias no significa que las 40 estén implementadas.
2. Un prototipo funcional no es un piloto productivo.
3. Declarar lo que falta es parte del trabajo del BA, no una debilidad del
   portafolio.

Repositorio: https://github.com/Vaxilium/nova-payments-aml

#BusinessAnalysis #QA #UAT #Pagos #AML

---

## Checklist antes de publicar

- [ ] Elegir un solo borrador por publicación.
- [ ] Verificar que el repositorio sea público y que el enlace abra sin login.
- [ ] Confirmar que las métricas coinciden con `README.md` y `08-qa-uat/`.
- [ ] No afirmar que se operaron Jira, Confluence, Azure DevOps, Figma, Power BI,
      Tableau, Camunda, Bizagi, Signavio, Lucidchart, Visio o Miro.
- [ ] Mantener la aclaración de caso ficticio.
- [ ] Agregar el repositorio a la sección Destacados.
- [ ] Guardar URL y captura en `docs/EVIDENCIAS.md` (EV-011).
- [ ] Subir `docs/assets/linkedin/carousel-novabank.pdf` como documento en LinkedIn.

## Nota de honestidad

Los textos anteriores describen artefactos y ejecuciones reales del repositorio.
No describen un proyecto en producción, un cliente real ni una validación
regulatoria. Las referencias a BCP, SWIFT, GAFI, SEPRELAD e ISO 20022 son
contexto público, no una afiliación.

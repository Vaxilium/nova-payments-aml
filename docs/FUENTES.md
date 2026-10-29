# FUENTES

Registro de fuentes oficiales consultadas para sostener afirmaciones normativas o técnicas del proyecto.

**Reglas**
- Solo se citan fuentes consultadas realmente y se indica la fecha de consulta.
- Se prefiere el dominio oficial de cada organismo o estándar.
- Se parafrasea el contenido; no se reproducen citas textuales largas.
- Nunca se inventan números de resolución, artículos ni URLs.
- Cuando un sitio oficial bloquea la descarga automatizada, se deja constancia expresa y se contrasta con fragmentos indexados o copias espejo identificables.
- Lo que no pueda verificarse se marca `SUPUESTO NO VERIFICADO` en el documento correspondiente y se anota en `PENDIENTES.md`.

**Criterios de verificación**
1. Dominio oficial o fuente primaria identificable.
2. Documento vigente a la fecha de consulta.
3. Contenido relevante para la afirmación que se quiere sostener.
4. Registro de la fecha y del uso concreto.

## Fuentes verificadas

| ID | Organismo / estándar | Documento | URL | Fecha de consulta | Uso en el proyecto | Nota de acceso |
|---|---|---|---|---|---|---|
| F-01 | Banco Central del Paraguay (BCP) | Sistemas de Pago y Tesorería — Consultas frecuentes | https://www.bcp.gov.py/sistemas-de-pago-y-tesoreria | 2026-10-27 | Características públicas del SPI: operación 24/7, transferencias en guaraníes hasta ₲10.000.000, acreditación máxima de 5 segundos, alias, devoluciones y carácter irrevocable. | Consulta directa correcta. |
| F-02 | Banco Central del Paraguay (BCP) | Sistema de Pagos del Paraguay (SIPAP) | https://www.bcp.gov.py/sistema-de-pagos-del-paraguay | 2026-10-27 | Rol de los módulos LBTR, ACH, DEPO y SPI dentro del SIPAP; participantes y funcionalidad general. | Consulta directa correcta. La tabla resumen indica para SPI “días hábiles”, en contradicción con F-01; se adopta F-01 y se registra P-006. |
| F-03 | SEPRELAD (UIF de Paraguay) | Preguntas Frecuentes | https://www.seprelad.gov.py/?page_id=1810 | 2026-10-27 | Rol de la UIF, Ley N° 1015/1997 y modificatorias, concepto de ROS, sujetos obligados, beneficiario final, PEP (Resolución N° 50/19) y deber de reserva. | Consulta directa correcta. |
| F-04 | GAFI / FATF | The FATF Recommendations (actualización febrero 2025) | https://www.fatf-gafi.org/content/dam/fatf-gafi/recommendations/Feburary%202025%20FATF%20Recommendations.pdf | 2026-10-27 | Recomendación 10 (debida diligencia del cliente), Recomendación 16 (transparencia de transferencias electrónicas) y Recomendación 20 (reporte de operaciones sospechosas). | El sitio oficial devolvió HTTP 403 a la descarga automatizada. Contenido corroborado mediante fragmentos indexados y copias espejo gubernamentales. Ver P-007. |
| F-05 | ISO | ISO 4217:2015 — Codes for the representation of currencies | https://www.iso.org/standard/64758.html | 2026-10-27 | Estructura de códigos alfabéticos de tres letras y numéricos de tres dígitos; relación con unidades menores. | Consulta directa correcta. |
| F-06 | ISO | ISO 13616-1:2020 — IBAN, Part 1: Structure of the IBAN | https://www.iso.org/standard/81090.html | 2026-10-27 | Estructura del IBAN y función en el intercambio internacional de datos. | Ficha oficial consultada; norma completa no descargada. |
| F-07 | SWIFT (Registration Authority de ISO 13616) | International Bank Account Number (IBAN) | https://www.swift.com/standards/data-standards/iban-international-bank-account-number | 2026-10-27 | IBAN como estándar internacional de identificación de cuentas; SWIFT como autoridad de registro de formatos nacionales. | Contenido verificado mediante el resultado indexado del sitio oficial. |
| F-08 | ISO 20022 | ISO 20022 Message Definitions — Payments Clearing and Settlement (pacs.008) | https://www.iso20022.org/iso-20022-message-definitions?search=pacs.008 | 2026-10-27 | Definición de pacs.008 como mensaje de transferencia de crédito de cliente entre instituciones financieras y su relación con pacs.002. | El sitio oficial devolvió HTTP 403 a la consulta automatizada. Contenido corroborado con F-09 y fragmentos indexados. Ver P-008. |
| F-09 | SWIFT | ISO 20022: Implementation — CBPR+ | https://www.swift.com/standards/iso-20022/iso-20022-faqs/implementation | 2026-10-27 | Fin del período de coexistencia MT/ISO 20022 para pagos transfronterizos el 22 de noviembre de 2025; uso de ISO 20022 como estándar para pagos cross-border. | El sitio devolvió HTTP 403 a la descarga automatizada; contenido corroborado mediante fragmentos indexados y documentos públicos de SWIFT. |
| F-10 | SWIFT | Payments and Cash Management using Standards MT messages — MT 103 | https://www.swift.com/myswift/services/training/swift-training-catalogue/browse-swift-training-catalogue/payments-and-cash-management-using-standards-mt-messages | 2026-10-27 | MT 103 como Single Customer Credit Transfer y su relación con MT 202 COV. | Contenido verificado mediante el resultado indexado del sitio oficial. |
| F-11 | BIS / CPMI | Harmonised ISO 20022 data requirements for enhancing cross-border payments — updated report (CPMI Papers d230) | https://www.bis.org/cpmi/publ/d230.htm | 2026-10-27 | Conjunto armonizado de mensajes ISO 20022 para pagos transfronterizos (pacs.008, pacs.009, pacs.002, camt.056 y devoluciones). | Página oficial y PDF localizados; contenido verificado por fragmentos indexados, sin descarga completa. |
| F-12 | ISO 20022 | Message Definitions — Payments Clearing and Settlement / Payments Initiation | https://www.iso20022.org/iso-20022-message-definitions | 2026-10-28 | Catálogo de definiciones y versiones de pacs.008, pacs.002, pain.001 y camt.053; nomenclatura área.mensaje.variante.versión. | El sitio devolvió HTTP 403 a la consulta automatizada. Contenido corroborado con resultados indexados del catálogo oficial y con F-09/F-11. Ver P-008. |
| F-13 | SIX Group (ISO 4217 Maintenance Agency) | ISO 4217 list-one XML — List of currencies and funds | https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml | 2026-10-28 | Códigos alfabéticos activos, nombres y unidades menores; PYG con 0 decimales y USD con 2. | Descarga directa correcta. Lista publicada 2026-09-17; 178 códigos únicos extraídos. |
| F-14 | SWIFT (Registration Authority de ISO 13616) | IBAN Registry, version 101 | https://www.swift.com/sites/default/files/files/iban-registry-v101.pdf | 2026-10-28 | Estructura, longitud y ejemplos de IBAN por país; confirmación de que el registro no incluye a Paraguay como país IBAN. | PDF no descargado por bloqueo de acceso automatizado; contenido corroborado con fragmentos indexados del registro. Ver P-008. |
| F-15 | ISO | ISO 9362:2022 — Banking telecommunication messages — Business identifier code (BIC) | https://www.iso.org/standard/84108.html | 2026-10-28 | Estructura del BIC: prefijo de entidad, código de país, sufijo y rama opcional; edición vigente. | Ficha oficial consultada; norma completa no descargada. |
| F-16 | SWIFT | Business Identifier Code (BIC) | https://www.swift.com/standards/data-standards/bic-business-identifier-code | 2026-10-28 | BIC de 8 caracteres (4!a + 2!a + 2!c) y rama opcional de 3 caracteres; SWIFT como autoridad de registro. | El sitio devolvió HTTP 403 a la consulta automatizada; contenido corroborado con resultado indexado del sitio oficial y F-15. |
| F-17 | ISO | ISO/IEC 7064:2003 — Check character systems | https://www.iso.org/standard/31531.html | 2026-10-28 | Sistemas de carácter de control; base del cálculo MOD 97-10 usado por el IBAN. | Ficha oficial consultada; norma completa no descargada. |
| F-18 | SWIFT | ISO 20022 Programme — Customer Workshop (message structure and translation overview) | https://www.swift.com/swift-resource/248681/download | 2026-10-28 | Nomenclatura de mensajes ISO 20022 y relación de traducción MT103/MT102 ↔ pacs.008, MT103 REJECT ↔ pacs.002 y MT940/MT950 ↔ camt.053. | Documento localizado por resultado indexado; no descargado en esta sesión. Se usa solo como orientación de correspondencia, no como regla normativa de traducción. Ver P-008. |

## Fuentes consultadas pero no utilizadas como base normativa

| Fuente | Motivo |
|---|---|
| Resolución SEPRELAD N° 77/2020 | Aplica a Empresas de Medios de Pago Electrónicos (EMPE), no a un banco. Se deja fuera del alcance normativo de NovaBank hasta validación legal en Fase 5. |
| Resolución G.G. BCP N° 22/2026 (QR Hub) | Fuera del alcance del caso (pagos QR). |

## Brechas y verificaciones pendientes

| Tema | Estado | Acción |
|---|---|---|
| Reglamento General del SIPAP y resoluciones BCP aplicables al SPI | No descargado en esta sesión | Validar número, vigencia y texto antes de Fase 5. |
| Resolución SEPRELAD aplicable específicamente a bancos supervisados por la SIB | No verificada en esta sesión | Confirmar con el área de Cumplimiento y registrar en Fase 5. |
| Listas de sanciones y PEP utilizadas en el caso | Ficticias | No se usan listas reales; se documentará el carácter sintético en Fase 5. |
| Tasas, comisiones y límites comerciales | Ficticios | Son parámetros de diseño, no datos de mercado. |

## Historial de consultas

| Fecha | Fuente | Resultado |
|---|---|---|
| 2026-10-27 | BCP — Sistemas de Pago y Tesorería | Verificada. |
| 2026-10-27 | BCP — SIPAP | Verificada; detectada contradicción de horario SPI (P-006). |
| 2026-10-27 | SEPRELAD — Preguntas Frecuentes | Verificada. |
| 2026-10-27 | GAFI / FATF — Recomendaciones | Acceso directo 403; contenido corroborado por índice y espejos (P-007). |
| 2026-10-27 | ISO 4217:2015 | Verificada. |
| 2026-10-27 | ISO 13616-1:2020 | Ficha verificada. |
| 2026-10-27 | SWIFT — IBAN / ISO 20022 / MT 103 | Contenido verificado por resultados indexados; acceso directo parcialmente bloqueado (P-008). |
| 2026-10-27 | BIS / CPMI — Harmonised ISO 20022 data requirements | Página oficial y PDF localizados; contenido verificado por fragmentos indexados. |
| 2026-10-28 | ISO 20022 — Message Definitions | Acceso directo 403; contenido corroborado por resultados indexados (P-008). |
| 2026-10-28 | SIX Group — ISO 4217 list-one XML | Descarga directa correcta; 178 códigos únicos. |
| 2026-10-28 | SWIFT — IBAN Registry v101 | PDF no descargado por bloqueo; estructura y países corroborados por fragmentos indexados. |
| 2026-10-28 | ISO 9362:2022 / SWIFT BIC | Ficha ISO consultada; página SWIFT con 403 y contenido corroborado por índice. |
| 2026-10-28 | ISO/IEC 7064:2003 | Ficha oficial consultada. |
| 2026-10-28 | SWIFT — ISO 20022 Programme Workshop | Documento localizado; correspondencia MT/MX corroborada por fragmento indexado. |

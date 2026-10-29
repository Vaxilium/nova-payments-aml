"""Registro de defectos de ejemplo observados durante la preparación de la UAT.

Los defectos describen brechas reales del prototipo. No representan incidentes
de producción ni se presentan como corregidos.
"""

from __future__ import annotations

DEFECTS: list[dict] = [
    {
        "id": "DEF-001",
        "titulo": "El canal no resuelve alias de beneficiario ni devuelve titular enmascarado",
        "severidad": "Alta",
        "prioridad": "P1",
        "estado": "Abierto",
        "ambiente": "Prototipo local - API /v1 y simulador",
        "caso": "TC-002",
        "historia": "US-002",
        "descripcion": (
            "El simulador acepta un alias como referencia del acreedor, pero no existe un "
            "directorio de alias ni una operación que devuelva el titular y la cuenta "
            "enmascarados. Tampoco se rechaza un alias inexistente con ALIAS_NO_ENCONTRADO."
        ),
        "pasos": (
            "1) Abrir el flujo de transferencia local. "
            "2) Ingresar el alias BENEFICIARIO-INEXISTENTE. "
            "3) Confirmar la búsqueda."
        ),
        "esperado": "El sistema devuelve ALIAS_NO_ENCONTRADO y no crea el pago.",
        "obtenido": "No hay endpoint de resolución; el alias solo se transporta como texto.",
        "evidencia": "08-qa-uat/casos-prueba.csv (TC-002); 06-mensajeria/simulator/instant.py.",
        "impacto": "El cliente no puede verificar al beneficiario antes de confirmar.",
        "responsable": "Product Owner / Desarrollo de canales",
    },
    {
        "id": "DEF-002",
        "titulo": "No existe flujo de devolución de pagos locales ni devolución internacional",
        "severidad": "Alta",
        "prioridad": "P1",
        "estado": "Abierto",
        "ambiente": "Prototipo local - procesos BPMN y simuladores",
        "caso": "TC-004; TC-010",
        "historia": "US-004; US-010",
        "descripcion": (
            "Los procesos de devolución están modelados en BPMN, pero no hay endpoint, "
            "máquina de estados ni asiento de reverso para devolver un pago local o "
            "internacional. El simulador solo cubre rechazo y timeout."
        ),
        "pasos": (
            "1) Tomar un pago ACREDITADO. "
            "2) Solicitar devolución dentro del plazo. "
            "3) Confirmar la solicitud."
        ),
        "esperado": "Se crea un caso de devolución con número, dueño y SLA, y se reversa el asiento.",
        "obtenido": "No existe operación de devolución; el flujo queda en el modelo de procesos.",
        "evidencia": "08-qa-uat/casos-prueba.csv (TC-004, TC-010); 02-procesos/bpmn/transferencia-instantanea-to-be.bpmn.",
        "impacto": "Un cliente no puede recuperar fondos por el canal digital.",
        "responsable": "Desarrollo Core / Operaciones",
    },
    {
        "id": "DEF-003",
        "titulo": "La API no implementa autenticación ni autorización por rol",
        "severidad": "Crítica",
        "prioridad": "P1",
        "estado": "Abierto - brecha de alcance conocida",
        "ambiente": "Prototipo local - FastAPI /v1",
        "caso": "TC-037",
        "historia": "US-037",
        "descripcion": (
            "Cualquier cliente puede invocar los endpoints de crédito, débito y transferencia "
            "sin autenticarse. No hay validación de rol ni segregación de funciones. La "
            "limitación está registrada en el supuesto S-055."
        ),
        "pasos": (
            "1) Invocar POST /v1/transfers sin credenciales. "
            "2) Repetir con un usuario de solo lectura."
        ),
        "esperado": "Sin credenciales se responde 401; con rol LECTURA se responde 403.",
        "obtenido": "La operación se ejecuta porque el prototipo no tiene capa de identidad.",
        "evidencia": "08-qa-uat/casos-prueba.csv (TC-037); 05-core-middleware/app/api.py; docs/SUPUESTOS.md (S-055).",
        "impacto": "El prototipo no es apto para exposición fuera de un entorno controlado.",
        "responsable": "Arquitectura / Seguridad",
    },
    {
        "id": "DEF-004",
        "titulo": "Discrepancia entre el corte de alertas de Fase 5 y el dataset analítico",
        "severidad": "Media",
        "prioridad": "P2",
        "estado": "Abierto",
        "ambiente": "Dataset analítico y documentación de evidencias",
        "caso": "TC-029",
        "historia": "US-029",
        "descripcion": (
            "La evidencia de Fase 5 documenta 775 alertas deduplicadas (1.326 coincidencias), "
            "mientras que el corte reproducible de Fase 6 genera 377 alertas (786 coincidencias). "
            "La diferencia proviene de ejecutar las reglas sobre la base actual y no sobre el "
            "snapshot original; está registrada como P-018."
        ),
        "pasos": (
            "1) Ejecutar 07-aml-compliance/scripts/evaluate_rules.py sobre la base actual. "
            "2) Ejecutar 09-analitica/scripts/export_analytics.py. "
            "3) Comparar el conteo de alertas con docs/EVIDENCIAS.md de Fase 5."
        ),
        "esperado": "Un único corte documentado y trazable para todas las fases.",
        "obtenido": "Dos cortes con conteos distintos y sin reconciliación automática.",
        "evidencia": "docs/PENDIENTES.md (P-018); 09-analitica/data/export_report.json; docs/EVIDENCIAS.md.",
        "impacto": "Riesgo de inconsistencia en tableros y en la narrativa del portafolio.",
        "responsable": "BA / Analítica",
    },
    {
        "id": "DEF-005",
        "titulo": "El límite diario agregado de pagos locales no se valida",
        "severidad": "Media",
        "prioridad": "P2",
        "estado": "Abierto - aceptado como alcance del prototipo",
        "ambiente": "Prototipo local - simulador instantáneo",
        "caso": "TC-005; TC-034",
        "historia": "US-005; US-034",
        "descripcion": (
            "El simulador aplica el tope por operación de 10.000.000 PYG, pero no acumula "
            "el importe diario por cliente. Un cliente podría realizar varias operaciones "
            "por debajo del tope y superar el límite diario definido en el BRD."
        ),
        "pasos": (
            "1) Enviar dos pagos de 9.000.000 PYG el mismo día. "
            "2) Revisar el total acumulado del cliente."
        ),
        "esperado": "El segundo pago se rechaza por límite diario.",
        "obtenido": "Ambos pagos se aceptan porque solo se evalúa el tope por operación.",
        "evidencia": "08-qa-uat/casos-prueba.csv (TC-005, TC-034); 06-mensajeria/simulator/instant.py.",
        "impacto": "El control de límites no cubre el riesgo de fragmentación diaria.",
        "responsable": "Desarrollo Core / Riesgos",
    },
]

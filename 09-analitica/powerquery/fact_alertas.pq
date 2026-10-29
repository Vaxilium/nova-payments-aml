// Hecho de alertas AML.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\fact_alerts.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"alert_id", Int64.Type},
            {"date_key", type date},
            {"created_at", type datetime},
            {"alert_type", type text},
            {"rule_id", type text},
            {"rule_name", type text},
            {"severity", type text},
            {"priority", type text},
            {"risk_score", Int64.Type},
            {"status", type text},
            {"transaction_count", Int64.Type},
            {"customer_id", type text},
            {"account_id", type text},
            {"transaction_id", type text},
            {"assigned_to", type text},
            {"assigned_at", type datetime},
            {"assignment_minutes", Int64.Type},
            {"due_at", type datetime},
            {"closed_at", type datetime},
            {"closure_notes", type text},
            {"case_id", Int64.Type},
            {"segment", type text},
            {"risk_rating", type text},
            {"kyc_score", Int64.Type},
            {"is_false_positive", Int64.Type},
            {"is_closed", Int64.Type},
            {"is_escalated", Int64.Type}
        }
    ),
    ConPrioridad = Table.AddColumn(
        Tipos,
        "priority_order",
        each if [priority] = "P1" then 1 else if [priority] = "P2" then 2 else 3,
        Int64.Type
    )
in
    ConPrioridad

// Hecho de casos AML.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\fact_cases.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"case_id", Int64.Type},
            {"customer_id", type text},
            {"title", type text},
            {"status", type text},
            {"priority", type text},
            {"risk_score", Int64.Type},
            {"opened_at", type datetime},
            {"assigned_to", type text},
            {"due_at", type datetime},
            {"closed_at", type datetime},
            {"ros_reported", Int64.Type},
            {"alert_count", Int64.Type},
            {"is_closed", Int64.Type},
            {"is_reported", Int64.Type},
            {"is_on_time_close", Int64.Type}
        }
    ),
    FechaApertura = Table.AddColumn(
        Tipos,
        "opened_date",
        each DateTime.Date([opened_at]),
        type date
    )
in
    FechaApertura

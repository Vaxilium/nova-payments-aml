// Catálogo de prioridades y SLA.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\dim_priority.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"priority", type text},
            {"assignment_sla_minutes", Int64.Type},
            {"closure_sla_business_days", Int64.Type}
        }
    ),
    Orden = Table.AddColumn(
        Tipos,
        "priority_order",
        each if [priority] = "P1" then 1 else if [priority] = "P2" then 2 else 3,
        Int64.Type
    )
in
    Orden

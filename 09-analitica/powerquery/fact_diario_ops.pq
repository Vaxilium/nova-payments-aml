// Agregado diario de operaciones.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\fact_daily_ops.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"date_key", type date},
            {"currency", type text},
            {"ops", Int64.Type},
            {"amount", type number},
            {"fee", type number},
            {"stp_ops", Int64.Type}
        }
    ),
    ConClave = Table.AddColumn(
        Tipos,
        "Clave",
        each Date.ToText([date_key], "yyyy-MM-dd") & "|" & [currency],
        type text
    )
in
    ConClave

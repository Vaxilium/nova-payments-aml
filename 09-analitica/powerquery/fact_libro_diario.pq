// Agregado diario del libro mayor.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\fact_ledger_daily.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"date_key", type date},
            {"currency", type text},
            {"entries", Int64.Type},
            {"debit", type number},
            {"credit", type number}
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

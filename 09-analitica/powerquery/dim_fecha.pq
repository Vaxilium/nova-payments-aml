// Dimensión de calendario.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\dim_date.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"date_key", type date},
            {"year", Int64.Type},
            {"quarter", Int64.Type},
            {"month", Int64.Type},
            {"year_month", type text},
            {"week", Int64.Type},
            {"weekday", Int64.Type},
            {"weekday_name", type text},
            {"is_weekend", Int64.Type}
        }
    ),
    NombreMes = Table.AddColumn(
        Tipos,
        "month_name",
        each Date.ToText([date_key], "MMMM", "es-PY"),
        type text
    )
in
    NombreMes

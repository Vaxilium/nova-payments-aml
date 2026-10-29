// Catálogo de monedas ISO 4217.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\dim_currency.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"currency", type text},
            {"name", type text},
            {"minor_unit", Int64.Type}
        }
    )
in
    Tipos

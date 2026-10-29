// Catálogo de reglas AML.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\dim_rule.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"rule_id", type text},
            {"rule_name", type text},
            {"severity", type text},
            {"base_score", Int64.Type},
            {"intended_pattern", type text}
        }
    )
in
    Tipos

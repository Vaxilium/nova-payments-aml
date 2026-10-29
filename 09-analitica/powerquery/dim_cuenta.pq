// Dimensión de cuentas.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\dim_account.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"account_id", type text},
            {"customer_id", type text},
            {"account_number", type text},
            {"account_type", type text},
            {"currency", type text},
            {"status", type text},
            {"balance", type number},
            {"opened_at", type datetime},
            {"segment", type text},
            {"risk_rating", type text},
            {"kyc_score", Int64.Type}
        }
    )
in
    Tipos

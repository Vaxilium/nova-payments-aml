// Hecho de pagos locales con latencia sintética.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\fact_payment_sla.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"transaction_id", type text},
            {"date_key", type date},
            {"customer_id", type text},
            {"segment", type text},
            {"channel", type text},
            {"amount", type number},
            {"latency_ms", Int64.Type},
            {"within_sla", Int64.Type}
        }
    )
in
    Tipos

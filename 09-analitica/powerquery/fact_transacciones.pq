// Hecho principal de transacciones.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\fact_transactions.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"transaction_id", type text},
            {"date_key", type date},
            {"created_at", type datetime},
            {"transaction_type", type text},
            {"status", type text},
            {"currency", type text},
            {"amount", type number},
            {"fee", type number},
            {"channel", type text},
            {"debit_account_id", type text},
            {"credit_account_id", type text},
            {"customer_id", type text},
            {"segment", type text},
            {"risk_rating", type text},
            {"kyc_score", Int64.Type},
            {"payment_scope", type text},
            {"truth_label", type text},
            {"truth_pattern", type text},
            {"alert_id", Int64.Type},
            {"is_stp", Int64.Type}
        }
    ),
    ConAnioMes = Table.AddColumn(Tipos, "year_month", each Date.ToText([date_key], "yyyy-MM"), type text)
in
    ConAnioMes

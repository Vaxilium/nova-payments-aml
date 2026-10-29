// Dimensión de clientes.
let
    Origen = Csv.Document(
        File.Contents(RutaDatos & "\dim_customer.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(
        Encabezados,
        {
            {"customer_id", type text},
            {"customer_type", type text},
            {"display_name", type text},
            {"document_type", type text},
            {"country_code", type text},
            {"city", type text},
            {"segment", type text},
            {"risk_rating", type text},
            {"kyc_status", type text},
            {"is_active", Int64.Type},
            {"created_at", type datetime},
            {"kyc_score", Int64.Type},
            {"risk_category", type text},
            {"requires_edd", Int64.Type},
            {"is_pep", Int64.Type},
            {"occupation", type text},
            {"activity_risk", type text},
            {"onboarding_channel", type text},
            {"product_complexity", type text},
            {"expected_monthly_volume_minor", Int64.Type}
        }
    )
in
    Tipos

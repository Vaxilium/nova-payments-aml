// Consulta de conciliación: hechos diarios contra libro mayor.
let
    HechosOrigen = Csv.Document(
        File.Contents(RutaDatos & "\fact_daily_ops.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Hechos = Table.PromoteHeaders(HechosOrigen, [PromoteAllScalars = true]),
    HechosTipos = Table.TransformColumnTypes(
        Hechos,
        {
            {"date_key", type date},
            {"currency", type text},
            {"ops", Int64.Type},
            {"amount", type number},
            {"fee", type number},
            {"stp_ops", Int64.Type}
        }
    ),
    HechosClave = Table.AddColumn(
        HechosTipos,
        "Clave",
        each Date.ToText([date_key], "yyyy-MM-dd") & "|" & [currency],
        type text
    ),
    LibroOrigen = Csv.Document(
        File.Contents(RutaDatos & "\fact_ledger_daily.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Libro = Table.PromoteHeaders(LibroOrigen, [PromoteAllScalars = true]),
    LibroTipos = Table.TransformColumnTypes(
        Libro,
        {
            {"date_key", type date},
            {"currency", type text},
            {"entries", Int64.Type},
            {"debit", type number},
            {"credit", type number}
        }
    ),
    LibroClave = Table.AddColumn(
        LibroTipos,
        "Clave",
        each Date.ToText([date_key], "yyyy-MM-dd") & "|" & [currency],
        type text
    ),
    Unido = Table.NestedJoin(HechosClave, {"Clave"}, LibroClave, {"Clave"}, "Libro", JoinKind.LeftOuter),
    Expandido = Table.ExpandTableColumn(
        Unido,
        "Libro",
        {"entries", "debit", "credit"},
        {"entries_ledger", "debit", "credit"}
    ),
    Diferencia = Table.AddColumn(Expandido, "Diferencia", each [debit] - [credit], type number),
    Resultado = Table.AddColumn(
        Diferencia,
        "Resultado",
        each if Number.Abs([Diferencia]) < 0.01 then "CUADRADO" else "DIFERENCIA",
        type text
    )
in
    Resultado

"""Gráficos del portafolio generados con datos reales del repositorio."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from .assetlib import IMG_DIR, PALETTE, format_int, optimize_png  # noqa: E402
from .data import Dataset, alert_counts, currency_summary, daily_series, latency_summary, percentile  # noqa: E402

NAVY = PALETTE["navy_800"]
PANEL = PALETTE["navy_700"]
INK = "#E6F1F8"
MUTED = PALETTE["slate_400"]
GRID = "#1E4E75"
CYAN = PALETTE["cyan_400"]
TURQ = PALETTE["turquoise_400"]
MINT = PALETTE["mint_300"]
AMBER = PALETTE["amber_400"]
RED = PALETTE["red_400"]
GREEN = PALETTE["green_400"]

SHORT_RULES = {
    "R01": "Estructuración",
    "R02": "Velocidad (cantidad)",
    "R03": "Velocidad (monto)",
    "R04": "Cuenta de paso",
    "R05": "Depósitos redondos",
    "R06": "Cuenta dormida",
    "R07": "Jurisdicción de riesgo",
    "R08": "Importe atípico",
    "R09": "Cambio de conducta",
    "R10": "Fondos circulares",
    "R11": "Contraparte concentrada",
    "R12": "Fan-in de remitentes",
}


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": NAVY,
            "savefig.facecolor": NAVY,
            "axes.facecolor": PANEL,
            "axes.edgecolor": GRID,
            "axes.labelcolor": PALETTE["slate_300"],
            "axes.titlecolor": INK,
            "text.color": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 16,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
        }
    )


def _frame(
    fig: plt.Figure,
    *,
    title: str,
    subtitle: str,
    source: str,
) -> None:
    fig.text(0.055, 0.945, title, fontsize=24, fontweight="bold", color=INK, va="top")
    fig.text(0.055, 0.885, subtitle, fontsize=11.5, color=PALETTE["slate_300"], va="top")
    fig.add_artist(Line2D([0.0, 1.0], [0.965, 0.965], color=CYAN, linewidth=2, alpha=0.8))
    fig.text(0.055, 0.035, source, fontsize=9, color=MUTED, va="bottom")
    fig.text(
        0.955,
        0.035,
        "NovaBank · caso ficticio",
        fontsize=9,
        color=PALETTE["turquoise_400"],
        ha="right",
        va="bottom",
    )
    fig.subplots_adjust(left=0.075, right=0.955, top=0.80, bottom=0.14)


def _save(fig: plt.Figure, name: str) -> Path:
    path = IMG_DIR / name
    fig.savefig(path, dpi=150, facecolor=NAVY)
    plt.close(fig)
    optimize_png(path, max_kb=500)
    return path


def chart_daily_volume(data: Dataset) -> Path:
    series = daily_series(data.daily)
    days = [date.fromisoformat(day) for day, _, _ in series]
    ops = [value for _, value, _ in series]
    rolling = []
    for index in range(len(ops)):
        window = ops[max(0, index - 6) : index + 1]
        rolling.append(sum(window) / len(window))

    fig, ax = plt.subplots(figsize=(10.67, 6))
    ax.grid(axis="y", alpha=0.55)
    ax.plot(days, ops, color=CYAN, linewidth=1.0, alpha=0.45, label="Operaciones diarias")
    ax.fill_between(days, ops, color=CYAN, alpha=0.10)
    ax.plot(days, rolling, color=MINT, linewidth=2.4, label="Media móvil de 7 días")
    ax.set_ylim(0, max(ops) * 1.22)
    ax.set_xlabel("Fecha (2026)")
    ax.set_ylabel("Operaciones")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{int(value):,}".replace(",", ".")))

    peak_index = max(range(len(ops)), key=ops.__getitem__)
    ax.annotate(
        f"Pico: {format_int(ops[peak_index])} ops",
        xy=(days[peak_index], ops[peak_index]),
        xytext=(12, 16),
        textcoords="offset points",
        color=INK,
        fontsize=10,
        arrowprops={"arrowstyle": "-", "color": MINT, "lw": 1},
    )
    ax.legend(loc="upper left", fontsize=10, labelcolor=INK)
    total = sum(ops)
    avg = total / len(ops)
    ax.text(
        0.985,
        0.93,
        f"{format_int(total)} operaciones\n{len(ops)} días · media {avg:.0f}/día",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=11,
        color=INK,
        bbox={"boxstyle": "round,pad=0.55", "facecolor": NAVY, "edgecolor": GRID},
    )
    _frame(
        fig,
        title="Volumen diario de transacciones",
        subtitle="Abril a septiembre de 2026 · todas las monedas y tipos de operación",
        source="Fuente: 09-analitica/data/fact_daily_ops.csv (49.582 movimientos sintéticos, semilla 20261027).",
    )
    return _save(fig, "chart-daily-volume.png")


def chart_currency_mix(data: Dataset) -> Path:
    summary = currency_summary(data.transactions)
    total = sum(int(item["ops"]) for item in summary)
    labels = [str(item["currency"]) for item in summary]
    values = [int(item["ops"]) for item in summary]
    colors = [CYAN, TURQ]

    fig = plt.figure(figsize=(10.67, 6))
    ax = fig.add_axes([0.075, 0.16, 0.40, 0.56])
    wedges, _ = ax.pie(
        values,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.36, "edgecolor": NAVY, "linewidth": 3},
    )
    ax.text(0, 0.08, format_int(total), ha="center", va="center", fontsize=24, fontweight="bold", color=INK)
    ax.text(0, -0.12, "operaciones", ha="center", va="center", fontsize=11, color=MUTED)
    ax.set_aspect("equal")

    y_positions = [0.50, 0.32]
    for index, item in enumerate(summary):
        currency = str(item["currency"])
        share = float(item["share"]) * 100
        amount_millions = float(item["amount_minor"]) / 1_000_000
        amount_label = (
            f"{format_int(amount_millions)} millones de {currency}"
            if currency == "PYG"
            else f"{amount_millions:.1f} millones de {currency}".replace(".", ",")
        )
        y = y_positions[index]
        fig.add_artist(
            Rectangle(
                (0.53, y - 0.045),
                0.40,
                0.11,
                transform=fig.transFigure,
                facecolor=PANEL,
                edgecolor=GRID,
                linewidth=1,
                zorder=0,
            )
        )
        fig.text(0.555, y + 0.035, currency, fontsize=18, fontweight="bold", color=colors[index])
        fig.text(
            0.635,
            y + 0.035,
            f"{format_int(int(item['ops']))} ops · {share:.1f} %".replace(".", ","),
            fontsize=13,
            color=INK,
        )
        fig.text(0.555, y - 0.015, amount_label, fontsize=10.5, color=MUTED)

    first, second = summary[0], summary[1]
    fig.text(
        0.53,
        0.175,
        f"{first['currency']} concentra el {float(first['share']) * 100:.1f} % de las operaciones.\n"
        f"{second['currency']} aporta el {float(second['share']) * 100:.1f} % restante.\n"
        "No hay operaciones en EUR en este corte.",
        fontsize=10,
        color=PALETTE["slate_300"],
        va="bottom",
    )
    _frame(
        fig,
        title="Distribución por moneda",
        subtitle="Participación sobre 49.582 operaciones del dataset sintético",
        source="Fuente: 09-analitica/data/fact_transactions.csv y dim_currency.csv.",
    )
    return _save(fig, "chart-currency-mix.png")


def chart_latency(data: Dataset) -> Path:
    summary = latency_summary(data.sla)
    values = [min(int(value), 12_000) for value in summary["values"]]  # type: ignore[index]
    fig, ax = plt.subplots(figsize=(10.67, 6))
    ax.grid(axis="y", alpha=0.55)
    counts, bins, patches = ax.hist(values, bins=48, color=CYAN, alpha=0.78, edgecolor=NAVY, linewidth=0.5)
    for patch, left in zip(patches, bins[:-1]):
        if left >= 10_000:
            patch.set_facecolor(AMBER)
            patch.set_alpha(0.9)

    for value, label, color in [
        (summary["p50"], "p50", CYAN),
        (summary["p95"], "p95", MINT),
        (summary["p99"], "p99", AMBER),
    ]:
        ax.axvline(int(value), color=color, linewidth=1.6, linestyle="--", alpha=0.95)
        ax.text(
            int(value) + 80,
            max(counts) * 0.92,
            f"{label} {int(value) / 1000:.1f} s".replace(".", ","),
            color=color,
            fontsize=9.5,
            rotation=90,
            va="top",
        )
    ax.axvline(10_000, color=RED, linewidth=1.8, linestyle=":", alpha=0.95)
    ax.text(
        10_000 - 160,
        max(counts) * 0.55,
        "SLA 10 s",
        color=RED,
        fontsize=10,
        ha="right",
        fontweight="bold",
    )

    ax.set_xlim(0, 12_000)
    ax.set_xlabel("Latencia de acreditación")
    ax.set_ylabel("Operaciones")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}s"))
    ax.text(
        0.985,
        0.93,
        f"{summary['within_share'] * 100:.1f} % dentro de SLA\n"
        f"p50 {summary['p50'] / 1000:.1f} s · p95 {summary['p95'] / 1000:.1f} s · p99 {summary['p99'] / 1000:.1f} s",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=11,
        color=INK,
        bbox={"boxstyle": "round,pad=0.55", "facecolor": NAVY, "edgecolor": GRID},
    )
    _frame(
        fig,
        title="Tiempos del pago instantáneo",
        subtitle="10.820 pagos locales · latencia sintética y determinista",
        source="Fuente: 09-analitica/data/fact_payment_sla.csv. La latencia es sintética (S-080), no una medición operativa.",
    )
    return _save(fig, "chart-instant-latency.png")


def chart_alerts_by_rule(data: Dataset) -> Path:
    counts = alert_counts(data.alerts)
    ordered = list(reversed(counts))
    labels = [f"{item['rule_id']} · {SHORT_RULES.get(str(item['rule_id']), str(item['rule_name']))}" for item in ordered]
    values = [int(item["count"]) for item in ordered]
    color_map = {"CRITICAL": RED, "HIGH": AMBER, "MEDIUM": CYAN, "LOW": MINT}
    colors = [color_map.get(str(item["severity"]), CYAN) for item in ordered]

    fig, ax = plt.subplots(figsize=(10.67, 6))
    ax.grid(axis="x", alpha=0.55)
    bars = ax.barh(labels, values, color=colors, height=0.62, edgecolor=NAVY, linewidth=0.8)
    for bar, value in zip(bars, values):
        ax.text(
            value + 1.2,
            bar.get_y() + bar.get_height() / 2,
            str(value),
            va="center",
            fontsize=10.5,
            color=INK,
            fontweight="bold",
        )
    ax.set_xlim(0, max(values) * 1.16)
    ax.set_xlabel("Alertas deduplicadas")
    ax.tick_params(axis="y", labelsize=10)
    legend_handles = [
        Line2D([0], [0], marker="s", color="none", markerfacecolor=AMBER, markeredgecolor="none", markersize=10, label="Severidad HIGH"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor=CYAN, markeredgecolor="none", markersize=10, label="Severidad MEDIUM"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=2,
        fontsize=9.5,
        labelcolor=INK,
    )
    _frame(
        fig,
        title="Alertas AML por regla",
        subtitle="377 alertas deduplicadas · 12 reglas configuradas · 9 con coincidencias",
        source="Fuente: fact_alerts.csv. Corte 2026-10-29; R07, R10 y R11 sin alertas. No es el snapshot de 775 de Fase 5.",
    )
    fig.subplots_adjust(left=0.31, right=0.955, top=0.80, bottom=0.14)
    return _save(fig, "chart-alerts-by-rule.png")


def chart_rule_quality(data: Dataset) -> Path:
    rows = [row for row in data.eval_rules if row["rule_id"] in SHORT_RULES]
    rows.sort(key=lambda row: float(row["recall"]))
    labels = [f"{row['rule_id']} · {SHORT_RULES[str(row['rule_id'])]}" for row in rows]
    precision = [float(row["precision"]) * 100 for row in rows]
    recall = [float(row["recall"]) * 100 for row in rows]
    positions = list(range(len(rows)))
    height = 0.36

    fig, ax = plt.subplots(figsize=(10.67, 6))
    ax.grid(axis="x", alpha=0.55)
    ax.barh([p + height / 2 for p in positions], precision, height=height, color=CYAN, label="Precisión (etiquetadas)")
    ax.barh([p - height / 2 for p in positions], recall, height=height, color=TURQ, label="Recall (sospechosas)")
    ax.set_yticks(positions)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Porcentaje (%)")
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=2,
        fontsize=9.5,
        labelcolor=INK,
    )

    ax.text(
        0.985,
        0.93,
        "Global: recall 100 % · precisión 99,13 %\nsobre etiquetadas · 150 alertas sin etiqueta",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        color=INK,
        bbox={"boxstyle": "round,pad=0.5", "facecolor": NAVY, "edgecolor": GRID},
    )
    _frame(
        fig,
        title="Precisión y recall por regla",
        subtitle="Evaluación contra la verdad etiquetada de Fase 3 (341 sospechosas)",
        source="Fuente: evaluacion-verdad.md. Cada regla cubre un patrón específico; el recall individual es bajo por diseño.",
    )
    fig.subplots_adjust(left=0.31, right=0.955, top=0.80, bottom=0.14)
    return _save(fig, "chart-rule-quality.png")


def chart_confusion(data: Dataset) -> Path:
    fig, ax = plt.subplots(figsize=(10.67, 6))
    ax.set_axis_off()
    cells = [
        (0.06, 0.52, 0.42, 0.31, "Verdaderos positivos", "341", GREEN, "Sospechosa · alertada"),
        (0.54, 0.52, 0.42, 0.31, "Falsos positivos", "3", AMBER, "Normal · alertada"),
        (0.06, 0.14, 0.42, 0.31, "Falsos negativos", "0", RED, "Sospechosa · no alertada"),
        (0.54, 0.14, 0.42, 0.31, "Verdaderos negativos", "489", CYAN, "Normal · no alertada"),
    ]
    for x, y, width, height, label, value, color, detail in cells:
        ax.add_patch(
            Rectangle(
                (x, y),
                width,
                height,
                transform=ax.transAxes,
                facecolor=PANEL,
                edgecolor=color,
                linewidth=2.2,
            )
        )
        ax.text(x + 0.03, y + height - 0.05, label, transform=ax.transAxes, fontsize=13, color=color, fontweight="bold")
        ax.text(x + 0.03, y + height - 0.15, value, transform=ax.transAxes, fontsize=34, color=INK, fontweight="bold")
        ax.text(x + 0.03, y + 0.045, detail, transform=ax.transAxes, fontsize=10, color=MUTED)

    ax.text(0.06, 0.87, "Real: sospechosa", transform=ax.transAxes, fontsize=10.5, color=MUTED)
    ax.text(0.54, 0.87, "Real: normal (muestra)", transform=ax.transAxes, fontsize=10.5, color=MUTED)
    ax.text(0.02, 0.66, "Modelo\nalerta", transform=ax.transAxes, fontsize=10.5, color=MUTED, rotation=90, va="center")
    ax.text(0.02, 0.28, "Modelo\nno alerta", transform=ax.transAxes, fontsize=10.5, color=MUTED, rotation=90, va="center")
    ax.text(
        0.985,
        0.055,
        "150 alertas sin etiqueta quedan fuera de la matriz.\n"
        "Si se cuentan como FP, la precisión conservadora baja a 69,03 %.",
        transform=ax.transAxes,
        ha="right",
        fontsize=9.5,
        color=MUTED,
    )
    _frame(
        fig,
        title="Matriz de confusión AML",
        subtitle="Sobre 833 transacciones etiquetadas: 341 sospechosas y 492 normales muestreadas",
        source="Fuente: 07-aml-compliance/docs/evaluacion-verdad.md. La muestra normal es ~1 % del dataset (P-017).",
    )
    fig.subplots_adjust(left=0.075, right=0.955, top=0.80, bottom=0.14)
    return _save(fig, "chart-confusion-matrix.png")


def render_all(data: Dataset) -> list[Path]:
    _style()
    return [
        chart_daily_volume(data),
        chart_currency_mix(data),
        chart_latency(data),
        chart_alerts_by_rule(data),
        chart_rule_quality(data),
        chart_confusion(data),
    ]

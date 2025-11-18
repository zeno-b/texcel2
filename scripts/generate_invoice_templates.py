#!/usr/bin/env python3
"""Generate multiple styled invoice template variants."""
from __future__ import annotations

from pathlib import Path
from string import Template
import textwrap


BASE_HTML = Template(
    textwrap.dedent(
        """\
        <!doctype html>
        <html lang="nl-BE">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>$STYLE_NAME · Factuur {{InvoiceNumber}}</title>
          <style>
          $STYLE_CSS
          </style>
        </head>
        <body class="theme-$SLUG">
          <article class="page" aria-label="$STYLE_NAME invoice">
            <header class="hero" role="banner" aria-label="Invoice header">
              <div>
                <div class="hero__brand">
                  <div class="logo">
                    <span>{{CompanyShort}}</span>
                  </div>
                  <div class="org-block">
                    <div class="org-name">{{CompanyName}}</div>
                    <p class="subtle">{{CompanyAddress}} · BTW {{CompanyVAT}} · {{CompanyEmail}} · {{CompanyPhone}}</p>
                    <dl class="meta-list" aria-label="bedrijfsgegevens">
                      <div>
                        <dt>Factuurnummer</dt>
                        <dd>{{InvoiceNumber}}</dd>
                      </div>
                      <div>
                        <dt>Datum</dt>
                        <dd>{{InvoiceDate}}</dd>
                      </div>
                      <div>
                        <dt>Vervaldatum</dt>
                        <dd>{{DueDate}}</dd>
                      </div>
                      <div>
                        <dt>Valuta</dt>
                        <dd>{{Currency}}</dd>
                      </div>
                    </dl>
                  </div>
                </div>
              </div>
              <div class="hero__totals" aria-label="Invoice totals">
                <div class="hero__flag">Factuur</div>
                <article class="billto-card" aria-label="Bill to">
                  <div class="pill">Bill to</div>
                  <div class="stack">
                    <strong>{{ClientName}}</strong>
                    <span>{{ClientAddress}}</span>
                    <span>BTW {{ClientVAT}}</span>
                    <span>Contact {{ContactName}} · {{ContactEmail}}</span>
                    <span>PO {{PONumber}} · Ref {{AdditionalNumber}}</span>
                    <span>Contract {{ContractID}}</span>
                  </div>
                </article>
                <div class="stat-card" role="status" aria-live="polite">
                  <span>Totaal te betalen</span>
                  <strong>{{Currency}} {{Total}}</strong>
                  <small>Te betalen vóór {{DueDate}} · {{PaymentTerms}} dagen</small>
                </div>
              </div>
            </header>

            <section class="grid" aria-label="invoice details">
              <article class="card details-card">
                <div class="pill">Details</div>
                <div class="stack">
                  <span><strong>Resource:</strong> {{ResourceName}}</span>
                  <span><strong>End-Customer name:</strong> {{EndCustomer}}</span>
                  <span><strong>Mission:</strong> {{Mission}}</span>
                  <span><strong>Period:</strong> van {{PeriodStart}} tot {{PeriodEnd}}</span>
                  <span><strong>Reference:</strong> {{Reference}}</span>
                  <span><strong>Cost center:</strong> {{CostCenter}}</span>
                </div>
              </article>
            </section>

            <section class="table-card" aria-labelledby="invoice-lines">
              <header>
                <div class="pill" id="invoice-lines">Invoice lines</div>
                <p class="subtle">{{ConsultantName}} · Periode {{PeriodStart}} – {{PeriodEnd}}</p>
              </header>
              <div class="table-wrap">
                <table>
                  <colgroup>
                    <col style="width:40%" />
                    <col style="width:12%" />
                    <col style="width:18%" />
                    <col style="width:10%" />
                    <col style="width:20%" />
                  </colgroup>
                  <thead>
                    <tr>
                      <th>Omschrijving</th>
                      <th class="right">Hoeveelheid</th>
                      <th class="right">Tarief excl. btw ({{Currency}})</th>
                      <th class="right">BTW %</th>
                      <th class="right">Bedrag excl. btw ({{Currency}})</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td data-label="Omschrijving">{{ConsultantName}} — {{Mission}}</td>
                      <td class="right mono" data-label="Hoeveelheid">{{BaseQuantity}} {{RateUnit}}</td>
                      <td class="right mono" data-label="Tarief">{{Currency}} {{ChargeRate}} / {{RateUnit}}</td>
                      <td class="right mono" data-label="BTW">{{VATRate}}</td>
                      <td class="right mono" data-label="Bedrag">{{Currency}} {{BaseLineTotal}}</td>
                    </tr>
                    {{ExtrasRows}}
                  </tbody>
                </table>
              </div>
              <div class="totals-card" role="contentinfo" aria-label="Totals">
                <div class="row">
                  <span>Subtotaal</span>
                  <strong>{{Currency}} {{Subtotal}}</strong>
                </div>
                <div class="row">
                  <span>Totaal BTW</span>
                  <strong>{{Currency}} {{VATAmount}}</strong>
                </div>
                <div class="row grand">
                  <span>Totaal te betalen vóór {{DueDate}}</span>
                  <strong>{{Currency}} {{Total}}</strong>
                </div>
              </div>
            </section>

            <section class="info-grid" aria-label="payment and notes">
              <article class="card">
                <div class="pill">Betalingsinformatie</div>
                <div class="stack">
                  <span><strong>IBAN</strong> · <span class="mono">{{BankIBAN}}</span></span>
                  <span><strong>BIC</strong> · <span class="mono">{{BankBIC}}</span></span>
                  <span><strong>Mededeling / Ref</strong> · <span class="mono">{{StructuredReference}}</span></span>
                  <span><strong>Banknaam</strong> · {{BankName}}</span>
                  <span><strong>Betalen aan</strong> · {{CompanyName}}</span>
                </div>
              </article>
              <article class="card">
                <div class="pill">Opmerkingen & voorwaarden</div>
                <div class="notes">
                  <p>{{Notes}}</p>
                  <p>{{ReverseChargeNote}}</p>
                </div>
              </article>
            </section>

            <footer>
              <div>Gegenereerd {{InvoiceDate}} · Valuta {{Currency}}</div>
              <div>Factuur {{InvoiceNumber}} · Pagina 1 van 1</div>
            </footer>
            <div class="no-print">
              Print of exporteer naar PDF vanuit uw browser voor een productieklare factuur.
            </div>
          </article>
        </body>
        </html>
        """
    )
)

BASE_CSS = Template(
    textwrap.dedent(
        """\
        :root {
          color-scheme: $color_scheme;
          font-size: 15px;
          --font-sans: $font_sans;
          --font-mono: $font_mono;
        }
        *,
        *::before,
        *::after {
          box-sizing: border-box;
        }
        body {
          margin: 0;
          background: $body_bg;
          color: $text_primary;
          font-family: var(--font-sans);
          line-height: 1.6;
          -webkit-font-smoothing: antialiased;
        }
        h1,
        h2,
        h3,
        h4 {
          margin: 0;
          font-weight: 600;
          color: inherit;
        }
        h3 {
          font-size: 0.85rem;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          color: $text_muted;
        }
        p {
          margin: 0;
        }
        a {
          color: $accent;
          text-decoration: none;
        }
        a:hover {
          text-decoration: underline;
        }
        .page {
          max-width: 1020px;
          margin: clamp(12px, 4vw, 72px) auto;
          padding: clamp(28px, 4vw, 72px);
          background: $surface;
          border-radius: $radius;
          border: $page_border;
          box-shadow: $shadow;
          display: flex;
          flex-direction: column;
          gap: 36px;
        }
        header.hero {
          background: $hero_bg;
          border: $hero_border;
          border-radius: $radius;
          padding: clamp(24px, 4vw, 48px);
          display: grid;
          grid-template-columns: minmax(0, 2fr) minmax(260px, 1fr);
          gap: clamp(20px, 3vw, 32px);
          align-items: flex-start;
          color: $hero_text;
          position: relative;
        }
        .hero__brand {
          display: flex;
          flex-direction: column;
          gap: 18px;
        }
        .logo {
          min-height: 72px;
          border-radius: calc($radius / 2);
          border: $logo_border;
          background: $logo_bg;
          color: $logo_text;
          font-weight: 700;
          letter-spacing: 0.18em;
          display: grid;
          place-items: center;
          text-transform: uppercase;
        }
        .org-name {
          font-size: clamp(1.4rem, 2.4vw, 2rem);
        }
        .subtle {
          color: $text_muted;
        }
        .meta-list {
          margin-top: 16px;
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
          gap: 10px 20px;
        }
        .meta-list dt {
          font-size: 0.75rem;
          letter-spacing: 0.16em;
          text-transform: uppercase;
          color: $text_muted;
        }
        .meta-list dd {
          margin: 0;
          font-family: var(--font-mono);
          font-size: 0.98rem;
        }
        .hero__totals {
          display: flex;
          flex-direction: column;
          gap: 18px;
          align-items: flex-end;
        }
        .hero__flag {
          font-size: clamp(2.2rem, 5vw, 3.4rem);
          letter-spacing: 0.2em;
          text-transform: uppercase;
          font-weight: 700;
          color: $hero_flag;
        }
        .billto-card {
          width: 100%;
          padding: 18px;
          border-radius: $radius;
          background: $surface_alt;
          border: 1px solid $line;
        }
        .pill {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 0.78rem;
          letter-spacing: 0.18em;
          text-transform: uppercase;
          padding: 6px 14px;
          border-radius: 999px;
          background: $pill_bg;
          color: $pill_text;
          font-weight: 600;
        }
        .stack {
          margin-top: 12px;
          display: grid;
          gap: 6px;
          font-size: 0.95rem;
          color: inherit;
        }
        .stat-card {
          width: 100%;
          padding: 20px;
          border-radius: $radius;
          background: $stat_bg;
          border: $stat_border;
          color: $stat_text;
          box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }
        .stat-card span {
          font-size: 0.78rem;
          letter-spacing: 0.14em;
          text-transform: uppercase;
          color: inherit;
        }
        .stat-card strong {
          display: block;
          font-size: 1.8rem;
          font-family: var(--font-mono);
          letter-spacing: -0.02em;
          color: $stat_accent;
        }
        .stat-card small {
          color: inherit;
          font-size: 0.85rem;
        }
        .grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
          gap: 24px;
        }
        .card {
          border-radius: $radius;
          border: 1px solid $line;
          background: $surface_alt;
          padding: 24px;
        }
        .details-card {
          max-width: 520px;
        }
        .chip-group span {
          background: $chip_bg;
          border-radius: 12px;
          padding: 6px 12px;
        }
        .table-card {
          border-radius: $radius;
          border: 1px solid $line;
          background: $surface_alt;
          padding: 0 0 12px;
        }
        .table-card header {
          padding: 24px;
          border-bottom: 1px solid $line;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          font-size: 0.95rem;
        }
        thead {
          background: $table_header_bg;
          color: $table_header_text;
        }
        th,
        td {
          padding: 14px 20px;
          border-bottom: $table_border;
        }
        th {
          text-align: left;
          font-size: 0.72rem;
          letter-spacing: 0.15em;
          text-transform: uppercase;
        }
        tbody tr:nth-child(even) {
          background: $table_row_alt;
        }
        td.right,
        th.right {
          text-align: right;
        }
        td.mono {
          font-family: var(--font-mono);
          letter-spacing: -0.01em;
        }
        .totals-card {
          padding: 24px;
          display: grid;
          gap: 12px;
          background: $surface;
        }
        .totals-card .row {
          display: grid;
          grid-template-columns: 1fr auto;
          align-items: baseline;
          gap: 16px;
        }
        .totals-card span {
          font-size: 0.82rem;
          letter-spacing: 0.12em;
          text-transform: uppercase;
          color: $text_muted;
        }
        .totals-card strong {
          font-family: var(--font-mono);
          font-size: 1rem;
        }
        .totals-card .grand {
          padding-top: 12px;
          border-top: 1px solid $line;
        }
        .totals-card .grand strong {
          font-size: 1.4rem;
          color: $accent;
        }
        .info-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
          gap: 24px;
        }
        .notes {
          margin-top: 12px;
          font-size: 0.92rem;
          color: $text_muted;
        }
        footer {
          border-top: 1px solid $line;
          padding-top: 18px;
          display: flex;
          flex-wrap: wrap;
          justify-content: space-between;
          gap: 12px;
          font-size: 0.82rem;
          color: $text_muted;
        }
        .no-print {
          text-align: center;
          font-size: 0.82rem;
          color: $text_muted;
        }
        @media (max-width: 720px) {
          header.hero {
            grid-template-columns: 1fr;
          }
          .hero__totals {
            align-items: flex-start;
          }
          th,
          td {
            padding: 12px 14px;
          }
        }
        @media (max-width: 560px) {
          thead {
            display: none;
          }
          table tbody tr {
            display: grid;
            grid-template-columns: 1fr;
            gap: 6px;
            padding: 14px;
            border-bottom: $table_border;
          }
          table tbody td {
            border: 0;
            padding: 0;
          }
          table tbody td::before {
            content: attr(data-label);
            display: block;
            font-size: 0.7rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: $text_muted;
            margin-bottom: 2px;
          }
          table tbody td.right {
            text-align: left;
          }
        }
        @media print {
          body {
            background: #fff;
          }
          .page {
            box-shadow: none;
            border: none;
            margin: 0;
            padding: 12mm;
          }
        }
        $extra_css
        """
    )
)


def clamp(value: float, minimum: float = 0.0, maximum: float = 255.0) -> float:
    return max(minimum, min(maximum, value))


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    if len(color) == 3:
        color = "".join(ch * 2 for ch in color)
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        int(clamp(round(rgb[0]))),
        int(clamp(round(rgb[1]))),
        int(clamp(round(rgb[2]))),
    )


def mix(color_a: str, color_b: str, weight: float) -> str:
    weight = clamp(weight, 0.0, 1.0)
    ra, ga, ba = hex_to_rgb(color_a)
    rb, gb, bb = hex_to_rgb(color_b)
    return rgb_to_hex((ra * (1 - weight) + rb * weight, ga * (1 - weight) + gb * weight, ba * (1 - weight) + bb * weight))


def lighten(color: str, amount: float) -> str:
    return mix(color, "#ffffff", amount)


def darken(color: str, amount: float) -> str:
    return mix(color, "#000000", amount)


def as_rgba(color: str, alpha: float) -> str:
    r, g, b = hex_to_rgb(color)
    return f"rgba({int(r)}, {int(g)}, {int(b)}, {alpha})"


def soften(color: str) -> str:
    return lighten(color, 0.7)


STYLE_OVERRIDES: dict[str, callable] = {}


def register_style(name: str):
    def decorator(func):
        STYLE_OVERRIDES[name] = func
        return func

    return decorator


@register_style("minimal-border")
def _style_minimal(slug: str, palette: dict) -> str:
    return textwrap.dedent(
        f"""\
        body.theme-{slug} .page {{
          border-left: 8px solid {palette['accent']};
        }}
        body.theme-{slug} .hero__flag {{
          letter-spacing: 0.3em;
        }}
        """
    )


@register_style("double-frame")
def _style_double(slug: str, palette: dict) -> str:
    palette["radius"] = "0px"
    palette["page_border"] = f"6px double {palette['accent']}"
    palette["hero_border"] = f"3px double {palette['accent']}"
    return textwrap.dedent(
        f"""\
        body.theme-{slug} .table-card {{
          border-width: 2px;
        }}
        """
    )


@register_style("gradient-panel")
def _style_gradient(slug: str, palette: dict) -> str:
    palette["hero_bg"] = f"linear-gradient(135deg, {lighten(palette['accent'], 0.85)}, {lighten(palette['accent'], 0.65)})"
    return textwrap.dedent(
        f"""\
        body.theme-{slug} header.hero::after {{
          content: "";
          position: absolute;
          inset: 12px;
          border: 1px dashed {soften(palette['accent'])};
          border-radius: calc({palette['radius']} / 1.4);
          pointer-events: none;
        }}
        """
    )


@register_style("ledger-pillars")
def _style_pillars(slug: str, palette: dict) -> str:
    return textwrap.dedent(
        f"""\
        body.theme-{slug} header.hero {{
          border-left: 10px solid {palette['accent']};
          border-right: 10px solid {palette['accent']};
        }}
        """
    )


@register_style("ribbon-top")
def _style_ribbon(slug: str, palette: dict) -> str:
    return textwrap.dedent(
        f"""\
        body.theme-{slug} .page {{
          border-top: 12px solid {palette['accent']};
        }}
        """
    )


@register_style("dark-glow")
def _style_glow(slug: str, palette: dict) -> str:
    return textwrap.dedent(
        f"""\
        body.theme-{slug} .page {{
          backdrop-filter: blur(14px);
        }}
        body.theme-{slug} table tbody tr:hover {{
          background: {as_rgba(palette['accent'], 0.08)};
        }}
        """
    )


@register_style("dashed-ledger")
def _style_dashed(slug: str, palette: dict) -> str:
    palette["page_border"] = f"4px dashed {palette['accent']}"
    palette["hero_border"] = f"3px dotted {palette['accent']}"
    palette["table_border"] = f"2px dotted {soften(palette['accent'])}"
    return ""


@register_style("print")
def _style_print(slug: str, palette: dict) -> str:
    palette["shadow"] = "none"
    palette["body_bg"] = "#ffffff"
    palette["surface"] = "#ffffff"
    palette["surface_alt"] = "#ffffff"
    palette["page_border"] = "2px solid #000000"
    palette["hero_border"] = "1px solid #000000"
    palette["line"] = "#000000"
    palette["table_border"] = "1px solid #000000"
    return textwrap.dedent(
        f"""\
        body.theme-{slug} * {{
          box-shadow: none !important;
        }}
        """
    )


@register_style("blueprint")
def _style_blueprint(slug: str, palette: dict) -> str:
    grid_color = as_rgba(palette["accent"], 0.08)
    return textwrap.dedent(
        f"""\
        body.theme-{slug} .page {{
          background-image: linear-gradient({grid_color} 1px, transparent 1px), linear-gradient(90deg, {grid_color} 1px, transparent 1px);
          background-size: 28px 28px;
        }}
        """
    )


@register_style("glass")
def _style_glass(slug: str, palette: dict) -> str:
    palette["surface"] = as_rgba(palette["surface"], 0.9)
    palette["surface_alt"] = as_rgba(palette["surface_alt"], 0.85)
    palette["page_border"] = as_rgba("#ffffff", 0.08)
    return textwrap.dedent(
        f"""\
        body.theme-{slug} .page {{
          backdrop-filter: blur(20px);
        }}
        """
    )


@register_style("accent-bottom")
def _style_bottom(slug: str, palette: dict) -> str:
    return textwrap.dedent(
        f"""\
        body.theme-{slug} .page {{
          border-bottom: 10px solid {palette['accent']};
        }}
        """
    )


@register_style("banded-hero")
def _style_banded(slug: str, palette: dict) -> str:
    return textwrap.dedent(
        f"""\
        body.theme-{slug} header.hero {{
          background-image: repeating-linear-gradient(135deg, {as_rgba(palette['accent'], 0.08)} 0, {as_rgba(palette['accent'], 0.08)} 10px, transparent 10px, transparent 20px);
        }}
        """
    )


def main() -> None:
    """Entry point."""
    output_dir = Path("invoice_templates")
    output_dir.mkdir(exist_ok=True)
    # Theme data and palette generation will be added here.
    raise NotImplementedError("Theme generation not implemented yet")


if __name__ == "__main__":
    main()

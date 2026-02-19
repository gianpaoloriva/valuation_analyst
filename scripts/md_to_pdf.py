"""Converte i report markdown in PDF con layout professionale.

Uso:
    python scripts/md_to_pdf.py                    # Tutti i report
    python scripts/md_to_pdf.py GOOGL MSFT         # Solo specifici
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "report"
PDF_DIR = REPORT_DIR / "pdf"

# ---------------------------------------------------------------------------
# Palette colori
# ---------------------------------------------------------------------------
NAVY = (15, 32, 65)           # Titoli, header tabelle
DARK_BLUE = (25, 55, 109)     # H2
STEEL = (55, 80, 120)         # H3
LIGHT_BG = (240, 244, 250)    # Sfondo righe alternate tabella
WHITE = (255, 255, 255)
ACCENT = (0, 120, 180)        # Linee decorative
GREY_TEXT = (80, 80, 80)      # Testo corpo
LIGHT_GREY = (200, 200, 200)  # Bordi sottili

# Colori raccomandazione
REC_COLORS = {
    "BUY": (16, 124, 65),
    "MODERATE BUY": (40, 167, 69),
    "HOLD": (255, 165, 0),
    "MODERATE SELL": (220, 120, 50),
    "SELL": (200, 50, 50),
    "STRONG SELL": (160, 20, 20),
}


def _clean(text: str) -> str:
    """Rimuove markup markdown e caratteri non-latin1."""
    text = (text
            .replace("\u2018", "'").replace("\u2019", "'")
            .replace("\u2013", "-").replace("\u2014", "--")
            .replace("\u2022", "-"))
    # Block chars per istogramma ASCII
    for ch in "\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581":
        text = text.replace(ch, "#")
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _strip_bold(text: str) -> tuple[str, bool]:
    """Restituisce (testo_pulito, era_bold)."""
    t = text.strip()
    is_bold = t.startswith("**") and t.endswith("**")
    clean = t.replace("**", "").replace("*", "").replace("`", "")
    return _clean(clean), is_bold


class ReportPDF(FPDF):
    """PDF con header e footer brandizzati."""

    _ticker: str = ""
    _company: str = ""
    _report_date: str = ""

    def header(self):
        if self.page_no() == 1:
            return  # La copertina ha il suo layout
        # Barra superiore
        self.set_fill_color(*NAVY)
        self.rect(0, 0, self.w, 12, "F")
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*WHITE)
        self.set_xy(self.l_margin, 3)
        self.cell(0, 6,
                  f"VALUATION REPORT  |  {self._ticker}  |  {self._report_date}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*GREY_TEXT)
        self.set_y(16)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*LIGHT_GREY)
        self.cell(0, 10,
                  f"Valuation Analyst Multi-Agent System  -  Pagina {self.page_no() - 1}",
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        self.set_text_color(*GREY_TEXT)


def _draw_cover(pdf: ReportPDF, lines: list[str]) -> int:
    """Disegna la pagina di copertina e restituisce l'indice della prima riga dopo l'header."""
    # Sfondo blu scuro in alto (60% della pagina)
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, 180, "F")

    # Linea accent
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(1.2)
    pdf.line(20, 170, pdf.w - 20, 170)

    # Estrai info dall'header markdown
    title = ""
    meta: dict[str, str] = {}
    skip_until = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("# "):
            title = s[2:]
            skip_until = i + 1
        elif s.startswith("**") and ":**" in s:
            # es. "**Data:** 2026-02-19"
            match = re.match(r"\*\*(.+?):\*\*\s*(.*)", s)
            if match:
                meta[match.group(1)] = match.group(2)
            skip_until = i + 1
        elif s == "---":
            skip_until = i + 1
            break
        elif s == "" and skip_until > 0:
            continue
        elif skip_until > 0:
            break

    # Ticker grande
    ticker = pdf._ticker
    pdf.set_font("Helvetica", "B", 72)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 40)
    pdf.cell(0, 30, ticker, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Titolo azienda
    company = title.replace(f"({ticker})", "").replace("Report di Valutazione -", "").strip()
    pdf._company = company
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(180, 200, 230)
    pdf.set_xy(20, 78)
    pdf.cell(0, 10, _clean(company), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Sottotitolo
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 100)
    pdf.cell(0, 10, "REPORT DI VALUTAZIONE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Linea decorativa piccola
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.6)
    pdf.line(20, 116, 80, 116)

    # Metadati
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(200, 210, 230)
    y = 125
    for key in ["Data", "Analista", "Metodologia"]:
        if key in meta:
            pdf.set_xy(20, y)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(30, 7, _clean(key + ":"),
                     new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(0, 7, _clean(meta[key]),
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            y += 12

    # Area bianca in basso
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*STEEL)
    pdf.set_xy(20, 192)
    pdf.cell(0, 6, "Metodologie Damodaran (NYU Stern)  |  DCF  |  Multipli  |  Monte Carlo",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_text_color(*GREY_TEXT)
    return skip_until


def _draw_section_header(pdf: ReportPDF, text: str) -> None:
    """H2: barra colorata con titolo bianco."""
    pdf.ln(6)
    y = pdf.get_y()
    if y > pdf.h - 35:
        pdf.add_page()
        y = pdf.get_y()
    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(pdf.l_margin, y, pdf.w - pdf.l_margin - pdf.r_margin, 9, "F")
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(pdf.l_margin + 3, y + 1)
    txt, _ = _strip_bold(text)
    pdf.cell(0, 7, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*GREY_TEXT)
    pdf.ln(3)


def _draw_subsection_header(pdf: ReportPDF, text: str) -> None:
    """H3: testo colorato con linea sotto."""
    pdf.ln(4)
    txt, _ = _strip_bold(text)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*STEEL)
    pdf.cell(0, 6, txt, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    y = pdf.get_y()
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, y, pdf.l_margin + 60, y)
    pdf.set_draw_color(*LIGHT_GREY)
    pdf.set_text_color(*GREY_TEXT)
    pdf.ln(2)

    # Controlla se e' la raccomandazione
    for rec_key, rec_color in REC_COLORS.items():
        if rec_key in txt.upper() and "RACCOMANDAZIONE" in txt.upper():
            _draw_recommendation_badge(pdf, rec_key, rec_color)
            break


def _draw_recommendation_badge(pdf: ReportPDF, label: str, color: tuple) -> None:
    """Disegna un badge colorato per la raccomandazione."""
    pdf.ln(2)
    y = pdf.get_y()
    badge_w = 50
    badge_h = 12
    x = pdf.l_margin
    # Sfondo badge
    pdf.set_fill_color(*color)
    pdf.rect(x, y, badge_w, badge_h, "F")
    # Testo badge
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(x, y + 1)
    pdf.cell(badge_w, badge_h - 1, label, align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*GREY_TEXT)
    pdf.ln(4)


def _flush_table(pdf: ReportPDF, rows: list[list[str]]) -> None:
    """Tabella con header colorato e righe alternate."""
    if not rows:
        return
    header = rows[0]
    data = [r for r in rows[1:]
            if not all(c.strip().replace("-", "").replace(":", "") == "" for c in r)]

    n_cols = len(header)
    page_w = pdf.w - pdf.l_margin - pdf.r_margin
    col_w = page_w / n_cols

    # Controlla se serve un page break
    needed_h = (len(data) + 1) * 5.5 + 8
    if pdf.get_y() + needed_h > pdf.h - 25:
        pdf.add_page()

    # Header
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7.5)
    for cell_text in header:
        txt, _ = _strip_bold(cell_text)
        pdf.cell(col_w, 6.5, txt, border=0, align="C",
                 new_x=XPos.RIGHT, new_y=YPos.TOP, fill=True)
    pdf.ln()

    # Righe dati
    pdf.set_text_color(*GREY_TEXT)
    for row_idx, row in enumerate(data):
        # Righe alternate
        if row_idx % 2 == 0:
            pdf.set_fill_color(*LIGHT_BG)
        else:
            pdf.set_fill_color(*WHITE)

        for i, cell_text in enumerate(row):
            txt, is_bold = _strip_bold(cell_text)
            pdf.set_font("Helvetica", "B" if is_bold else "", 7.5)
            align = "L" if i == 0 else "R"
            pdf.cell(col_w, 5, txt, border=0, align=align,
                     new_x=XPos.RIGHT, new_y=YPos.TOP, fill=True)
        pdf.ln()

    # Linea sotto la tabella
    y = pdf.get_y()
    pdf.set_draw_color(*LIGHT_GREY)
    pdf.set_line_width(0.2)
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(4)


def md_to_pdf(md_path: Path, pdf_path: Path) -> None:
    """Converte un file markdown in PDF con layout professionale."""
    lines = md_path.read_text(encoding="utf-8").splitlines()

    # Estrai ticker dal nome file
    ticker = md_path.name.split("_")[0]

    pdf = ReportPDF(orientation="P", unit="mm", format="A4")
    pdf._ticker = ticker
    pdf._report_date = md_path.name.split("_")[-1].replace(".md", "")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(left=18, top=18, right=18)

    # --- Copertina ---
    pdf.add_page()
    start_line = _draw_cover(pdf, lines)

    # --- Pagine contenuto ---
    pdf.add_page()

    in_code_block = False
    table_rows: list[list[str]] = []
    in_table = False

    for line in lines[start_line:]:
        # --- Code blocks ---
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                # Sfondo grigio per code block
                pdf.ln(1)
            else:
                in_code_block = False
                pdf.ln(3)
            continue
        if in_code_block:
            pdf.set_fill_color(245, 245, 248)
            pdf.set_font("Courier", "", 6.5)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 3.5, _clean(line), new_x=XPos.LMARGIN, new_y=YPos.NEXT,
                     fill=True)
            pdf.set_text_color(*GREY_TEXT)
            continue

        # --- Tables ---
        stripped = line.strip()
        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(c.replace("-", "").replace(":", "") == "" for c in cells):
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            _flush_table(pdf, table_rows)
            in_table = False
            table_rows = []

        # --- Reset X ---
        pdf.set_x(pdf.l_margin)

        # --- Empty line ---
        if not stripped:
            pdf.ln(2)
            continue

        # --- H2: Section header ---
        if stripped.startswith("## "):
            _draw_section_header(pdf, stripped[3:])
            continue

        # --- H3: Subsection ---
        if stripped.startswith("### "):
            _draw_subsection_header(pdf, stripped[4:])
            continue

        # --- H1 (skip, gia' nella copertina) ---
        if stripped.startswith("# "):
            continue

        # --- Horizontal rule ---
        if stripped == "---":
            y = pdf.get_y()
            pdf.set_draw_color(*LIGHT_GREY)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(3)
            continue

        # --- Bullet points ---
        if stripped.startswith("- "):
            txt, is_bold = _strip_bold(stripped[2:])
            pdf.set_font("Helvetica", "B" if is_bold else "", 8.5)
            indent = 6
            pdf.set_x(pdf.l_margin + indent)
            w = pdf.w - pdf.l_margin - pdf.r_margin - indent
            # Pallino accent
            pdf.set_fill_color(*ACCENT)
            bullet_y = pdf.get_y() + 1.8
            pdf.circle(pdf.get_x() - 3, bullet_y, 0.8, "F")
            pdf.multi_cell(w, 4.5, txt)
            continue

        # --- Blockquote ---
        if stripped.startswith("> "):
            txt, _ = _strip_bold(stripped[2:])
            indent = 5
            # Barra laterale accent
            y_start = pdf.get_y()
            pdf.set_x(pdf.l_margin + indent + 3)
            w = pdf.w - pdf.l_margin - pdf.r_margin - indent - 3
            pdf.set_font("Helvetica", "I", 8.5)
            pdf.set_text_color(*STEEL)
            pdf.multi_cell(w, 4.5, txt)
            y_end = pdf.get_y()
            pdf.set_draw_color(*ACCENT)
            pdf.set_line_width(0.8)
            pdf.line(pdf.l_margin + indent, y_start, pdf.l_margin + indent, y_end)
            pdf.set_draw_color(*LIGHT_GREY)
            pdf.set_text_color(*GREY_TEXT)
            pdf.ln(2)
            continue

        # --- Bold label line (es. "**Formula:** ...") ---
        if stripped.startswith("**") and ":**" in stripped:
            match = re.match(r"\*\*(.+?):\*\*\s*(.*)", stripped)
            if match:
                label = _clean(match.group(1) + ":")
                value = _clean(match.group(2).replace("**", "").replace("*", "").replace("`", ""))
                pdf.set_font("Helvetica", "B", 8.5)
                pdf.cell(pdf.get_string_width(label) + 2, 5, label,
                         new_x=XPos.RIGHT, new_y=YPos.TOP)
                pdf.set_font("Helvetica", "", 8.5)
                pdf.multi_cell(0, 5, value)
                continue

        # --- Regular text ---
        txt, is_bold = _strip_bold(stripped)
        pdf.set_font("Helvetica", "B" if is_bold else "", 8.5)
        pdf.multi_cell(0, 4.5, txt)

    # Flush remaining table
    if in_table:
        _flush_table(pdf, table_rows)

    pdf.output(str(pdf_path))


def main() -> None:
    tickers = [t.upper() for t in sys.argv[1:]] if len(sys.argv) > 1 else []

    md_files = sorted(REPORT_DIR.glob("*_valuation_report_*.md"))
    if tickers:
        md_files = [f for f in md_files if any(f.name.startswith(t) for t in tickers)]

    if not md_files:
        print("Nessun report .md trovato in report/")
        sys.exit(1)

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for md_file in md_files:
        pdf_file = PDF_DIR / md_file.with_suffix(".pdf").name
        md_to_pdf(md_file, pdf_file)
        size = pdf_file.stat().st_size
        print(f"report/pdf/{pdf_file.name} ({size:,} bytes)")


if __name__ == "__main__":
    main()

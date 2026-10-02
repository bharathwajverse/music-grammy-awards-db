#!/usr/bin/env python3
"""
=============================================================================
Phase 30 Artifact Generator: Viva Voce Defense Preparation Handbook (PDF)
=============================================================================
Course: Advanced Database Management Systems (ADBMS) — Graduate Capstone
Target File: docs/viva-preparation.pdf
Source File: docs/viva-preparation.md

Generates an academic handbook PDF containing:
- Title Cover Page with dynamically parsed executive metadata block
- Table of Contents parsed from source markdown
- Five-Member Responsibility & Defense Matrix table parsed from source markdown
- 230 Project-Grounded Questions across 13 Categories
- Distinct question styling, clear formatted answers
- Dedicated syntax-highlighted code block boxes for JSON / SQL / scripts
- Clean LaTeX mathematical symbol rendering (Armstrong Axioms, Relational Algebra)
- Two-pass NumberedCanvas for "Page X of Y" and running headers/footers
=============================================================================
"""

import os
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
    Preformatted,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE_MD = REPO_ROOT / "docs" / "viva-preparation.md"
OUTPUT_PDF = REPO_ROOT / "docs" / "viva-preparation.pdf"

# Color Palette: Academic Grammy Gold & Slate
COLOR_NAVY = colors.HexColor("#0f172a")       # Slate-900
COLOR_DARK_SLATE = colors.HexColor("#1e293b") # Slate-800
COLOR_GOLD = colors.HexColor("#d4af37")       # Grammy Gold
COLOR_GOLD_DARK = colors.HexColor("#b8860b")  # Dark Goldenrod
COLOR_SILVER = colors.HexColor("#64748b")     # Slate-500
COLOR_LIGHT_BG = colors.HexColor("#f8fafc")   # Slate-50
COLOR_BORDER = colors.HexColor("#e2e8f0")     # Slate-200
COLOR_ROW_ALT = colors.HexColor("#f1f5f9")    # Slate-100
COLOR_CODE = colors.HexColor("#0369a1")       # Sky-700
COLOR_CODE_BG = colors.HexColor("#f8fafc")    # Slate-50 for code container

# Font Registration & Fallbacks
HAS_SEGOE_SYM = False
FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"
FONT_CODE = "Courier"
FONT_CODE_BOLD = "Courier-Bold"

try:
    if os.path.exists("C:/Windows/Fonts/seguisym.ttf"):
        pdfmetrics.registerFont(TTFont("SegoeUISymbol", "C:/Windows/Fonts/seguisym.ttf"))
        HAS_SEGOE_SYM = True
except Exception:
    HAS_SEGOE_SYM = False


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to calculate total page count and draw running headers/footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Suppress header and footer on cover page (page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_SILVER)

        page_w = 8.5 * inch
        margin_x = 54

        # Running Top Header
        self.drawString(margin_x, 11 * inch - 36, "GRAMMY Awards DBMS Capstone  |  Comprehensive Viva Voce Examination Handbook")
        self.setStrokeColor(COLOR_GOLD)
        self.setLineWidth(0.75)
        self.line(margin_x, 11 * inch - 42, page_w - margin_x, 11 * inch - 42)

        # Running Bottom Footer
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(margin_x, 48, page_w - margin_x, 48)

        self.drawString(margin_x, 34, "Advanced Database Management Systems (ADBMS) — Graduate Capstone  •  October 2026")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(page_w - margin_x, 34, page_str)
        self.restoreState()


def clean_markdown_to_xml(text: str) -> str:
    """Translates Markdown formatting and LaTeX mathematical symbols to safe ReportLab XML tags."""
    if not text:
        return ""

    # 1. Protect intentional line breaks
    text = re.sub(r"<br\s*/?>", "@@BR@@", text, flags=re.IGNORECASE)

    # 2. Escape raw XML entities
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # 3. Restore intentional line breaks
    text = text.replace("@@BR@@", "<br/>")

    # 4. Handle LaTeX escaped characters
    text = text.replace(r"\_", "_")
    text = text.replace(r"\%", "%")
    text = text.replace(r"\{", "{").replace(r"\}", "}")

    # 5. Handle \text{...} and \mathcal{...} BEFORE \frac to prevent nested brace issues
    text = re.sub(r"\\text\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\mathcal\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"(\1 / \2)", text)

    # Math Symbols
    bowtie_repr = '<font name="SegoeUISymbol">⋈</font>' if HAS_SEGOE_SYM else "[⋈ JOIN]"
    twohead_repr = '<font name="SegoeUISymbol">↠</font>' if HAS_SEGOE_SYM else "↠"
    models_repr = '<font name="SegoeUISymbol">⊨</font>' if HAS_SEGOE_SYM else "|="
    oplus_repr = '<font name="SegoeUISymbol">⊕</font>' if HAS_SEGOE_SYM else "(+)"

    math_symbols = [
        (r"\bowtie", bowtie_repr),
        (r"\twoheadrightarrow", twohead_repr),
        (r"\models", models_repr),
        (r"\oplus", oplus_repr),
        (r"\rightarrow", "→"),
        (r"\implies", "⇒"),
        (r"\equiv", "≡"),
        (r"\subseteq", "⊆"),
        (r"\supseteq", "⊇"),
        (r"\subset", "⊂"),
        (r"\cup", "∪"),
        (r"\cap", "∩"),
        (r"\wedge", "∧"),
        (r"\vee", "∨"),
        (r"\approx", "≈"),
        (r"\pi", "π"),
        (r"\sigma", "σ"),
        (r"\div", "÷"),
        (r"\times", "×"),
        (r"\ge", "≥"),
        (r"\le", "≤"),
        (r"\in", "∈"),
        (r"\mu", "μ"),
        (r"\dots", "..."),
    ]
    for cmd, sym in math_symbols:
        text = text.replace(cmd, sym)

    # Subscripts & superscripts in math
    text = re.sub(r"_\{([^}]+)\}", r"<sub>\1</sub>", text)
    text = re.sub(r"(?<=[a-zA-Z])_([0-9ijkmn])\b", r"<sub>\1</sub>", text)
    text = re.sub(r"\^\{([^}]+)\}", r"<sup>\1</sup>", text)
    text = re.sub(r"\^([a-zA-Z0-9+])", r"<sup>\1</sup>", text)

    # Remove remaining dollar signs from math mode
    text = text.replace("$", "")

    # 5. Handle Markdown links: [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # 6. Handle code spans: `code`
    text = re.sub(r"`([^`]+)`", r'<font name="Courier" color="#0369a1"><b>\1</b></font>', text)

    # 7. Handle bold text: **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

    # 8. Handle italic text: *text* (excluding already formatted bold)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)

    return text


def create_code_block_flowable(code_content: str, language: str = "") -> Table:
    """Wraps preformatted source code in an executive padded, bordered syntax container."""
    # Clean language identifier if first line is purely language name (e.g. ```json)
    code_lines = code_content.strip().splitlines()
    if code_lines and code_lines[0].strip().lower() in ["json", "python", "javascript", "js", "bash", "sh", "sql"]:
        code_lines = code_lines[1:]
    clean_code = "\n".join(code_lines)

    # Escape XML
    safe_code = clean_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    code_style = ParagraphStyle(
        "PreformattedCode",
        fontName="Courier",
        fontSize=8,
        leading=10.5,
        textColor=COLOR_NAVY,
    )

    p = Preformatted(safe_code, code_style)
    tbl = Table([[p]], colWidths=[504])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_ROW_ALT),
        ("BOX", (0, 0), (-1, -1), 0.8, COLOR_GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return tbl


def parse_metadata_from_md(raw_content: str):
    """Dynamically parses the executive metadata block from the top blockquote."""
    metadata = []
    lines = raw_content.splitlines()
    for line in lines[:25]:
        line = line.strip()
        m = re.match(r"^>\s*\*\*([^*]+)\*\*:\s*(.+)$", line)
        if m:
            key, val = m.group(1).strip(), m.group(2).strip()
            # Clean markdown formatting from key and value
            val = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", val)
            metadata.append((key, val))
    return metadata


def parse_toc_from_md(raw_content: str):
    """Dynamically parses Table of Contents items from the source markdown."""
    toc_items = []
    in_toc = False
    for line in raw_content.splitlines():
        line = line.strip()
        if line.startswith("# Table of Contents"):
            in_toc = True
            continue
        if in_toc:
            if line.startswith("---") or line.startswith("# Five-Member"):
                break
            m = re.match(r"^(\d+)\.\s*\[([^\]]+)\]", line)
            if m:
                num = m.group(1)
                title = m.group(2)
                toc_items.append((num, title))
    return toc_items


def parse_matrix_table_from_md(raw_content: str):
    """Dynamically parses the Five-Member Responsibility Matrix table from source markdown."""
    matrix_rows = []
    in_matrix = False
    for line in raw_content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# Five-Member Viva Responsibility & Defense Matrix"):
            in_matrix = True
            continue
        if in_matrix:
            if stripped.startswith("---") or stripped.startswith("# Section"):
                break
            if stripped.startswith("|"):
                # Check if it's separator row
                if re.match(r"^\|\s*:?---", stripped):
                    continue
                # Split cells
                parts = [c.strip() for c in stripped.strip("|").split("|")]
                if len(parts) >= 6:
                    matrix_rows.append(parts[:6])
    return matrix_rows


def build_viva_pdf():
    """Parses docs/viva-preparation.md and compiles docs/viva-preparation.pdf."""
    print(f"Reading source: {SOURCE_MD}...")
    assert SOURCE_MD.exists(), f"Source file {SOURCE_MD} does not exist!"
    raw_content = SOURCE_MD.read_text(encoding="utf-8")

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    base_styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=base_styles["Title"],
        fontName=FONT_BOLD,
        fontSize=24,
        leading=28,
        textColor=COLOR_NAVY,
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=base_styles["Normal"],
        fontName=FONT_NORMAL,
        fontSize=13,
        leading=17,
        textColor=COLOR_GOLD_DARK,
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    meta_label_style = ParagraphStyle(
        "MetaLabel",
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=13,
        textColor=COLOR_NAVY,
    )

    meta_val_style = ParagraphStyle(
        "MetaValue",
        fontName=FONT_NORMAL,
        fontSize=9.5,
        leading=13,
        textColor=COLOR_DARK_SLATE,
    )

    h1_style = ParagraphStyle(
        "SectionHeading",
        fontName=FONT_BOLD,
        fontSize=14,
        leading=18,
        textColor=COLOR_NAVY,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True,
    )

    q_style = ParagraphStyle(
        "QuestionHeading",
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=13.5,
        textColor=COLOR_NAVY,
        backColor=COLOR_LIGHT_BG,
        borderColor=COLOR_GOLD,
        borderWidth=0.8,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True,
    )

    ans_style = ParagraphStyle(
        "AnswerText",
        fontName=FONT_NORMAL,
        fontSize=9,
        leading=13,
        textColor=COLOR_DARK_SLATE,
        leftIndent=8,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        fontName=FONT_NORMAL,
        fontSize=9,
        leading=13,
        textColor=COLOR_DARK_SLATE,
        leftIndent=20,
        spaceAfter=2.5,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        fontName=FONT_NORMAL,
        fontSize=7.5,
        leading=10,
        textColor=COLOR_DARK_SLATE,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        fontName=FONT_BOLD,
        fontSize=7.5,
        leading=10,
        textColor=COLOR_NAVY,
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    print("Building Cover Page...")
    story.append(Spacer(1, 35))
    story.append(Paragraph("GRAMMY Awards Information &amp; Analytics System", title_style))
    story.append(Paragraph("Comprehensive Viva Voce Preparation Guide &amp; Examination Handbook", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_GOLD, spaceBefore=4, spaceAfter=22))

    parsed_meta = parse_metadata_from_md(raw_content)
    meta_table_data = []
    for k, v in parsed_meta:
        meta_table_data.append([
            Paragraph(clean_markdown_to_xml(f"<b>{k}:</b>"), meta_label_style),
            Paragraph(clean_markdown_to_xml(v), meta_val_style),
        ])

    # If parsed metadata had fewer items, append standard academic completion entries
    if not any(k.lower().startswith("academic lifecycle") for k, _ in parsed_meta):
        meta_table_data.append([
            Paragraph("<b>Academic Lifecycle Status:</b>", meta_label_style),
            Paragraph("Phases 1 through 30 Fully Completed &amp; Formally Certified (30 / 30)", meta_val_style),
        ])
    if not any(k.lower().startswith("date of") for k, _ in parsed_meta):
        meta_table_data.append([
            Paragraph("<b>Date of Compilation:</b>", meta_label_style),
            Paragraph("October 2026", meta_val_style),
        ])

    meta_table = Table(meta_table_data, colWidths=[150, 354])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 1, COLOR_GOLD),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 20))
    intro_p = Paragraph(
        "<b>Executive Examination Overview:</b> This official academic handbook serves as the exhaustive "
        "oral defense preparation curriculum for the master's capstone evaluation of the GRAMMY Awards "
        "Information &amp; Analytics System. Covering all 10 modules of the graduate ADBMS syllabus, it compiles "
        "230 project-grounded technical questions and model answers, spanning relational DBMS theory, "
        "normalization proofs (1NF–5NF), multi-document ACID transactions, concurrency control protocols, "
        "WiredTiger physical storage mechanics, ARIES recovery algorithms, and distributed join federation.",
        ParagraphStyle("CoverIntro", parent=base_styles["Normal"], fontSize=9, leading=13.5, textColor=COLOR_DARK_SLATE, alignment=TA_JUSTIFY)
    )
    story.append(intro_p)
    story.append(PageBreak())

    # =========================================================================
    # 2. TABLE OF CONTENTS
    # =========================================================================
    print("Building Table of Contents...")
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD, spaceBefore=2, spaceAfter=12))

    toc_items = parse_toc_from_md(raw_content)
    toc_data = []
    for num, title in toc_items:
        p_num = Paragraph(f"<b>{num}.</b>", meta_label_style)
        p_desc = Paragraph(clean_markdown_to_xml(f"<b>{title}</b>"), table_cell_style)
        toc_data.append([p_num, p_desc])

    toc_table = Table(toc_data, colWidths=[30, 474])
    toc_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # 3. FIVE-MEMBER VIVA RESPONSIBILITY MATRIX
    # =========================================================================
    print("Building Five-Member Responsibility Matrix...")
    story.append(Paragraph("Five-Member Viva Responsibility &amp; Defense Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD, spaceBefore=2, spaceAfter=10))

    matrix_raw_rows = parse_matrix_table_from_md(raw_content)
    matrix_table_rows = []

    for row_idx, row in enumerate(matrix_raw_rows):
        formatted_row = []
        is_header = (row_idx == 0)
        for col_idx, cell in enumerate(row):
            xml_text = clean_markdown_to_xml(cell)
            style = table_cell_bold if (is_header or col_idx == 0) else table_cell_style
            formatted_row.append(Paragraph(xml_text, style))
        matrix_table_rows.append(formatted_row)

    col_widths = [55, 80, 95, 75, 110, 89]
    matrix_table = Table(matrix_table_rows, colWidths=col_widths, repeatRows=1)
    matrix_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_GOLD),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_LIGHT_BG, COLOR_ROW_ALT]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(matrix_table)
    story.append(PageBreak())

    # =========================================================================
    # 4. QUESTION SECTIONS (SECTIONS 1 THROUGH 13)
    # =========================================================================
    print("Parsing Question Sections from Markdown...")
    lines = raw_content.splitlines()

    i = 0
    question_count = 0

    while i < len(lines):
        line = lines[i].strip()

        # Section Heading (# Section X: ...)
        if line.startswith("# Section "):
            sec_title = line.lstrip("#").strip()
            print(f"  Formatting {sec_title}...")
            story.append(Spacer(1, 10))
            story.append(Paragraph(clean_markdown_to_xml(sec_title), h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD, spaceBefore=2, spaceAfter=8))
            i += 1
            continue

        # Question Heading (#### QX: ...)
        if line.startswith("#### Q"):
            question_count += 1
            q_header = line.lstrip("#").strip()
            formatted_q = clean_markdown_to_xml(q_header)
            story.append(Paragraph(formatted_q, q_style))
            i += 1

            # Parse Answer Block
            ans_lines = []
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip().startswith("#### Q") or next_line.strip().startswith("# Section "):
                    break
                ans_lines.append(next_line)
                i += 1

            ans_raw = "\n".join(ans_lines).strip()
            if ans_raw.startswith("**Answer**:"):
                ans_raw = ans_raw[len("**Answer**:") :].strip()

            # Process answer content by chunks (handling code blocks vs text blocks)
            # Fenced code blocks regex pattern: ```([a-zA-Z]*)\n([\s\S]*?)```
            chunks = re.split(r"(```[a-zA-Z]*\n[\s\S]*?```)", ans_raw)
            is_first_paragraph = True

            for chunk in chunks:
                chunk = chunk.strip()
                if not chunk:
                    continue

                if chunk.startswith("```") and chunk.endswith("```"):
                    # Code block chunk
                    # Strip outer ```
                    lines_code = chunk.splitlines()
                    lang = lines_code[0].lstrip("`").strip()
                    code_body = "\n".join(lines_code[1:-1])
                    if is_first_paragraph:
                        story.append(Paragraph("<b>Answer:</b>", ans_style))
                        is_first_paragraph = False
                    story.append(create_code_block_flowable(code_body, lang))
                    story.append(Spacer(1, 4))
                else:
                    # Regular text / paragraphs chunk
                    sub_paras = chunk.split("\n\n")
                    for par in sub_paras:
                        par = par.strip()
                        if not par:
                            continue

                        sub_lines = par.split("\n")
                        is_list = any(sub.strip().startswith(("- ", "• ", "1. ", "2. ", "3. ", "4. ", "5. ")) for sub in sub_lines)

                        if is_list:
                            if is_first_paragraph:
                                story.append(Paragraph("<b>Answer:</b>", ans_style))
                                is_first_paragraph = False
                            for sub in sub_lines:
                                sub = sub.strip()
                                if not sub:
                                    continue
                                formatted_sub = clean_markdown_to_xml(sub)
                                story.append(Paragraph(formatted_sub, bullet_style))
                        else:
                            formatted_p = clean_markdown_to_xml(par.replace("\n", " "))
                            if is_first_paragraph:
                                story.append(Paragraph(f"<b>Answer:</b> {formatted_p}", ans_style))
                                is_first_paragraph = False
                            else:
                                story.append(Paragraph(formatted_p, ans_style))

            continue

        i += 1

    print(f"Total Questions Parsed and Formatted: {question_count} / 230")

    print(f"Compiling PDF document to {OUTPUT_PDF}...")
    doc.build(story, canvasmaker=NumberedCanvas)

    size_kb = OUTPUT_PDF.stat().st_size / 1024
    print(f"[SUCCESS] Successfully generated Viva Voce Handbook PDF: {OUTPUT_PDF} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    build_viva_pdf()

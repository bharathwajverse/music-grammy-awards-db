#!/usr/bin/env python3
"""
=============================================================================
Phase 30 Artifact Generator: Viva Voce Defense Preparation Handbook (PDF)
=============================================================================
Course: Advanced Database Management Systems (ADBMS) — Graduate Capstone
Target File: docs/viva-preparation.pdf
Source File: docs/viva-preparation.md

Generates an academic handbook PDF containing:
- Title Cover Page with executive metadata block
- Table of Contents
- Five-Member Responsibility & Defense Matrix table
- 230 Project-Grounded Questions across 13 Categories
- Distinct question styling, clear formatted answers
- Two-pass NumberedCanvas for "Page X of Y" and running headers/footers
=============================================================================
"""

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
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE_MD = REPO_ROOT / "docs" / "viva-preparation.md"
OUTPUT_PDF = REPO_ROOT / "docs" / "viva-preparation.pdf"

# Color Palette: Academic Grammy Gold & Slate
COLOR_NAVY = colors.HexColor("#0f172a")      # Slate-900
COLOR_DARK_SLATE = colors.HexColor("#1e293b")# Slate-800
COLOR_GOLD = colors.HexColor("#d4af37")      # Grammy Gold
COLOR_GOLD_DARK = colors.HexColor("#b8860b") # Dark Goldenrod
COLOR_SILVER = colors.HexColor("#64748b")    # Slate-500
COLOR_LIGHT_BG = colors.HexColor("#f8fafc")  # Slate-50
COLOR_BORDER = colors.HexColor("#e2e8f0")    # Slate-200
COLOR_ROW_ALT = colors.HexColor("#f1f5f9")   # Slate-100
COLOR_CODE = colors.HexColor("#0369a1")      # Sky-700


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
    """Translates Markdown formatting and mathematical symbols to safe ReportLab XML tags."""
    if not text:
        return ""

    # Replace common LaTeX math symbols
    replacements = {
        r"$\pi$": "π",
        r"$\sigma$": "σ",
        r"$\bowtie$": "⋈",
        r"$\div$": "÷",
        r"$\cup$": "∪",
        r"$\cap$": "∩",
        r"$\times$": "×",
        r"$\ge$": "≥",
        r"$\le$": "≤",
        r"$\in$": "∈",
        r"$\approx$": "≈",
        r"$\rightarrow$": "→",
        r"$\twoheadrightarrow$": "↠",
        r"$\wedge$": "∧",
        r"$\vee$": "∨",
        r"$\dots$": "...",
        r"$": "",  # Remove remaining dollar signs
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)

    # Escape raw XML characters, keeping intentional tags safe later
    text = text.replace("&", "&amp;")

    # Handle code spans: `code`
    text = re.sub(r"`([^`]+)`", r'<font name="Courier" color="#0369a1"><b>\1</b></font>', text)

    # Handle bold text: **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

    # Handle italic text: *text* (excluding already formatted bold)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)

    # Clean double escapes if any
    text = text.replace("&amp;lt;", "&lt;").replace("&amp;gt;", "&gt;")
    return text


def build_viva_pdf():
    """Parses docs/viva-preparation.md and compiles docs/viva-preparation.pdf."""
    print(f"Reading source: {SOURCE_MD}...")
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
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=COLOR_NAVY,
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=17,
        textColor=COLOR_GOLD_DARK,
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    meta_label_style = ParagraphStyle(
        "MetaLabel",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=COLOR_NAVY,
    )

    meta_val_style = ParagraphStyle(
        "MetaValue",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=COLOR_DARK_SLATE,
    )

    h1_style = ParagraphStyle(
        "SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=COLOR_NAVY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SubSectionHeading",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=COLOR_GOLD_DARK,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )

    q_style = ParagraphStyle(
        "QuestionHeading",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=COLOR_NAVY,
        backColor=COLOR_LIGHT_BG,
        borderColor=COLOR_GOLD,
        borderWidth=0.8,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    ans_style = ParagraphStyle(
        "AnswerText",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=10,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=22,
        spaceAfter=3,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=COLOR_DARK_SLATE,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=COLOR_NAVY,
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    print("Building Cover Page...")
    story.append(Spacer(1, 40))
    story.append(Paragraph("GRAMMY Awards Information &amp; Analytics System", title_style))
    story.append(Paragraph("Comprehensive Viva Voce Preparation Guide &amp; Examination Handbook", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_GOLD, spaceBefore=5, spaceAfter=25))

    meta_data = [
        [Paragraph("Academic Course:", meta_label_style), Paragraph("Advanced Database Management Systems (ADBMS) — Graduate Capstone", meta_val_style)],
        [Paragraph("System Title:", meta_label_style), Paragraph("GRAMMY Awards Information &amp; Analytics System", meta_val_style)],
        [Paragraph("Target Engine:", meta_label_style), Paragraph("MongoDB Atlas (Cluster0, 3-Node Replica Set) &amp; WiredTiger Storage Engine", meta_val_style)],
        [Paragraph("Certification Status:", meta_label_style), Paragraph("<b>100% Certified</b> across 670 Automated Tests (629 baseline + 41 capstone)", meta_val_style)],
        [Paragraph("Authors / Engineering Team:", meta_label_style), Paragraph("Five-Member Distributed Database Team (Members 1–5)", meta_val_style)],
        [Paragraph("Comprehensive Scope:", meta_label_style), Paragraph("Master Question Bank (230 Questions across 13 Categories) + 5-Member Responsibility Matrix", meta_val_style)],
        [Paragraph("Academic Lifecycle Status:", meta_label_style), Paragraph("Phases 1 through 30 Fully Completed &amp; Formally Certified (30 / 30)", meta_val_style)],
        [Paragraph("Date of Compilation:", meta_label_style), Paragraph("October 2026", meta_val_style)],
    ]

    meta_table = Table(meta_data, colWidths=[150, 354])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 1, COLOR_GOLD),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 25))
    intro_p = Paragraph(
        "<b>Executive Examination Overview:</b> This official academic handbook serves as the exhaustive "
        "oral defense preparation curriculum for the master's capstone evaluation of the GRAMMY Awards "
        "Information &amp; Analytics System. Covering all 10 modules of the graduate ADBMS syllabus, it compiles "
        "230 project-grounded technical questions and model answers, spanning relational DBMS theory, "
        "normalization proofs (1NF–5NF), multi-document ACID transactions, concurrency control protocols, "
        "WiredTiger physical storage mechanics, ARIES recovery algorithms, and distributed join federation.",
        ParagraphStyle("CoverIntro", parent=base_styles["Normal"], fontSize=9.5, leading=14, textColor=COLOR_DARK_SLATE, alignment=TA_JUSTIFY)
    )
    story.append(intro_p)
    story.append(PageBreak())

    # =========================================================================
    # 2. TABLE OF CONTENTS
    # =========================================================================
    print("Building Table of Contents...")
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD, spaceBefore=2, spaceAfter=12))

    toc_items = [
        ("1", "Five-Member Viva Responsibility &amp; Defense Matrix", "Cross-Member Syllabus &amp; Artifact Mapping"),
        ("2", "Section 1: 50 Basic Viva Questions &amp; Answers", "Foundations, Quotas, Boundaries &amp; Engine Basics (Q1–Q50)"),
        ("3", "Section 2: 50 Intermediate Viva Questions &amp; Answers", "Indexing, Transactions, MGL &amp; Architecture (Q51–Q100)"),
        ("4", "Section 3: 30 Advanced Viva Questions &amp; Answers", "Deep Distributed Theory &amp; Empirical Mechanics (Q101–Q130)"),
        ("5", "Section 4: Dedicated Questions on Conceptual EER Modeling", "Weak Entities, Hierarchies &amp; Aggregations (Q131–Q140)"),
        ("6", "Section 5: Questions on Functional Dependencies &amp; Normalization", "Armstrong Axioms, Minimal Cover &amp; 1NF–5NF (Q141–Q150)"),
        ("7", "Section 6: Dedicated Questions on MongoDB Document Modeling", "Embedded vs Reference &amp; JSON Schema (Q151–Q160)"),
        ("8", "Section 7: Dedicated Questions on Aggregation Pipelines", "Multi-Stage Pipelines &amp; Faceted Bucketing (Q161–Q170)"),
        ("9", "Section 8: Dedicated Questions on Multi-Document ACID Transactions", "Replica Sessions &amp; Rollback Mechanics (Q171–Q180)"),
        ("10", "Section 9: Questions on Concurrency Control &amp; Serializability", "Strict 2PL, WFG Deadlocks &amp; MVCC (Q181–Q190)"),
        ("11", "Section 10: Questions on Physical Storage Architecture &amp; RAID", "Slotted Pages, Snappy &amp; RAID Penalties (Q191–Q200)"),
        ("12", "Section 11: Dedicated Questions on Crash Recovery &amp; ARIES", "WAL Invariants, Checkpointing &amp; 3 Phases (Q201–Q210)"),
        ("13", "Section 12: Dedicated Questions on Data Sources &amp; Ingestion", "Recording Academy, MusicBrainz &amp; Kaggle (Q211–Q220)"),
        ("14", "Section 13: Dedicated Questions on Licensing &amp; Provenance", "Feist Doctrine, CC0 &amp; Audit Lineage (Q221–Q230)"),
    ]

    toc_data = []
    for num, title, subtitle in toc_items:
        p_num = Paragraph(f"<b>{num}.</b>", meta_label_style)
        p_desc = Paragraph(f"<b>{title}</b><br/><font color='#64748b' size='8'>{subtitle}</font>", table_cell_style)
        toc_data.append([p_num, p_desc])

    toc_table = Table(toc_data, colWidths=[30, 474])
    toc_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # 3. FIVE-MEMBER VIVA RESPONSIBILITY MATRIX
    # =========================================================================
    print("Building Five-Member Responsibility Matrix...")
    story.append(Paragraph("Five-Member Viva Responsibility &amp; Defense Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD, spaceBefore=2, spaceAfter=10))

    matrix_rows = [
        [
            Paragraph("<b>Member</b>", table_cell_bold),
            Paragraph("<b>Database</b>", table_cell_bold),
            Paragraph("<b>Collection Portfolio</b>", table_cell_bold),
            Paragraph("<b>Syllabus Modules</b>", table_cell_bold),
            Paragraph("<b>Key Defense Specialties</b>", table_cell_bold),
            Paragraph("<b>Target Scripts &amp; Tests</b>", table_cell_bold),
        ],
        [
            Paragraph("<b>Member 1</b>", table_cell_bold),
            Paragraph("<code>grammy_history_db</code>", table_cell_style),
            Paragraph("ceremonies, venues, telecast_broadcasters, ratings, hosts, milestones, eras, leadership, press, honors", table_cell_style),
            Paragraph("<b>Module 6</b>: Storage &amp; RAID<br/><b>Module 7</b>: Recovery &amp; ARIES", table_cell_style),
            Paragraph("• Slotted-Page architecture<br/>• RAID 0/1/5/6/10 penalties<br/>• Snappy compression (32.9%)<br/>• WAL &amp; 3 ARIES phases<br/>• Bitwise recovery drill", table_cell_style),
            Paragraph("generate_data_dictionary.py<br/>controlled_recovery_drill.py<br/>tests/test_storage.py<br/>tests/test_recovery.py", table_cell_style),
        ],
        [
            Paragraph("<b>Member 2</b>", table_cell_bold),
            Paragraph("<code>grammy_categories_db</code>", table_cell_style),
            Paragraph("award_fields, award_categories, lineage, eligibility_rules, voting, quotas, craft_definitions, discontinued, merged, special_merit", table_cell_style),
            Paragraph("<b>Module 1</b>: Relational &amp; EER<br/><b>Module 2</b>: FDs &amp; 1NF/2NF", table_cell_style),
            Paragraph("• Conceptual EER &amp; weak entities<br/>• Specialization &amp; category unions<br/>• Conceptual aggregation<br/>• Closure sets (F+)<br/>• Minimal Cover (Fmin)", table_cell_style),
            Paragraph("docs/eer-design.md<br/>relational-model/<br/>tests/test_relational_model.py<br/>tests/test_functional_dependencies.py", table_cell_style),
        ],
        [
            Paragraph("<b>Member 3</b>", table_cell_bold),
            Paragraph("<code>grammy_nominations_db</code>", table_cell_style),
            Paragraph("nomination_entries, nominated_works, nomination_credits, submission_batches, voter_screening, tied, audit_logs, genres, first_time, packages", table_cell_style),
            Paragraph("<b>Module 4</b>: ACID Transactions<br/><b>Module 5</b>: Concurrency &amp; Locks", table_cell_style),
            Paragraph("• Multi-document ACID sessions<br/>• Snapshot isolation &amp; majority<br/>• Strict 2PL locking protocols<br/>• Wait-For Graph (WFG) cycles<br/>• OCC vs WiredTiger MVCC", table_cell_style),
            Paragraph("run_transaction_demo.py<br/>simulate_concurrency.py<br/>tests/test_transactions.py<br/>tests/test_concurrency.py", table_cell_style),
        ],
        [
            Paragraph("<b>Member 4</b>", table_cell_bold),
            Paragraph("<code>grammy_winners_db</code>", table_cell_style),
            Paragraph("winner_records, big_four_sweeps, record_breakers, speeches, trophy_tracking, consecutive, hall_of_fame, posthumous, benchmarks, press_releases", table_cell_style),
            Paragraph("<b>Module 9</b>: CRUD &amp; Queries<br/><b>Module 10</b>: Aggregations &amp; Indexes", table_cell_style),
            Paragraph("• High-selectivity CRUD &amp; ESR rule<br/>• Operators ($elemMatch, $regex)<br/>• 44 B+ tree indexes<br/>• COLLSCAN to IXSCAN proofs<br/>• Multi-stage pipelines &amp; $facet", table_cell_style),
            Paragraph("verify_indexes.py<br/>queries/crud/<br/>queries/advanced/<br/>queries/aggregation/<br/>tests/test_indexing.py", table_cell_style),
        ],
        [
            Paragraph("<b>Member 5</b>", table_cell_bold),
            Paragraph("<code>grammy_creators_db</code>", table_cell_style),
            Paragraph("artists, producers, audio_engineers, songwriters, arrangers, labels, musical_groups, memberships, collaborations, discographies", table_cell_style),
            Paragraph("<b>Module 3</b>: 3NF/BCNF/4NF/5NF<br/><b>Integration</b>: Join Federation", table_cell_style),
            Paragraph("• Lossless join BCNF proofs<br/>• MVDs (4NF) &amp; PJNF (5NF)<br/>• Justified denormalization<br/>• Atlas M0 cross-DB limits<br/>• Client-side join federation", table_cell_style),
            Paragraph("cross_database_validation.py<br/>docs/integration.md<br/>tests/test_normalization_proofs.py<br/>tests/test_cross_database.py", table_cell_style),
        ],
    ]

    col_widths = [55, 80, 95, 75, 110, 89]
    matrix_table = Table(matrix_rows, colWidths=col_widths, repeatRows=1)
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

    current_section = None
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

            # Parse Answer
            ans_lines = []
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip().startswith("#### Q") or next_line.strip().startswith("# Section "):
                    break
                ans_lines.append(next_line)
                i += 1

            ans_text = "\n".join(ans_lines).strip()
            if ans_text.startswith("**Answer**:"):
                ans_text = ans_text[len("**Answer**:") :].strip()

            # Render answer paragraphs / bullet points
            ans_paragraphs = ans_text.split("\n\n")
            for par in ans_paragraphs:
                par = par.strip()
                if not par:
                    continue

                # Check if paragraph contains bullet points
                sub_lines = par.split("\n")
                in_list = any(sub.strip().startswith(("- ", "• ", "1. ", "2. ", "3. ", "4. ", "5. ")) for sub in sub_lines)

                if in_list:
                    for sub in sub_lines:
                        sub = sub.strip()
                        if not sub:
                            continue
                        formatted_sub = clean_markdown_to_xml(sub)
                        story.append(Paragraph(formatted_sub, bullet_style))
                else:
                    formatted_p = clean_markdown_to_xml(par.replace("\n", " "))
                    story.append(Paragraph(f"<b>Answer:</b> {formatted_p}", ans_style))

            continue

        i += 1

    print(f"Total Questions Parsed and Formatted: {question_count} / 230")

    print(f"Compiling PDF document to {OUTPUT_PDF}...")
    doc.build(story, canvasmaker=NumberedCanvas)

    size_kb = OUTPUT_PDF.stat().st_size / 1024
    print(f"[SUCCESS] Successfully generated Viva Voce Handbook PDF: {OUTPUT_PDF} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    build_viva_pdf()

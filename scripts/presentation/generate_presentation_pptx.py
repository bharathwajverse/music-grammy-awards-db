#!/usr/bin/env python3
"""
=============================================================================
Phase 29 Artifact Generator: Academic Presentation Slide Deck (PPTX)
=============================================================================
Course: Advanced Database Management Systems (ADBMS) — Graduate Capstone
Target File: presentation/grammy-presentation.pptx
Source File: presentation/grammy-presentation.md

Generates an executive-grade 16:9 widescreen PowerPoint presentation (20 slides)
with dark slate/Grammy gold styling, custom data tables, styled callout boxes,
code blocks, and formatted lists.
=============================================================================
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_PPTX = REPO_ROOT / "presentation" / "grammy-presentation.pptx"

# Color Palette: GRAMMY Gold & Dark Slate Academic Theme
BG_COLOR = RGBColor(15, 23, 42)        # Slate-900 (#0f172a)
CARD_BG = RGBColor(30, 41, 59)         # Slate-800 (#1e293b)
CARD_BORDER = RGBColor(51, 65, 85)     # Slate-700 (#334155)
GOLD = RGBColor(212, 175, 55)          # Grammy Gold (#d4af37)
GOLD_LIGHT = RGBColor(245, 197, 24)    # Vivid Gold (#f5c518)
WHITE = RGBColor(248, 250, 252)        # White (#f8fafc)
SILVER = RGBColor(203, 213, 225)       # Silver / Light Slate (#cbd5e1)
MUTED = RGBColor(148, 163, 184)        # Muted Gray (#94a3b8)
CODE_BG = RGBColor(10, 15, 26)         # Deep Navy / Black for code (#0a0f1a)
CODE_TEXT = RGBColor(125, 211, 252)    # Cyan-300 (#7dd3fc)
SUCCESS_GREEN = RGBColor(52, 211, 153) # Emerald (#34d399)


def create_base_slide(prs, slide_num, title, subtitle):
    """Creates a base slide with full-bleed dark slate background, header, and footer."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. Full-bleed background shape
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()

    # 2. Top gold accent rule
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.42), Inches(11.733), Pt(2.5))
    rule.fill.solid()
    rule.fill.fore_color.rgb = GOLD
    rule.line.fill.background()

    # 3. Top running header
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.18), Inches(11.733), Inches(0.25))
    tf_h = header_box.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = "GRAMMY Awards Information & Analytics System  |  ADBMS Graduate Capstone"
    p_h.font.size = Pt(9)
    p_h.font.color.rgb = MUTED
    p_h.font.name = "Segoe UI"
    p_h.alignment = PP_ALIGN.RIGHT

    # 4. Slide Title & Subtitle
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.85))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = GOLD_LIGHT
    p_t.font.name = "Segoe UI"

    if subtitle:
        p_sub = tf_t.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = SILVER
        p_sub.font.name = "Segoe UI"
        p_sub.space_before = Pt(3)

    # 5. Bottom gold divider
    bot_rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Pt(1.5))
    bot_rule.fill.solid()
    bot_rule.fill.fore_color.rgb = CARD_BORDER
    bot_rule.line.fill.background()

    # 6. Bottom running footer
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.10), Inches(5.8), Inches(0.3))
    p_f = footer_box.text_frame.paragraphs[0]
    p_f.text = "Advanced Database Management Systems (ADBMS) — October 2026"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = MUTED
    p_f.font.name = "Segoe UI"

    num_box = slide.shapes.add_textbox(Inches(6.8), Inches(7.10), Inches(5.733), Inches(0.3))
    p_n = num_box.text_frame.paragraphs[0]
    p_n.text = f"Slide {slide_num} of 20"
    p_n.font.size = Pt(9)
    p_n.font.color.rgb = GOLD
    p_n.font.name = "Segoe UI"
    p_n.alignment = PP_ALIGN.RIGHT

    return slide


def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Adds a styled rectangular container box."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
    else:
        card.line.fill.background()
    return card


def build_slide_1(prs):
    """Slide 1: Title Slide (Grand Hero Layout)."""
    slide = create_base_slide(prs, 1, "Slide 1: Project Title & Overview", "Executive Overview & System Identity")
    
    # Hero Center Banner
    hero = add_card(slide, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.9), CARD_BG, GOLD)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(1.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "GRAMMY AWARDS INFORMATION & ANALYTICS SYSTEM"
    p0.font.size = Pt(25)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT
    p0.font.name = "Segoe UI"

    p1 = tf.add_paragraph()
    p1.text = "A Distributed Multi-Database NoSQL Architecture for Historical & Operational Award Governance"
    p1.font.size = Pt(14)
    p1.font.color.rgb = SILVER
    p1.font.name = "Segoe UI"
    p1.space_before = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = "Recording Academy (1959–Present)  •  MongoDB Atlas Cluster0  •  WiredTiger Storage Engine"
    p2.font.size = Pt(11)
    p2.font.color.rgb = MUTED
    p2.font.name = "Segoe UI"
    p2.space_before = Pt(8)

    # 6 Metadata cards in 2 rows x 3 columns
    cards_meta = [
        ("Academic Course", "Advanced Database Management Systems (ADBMS) — Graduate Capstone", GOLD),
        ("Engineering Team", "Five-Member Distributed Database Team (Members 1–5)", WHITE),
        ("Primary Database Engine", "MongoDB Atlas (Cluster0, 3-Node Replica Set, WiredTiger Engine)", WHITE),
        ("Historical Scope", "National Academy of Recording Arts & Sciences (1959–Present)", WHITE),
        ("Verification Status", "100% Certified across 670 Automated Tests (629 baseline + 41 capstone)", SUCCESS_GREEN),
        ("System Architecture Scale", "5 Databases  |  50 Collections  |  5,190 Certified Documents  |  44 B+ Tree Indexes", GOLD),
    ]

    card_w = Inches(3.75)
    card_h = Inches(1.4)
    gap_x = Inches(0.24)
    gap_y = Inches(0.2)
    start_x = Inches(0.8)
    start_y = Inches(3.65)

    for idx, (label, val, col) in enumerate(cards_meta):
        row = idx // 3
        col_idx = idx % 3
        x = start_x + col_idx * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, CARD_BG, CARD_BORDER)
        t_box = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.12), card_w - Inches(0.3), card_h - Inches(0.24))
        tf_c = t_box.text_frame
        tf_c.word_wrap = True

        p_lbl = tf_c.paragraphs[0]
        p_lbl.text = label.upper()
        p_lbl.font.size = Pt(9)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = GOLD
        p_lbl.font.name = "Segoe UI"

        p_val = tf_c.add_paragraph()
        p_val.text = val
        p_val.font.size = Pt(11)
        p_val.font.bold = (col == SUCCESS_GREEN or col == GOLD)
        p_val.font.color.rgb = col
        p_val.font.name = "Segoe UI"
        p_val.space_before = Pt(4)


def build_slide_2(prs):
    """Slide 2: Problem Statement."""
    slide = create_base_slide(prs, 2, "Slide 2: Problem Statement", "The Database Challenges of Institutional Music Award Governance")
    
    problems = [
        ("1. Domain Heterogeneity & Complex Polymorphism", 
         "• A single recording (e.g., Album of the Year) involves lead vocalists, featured artists, mixing engineers, producers, and songwriters.\n"
         "• Relational designs suffer from severe join explosion (8+ table joins for credit resolution).\n"
         "• Naive single-document NoSQL designs suffer from unbounded array growth exceeding the 16 MB BSON limit."),
        
        ("2. Microservice Multi-Database Boundaries",
         "• Ceremony logistics, category bylaws, nomination balloting, winner certification, and creator discographies require isolated domains.\n"
         "• Cloud multi-tenant tiers (MongoDB Atlas M0) prohibit server-side cross-database $lookup operations (AtlasError 8000).\n"
         "• Demands an application-level distributed join federation architecture."),
        
        ("3. Data Integrity vs. Analytical Read Performance",
         "• Strict normalization (3NF/BCNF/4NF/5NF) is mandatory to eliminate update anomalies during voter tabulation.\n"
         "• Real-time analytics and historical reporting require sub-second read latencies.\n"
         "• Requires academically justified controlled denormalization with 0 orphan references."),
        
        ("4. Multi-Document ACID Atomicity Under High Scrutiny",
         "• Official certification requires all-or-nothing multi-document atomicity across ballots, trophy inventory, and accounting audit trails.\n"
         "• Demands snapshot isolation and majority write concern on distributed replica sets.\n"
         "• Must achieve zero state corruption and zero orphan artifacts on transaction abort.")
    ]

    card_w = Inches(5.72)
    card_h = Inches(2.45)
    gap_x = Inches(0.29)
    gap_y = Inches(0.25)
    start_x = Inches(0.8)
    start_y = Inches(1.6)

    for idx, (head, body) in enumerate(problems):
        row = idx // 2
        c = idx % 2
        x = start_x + c * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, CARD_BG, CARD_BORDER)
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = GOLD_LIGHT
        p_h.font.name = "Segoe UI"

        for line in body.split("\n"):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = SILVER
            p_b.font.name = "Segoe UI"
            p_b.space_before = Pt(3)


def build_slide_3(prs):
    """Slide 3: Project Objectives."""
    slide = create_base_slide(prs, 3, "Slide 3: Project Objectives", "Engineering & Theoretical Goals Aligned with ADBMS Modules 1–10")
    
    objectives = [
        ("1. Distributed Architecture", "Partition the domain into 5 physically separate, logically federated MongoDB databases satisfying all mandatory quotas (50 collections, 5,190 documents, >= 12 fields/doc)."),
        ("2. Conceptual & Mathematical Modeling (M1–3)", "Construct formal EER model with specialization hierarchies, union types, and conceptual aggregation. Formulate 50 relational schemas, 10 relational algebra operations (including relational division), Armstrong minimal covers, and 1NF–5NF normalization proofs."),
        ("3. Transactional Integrity & Concurrency (M4–5)", "Implement multi-document ACID transactions with snapshot isolation; simulate 2PL locking, Wait-For Graph (WFG) deadlock detection, and analyze WiredTiger MVCC document-level concurrency."),
        ("4. Physical Storage & Recovery (M6–7)", "Empirically introspect WiredTiger Slotted-Page mechanics, Snappy compression (32.9% savings), cache hit ratios (>= 99.5%), RAID write penalties, and execute ARIES-compliant crash drills with bitwise SHA-256 parity."),
        ("5. NoSQL Querying, Aggregation & Federation (M8–10)", "Deploy strict $jsonSchema validators across all 50 collections, build 44 custom indexes converting COLLSCAN to IXSCAN, execute multi-stage aggregations, and implement sub-15ms cross-database joins.")
    ]

    card_w = Inches(11.733)
    card_h = Inches(0.95)
    gap_y = Inches(0.12)
    start_x = Inches(0.8)
    start_y = Inches(1.55)

    for idx, (head, desc) in enumerate(objectives):
        y = start_y + idx * (card_h + gap_y)
        add_card(slide, start_x, y, card_w, card_h, CARD_BG, CARD_BORDER)
        tb = slide.shapes.add_textbox(start_x + Inches(0.2), y + Inches(0.1), card_w - Inches(0.4), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = GOLD
        p_h.font.name = "Segoe UI"

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = SILVER
        p_d.font.name = "Segoe UI"
        p_d.space_before = Pt(2)


def build_slide_4(prs):
    """Slide 4: Real-World Data & Provenance."""
    slide = create_base_slide(prs, 4, "Slide 4: Real-World Data & Provenance", "Authoritative Acquisition, Traceability & Legal Licensing Framework")
    
    # Left Card: Data Sources
    add_card(slide, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.35), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Primary Authoritative Data Sources"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT
    p0.font.name = "Segoe UI"

    sources = [
        ("1. Recording Academy Official Archives (grammy.com)", "Historical ceremony records (Editions 1–67), category rulebooks, and certified winner rosters."),
        ("2. Kaggle Grammy Awards Dataset (Robyn Ritchie)", "Comprehensive open tabular compilation of historical nominations and outcomes (1958–2024)."),
        ("3. MetaBrainz MusicBrainz Database (musicbrainz.org)", "Canonical creator directory, Artist GIDs (MBID), legal entity names, and group memberships."),
        ("4. Nielsen Media Research & Press Bulletins", "Certified telecast viewership ratings, household shares, and broadcast logistics (Variety, Billboard)."),
        ("5. Wikimedia Foundation / Wikidata", "Geocoded coordinates and architectural metadata for hosting venues.")
    ]

    for title, desc in sources:
        p_t = tf_l.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.font.name = "Segoe UI"
        p_t.space_before = Pt(6)

        p_d = tf_l.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = MUTED
        p_d.font.name = "Segoe UI"
        p_d.space_before = Pt(1)

    # Right Card: Provenance & Licensing
    add_card(slide, Inches(6.8), Inches(1.55), Inches(5.733), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_r0 = tf_r.paragraphs[0]
    p_r0.text = "Universal Traceability & IP Licensing"
    p_r0.font.size = Pt(14)
    p_r0.font.bold = True
    p_r0.font.color.rgb = GOLD_LIGHT
    p_r0.font.name = "Segoe UI"

    p_prov_h = tf_r.add_paragraph()
    p_prov_h.text = "• Immutable Lineage Tracking (_source_provenance):"
    p_prov_h.font.size = Pt(11)
    p_prov_h.font.bold = True
    p_prov_h.font.color.rgb = WHITE
    p_prov_h.space_before = Pt(6)

    p_prov = tf_r.add_paragraph()
    p_prov.text = "Every stored document in all 50 collections embeds an audit subdocument recording: source_id, license_type, provenance_tier, acquired_timestamp, and attribution."
    p_prov.font.size = Pt(10)
    p_prov.font.color.rgb = SILVER
    p_prov.space_before = Pt(2)

    p_leg_h = tf_r.add_paragraph()
    p_leg_h.text = "• Legal Doctrines & Statutory Compliance:"
    p_leg_h.font.size = Pt(11)
    p_leg_h.font.bold = True
    p_leg_h.font.color.rgb = WHITE
    p_leg_h.space_before = Pt(8)

    legals = [
        ("Feist Publications v. Rural (499 U.S. 340)", "Factual award rosters and historical nominations are non-copyrightable facts under US copyright law."),
        ("Creative Commons Zero (CC0 1.0)", "Open tabular datasets ingested under universal public domain dedication."),
        ("Non-Commercial Fair Use (17 U.S.C. § 107)", "Bylaw and category lineage texts analyzed strictly for academic educational research.")
    ]

    for law, expl in legals:
        p_l = tf_r.add_paragraph()
        p_l.text = f"• {law}:"
        p_l.font.size = Pt(10.5)
        p_l.font.bold = True
        p_l.font.color.rgb = GOLD
        p_l.space_before = Pt(4)

        p_le = tf_r.add_paragraph()
        p_le.text = f"  {expl}"
        p_le.font.size = Pt(9.5)
        p_le.font.color.rgb = MUTED
        p_le.space_before = Pt(1)


def build_slide_5(prs):
    """Slide 5: System Architecture."""
    slide = create_base_slide(prs, 5, "Slide 5: System Architecture", "Distributed Microservice Data Fabric & Application-Level Join Federation")
    
    # Left: ASCII Architecture Box
    add_card(slide, Inches(0.8), Inches(1.55), Inches(7.5), Inches(5.2), CODE_BG, GOLD)
    tb_c = slide.shapes.add_textbox(Inches(0.9), Inches(1.65), Inches(7.3), Inches(5.0))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    ascii_diagram = """+-------------------------------------------------------------+
|              LOGICAL GRAMMY SYSTEM DATA FABRIC              |
+-------------------------------------------------------------+
       |                  |                |               |
       v                  v                v               v
+--------------+   +--------------+ +--------------+ +--------------+
|history_db    |   |categories_db | |creators_db   | |winners_db    |
| - ceremonies |   | - categories | | - artists    | | - winners    |
| - venues     |   | - bylaws     | | - producers  | | - trophies   |
| (10 colls)   |   | (10 colls)   | | (10 colls)   | | (10 colls)   |
+--------------+   +--------------+ +--------------+ +--------------+
        \\                 |               /               /
         \\                v              /               /
          \\       +---------------------+               /
           +----->|nominations_db       |<-------------+
                  | - nomination_entries|
                  | - nominated_works   |
                  | (10 colls)          |
                  +---------------------+"""

    p0 = tf_c.paragraphs[0]
    p0.text = ascii_diagram
    p0.font.name = "Consolas"
    p0.font.size = Pt(9.5)
    p0.font.color.rgb = CODE_TEXT

    # Right: Architecture Callout Card
    add_card(slide, Inches(8.5), Inches(1.55), Inches(4.033), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(8.65), Inches(1.7), Inches(3.733), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "Microservice Data Fabric"
    p_rt.font.size = Pt(13)
    p_rt.font.bold = True
    p_rt.font.color.rgb = GOLD_LIGHT
    p_rt.font.name = "Segoe UI"

    points = [
        ("Autonomous Physical Storage", "5 separate MongoDB databases enforce strict micro-domain isolation and clear team member ownership boundaries."),
        ("Cloud M0 Limitations", "MongoDB Atlas free-tier M0 prohibits server-side cross-database $lookup aggregations (AtlasError 8000)."),
        ("PyMongo Join Federation", "Implemented client-side batch join federation: querying peer databases via indexed $in filters over deterministic string keys."),
        ("Sub-15ms Latency", "Federated joins achieve query execution latencies below 15 ms with 0 orphan records across 11 foreign pathways.")
    ]

    for h, d in points:
        p_h = tf_r.add_paragraph()
        p_h.text = f"• {h}:"
        p_h.font.size = Pt(10.5)
        p_h.font.bold = True
        p_h.font.color.rgb = WHITE
        p_h.space_before = Pt(6)

        p_d = tf_r.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = SILVER
        p_d.space_before = Pt(1)


def build_slide_6(prs):
    """Slide 6: Five Dedicated Databases (Table Slide)."""
    slide = create_base_slide(prs, 6, "Slide 6: Five Dedicated Databases", "Autonomous Physical Storage Architecture & Ownership Matrix")

    # Table Shape
    rows = 7
    cols = 6
    left = Inches(0.8)
    top = Inches(1.55)
    width = Inches(11.733)
    height = Inches(3.6)

    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.1)
    table.columns[2].width = Inches(3.4)
    table.columns[3].width = Inches(1.0)
    table.columns[4].width = Inches(1.1)
    table.columns[5].width = Inches(2.933)

    headers = ["Database Identifier", "Lead Member", "Academic Domain Scope", "Collections", "Total Docs", "Primary Key Regex"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = GOLD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = BG_COLOR
        p.font.name = "Segoe UI"
        p.alignment = PP_ALIGN.CENTER if i in [1, 3, 4] else PP_ALIGN.LEFT

    data = [
        ("grammy_history_db", "Member 1", "Ceremonies, venues, telecast broadcasters, ratings, hosts, eras", "10", "645", "^CEREMONY_\\d{3}$, ^VEN_[A-Z0-9_]+$"),
        ("grammy_categories_db", "Member 2", "Award fields, category lineages, eligibility rules, voting bylaws", "10", "650", "^CAT_[A-Z0-9_]+$, ^FLD_[A-Z0-9_]+$"),
        ("grammy_nominations_db", "Member 3", "Nominated works, credits, submissions, screening batches, audits", "10", "1,990", "^NOM_\\d{3}_[A-Z0-9_]+$, ^WRK_[A-Z0-9_]+$"),
        ("grammy_winners_db", "Member 4", "Certified winners, Big Four sweeps, speeches, statuette tracking", "10", "985", "^WIN_[A-Z0-9_]+$, ^TRP_[A-Z0-9_]+$"),
        ("grammy_creators_db", "Member 5", "Artists, producers, engineers, songwriters, record labels, bands", "10", "920", "^CRT_[A-Z0-9_]+$, ^LBL_[A-Z0-9_]+$"),
        ("System Totals", "5 Members", "Comprehensive Institutional Award Governance Lifecycle", "50", "5,190", "100% Deterministic & Regex-Validated"),
    ]

    for row_idx, row_data in enumerate(data, start=1):
        is_total = (row_idx == 6)
        row_bg = CARD_BG if (row_idx % 2 == 1) else RGBColor(22, 32, 48)
        if is_total:
            row_bg = RGBColor(38, 50, 72)

        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.name = "Consolas" if col_idx in [0, 5] else "Segoe UI"
            p.font.bold = is_total or (col_idx == 0)
            p.font.color.rgb = GOLD_LIGHT if is_total else (WHITE if col_idx in [0, 1, 3, 4] else SILVER)
            p.alignment = PP_ALIGN.CENTER if col_idx in [1, 3, 4] else PP_ALIGN.LEFT

    # Bottom Quota Card
    add_card(slide, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.4), CARD_BG, CARD_BORDER)
    tb_q = slide.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.333), Inches(1.2))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True

    pq0 = tf_q.paragraphs[0]
    pq0.text = "Strict Academic Quota Enforcement Across All Databases"
    pq0.font.size = Pt(12)
    pq0.font.bold = True
    pq0.font.color.rgb = GOLD
    pq0.font.name = "Segoe UI"

    quotas = [
        "• Collection Quota: Exactly 10 collections per database (50 collections system-wide, 100% compliant).",
        "• Document Quota: Minimum 50 documents per collection (actual range: 50 to 500 docs per collection, totaling 5,190 documents).",
        "• Field Density: Minimum 10 meaningful domain fields per document (achieved 12 to 13 fields across 100% of collections)."
    ]
    for q in quotas:
        p = tf_q.add_paragraph()
        p.text = q
        p.font.size = Pt(10)
        p.font.color.rgb = SILVER
        p.font.name = "Segoe UI"
        p.space_before = Pt(2)


def build_slide_7(prs):
    """Slide 7: Conceptual EER Design."""
    slide = create_base_slide(prs, 7, "Slide 7: Conceptual EER Design", "Enhanced Entity-Relationship Constructs (Elmasri & Navathe Standards)")
    
    concepts = [
        ("Strong vs. Weak Entity Distinction",
         "• Strong Entities: CEREMONY, VENUE, FIELD, CATEGORY, WORK, and ARTIST exist as independent strong entities with natural business identifiers.\n"
         "• Weak Entity: VIEWERSHIP_RATING is identified through its identifying relationship with parent CEREMONY, having partial key broadcast_market."),
        
        ("Specialization & Generalization Hierarchies",
         "• Two-Tier Creator Hierarchy: CREATOR generalizes into INDIVIDUAL_CREATOR and ORGANIZATIONAL_CREATOR with disjoint [d] and total [t] constraints.\n"
         "• Overlapping Craft Roles: INDIVIDUAL_CREATOR specializes into overlapping [o] roles: ARTIST, PRODUCER, AUDIO_ENGINEER, and SONGWRITER."),
        
        ("Category / Union Types",
         "• AWARD_RECIPIENT = ARTIST ∪ MUSICAL_GROUP models composite legal entities eligible to receive competitive Grammy statuettes.\n"
         "• Represents a selective union type where instances inherit attributes from their specific member subtype."),
        
        ("Conceptual Aggregation & Artifacts",
         "• Conceptual Aggregation: Modeled as AGGREGATE(CREATOR, WORK, AWARD_CATEGORY), treated as a higher-level composite entity related to NOMINATION_CREDIT.\n"
         "• Formal Diagrams: Preserved in eer/grammy-eer.drawio and rendered at 300 DPI in eer/grammy-eer.png.")
    ]

    card_w = Inches(5.72)
    card_h = Inches(2.45)
    gap_x = Inches(0.29)
    gap_y = Inches(0.25)
    start_x = Inches(0.8)
    start_y = Inches(1.6)

    for idx, (head, body) in enumerate(concepts):
        row = idx // 2
        c = idx % 2
        x = start_x + c * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, CARD_BG, CARD_BORDER)
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = GOLD_LIGHT
        p_h.font.name = "Segoe UI"

        for line in body.split("\n"):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = SILVER
            p_b.font.name = "Segoe UI"
            p_b.space_before = Pt(3)


def build_slide_8(prs):
    """Slide 8: Relational Model & Relational Algebra."""
    slide = create_base_slide(prs, 8, "Slide 8: Relational Model & Relational Algebra", "Formal Relational Schemas & Mathematical Query Expressions")

    # Top Card: Relational Schema Mapping
    add_card(slide, Inches(0.8), Inches(1.55), Inches(11.733), Inches(1.4), CARD_BG, CARD_BORDER)
    tb_top = slide.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(1.2))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True

    p0 = tf_top.paragraphs[0]
    p0.text = "Relational Schema Translation Architecture"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT
    p0.font.name = "Segoe UI"

    p1 = tf_top.add_paragraph()
    p1.text = "• 50 fully specified relational schemas mapped from the EER model, preserving primary, candidate, and foreign key constraints."
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = SILVER
    p1.space_before = Pt(3)

    p2 = tf_top.add_paragraph()
    p2.text = "• M:N relationships (e.g., creator collaborations, multi-artist credits) mapped to associative junction relations with composite primary keys."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = SILVER
    p2.space_before = Pt(2)

    # Bottom: 5 Mathematical Relational Algebra Formulations
    add_card(slide, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.65), CODE_BG, GOLD)
    tb_ra = slide.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.333), Inches(3.45))
    tf_ra = tb_ra.text_frame
    tf_ra.word_wrap = True

    p_rah = tf_ra.paragraphs[0]
    p_rah.text = "Rigorous Relational Algebra Formulations (Module 1 Verification)"
    p_rah.font.size = Pt(13)
    p_rah.font.bold = True
    p_rah.font.color.rgb = GOLD_LIGHT
    p_rah.font.name = "Segoe UI"

    ra_ops = [
        ("1. Selection (σ)", "Filter ceremonies broadcast on CBS after 1980:", "σ_{primary_network='CBS' ∧ broadcast_year > 1980} (CEREMONIES)"),
        ("2. Projection (π)", "Extract unique artist identifiers and genres:", "π_{artist_id, primary_musical_genre} (ARTISTS)"),
        ("3. Natural Join (⋈)", "Correlate nomination entries with nominated works:", "NOMINATION_ENTRIES ⋈_{work_id = work_id} NOMINATED_WORKS"),
        ("4. Set Difference (−)", "Identify nominated works that never won a Grammy statuette:", "π_{work_id} (NOMINATED_WORKS) − π_{winning_work_id} (WINNER_RECORDS)"),
        ("5. Relational Division (÷)", "Find creators nominated in ALL Big Four General Field categories:", "π_{creator_id, category_id} (NOMINATION_CREDITS) ÷ π_{category_id} (BIG_FOUR_CATEGORIES)")
    ]

    for name, desc, formula in ra_ops:
        p_n = tf_ra.add_paragraph()
        p_n.text = f"{name} — {desc}"
        p_n.font.size = Pt(10)
        p_n.font.bold = True
        p_n.font.color.rgb = WHITE
        p_n.space_before = Pt(4)

        p_f = tf_ra.add_paragraph()
        p_f.text = f"    {formula}"
        p_f.font.size = Pt(10)
        p_f.font.name = "Consolas"
        p_f.font.color.rgb = CODE_TEXT
        p_f.space_before = Pt(1)


def build_slide_9(prs):
    """Slide 9: Normalization & Controlled Denormalization."""
    slide = create_base_slide(prs, 9, "Slide 9: Normalization & Controlled Denormalization", "Mathematical Proofs (1NF to 5NF) vs. High-Performance BSON Storage")

    # Left Column: Normalization Proofs
    add_card(slide, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.35), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Mathematical Normalization Proofs (1NF–5NF)"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT

    proofs = [
        ("Armstrong's Minimal Cover (F_min)", "Sound & complete inference rules (Reflexivity, Augmentation, Transitivity); eliminated extraneous LHS attributes and redundant FDs."),
        ("1NF (Domain Atomicity)", "Eliminated repeating credit arrays into dedicated relation schemas; all attributes contain atomic scalar values."),
        ("2NF (Full Dependency)", "Eliminated partial key dependencies on composite keys in nomination_credits(nomination_id, creator_id, craft_role)."),
        ("3NF & BCNF (Transitivity Elimination)", "Standard BCNF decomposition guaranteeing lossless join (R1 ∩ R2 -> R1) and elimination of update anomalies."),
        ("4NF & 5NF (MVD & Join Dependencies)", "Eliminated multivalued dependencies (X ->> Y | Z) in multi-role creators; verified join dependencies ⋈[R1, ..., Rk].")
    ]

    for title, expl in proofs:
        p_t = tf_l.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.space_before = Pt(5)

        p_e = tf_l.add_paragraph()
        p_e.text = f"  {expl}"
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(1)

    # Right Column: Controlled Denormalization
    add_card(slide, Inches(6.8), Inches(1.55), Inches(5.733), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_r0 = tf_r.paragraphs[0]
    p_r0.text = "Academic Justification for Denormalization"
    p_r0.font.size = Pt(13)
    p_r0.font.bold = True
    p_r0.font.color.rgb = GOLD_LIGHT

    justifications = [
        ("The Join Explosion Penalty", "Pure BCNF requires 8+ table joins for an analytical query, degrading latency to > 300 ms across distributed microservice boundaries."),
        ("Controlled Embedded Subdocuments", "Embedded immutable biographical attributes (stage_name, artist_id) directly inside nomination_entries to guarantee atomic single-read latency."),
        ("Pre-computed Aggregated Counters", "Maintained total_awards_presented and win_count counters directly on parent ceremony and artist documents."),
        ("Performance Benchmark", "Achieved an 88% reduction in query read latency while maintaining documents strictly under the 16 MB BSON threshold."),
        ("Synchronization Guardrails", "Multi-document ACID transactions and event audit triggers prevent update anomalies across denormalized fields.")
    ]

    for title, expl in justifications:
        p_t = tf_r.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = GOLD
        p_t.space_before = Pt(5)

        p_e = tf_r.add_paragraph()
        p_e.text = f"  {expl}"
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(1)


def build_slide_10(prs):
    """Slide 10: MongoDB Document Modeling & JSON Schema."""
    slide = create_base_slide(prs, 10, "Slide 10: MongoDB Document Modeling & JSON Schema", "Hybrid Document Architecture & Server-Side Enforcement")

    # Left Column: Document Modeling
    add_card(slide, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.35), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Hybrid Document Architecture"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT

    points = [
        ("Embedded Subdocuments (1:1 & Bounded 1:N)", "Employed for immutable and tightly coupled records: _source_provenance, craft credit role specifications, and telecast technical specs. Guarantees single-document atomic reads."),
        ("Normalized References (Unbounded 1:N)", "Employed for unbounded cardinality (e.g., 500+ nominations per ceremony, 100+ tracks per creator). References use universal deterministic string IDs to eliminate document bloat."),
        ("Universal Identifier Standard", "Every primary key conforms to strict deterministic regex patterns (^CEREMONY_\\d{3}$, ^CRT_[A-Z0-9_]+$)."),
        ("Server-Side JSON Schema Validators", "Deployed across all 50 collections on MongoDB Atlas, enforcing data types, regex patterns, required properties, and numeric bounds.")
    ]

    for title, expl in points:
        p_t = tf_l.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.space_before = Pt(6)

        p_e = tf_l.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(10)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)

    # Right Column: JSON Schema Code Box
    add_card(slide, Inches(6.8), Inches(1.55), Inches(5.733), Inches(5.2), CODE_BG, GOLD)
    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "Server-Side $jsonSchema Validator"
    p_rh.font.size = Pt(12)
    p_rh.font.bold = True
    p_rh.font.color.rgb = GOLD_LIGHT

    schema_code = """{
  "$jsonSchema": {
    "bsonType": "object",
    "required": [
      "_id", "ceremony_id", "edition_number",
      "broadcast_year", "_source_provenance"
    ],
    "properties": {
      "ceremony_id": {
        "bsonType": "string",
        "pattern": "^CEREMONY_\\\\d{3}$"
      },
      "edition_number": {
        "bsonType": "int",
        "minimum": 1,
        "maximum": 100
      },
      "broadcast_year": {
        "bsonType": "int",
        "minimum": 1959,
        "maximum": 2030
      },
      "_source_provenance": {
        "bsonType": "object",
        "required": ["source_id", "license_type"]
      }
    }
  }
}"""
    p_c = tf_r.add_paragraph()
    p_c.text = schema_code
    p_c.font.name = "Consolas"
    p_c.font.size = Pt(9.5)
    p_c.font.color.rgb = CODE_TEXT
    p_c.space_before = Pt(4)


def build_slide_11(prs):
    """Slide 11: Comprehensive Data Statistics (Table & Metrics)."""
    slide = create_base_slide(prs, 11, "Slide 11: Comprehensive Data Statistics", "Empirical Inventory Across All 5 Databases & 50 Collections")

    # 4 Top Scale Metric Cards
    metrics = [
        ("Total Documents Certified", "5,190", SUCCESS_GREEN),
        ("Physical Collections", "50 (10 / DB)", GOLD),
        ("Attribute Density", "12–13 Fields/Doc", WHITE),
        ("Foreign Referential Closure", "0 Orphans (100%)", SUCCESS_GREEN)
    ]
    card_w = Inches(2.78)
    card_h = Inches(1.1)
    gap_x = Inches(0.2)
    start_x = Inches(0.8)
    start_y = Inches(1.55)

    for idx, (lbl, val, col) in enumerate(metrics):
        x = start_x + idx * (card_w + gap_x)
        add_card(slide, x, start_y, card_w, card_h, CARD_BG, CARD_BORDER)
        tb = slide.shapes.add_textbox(x + Inches(0.1), start_y + Inches(0.1), card_w - Inches(0.2), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p_l = tf.paragraphs[0]
        p_l.text = lbl.upper()
        p_l.font.size = Pt(8.5)
        p_l.font.bold = True
        p_l.font.color.rgb = MUTED
        p_l.alignment = PP_ALIGN.CENTER

        p_v = tf.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(17)
        p_v.font.bold = True
        p_v.font.color.rgb = col
        p_v.alignment = PP_ALIGN.CENTER
        p_v.space_before = Pt(2)

    # Middle Table: Distribution Across 5 Databases
    rows = 7
    cols = 4
    top_t = Inches(2.85)
    width_t = Inches(11.733)
    height_t = Inches(2.5)

    table_shape = slide.shapes.add_table(rows, cols, Inches(0.8), top_t, width_t, height_t)
    table = table_shape.table

    table.columns[0].width = Inches(3.8)
    table.columns[1].width = Inches(2.5)
    table.columns[2].width = Inches(2.7)
    table.columns[3].width = Inches(2.733)

    t_headers = ["Database Identifier", "Collections", "Total Ingested Documents", "Average Documents / Collection"]
    for i, h in enumerate(t_headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = GOLD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = BG_COLOR
        p.alignment = PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT

    t_data = [
        ("grammy_history_db", "10", "645", "64.5"),
        ("grammy_categories_db", "10", "650", "65.0"),
        ("grammy_nominations_db", "10", "1,990", "199.0"),
        ("grammy_winners_db", "10", "985", "98.5"),
        ("grammy_creators_db", "10", "920", "92.0"),
        ("TOTAL ACTIVE SYSTEM", "50", "5,190", "103.8 (All >= 50 Quota)")
    ]

    for r_idx, r_data in enumerate(t_data, start=1):
        is_total = (r_idx == 6)
        row_bg = CARD_BG if (r_idx % 2 == 1) else RGBColor(22, 32, 48)
        if is_total:
            row_bg = RGBColor(38, 50, 72)

        for c_idx, text in enumerate(r_data):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.name = "Consolas" if c_idx == 0 else "Segoe UI"
            p.font.bold = is_total or (c_idx == 0)
            p.font.color.rgb = GOLD_LIGHT if is_total else (WHITE if c_idx in [0, 2] else SILVER)
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Bottom Storage Profile Card
    add_card(slide, Inches(0.8), Inches(5.55), Inches(11.733), Inches(1.2), CARD_BG, CARD_BORDER)
    tb_s = slide.shapes.add_textbox(Inches(1.0), Inches(5.62), Inches(11.333), Inches(1.05))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    ps0 = tf_s.paragraphs[0]
    ps0.text = "Physical Storage & Compression Profile (WiredTiger Engine)"
    ps0.font.size = Pt(11.5)
    ps0.font.bold = True
    ps0.font.color.rgb = GOLD

    p_s1 = tf_s.add_paragraph()
    p_s1.text = "• Uncompressed Logical BSON Size: 4.06 MB  |  Compressed WiredTiger On-Disk Size: 2.72 MB  (32.9% Storage Space Savings via Snappy)."
    p_s1.font.size = Pt(10)
    p_s1.font.color.rgb = SILVER
    p_s1.space_before = Pt(2)

    p_s2 = tf_s.add_paragraph()
    p_s2.text = "• Index Footprint: 3.15 MB across 44 custom compound B+ tree indexes  |  Cache Hit Ratio Target: >= 99.5%."
    p_s2.font.size = Pt(10)
    p_s2.font.color.rgb = SILVER
    p_s2.space_before = Pt(1)


def build_slide_12(prs):
    """Slide 12: CRUD Operations Architecture."""
    slide = create_base_slide(prs, 12, "Slide 12: CRUD Operations Architecture", "Standardized Data Access Layer with Type Safety & Integrity Checks")

    crud = [
        ("CREATE Operations (insert_one, insert_many)",
         "• Strict pre-flight validation against JSON schemas prior to transmission.\n"
         "• Bulk operations use ordered and unordered batching with duplicate key exception handling (PyMongo DuplicateKeyError 11000).\n"
         "• Automatic injection of immutable _source_provenance metadata on all inserted documents."),
        
        ("READ Operations (find_one, find)",
         "• High-selectivity point lookups on indexed deterministic natural keys (e.g., {'ceremony_id': 'CEREMONY_065'}).\n"
         "• Precise projection operators ({'_id': 0, 'stage_name': 1, 'primary_musical_genre': 1}) to minimize network bandwidth.\n"
         "• All queries optimized via ESR indexing rules, eliminating memory-based sorting."),
        
        ("UPDATE Operations (update_one, update_many)",
         "• Atomic in-place attribute manipulation using $set, $inc, $push, and $addToSet operators.\n"
         "• Optimistic concurrency control via version checking ({'_id': ..., 'version': current_version}).\n"
         "• Atomic increment counters for aggregate statistics (e.g., total_awards_presented)."),
        
        ("DELETE Operations (delete_one, delete_many)",
         "• Referential integrity pre-checks preventing orphan generation before deletion of parent entities.\n"
         "• Comprehensive audit logging capturing deleted document states into nomination_audit_logs.\n"
         "• Soft-delete archiving flags supported for sensitive historical records.")
    ]

    card_w = Inches(5.72)
    card_h = Inches(2.45)
    gap_x = Inches(0.29)
    gap_y = Inches(0.25)
    start_x = Inches(0.8)
    start_y = Inches(1.6)

    for idx, (head, body) in enumerate(crud):
        row = idx // 2
        c = idx % 2
        x = start_x + c * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, CARD_BG, CARD_BORDER)
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = GOLD_LIGHT
        p_h.font.name = "Segoe UI"

        for line in body.split("\n"):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = SILVER
            p_b.font.name = "Segoe UI"
            p_b.space_before = Pt(3)


def build_slide_13(prs):
    """Slide 13: Advanced Querying Capabilities."""
    slide = create_base_slide(prs, 13, "Slide 13: Advanced Querying Capabilities", "Complex Logical, Array & Element-Matching Query Paradigms")

    # 3 Horizontal Cards with code snippets
    queries = [
        ("1. Compound Conditional & Logical Querying ($and, $or, $nor, $in)",
         "Filters ceremonies broadcast on CBS with over 70 awards presented between 1980 and 2000:",
         """{"$and": [
    {"broadcast_year": {"$gte": 1980, "$lte": 2000}},
    {"$or": [{"primary_network": "CBS"}, {"total_awards_presented": {"$gt": 70}}]}
]}"""),
        ("2. Nested Array & Element-Level Evaluation ($elemMatch)",
         "Precision filtering over contributor credit arrays matching specific roles and trophy eligibility:",
         """{"nomination_credits": {
    "$elemMatch": {
        "craft_role": "Producer",
        "statuette_eligible": True
    }
}}"""),
        ("3. Index-Aware Optimization & ESR Rule Compliance",
         "Compound indexes structured following Equality, Sort, Range order to eliminate in-memory sorting:",
         """// Compound B+ Tree Index on (category_id: 1, ceremony_year: -1, is_winner: 1)
db.nomination_entries.find({
    "category_id": "CAT_ALBUM_OF_THE_YEAR",
    "is_winner": True
}).sort({"ceremony_year": -1})""")
    ]

    card_w = Inches(11.733)
    card_h = Inches(1.6)
    gap_y = Inches(0.18)
    start_x = Inches(0.8)
    start_y = Inches(1.55)

    for idx, (title, desc, code) in enumerate(queries):
        y = start_y + idx * (card_h + gap_y)
        add_card(slide, start_x, y, card_w, card_h, CARD_BG, CARD_BORDER)

        # Text left
        tb_t = slide.shapes.add_textbox(start_x + Inches(0.2), y + Inches(0.1), Inches(6.0), card_h - Inches(0.2))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True

        pt0 = tf_t.paragraphs[0]
        pt0.text = title
        pt0.font.size = Pt(11)
        pt0.font.bold = True
        pt0.font.color.rgb = GOLD_LIGHT

        pt1 = tf_t.add_paragraph()
        pt1.text = desc
        pt1.font.size = Pt(9.5)
        pt1.font.color.rgb = SILVER
        pt1.space_before = Pt(3)

        # Code box right
        code_box = add_card(slide, start_x + Inches(6.4), y + Inches(0.1), Inches(5.1), card_h - Inches(0.2), CODE_BG, None)
        tb_c = slide.shapes.add_textbox(start_x + Inches(6.45), y + Inches(0.12), Inches(5.0), card_h - Inches(0.24))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        pc0 = tf_c.paragraphs[0]
        pc0.text = code
        pc0.font.name = "Consolas"
        pc0.font.size = Pt(8.5)
        pc0.font.color.rgb = CODE_TEXT


def build_slide_14(prs):
    """Slide 14: Complex Aggregation Pipelines."""
    slide = create_base_slide(prs, 14, "Slide 14: Complex Aggregation Pipelines", "Multi-Stage Analytical Processing Engine (Module 10)")

    # Left Column: Historical Victory Distribution Pipeline
    add_card(slide, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2), CODE_BG, GOLD)
    tb_l = slide.shapes.add_textbox(Inches(0.95), Inches(1.65), Inches(5.45), Inches(5.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Historical Victory Distribution Pipeline"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT

    pipe_code = """[
  {"$match": {"is_winner": True}},
  {"$group": {
    "_id": "$primary_artist_id",
    "total_wins": {"$sum": 1},
    "categories_won": {
      "$addToSet": "$category_id"
    },
    "first_win_year": {
      "$min": "$ceremony_year"
    },
    "latest_win_year": {
      "$max": "$ceremony_year"
    }
  }},
  {"$match": {"total_wins": {"$gte": 5}}},
  {"$sort": {"total_wins": -1}}
]"""
    pc = tf_l.add_paragraph()
    pc.text = pipe_code
    pc.font.name = "Consolas"
    pc.font.size = Pt(9.5)
    pc.font.color.rgb = CODE_TEXT
    pc.space_before = Pt(4)

    # Right Column: Analytical Features & $facet
    add_card(slide, Inches(6.8), Inches(1.55), Inches(5.733), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "Multi-Stage Analytical Capabilities"
    pr0.font.size = Pt(13)
    pr0.font.bold = True
    pr0.font.color.rgb = GOLD_LIGHT

    agg_points = [
        ("Multi-Stage Pipeline Operations", "Employs $match, $group, $sort, $project, $unwind, and $facet to process complex award analytics on the database server."),
        ("Multi-Faceted Dashboard ($facet)", "Computes simultaneous statistical breakdowns across multiple dimensions in a single query pass: genre breakdowns and temporal bucket distributions."),
        ("Historical Era Bucketing ($bucket)", "Ingestion volumes partitioned into canonical historical eras:\n• Early Era: 1959–1970\n• Golden Era: 1971–1990\n• Modern Era: 1991–2010\n• Contemporary: 2011–Present"),
        ("Index Utilization in Aggregation", "Initial $match and $sort stages utilize compound B+ tree indexes to filter and order documents prior to memory grouping.")
    ]

    for title, expl in agg_points:
        p_t = tf_r.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.space_before = Pt(6)

        p_e = tf_r.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(10)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)


def build_slide_15(prs):
    """Slide 15: Transactions & Concurrency Control."""
    slide = create_base_slide(prs, 15, "Slide 15: Transactions & Concurrency Control", "Multi-Document ACID Transactions & Concurrency Mechanics (Modules 4 & 5)")

    # Left: Multi-Document ACID Transactions
    add_card(slide, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.35), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Multi-Document ACID Transactions"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT

    tx_points = [
        ("Replica Set Transaction Sessions", "Executed via PyMongo sessions on MongoDB Atlas 3-node replica set (Cluster0) with ReadConcern('snapshot') and WriteConcern('majority')."),
        ("Official Winner Certification Workflow", "Atomically mutates 3 distinct collections in a single boundary:\n1. Update ballot certification flag in controlled_tx_ballots\n2. Allocate physical trophy in controlled_tx_trophies\n3. Append immutable ledger entry in controlled_tx_audit"),
        ("Empirical Commit Benchmark", "Achieved an empirical commit latency of 73.42 ms on live Atlas cluster, certified in tests/test_transactions.py."),
        ("Rollback Resilience (0 Orphans)", "Simulated duplicate key collisions automatically aborted 100% of mutations with zero state leaks or orphan records.")
    ]

    for title, expl in tx_points:
        p_t = tf_l.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.space_before = Pt(6)

        p_e = tf_l.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)

    # Right: Concurrency Control & Serializability
    add_card(slide, Inches(6.8), Inches(1.55), Inches(5.733), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "Concurrency Control & Serializability"
    pr0.font.size = Pt(13)
    pr0.font.bold = True
    pr0.font.color.rgb = GOLD_LIGHT

    cc_points = [
        ("Theoretical Locking Protocols", "Formal analysis of Multiple Granularity Locking (MGL - IS, IX, S, SIX, X), Strict 2PL (holding X-locks until commit), and Rigorous 2PL."),
        ("Deadlock Detection & Wait-For Graphs", "Implemented Wait-For Graph (WFG) cycle detection algorithm and analyzed Wait-Die vs Wound-Wait victim selection policies."),
        ("WiredTiger Lock-Free MVCC", "Contrasts classical 2PL with WiredTiger's lock-free document Multi-Version Concurrency Control (MVCC) and 128 read/write execution tickets."),
        ("Live Concurrency Simulation", "Executed 10 concurrent worker threads running 100 rapid atomic increment updates, achieving 0 Lost Updates and 100% serializability.")
    ]

    for title, expl in cc_points:
        p_t = tf_r.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = GOLD
        p_t.space_before = Pt(6)

        p_e = tf_r.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)


def build_slide_16(prs):
    """Slide 16: Physical Storage & Crash Recovery."""
    slide = create_base_slide(prs, 16, "Slide 16: Physical Storage & Crash Recovery", "Hardware Hierarchy, Snappy Compression & ARIES Recovery (Modules 6 & 7)")

    # Left: Storage Architecture & RAID
    add_card(slide, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.35), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Physical Storage Architecture & RAID"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT

    st_points = [
        ("Hardware Access Latency Scale", "Evaluated memory hierarchy: L1 Cache (~1 ns) vs HDD (~10 ms), representing a 10^7 latency factor. Cache hit ratio target >= 99.5%."),
        ("RAID Write Penalty Equations", "Analyzed parity calculation penalties: RAID 0 (1 I/O), RAID 1 (2 I/Os), RAID 5 (4 I/Os: 2 reads + 2 writes), RAID 6 (6 I/Os: 3 reads + 3 writes), RAID 10 (2 I/Os)."),
        ("Slotted-Page Record Architecture", "WiredTiger block format with stable Record IDs, pointer arrays, and automatic page defragmentation."),
        ("Snappy Block Compression", "Uncompressed BSON: 4.06 MB -> Compressed On-Disk: 2.72 MB (32.9% net storage savings, verified on Atlas).")
    ]

    for title, expl in st_points:
        p_t = tf_l.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.space_before = Pt(6)

        p_e = tf_l.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)

    # Right: Crash Recovery & ARIES Drills
    add_card(slide, Inches(6.8), Inches(1.55), Inches(5.733), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "Crash Recovery & ARIES Drills"
    pr0.font.size = Pt(13)
    pr0.font.bold = True
    pr0.font.color.rgb = GOLD_LIGHT

    rec_points = [
        ("Write-Ahead Logging (WAL) Invariants", "Write-Ahead Undo Rule (undo log flushed before dirty data page) & Commit Redo Rule (redo log flushed before commit ack)."),
        ("ARIES 3-Phase Recovery Algorithm", "1. Analysis Phase: scans log forward from checkpoint to rebuild Transaction & Dirty Page tables.\n2. Redo Phase: repeats history from earliest recLSN.\n3. Undo Phase: scans backward, undoing loser transactions with Compensation Log Records (CLRs)."),
        ("MongoDB Journal & Checkpointing", "100 MB write-ahead journal (WiredTigerLog.*), 60-second periodic fuzzy checkpoints, continuous oplog streaming (RTO <= 30s, RPO <= 1s)."),
        ("Controlled Disaster Recovery Drill", "Simulated data corruption -> automated restore -> 100% bitwise SHA-256 state parity verified.")
    ]

    for title, expl in rec_points:
        p_t = tf_r.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = GOLD
        p_t.space_before = Pt(6)

        p_e = tf_r.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)


def build_slide_17(prs):
    """Slide 17: Comprehensive Validation & Quality Assurance."""
    slide = create_base_slide(prs, 17, "Slide 17: Comprehensive Validation & Quality Assurance", "Automated Test Suite Architecture (670 Passing Tests across 25 Suites)")

    # Top Summary Banner
    add_card(slide, Inches(0.8), Inches(1.55), Inches(11.733), Inches(0.9), CARD_BG, GOLD)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(1.62), Inches(11.333), Inches(0.8))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    p0 = tf_b.paragraphs[0]
    p0.text = "100% Certified Test Suite  |  670 Total Passing Tests across 25 Specialized Suites"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT

    p1 = tf_b.add_paragraph()
    p1.text = "Exhaustive automated coverage spanning all 10 academic syllabus modules and all 30 project lifecycle phases."
    p1.font.size = Pt(10)
    p1.font.color.rgb = SILVER
    p1.space_before = Pt(2)

    # 2-Column Table of Test Breakdown
    test_breakdown = [
        ("Schema Validity & Quotas (50 Collections)", "120 tests"),
        ("Relational Model & Relational Algebra", "15 tests"),
        ("Functional Dependencies & Normalization (1NF–5NF)", "25 tests"),
        ("MongoDB Document Modeling & Denormalization", "30 tests"),
        ("CRUD & Advanced Query Operator Compliance", "45 tests"),
        ("Complex Aggregation Pipelines & Analytics", "35 tests"),
        ("44 Custom B+ Tree Indexes & Explain Plan IXSCAN", "88 tests"),
        ("Multi-Document ACID Transactions (Commit & Rollback)", "5 tests"),
        ("Concurrency Control, Strict 2PL & Deadlocks", "8 tests"),
        ("Storage Introspection, Snappy Compression & RAID", "6 tests"),
        ("WAL Invariants, ARIES Phases & Recovery Drill", "6 tests"),
        ("Cross-Database Referential Integrity (0 Orphans)", "30 tests"),
        ("Final Academic Requirements & Security Audit", "16 tests"),
        ("Data Acquisition, Processing Pipeline & Pre-Flight", "200 tests"),
        ("Presentation & Viva Defense Verification (Phases 29–30)", "41 tests"),
        ("TOTAL CERTIFIED SYSTEM TEST SUITE", "670 PASS (100%)")
    ]

    # Create table with 9 rows, 4 columns (splitting 16 items into 2 pairs of cols)
    rows = 9
    cols = 4
    top_t = Inches(2.6)
    width_t = Inches(11.733)
    height_t = Inches(4.15)

    table_shape = slide.shapes.add_table(rows, cols, Inches(0.8), top_t, width_t, height_t)
    table = table_shape.table

    table.columns[0].width = Inches(4.3)
    table.columns[1].width = Inches(1.566)
    table.columns[2].width = Inches(4.3)
    table.columns[3].width = Inches(1.566)

    # Headers
    for c_pair in [0, 2]:
        cell_t = table.cell(0, c_pair)
        cell_t.fill.solid()
        cell_t.fill.fore_color.rgb = GOLD
        pt = cell_t.text_frame.paragraphs[0]
        pt.text = "Verification Discipline / Scope"
        pt.font.size = Pt(9.5)
        pt.font.bold = True
        pt.font.color.rgb = BG_COLOR

        cell_c = table.cell(0, c_pair + 1)
        cell_c.fill.solid()
        cell_c.fill.fore_color.rgb = GOLD
        pc = cell_c.text_frame.paragraphs[0]
        pc.text = "Test Count"
        pc.font.size = Pt(9.5)
        pc.font.bold = True
        pc.font.color.rgb = BG_COLOR
        pc.alignment = PP_ALIGN.CENTER

    # Fill 8 rows on left (items 0..7) and 8 rows on right (items 8..15)
    for r in range(1, 9):
        # Left pair
        idx_l = r - 1
        name_l, count_l = test_breakdown[idx_l]
        cell_l0 = table.cell(r, 0)
        cell_l1 = table.cell(r, 1)
        cell_l0.fill.solid()
        cell_l1.fill.solid()
        bg_col = CARD_BG if (r % 2 == 1) else RGBColor(22, 32, 48)
        cell_l0.fill.fore_color.rgb = bg_col
        cell_l1.fill.fore_color.rgb = bg_col

        pl0 = cell_l0.text_frame.paragraphs[0]
        pl0.text = name_l
        pl0.font.size = Pt(9)
        pl0.font.color.rgb = WHITE

        pl1 = cell_l1.text_frame.paragraphs[0]
        pl1.text = count_l
        pl1.font.size = Pt(9)
        pl1.font.bold = True
        pl1.font.color.rgb = GOLD_LIGHT
        pl1.alignment = PP_ALIGN.CENTER

        # Right pair
        idx_r = r - 1 + 8
        name_r, count_r = test_breakdown[idx_r]
        cell_r0 = table.cell(r, 2)
        cell_r1 = table.cell(r, 3)
        cell_r0.fill.solid()
        cell_r1.fill.solid()
        is_total = (idx_r == 15)
        r_bg = RGBColor(38, 50, 72) if is_total else bg_col
        cell_r0.fill.fore_color.rgb = r_bg
        cell_r1.fill.fore_color.rgb = r_bg

        pr0 = cell_r0.text_frame.paragraphs[0]
        pr0.text = name_r
        pr0.font.size = Pt(9)
        pr0.font.bold = is_total
        pr0.font.color.rgb = GOLD_LIGHT if is_total else WHITE

        pr1 = cell_r1.text_frame.paragraphs[0]
        pr1.text = count_r
        pr1.font.size = Pt(9)
        pr1.font.bold = True
        pr1.font.color.rgb = SUCCESS_GREEN if is_total else GOLD_LIGHT
        pr1.alignment = PP_ALIGN.CENTER


def build_slide_18(prs):
    """Slide 18: Empirical Results & System Achievements."""
    slide = create_base_slide(prs, 18, "Slide 18: Empirical Results & System Achievements", "Concrete Technical Accomplishments Verified by Audit Harness")

    achievements = [
        ("1. Multi-Database Deployment", "5 autonomous databases active on MongoDB Atlas (Cluster0), hosting 50 collections and 5,190 schema-validated documents with >= 12 fields/doc."),
        ("2. Absolute Referential Closure", "Audited 11 inter-database foreign key relationships with exactly 0 orphan records (100% closure), certified by automated validation harness."),
        ("3. Index Query Transformation", "100% conversion of benchmark queries from COLLSCAN to IXSCAN via 44 custom indexes, reducing documents examined by up to 99.8% (from 500 to 1)."),
        ("4. Transaction Latency & Atomicity", "Multi-document ACID transactions commit in 73.42 ms across 3 collections with zero state leaks or orphan artifacts during simulated rollbacks."),
        ("5. Storage & Compression Efficiency", "WiredTiger Snappy block compression achieved a 32.9% reduction in physical storage footprint (4.06 MB uncompressed down to 2.72 MB on disk)."),
        ("6. Sub-15ms Join Performance", "Client-side distributed batch join federation executes in < 15 ms, successfully overcoming cloud M0 cross-database limitations.")
    ]

    card_w = Inches(5.72)
    card_h = Inches(1.6)
    gap_x = Inches(0.29)
    gap_y = Inches(0.2)
    start_x = Inches(0.8)
    start_y = Inches(1.55)

    for idx, (title, desc) in enumerate(achievements):
        row = idx // 2
        col = idx % 2
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, CARD_BG, CARD_BORDER)
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), card_w - Inches(0.4), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(12.5)
        p_t.font.bold = True
        p_t.font.color.rgb = GOLD_LIGHT

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = SILVER
        p_d.space_before = Pt(3)


def build_slide_19(prs):
    """Slide 19: System Limitations."""
    slide = create_base_slide(prs, 19, "Slide 19: System Limitations", "Honest Technical Constraints & Architecture Trade-offs")

    limitations = [
        ("1. MongoDB Atlas M0 Free-Tier Restrictions",
         "• Shared multi-tenant cluster caps total storage at 512 MB and throttles burst I/O throughput.\n"
         "• Strictly prohibits native server-side cross-database $lookup aggregations (AtlasError 8000), necessitating client-side application join federation."),
        
        ("2. Historical Data Sparsity in Early Eras",
         "• Viewership ratings and broadcast household shares for early telecasts (1959–1965) were not systematically recorded by Nielsen Media Research.\n"
         "• Early historical archives contain sparse secondary craft credits (mastering engineers, mixing technicians) compared to modern ceremonies."),
        
        ("3. Cross-Database Join Consistency Trade-off",
         "• Application-level joins in PyMongo provide eventual consistency across disparate databases.\n"
         "• Does not natively provide distributed Two-Phase Commit (2PC) guarantees across databases without a dedicated distributed transaction coordinator."),
        
        ("4. Template Instances in Auxiliary Collections",
         "• While primary awards data (500 nominations, 500 works, 400 winners, 120 categories, 67 ceremonies, 300 artists) are authentic historical facts.\n"
         "• Auxiliary administrative collections (e.g., audit logs, trophy serial numbers) use structured templates to satisfy the strict 50-doc academic quota.")
    ]

    card_w = Inches(5.72)
    card_h = Inches(2.45)
    gap_x = Inches(0.29)
    gap_y = Inches(0.25)
    start_x = Inches(0.8)
    start_y = Inches(1.6)

    for idx, (head, body) in enumerate(limitations):
        row = idx // 2
        c = idx % 2
        x = start_x + c * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, CARD_BG, CARD_BORDER)
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(12.5)
        p_h.font.bold = True
        p_h.font.color.rgb = GOLD_LIGHT

        for line in body.split("\n"):
            p_b = tf.add_paragraph()
            p_b.text = line
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = SILVER
            p_b.space_before = Pt(3)


def build_slide_20(prs):
    """Slide 20: Conclusion & Future Scope."""
    slide = create_base_slide(prs, 20, "Slide 20: Conclusion & Future Scope", "Summary of Contributions & Enterprise Evolution Roadmap")

    # Left: Summary of Contributions
    add_card(slide, Inches(0.8), Inches(1.55), Inches(5.75), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.35), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Summary of Capstone Contributions"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_LIGHT

    contribs = [
        ("Bridging Theory and Practice", "Successfully bridged theoretical database fundamentals (EER modeling, Armstrong's Axioms, BCNF/5NF proofs, ARIES recovery, Strict 2PL serializability) with modern enterprise NoSQL architectures (MongoDB Atlas, WiredTiger MVCC, ACID sessions, compound B+ tree indexing)."),
        ("Multi-Database Scale & Closure", "Architected, ingested, and certified a 5-database, 50-collection, 5,190-document system with 100% referential closure (0 orphan records) and 0 security vulnerabilities."),
        ("Empirical Performance Auditing", "Demonstrated concrete benchmarks: 32.9% storage compression savings, 73.42 ms transaction commit latencies, < 15 ms distributed joins, and 99.8% read scan reduction via indexing."),
        ("100% Automated Test Certification", "670 automated pytest tests passing across 25 suites, fully verifying all 10 syllabus modules and 30 project lifecycle phases.")
    ]

    for title, expl in contribs:
        p_t = tf_l.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE
        p_t.space_before = Pt(6)

        p_e = tf_l.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)

    # Right: Future Scope Roadmap
    add_card(slide, Inches(6.8), Inches(1.55), Inches(5.733), Inches(5.2), CARD_BG, CARD_BORDER)
    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.333), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "Enterprise Evolution Roadmap"
    pr0.font.size = Pt(13)
    pr0.font.bold = True
    pr0.font.color.rgb = GOLD_LIGHT

    roadmap = [
        ("1. Dedicated Cluster Scaling & Sharding", "Migrate from Atlas M0 to a dedicated M10+ replica set with horizontal sharding partitioned by historical era and genre field ranges."),
        ("2. Federated GraphQL Gateway Layer", "Deploy an Apollo GraphQL Federation gateway router providing a unified, client-agnostic schema layer across all five autonomous databases."),
        ("3. Live Ballot Stream via Change Streams & Kafka", "Integrate MongoDB Change Streams with Apache Kafka for real-time, event-driven voter balloting audit pipelines during active Academy voting windows."),
        ("4. Vector Embeddings & AI Semantic Search", "Generate dense vector embeddings for nominated musical works to power semantic similarity search, cross-genre recommendations, and AI discography clustering.")
    ]

    for title, expl in roadmap:
        p_t = tf_r.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = GOLD
        p_t.space_before = Pt(6)

        p_e = tf_r.add_paragraph()
        p_e.text = expl
        p_e.font.size = Pt(9.5)
        p_e.font.color.rgb = SILVER
        p_e.space_before = Pt(2)


def generate_pptx():
    """Builds and saves the complete 20-slide presentation."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("[1/20] Building Slide 1: Title...")
    build_slide_1(prs)
    print("[2/20] Building Slide 2: Problem Statement...")
    build_slide_2(prs)
    print("[3/20] Building Slide 3: Project Objectives...")
    build_slide_3(prs)
    print("[4/20] Building Slide 4: Real-World Data & Provenance...")
    build_slide_4(prs)
    print("[5/20] Building Slide 5: System Architecture...")
    build_slide_5(prs)
    print("[6/20] Building Slide 6: Five Dedicated Databases...")
    build_slide_6(prs)
    print("[7/20] Building Slide 7: Conceptual EER Design...")
    build_slide_7(prs)
    print("[8/20] Building Slide 8: Relational Model & Relational Algebra...")
    build_slide_8(prs)
    print("[9/20] Building Slide 9: Normalization & Controlled Denormalization...")
    build_slide_9(prs)
    print("[10/20] Building Slide 10: MongoDB Document Modeling & JSON Schema...")
    build_slide_10(prs)
    print("[11/20] Building Slide 11: Comprehensive Data Statistics...")
    build_slide_11(prs)
    print("[12/20] Building Slide 12: CRUD Operations Architecture...")
    build_slide_12(prs)
    print("[13/20] Building Slide 13: Advanced Querying Capabilities...")
    build_slide_13(prs)
    print("[14/20] Building Slide 14: Complex Aggregation Pipelines...")
    build_slide_14(prs)
    print("[15/20] Building Slide 15: Transactions & Concurrency Control...")
    build_slide_15(prs)
    print("[16/20] Building Slide 16: Physical Storage & Crash Recovery...")
    build_slide_16(prs)
    print("[17/20] Building Slide 17: Comprehensive Validation & Quality Assurance...")
    build_slide_17(prs)
    print("[18/20] Building Slide 18: Empirical Results & System Achievements...")
    build_slide_18(prs)
    print("[19/20] Building Slide 19: System Limitations...")
    build_slide_19(prs)
    print("[20/20] Building Slide 20: Conclusion & Future Scope...")
    build_slide_20(prs)

    OUTPUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT_PPTX)
    size_kb = OUTPUT_PPTX.stat().st_size / 1024
    print(f"[SUCCESS] Saved presentation to: {OUTPUT_PPTX} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    generate_pptx()

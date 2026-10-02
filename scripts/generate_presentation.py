"""Generate the official SIH 2026 Selection-Winning 5-Slide Technical Presentation for KaryaSetu AI.

Theme: Blockchain & CyberSecurity | PS ID: SIH 26154
Team ID: 135343 | Team Name: KaryaSetu
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Curated Design System Color Palette ---
    DARK_NAVY   = RGBColor(11, 18, 32)      # #0B1220 - Deep enterprise navy
    SLATE_DARK  = RGBColor(30, 41, 59)      # #1E293B - Dark slate for cards/borders
    BG_LIGHT    = RGBColor(248, 250, 252)   # #F8FAFC - Clean subtle slate canvas
    CARD_WHITE  = RGBColor(255, 255, 255)   # #FFFFFF - Crisp elevated white card
    CARD_BORDER = RGBColor(226, 232, 240)   # #E2E8F0 - Clean slate card border
    
    # Accent Colors
    PRIMARY_BLUE = RGBColor(2, 132, 199)    # #0284C7 - Electric Sky Blue
    ACCENT_CYAN  = RGBColor(8, 145, 178)    # #0891B2 - Cyan for AI & Ingestion
    ACCENT_EMERALD= RGBColor(16, 185, 129)  # #10B981 - Emerald for Verification & Green
    ACCENT_PURPLE = RGBColor(124, 58, 237)  # #7C3AED - Purple for Policy & Governance
    ACCENT_AMBER  = RGBColor(217, 119, 6)   # #D97706 - Amber for Warnings & Cost
    ACCENT_ROSE   = RGBColor(225, 29, 72)   # #E11D48 - Rose for Threats & Risks
    
    # Text Colors
    TEXT_MAIN   = RGBColor(15, 23, 42)      # #0F172A - High-contrast charcoal/black
    TEXT_MUTED  = RGBColor(71, 85, 105)     # #475569 - Secondary slate
    TEXT_LIGHT  = RGBColor(148, 163, 184)   # #94A3B8 - Light muted slate
    WHITE       = RGBColor(255, 255, 255)

    def draw_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, bg_color=CARD_WHITE, border_color=CARD_BORDER, border_width=1.0):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
        return shape

    def add_badge(slide, left, top, width, height, text, bg_color, text_color=WHITE, font_size=9):
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_color
        badge.line.fill.background()
        tf = badge.text_frame
        tf.word_wrap = False
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = text
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = text_color
        return badge

    def add_header(slide, title_text, category_text="SMART INDIA HACKATHON 2026 • PS ID: SIH 26154 • THEME: BLOCKCHAIN & CYBERSECURITY"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(1.05))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_BLUE
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = DARK_NAVY

    def style_cell(cell, text, font_size=9, bold=False, color=TEXT_MAIN, bg_color=None, align=PP_ALIGN.LEFT):
        if bg_color:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = Inches(0.08)
        cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = align
        p.text = text
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color

    # =========================================================================
    # SLIDE 1 — PROBLEM STATEMENT, TEAM DETAILS & INNOVATION PROPOSITION
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    draw_bg(s1)

    # Top Tag Banner
    add_badge(s1, Inches(0.8), Inches(0.4), Inches(4.6), Inches(0.32),
              "SMART INDIA HACKATHON 2026  •  PS ID: SIH 26154", PRIMARY_BLUE, WHITE, 9)
    add_badge(s1, Inches(5.5), Inches(0.4), Inches(3.4), Inches(0.32),
              "THEME: BLOCKCHAIN & CYBERSECURITY", ACCENT_EMERALD, WHITE, 9)
    add_badge(s1, Inches(9.0), Inches(0.4), Inches(3.533), Inches(0.32),
              "TEAM ID: 135343  •  TEAM: KARYASETU", DARK_NAVY, WHITE, 9)

    # Title Hero Block
    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.733), Inches(1.3))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_t = tf1.paragraphs[0]
    p_t.text = "KARYASETU AI (कार्यसेतु)"
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_NAVY

    p_sub = tf1.add_paragraph()
    p_sub.text = "Zero-Trust Gen AI Platform for Governed Content Transformation, Dual-Route Orchestration & Decentralized Provenance"
    p_sub.font.size = Pt(13.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ACCENT_CYAN
    p_sub.space_after = Pt(2)

    p_m = tf1.add_paragraph()
    p_m.text = "One Trusted Source Document  ➔  Seven Governed, Audience-Tailored, Cryptographically Signed Deliverables in <25 Seconds"
    p_m.font.size = Pt(11)
    p_m.font.bold = False
    p_m.font.color.rgb = TEXT_MUTED

    # Hero Metric Callout Pills
    pills = [
        ("⚡ <25s Synthesis", ACCENT_CYAN),
        ("🛡️ 0% Cloud Leakage", ACCENT_PURPLE),
        ("⛓️ Ethereum Sepolia On-Chain", PRIMARY_BLUE),
        ("🔏 Ed25519 Sealed", ACCENT_EMERALD),
        ("💰 < ₹0.25 / Run", ACCENT_AMBER)
    ]
    pill_w = Inches(2.25)
    pill_gap = Inches(0.12)
    for idx, (p_text, p_col) in enumerate(pills):
        px = Inches(0.8) + idx * (pill_w + pill_gap)
        add_badge(s1, px, Inches(2.25), pill_w, Inches(0.32), p_text, p_col, WHITE, 9)

    # Left Card: THE CRITICAL PROBLEM
    add_card(s1, Inches(0.8), Inches(2.75), Inches(5.75), Inches(4.3), CARD_WHITE, CARD_BORDER, 1.2)
    # Header bar
    add_badge(s1, Inches(0.95), Inches(2.9), Inches(2.6), Inches(0.28), "CRITICAL INDUSTRY CHALLENGES", ACCENT_ROSE, WHITE, 8.5)
    
    prob_box = s1.shapes.add_textbox(Inches(0.95), Inches(3.28), Inches(5.45), Inches(3.6))
    tf_p = prob_box.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0

    probs = [
        ("Sensitive Data Exposure: ", "Confidential enterprise & defense memos cannot be sent to public cloud LLMs (OpenAI/Claude) without violating data sovereignty and compliance laws."),
        ("Adversarial Prompt Injections: ", "Untrusted user documents and embedded indirect prompt instructions hijack downstream transformation pipelines and leak secrets."),
        ("Ungrounded Hallucinations: ", "Generative AI invents fictitious metrics and unverified claims when unanchored to exact source citation offsets."),
        ("Inter-Format Cross-Output Drift: ", "Manual rewriting into summaries, slides, and advisories leads to severe factual contradictions and metric discrepancies across formats."),
        ("Severe Manual Labor Bottleneck: ", "Teams spend 4–6+ hours per report manually synthesizing, formatting, and vetting collateral for distinct audiences.")
    ]
    for idx, (b_title, b_desc) in enumerate(probs):
        p = tf_p.paragraphs[0] if idx == 0 else tf_p.add_paragraph()
        p.space_after = Pt(7)
        r1 = p.add_run()
        r1.text = "✖ " + b_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = ACCENT_ROSE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: THE KARYASETU INNOVATIVE SOLUTION
    add_card(s1, Inches(6.78), Inches(2.75), Inches(5.75), Inches(4.3), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s1, Inches(6.93), Inches(2.9), Inches(3.2), Inches(0.28), "KARYASETU ZERO-TRUST INNOVATION", ACCENT_EMERALD, WHITE, 8.5)

    sol_box = s1.shapes.add_textbox(Inches(6.93), Inches(3.28), Inches(5.45), Inches(3.6))
    tf_s = sol_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0

    sols = [
        ("Dual-Route Air-Gapped AI: ", "Deterministic policy gateway enforces 100% offline local LLM execution (Gemma 3 12B) for Restricted/Confidential data; Groq/Gemini for Public."),
        ("Zero-Trust Ingress & DLP Defense: ", "Magic-byte verification, local ClamAV anti-malware scan, and deterministic regex PII redaction mask sensitive entities before AI tokenization."),
        ("Evidence-Grounded Vector RAG: ", "Dense semantic retrieval in pgvector binds every generated output claim to exact source chunk IDs with SHA-256 digests."),
        ("Single Canonical Fact Brief: ", "All 7 deliverables ground to one unified facts model, cross-verified by automated NLI entailment consistency checks to guarantee zero drift."),
        ("Decentralized Blockchain Provenance: ", "Every artifact is sealed with SHA-256 digests anchored directly to an Ethereum Sepolia smart contract and signed with Ed25519 keys.")
    ]
    for idx, (b_title, b_desc) in enumerate(sols):
        p = tf_s.paragraphs[0] if idx == 0 else tf_s.add_paragraph()
        p.space_after = Pt(7)
        r1 = p.add_run()
        r1.text = "✔ " + b_title
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = ACCENT_EMERALD
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = TEXT_MUTED

    # Footer Link Bar
    foot_box = s1.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(11.733), Inches(0.3))
    tf_foot = foot_box.text_frame
    tf_foot.word_wrap = True
    p_ft = tf_foot.paragraphs[0]
    p_ft.text = "Live Demo: youtu.be/Lhi1ssHBfUk • Contract: 0x8AEf680b6891E7e3cAdCBD4a499AbA1310F87c08 • GitHub: github.com/KetanGaikwadKRG/KaryaSetu"
    p_ft.font.size = Pt(8.5)
    p_ft.font.bold = True
    p_ft.font.color.rgb = PRIMARY_BLUE
    p_ft.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2 — PROPOSED SOLUTION: END-TO-END PIPELINE & 7 DELIVERABLES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    draw_bg(s2)
    add_header(s2, "PROPOSED SOLUTION: ZERO-TRUST PIPELINE & 7 GOVERNED DELIVERABLES")

    # Pipeline Container Card
    add_card(s2, Inches(0.8), Inches(1.45), Inches(11.733), Inches(2.75), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s2, Inches(0.95), Inches(1.55), Inches(3.6), Inches(0.26), "7-STAGE SECURITY & AI ORCHESTRATION PIPELINE", DARK_NAVY, WHITE, 8.5)

    # 7 Stage Pipeline Flowchart Nodes
    nodes = [
        ("1. SOURCE INGEST", "MIME Validation\nClamAV Scan\nPDF/DOCX/TXT", ACCENT_CYAN),
        ("2. DLP & DEFENSE", "Deterministic PII\nRegex Masking\nPrompt Fencing", ACCENT_ROSE),
        ("3. POLICY GATE", "4-Tier Matrix\nZero-LLM Authority\nFail-Closed 403", ACCENT_PURPLE),
        ("4. DUAL-ROUTE AI", "Cloud (Groq/Gemini)\nAir-Gap (Gemma 3)\nLocal Inference", PRIMARY_BLUE),
        ("5. RAG RETRIEVAL", "pgvector HNSW\nTop-k Citation Offsets\nCanonical Brief", ACCENT_CYAN),
        ("6. NLI VERIFIER", "Claim Auditing\nGrounding Scoring\nFact Consistency", ACCENT_EMERALD),
        ("7. BLOCKCHAIN SEAL", "Ethereum Sepolia\nSHA-256 Digest\nEd25519 Sign", DARK_NAVY)
    ]
    node_w = Inches(1.52)
    node_h = Inches(1.7)
    node_gap = Inches(0.14)
    start_x = Inches(0.95)

    for i, (n_title, n_sub, n_color) in enumerate(nodes):
        nx = start_x + i * (node_w + node_gap)
        ny = Inches(1.95)
        # Card
        node_card = add_card(s2, nx, ny, node_w, node_h, RGBColor(250, 252, 255), n_color, 1.2)
        # Node Header Pill
        add_badge(s2, nx, ny, node_w, Inches(0.28), n_title, n_color, WHITE, 8)
        # Node text
        nt_box = s2.shapes.add_textbox(nx + Inches(0.06), ny + Inches(0.35), node_w - Inches(0.12), node_h - Inches(0.4))
        tf_nt = nt_box.text_frame
        tf_nt.word_wrap = True
        tf_nt.margin_left = tf_nt.margin_right = tf_nt.margin_top = tf_nt.margin_bottom = 0
        p_nt = tf_nt.paragraphs[0]
        p_nt.text = n_sub
        p_nt.font.size = Pt(8.5)
        p_nt.font.color.rgb = TEXT_MAIN
        p_nt.alignment = PP_ALIGN.CENTER
        
        # Arrow indicator between nodes
        if i < len(nodes) - 1:
            arr_box = s2.shapes.add_textbox(nx + node_w, ny + Inches(0.65), node_gap, Inches(0.3))
            tf_arr = arr_box.text_frame
            tf_arr.margin_left = tf_arr.margin_right = tf_arr.margin_top = tf_arr.margin_bottom = 0
            p_arr = tf_arr.paragraphs[0]
            p_arr.text = "➔"
            p_arr.font.size = Pt(11)
            p_arr.font.bold = True
            p_arr.font.color.rgb = PRIMARY_BLUE
            p_arr.alignment = PP_ALIGN.CENTER

    # Bottom Container: The 7 Governed Deliverables
    add_card(s2, Inches(0.8), Inches(4.35), Inches(11.733), Inches(2.9), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s2, Inches(0.95), Inches(4.45), Inches(4.0), Inches(0.26), "SEVEN GOVERNED, AUDIENCE-TAILORED DELIVERABLES", PRIMARY_BLUE, WHITE, 8.5)

    deliverables = [
        ("1. SUMMARY", "Executive C-Suite", "High-level strategic brief, key metrics, financial & policy impact.", "Markdown / Clean Text / DOCX", PRIMARY_BLUE),
        ("2. ADVISORY", "Technical Teams", "Structured threat/policy advisory, impact ratings, mitigation roadmap.", "Standardized Advisory Format", ACCENT_ROSE),
        ("3. PRESENTATION", "Board & Stakeholders", "Structured executive slide deck programmatically compiled into native slides.", "Native Microsoft PPTX (.pptx)", ACCENT_CYAN),
        ("4. INFOGRAPHIC", "Broad Audience", "Visual metrics breakdown, hierarchy blueprints, flow diagrams.", "Semantic JSON + Scalable SVG", ACCENT_PURPLE),
        ("5. VIDEO BRIEF", "Media & Production", "Scene-by-scene storyboard (PDF) + synchronized subtitle cue file (.srt).", "Storyboard PDF + SRT Subtitles", DARK_NAVY),
        ("6. LINKEDIN", "Professional Public", "Thought leadership payload, engagement hooks, structured key takeaways.", "Social Markdown + Hashtags", PRIMARY_BLUE),
        ("7. X THREAD", "Public / Press", "Sequential 280-char numbered announcement thread for rapid public alerts.", "Numbered Multi-Post Thread", ACCENT_EMERALD)
    ]
    del_w = Inches(1.58)
    del_h = Inches(2.25)
    del_gap = Inches(0.08)
    d_start_x = Inches(0.95)

    for j, (d_title, d_aud, d_desc, d_fmt, d_color) in enumerate(deliverables):
        dx = d_start_x + j * (del_w + del_gap)
        dy = Inches(4.82)
        add_card(s2, dx, dy, del_w, del_h, RGBColor(253, 254, 255), d_color, 1.0)
        # Top title badge
        add_badge(s2, dx, dy, del_w, Inches(0.26), d_title, d_color, WHITE, 8)
        # Content box
        d_box = s2.shapes.add_textbox(dx + Inches(0.06), dy + Inches(0.32), del_w - Inches(0.12), del_h - Inches(0.36))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
        
        # Audience
        p_aud = tf_d.paragraphs[0]
        p_aud.text = "Target: " + d_aud
        p_aud.font.size = Pt(8)
        p_aud.font.bold = True
        p_aud.font.color.rgb = d_color
        p_aud.space_after = Pt(2)
        
        # Description
        p_desc = tf_d.add_paragraph()
        p_desc.text = d_desc
        p_desc.font.size = Pt(7.5)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.space_after = Pt(3)

        # Format Pill
        p_fmt = tf_d.add_paragraph()
        p_fmt.text = "Format:\n" + d_fmt
        p_fmt.font.size = Pt(7.2)
        p_fmt.font.bold = True
        p_fmt.font.color.rgb = DARK_NAVY

    # =========================================================================
    # SLIDE 3 — TECHNICAL APPROACH: 4-TIER ARCHITECTURE & TECH STACK
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    draw_bg(s3)
    add_header(s3, "TECHNICAL APPROACH: 4-TIER ARCHITECTURE & CONCRETE STACK")

    # Left Side: 4 Horizontal Architectural Layers (Width: 7.8 Inches)
    layers = [
        ("TIER 1: USER EXPERIENCE & ENTERPRISE CONSOLE",
         "Next.js 14 (App Router) • React 18 • TypeScript 5.7 • Tailwind CSS 3.4",
         "Enterprise Trust Cockpit, Live Artifact Inspector, On-Demand Verification Tool, Real-time SSE streaming, and 38s Interactive Architecture Visualizer.",
         PRIMARY_BLUE),
        
        ("TIER 2: INGRESS DEFENSE, POLICY & ORCHESTRATION GATEWAY",
         "FastAPI 0.115 Async • Python 3.12 • Pydantic 2.10 • LangGraph 0.2 • Redis 7 + Python-RQ",
         "MIME magic-byte verification (%PDF-, PK), ClamAV daemon antivirus hooks, regex PII scrubbing (Aadhaar/PAN/Tokens), and deterministic 4-tier policy routing.",
         ACCENT_ROSE),

        ("TIER 3: AI INFERENCE, RAG GROUNDING & NLI FACT VERIFICATION",
         "Groq (openai/gpt-oss-120b) • Google Gemini API • Local Ollama/vLLM (Gemma 3 12B) • pgvector",
         "Dense semantic retrieval over HNSW index, chunk citation anchors, prompt delimiter fencing, and NLI entailment scoring (SUPPORTED/CONTRADICTED/UNVERIFIED).",
         ACCENT_PURPLE),

        ("TIER 4: STORAGE, DECENTRALIZED PROVENANCE & LEDGER PLANE",
         "PostgreSQL 16 + pgvector • MinIO / AWS S3 • Ethereum Sepolia Smart Contract • Ed25519 Web3.py",
         "Immutable SHA-256 artifact digests anchored on Ethereum Sepolia contract (0x8AEf...7c08) with Ed25519 asymmetric signatures (RFC 8032) for non-repudiation.",
         ACCENT_EMERALD)
    ]

    ly_top = Inches(1.45)
    ly_h = Inches(1.3)
    ly_gap = Inches(0.12)
    for k, (l_title, l_stack, l_desc, l_color) in enumerate(layers):
        curr_y = ly_top + k * (ly_h + ly_gap)
        add_card(s3, Inches(0.8), curr_y, Inches(7.6), ly_h, CARD_WHITE, CARD_BORDER, 1.2)
        # Left Accent Bar
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), curr_y, Inches(0.12), ly_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = l_color
        bar.line.fill.background()
        
        # Text Frame
        tb = s3.shapes.add_textbox(Inches(1.05), curr_y + Inches(0.08), Inches(7.2), ly_h - Inches(0.16))
        tf_l = tb.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
        
        p0 = tf_l.paragraphs[0]
        p0.text = l_title
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = l_color
        p0.space_after = Pt(1)

        p1 = tf_l.add_paragraph()
        p1.text = "Stack: " + l_stack
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = DARK_NAVY
        p1.space_after = Pt(2)

        p2 = tf_l.add_paragraph()
        p2.text = l_desc
        p2.font.size = Pt(8.2)
        p2.font.color.rgb = TEXT_MUTED

    # Right Side: Deep Technical Highlights & Engineering Metrics (Width: 3.9 Inches)
    add_card(s3, Inches(8.6), Inches(1.45), Inches(3.933), Inches(5.56), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s3, Inches(8.75), Inches(1.6), Inches(3.633), Inches(0.28), "CORE TECHNICAL & SECURITY SPECS", DARK_NAVY, WHITE, 8.5)

    specs = [
        ("Deterministic Policy Routing:", "Zero-LLM Authority: Policy engine is 100% pure Python. It decides whether content can use cloud or air-gapped local endpoints based on PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED classification.", PRIMARY_BLUE),
        ("Air-Gapped Sovereign Route:", "Sensitive data is physically restricted from cloud API egress; routed strictly to local Ollama / vLLM running Gemma 3 12B with 0% data leakage.", ACCENT_PURPLE),
        ("Fault Isolation Architecture:", "Nested database savepoints isolate individual generator errors. If one deliverable encounters an issue, the remaining 6 continue cleanly.", ACCENT_EMERALD),
        ("EVM Sepolia Smart Contract:", "Post-generation hook submits 32-byte content digests via Web3.py to Ethereum Sepolia. verifyDigest() enables public tamper detection.", ACCENT_CYAN),
        ("Automated Fact Verification:", "Natural Language Inference (NLI) cross-checks generated claims against source chunks, scoring grounding from 0.0 to 1.0.", ACCENT_AMBER)
    ]

    sp_box = s3.shapes.add_textbox(Inches(8.75), Inches(1.98), Inches(3.633), Inches(4.9))
    tf_sp = sp_box.text_frame
    tf_sp.word_wrap = True
    tf_sp.margin_left = tf_sp.margin_right = tf_sp.margin_top = tf_sp.margin_bottom = 0

    for idx, (sp_t, sp_d, sp_c) in enumerate(specs):
        p = tf_sp.paragraphs[0] if idx == 0 else tf_sp.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "▶ " + sp_t + " "
        r1.font.bold = True
        r1.font.size = Pt(8.8)
        r1.font.color.rgb = sp_c
        r2 = p.add_run()
        r2.text = sp_d
        r2.font.size = Pt(8.0)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4 — FEASIBILITY, VIABILITY & RISK MITIGATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    draw_bg(s4)
    add_header(s4, "FEASIBILITY, OPERATIONAL VIABILITY & RISK SAFEGUARDS")

    # 4 Feasibility Cards (Top Half: 2x2 Grid)
    f_cards = [
        ("TECHNICAL FEASIBILITY", PRIMARY_BLUE, [
            ("Asynchronous Queue Scaling: ", "Redis 7 + Python-RQ workers decouple generation from HTTP requests, eliminating timeouts on heavy PDF/PPTX builds."),
            ("Stateful Modular Isolation: ", "7 generator adapters execute independently. Failure in one output never crashes remaining siblings."),
            ("Hybrid Model Interoperability: ", "Provider interface dynamically routes between Groq, Gemini, and local Ollama Gemma 3.")
        ]),
        ("SECURITY & COMPLIANCE FEASIBILITY", ACCENT_ROSE, [
            ("NIST SP 800-207 Zero-Trust: ", "Pre-flight perimeter inspection: ClamAV anti-malware, magic-byte checks, and regex DLP PII scrubbing."),
            ("Air-Gapped Sovereign Enforcement: ", "Confidential institutional records physically forbidden from leaving private enclave networks."),
            ("Prompt Injection Fencing: ", "Strict instruction/data delimiters neutralize indirect prompt injection attacks.")
        ]),
        ("OPERATIONAL & WORKFLOW FEASIBILITY", ACCENT_PURPLE, [
            ("Dual-Key Human Approval Gate: ", "Mandatory human review checkpoint before external publication or social dissemination."),
            ("Destination-Aware Policies: ", "Restricted/internal outputs are hard-blocked from public social channels (LinkedIn/X)."),
            ("SIEM-Ready Structured Audit: ", "JSON audit logs capture all authentication, policy decisions, and verification events.")
        ]),
        ("ECONOMIC & FINANCIAL FEASIBILITY", ACCENT_EMERALD, [
            ("Ultra-Low Cost per Transformation: ", "Groq / Gemini Flash costs < ₹0.25 per 7-deliverable run; local air-gapped runs cost ₹0.00 in API fees."),
            ("Zero External Vector DB Fees: ", "Native pgvector inside PostgreSQL 16 eliminates costly third-party Pinecone/Weaviate subscriptions."),
            ("Massive 98%+ Operational ROI: ", "Replaces 4–6+ hours of human specialist synthesis with <25s automated execution.")
        ])
    ]

    for idx, (fc_title, fc_color, fc_bullets) in enumerate(f_cards):
        col = idx % 2
        row = idx // 2
        fx = Inches(0.8 + col * 5.95)
        fy = Inches(1.45 + row * 2.22)
        add_card(s4, fx, fy, Inches(5.75), Inches(2.1), CARD_WHITE, CARD_BORDER, 1.2)
        add_badge(s4, fx + Inches(0.12), fy + Inches(0.1), Inches(3.2), Inches(0.24), fc_title, fc_color, WHITE, 8)
        
        fc_box = s4.shapes.add_textbox(fx + Inches(0.12), fy + Inches(0.4), Inches(5.5), Inches(1.6))
        tf_fc = fc_box.text_frame
        tf_fc.word_wrap = True
        tf_fc.margin_left = tf_fc.margin_right = tf_fc.margin_top = tf_fc.margin_bottom = 0

        for b_idx, (b_t, b_d) in enumerate(fc_bullets):
            p = tf_fc.paragraphs[0] if b_idx == 0 else tf_fc.add_paragraph()
            p.space_after = Pt(3)
            r1 = p.add_run()
            r1.text = "• " + b_t
            r1.font.bold = True
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = DARK_NAVY
            r2 = p.add_run()
            r2.text = b_d
            r2.font.size = Pt(8.0)
            r2.font.color.rgb = TEXT_MUTED

    # Bottom Half: Risk vs Mitigation Strategy Table
    add_card(s4, Inches(0.8), Inches(5.95), Inches(11.733), Inches(1.25), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s4, Inches(0.95), Inches(5.78), Inches(3.6), Inches(0.24), "SECURITY & OPERATIONAL RISK MITIGATION MATRIX", DARK_NAVY, WHITE, 8)

    # Table Shape
    table_shape = s4.shapes.add_table(5, 3, Inches(0.9), Inches(6.08), Inches(11.5), Inches(1.0))
    table = table_shape.table
    table.columns[0].width = Inches(2.3)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(6.9)

    headers = ["Potential Risk Factor", "System Vulnerability", "KaryaSetu Concrete Mitigation Strategy"]
    for c_idx, h_text in enumerate(headers):
        style_cell(table.cell(0, c_idx), h_text, font_size=8, bold=True, color=WHITE, bg_color=DARK_NAVY, align=PP_ALIGN.CENTER)

    matrix_rows = [
        ("Prompt Injection & Hijacking", "Embedded commands inside untrusted files", "Strict delimiter encapsulation (<source_data>), tag neutralization, and input size clamping.", RGBColor(248, 250, 252)),
        ("Factual Hallucination & Drift", "Generators invent numbers/entities", "pgvector chunk-level citation anchoring + automated NLI entailment cross-verification.", WHITE),
        ("Confidential Data Exfiltration", "Sensitive data egress to public cloud", "Deterministic Python policy gate (zero LLM discretion); fails closed with HTTP 403 Forbidden.", RGBColor(248, 250, 252)),
        ("Post-Generation Deliverable Tamper", "Unauthorized document alteration", "Immutable SHA-256 hash anchored to Ethereum Sepolia smart contract + Ed25519 signature.", WHITE)
    ]
    for r_idx, (c0, c1, c2, r_bg) in enumerate(matrix_rows):
        style_cell(table.cell(r_idx + 1, 0), c0, font_size=7.5, bold=True, color=ACCENT_ROSE, bg_color=r_bg)
        style_cell(table.cell(r_idx + 1, 1), c1, font_size=7.5, bold=False, color=TEXT_MUTED, bg_color=r_bg)
        style_cell(table.cell(r_idx + 1, 2), c2, font_size=7.5, bold=False, color=TEXT_MAIN, bg_color=r_bg)

    # =========================================================================
    # SLIDE 5 — IMPACT, ECONOMIC COST, REFERENCES & VERIFIABLE PROOF
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    draw_bg(s5)
    add_header(s5, "INSTITUTIONAL IMPACT, COST STRUCTURE & VERIFIABLE PROOF")

    # Left Side: Cost Structure & Commercial Viability Table (Width: 6.2 Inches)
    add_card(s5, Inches(0.8), Inches(1.45), Inches(6.2), Inches(5.6), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s5, Inches(0.95), Inches(1.58), Inches(4.2), Inches(0.26), "ECONOMIC VIABILITY & OPERATIONAL COST BREAKDOWN", ACCENT_EMERALD, WHITE, 8.5)

    # Cost Table
    cost_table_shape = s5.shapes.add_table(8, 4, Inches(0.92), Inches(1.95), Inches(5.95), Inches(3.4))
    ct = cost_table_shape.table
    ct.columns[0].width = Inches(1.65)
    ct.columns[1].width = Inches(1.4)
    ct.columns[2].width = Inches(1.3)
    ct.columns[3].width = Inches(1.6)

    c_headers = ["Platform Component", "Unit / Monthly Cost", "Cost / 100 Runs", "Operational Notes"]
    for c_idx, ch_text in enumerate(c_headers):
        style_cell(ct.cell(0, c_idx), ch_text, font_size=7.8, bold=True, color=WHITE, bg_color=DARK_NAVY, align=PP_ALIGN.CENTER)

    cost_data = [
        ("Cloud LLM (Public Tier)", "Groq/Gemini (~$0.08/1M)", "~$0.60 – $1.20", "Generates all 7 deliverables per doc", WHITE),
        ("Air-Gapped LLM (Confidential)", "Local Gemma 3 12B", "$0.00 (Self-hosted)", "Runs on existing enterprise GPUs", RGBColor(248, 250, 252)),
        ("Blockchain Provenance", "Sepolia Testnet / Polygon", "<$0.15 (~₹12 total)", "45k gas per 32-byte digest anchor", WHITE),
        ("Compute Infrastructure", "Cloud VPS (2 vCPU, 4GB)", "~$15 – $25 / month", "Horizontally scalable RQ workers", RGBColor(248, 250, 252)),
        ("Vector & Relational DB", "PostgreSQL 16 + pgvector", "~$0 – $25 / month", "In-database HNSW cosine search", WHITE),
        ("Object Storage (Artifacts)", "MinIO / S3 on-premise", "~$1 – $5 / month", "Encrypted storage for PPTX/PDF/SVG", RGBColor(248, 250, 252)),
        ("TOTAL RUN COST", "< ₹0.25 / Document Run", "~$1.00 – $2.00 total", "Massive >98% cost savings vs manual", RGBColor(240, 253, 250))
    ]
    for r_idx, (col0, col1, col2, col3, r_bg) in enumerate(cost_data):
        is_total = (r_idx == len(cost_data) - 1)
        style_cell(ct.cell(r_idx + 1, 0), col0, font_size=7.5, bold=is_total, color=DARK_NAVY if not is_total else ACCENT_EMERALD, bg_color=r_bg)
        style_cell(ct.cell(r_idx + 1, 1), col1, font_size=7.2, bold=is_total, color=TEXT_MUTED if not is_total else DARK_NAVY, bg_color=r_bg)
        style_cell(ct.cell(r_idx + 1, 2), col2, font_size=7.2, bold=is_total, color=PRIMARY_BLUE if not is_total else ACCENT_EMERALD, bg_color=r_bg)
        style_cell(ct.cell(r_idx + 1, 3), col3, font_size=7.2, bold=False, color=TEXT_MUTED, bg_color=r_bg)

    # Cost Summary Callout at Bottom of Left Card
    cost_summary_box = s5.shapes.add_textbox(Inches(0.92), Inches(5.5), Inches(5.95), Inches(1.4))
    tf_cs = cost_summary_box.text_frame
    tf_cs.word_wrap = True
    tf_cs.margin_left = tf_cs.margin_right = tf_cs.margin_top = tf_cs.margin_bottom = 0
    p_cs = tf_cs.paragraphs[0]
    p_cs.text = "💰 Business ROI Impact: Manual human synthesis of 500 documents/month consumes ~250 hours costing ₹2,50,000+. With KaryaSetu AI, the identical volume completes in under 5 hours total review time at ~₹3,500 total infrastructure cost (>95% operational ROI)."
    p_cs.font.size = Pt(8.2)
    p_cs.font.color.rgb = DARK_NAVY

    # Right Side Top: Quantifiable Institutional Impact (Width: 5.3 Inches)
    add_card(s5, Inches(7.2), Inches(1.45), Inches(5.333), Inches(2.65), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s5, Inches(7.35), Inches(1.58), Inches(3.6), Inches(0.26), "QUANTIFIABLE INSTITUTIONAL IMPACT", PRIMARY_BLUE, WHITE, 8.5)

    imp_box = s5.shapes.add_textbox(Inches(7.35), Inches(1.92), Inches(5.0), Inches(2.1))
    tf_imp = imp_box.text_frame
    tf_imp.word_wrap = True
    tf_imp.margin_left = tf_imp.margin_right = tf_imp.margin_top = tf_imp.margin_bottom = 0

    impact_items = [
        ("10x Acceleration in Synthesis: ", "Transforms 50+ page technical briefs into 7 audience deliverables in under 25 seconds."),
        ("Zero Data Leakage Guarantee: ", "Rigid deterministic policy enforcement prevents classified national intelligence from leaving sovereign infrastructure."),
        ("Elimination of Multi-Channel Drift: ", "All deliverables ground to a single canonical fact brief with automated NLI consistency cross-checks."),
        ("Complete Tamper Detection: ", "Ethereum Sepolia smart contract anchoring ensures post-generation deliverable integrity.")
    ]
    for idx, (it_t, it_d) in enumerate(impact_items):
        p = tf_imp.paragraphs[0] if idx == 0 else tf_imp.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = "★ " + it_t
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = PRIMARY_BLUE
        r2 = p.add_run()
        r2.text = it_d
        r2.font.size = Pt(8.0)
        r2.font.color.rgb = TEXT_MUTED

    # Right Side Bottom: Live References & Proof Links (Width: 5.3 Inches)
    add_card(s5, Inches(7.2), Inches(4.25), Inches(5.333), Inches(2.8), CARD_WHITE, CARD_BORDER, 1.2)
    add_badge(s5, Inches(7.35), Inches(4.38), Inches(3.6), Inches(0.26), "LIVE VERIFICATION LINKS & CITED STANDARDS", DARK_NAVY, WHITE, 8.5)

    ref_box = s5.shapes.add_textbox(Inches(7.35), Inches(4.72), Inches(5.0), Inches(2.25))
    tf_ref = ref_box.text_frame
    tf_ref.word_wrap = True
    tf_ref.margin_left = tf_ref.margin_right = tf_ref.margin_top = tf_ref.margin_bottom = 0

    refs = [
        ("Smart Contract (Sepolia Etherscan):", "0x8AEf680b6891E7e3cAdCBD4a499AbA1310F87c08", "https://sepolia.etherscan.io/address/0x8AEf680b6891E7e3cAdCBD4a499AbA1310F87c08"),
        ("Relayer Signer Identity:", "0x460bb6AE2AD8a515d5E2886c69b78d8e3C2FBc41", "https://sepolia.etherscan.io/address/0x460bb6AE2AD8a515d5E2886c69b78d8e3C2FBc41"),
        ("GitHub Repository:", "https://github.com/KetanGaikwadKRG/KaryaSetu", "https://github.com/KetanGaikwadKRG/KaryaSetu"),
        ("Official Evaluation Video:", "https://youtu.be/Lhi1ssHBfUk?si=T5bIOl2TWDeIf7DJ", "https://youtu.be/Lhi1ssHBfUk?si=T5bIOl2TWDeIf7DJ"),
        ("Cited Standards & Literature:", "NIST SP 800-207 (Zero Trust) • RFC 8032 (Ed25519) • W3C PROV-DM • IT Act Section 70", "")
    ]
    for idx, (rt, rd, rurl) in enumerate(refs):
        p = tf_ref.paragraphs[0] if idx == 0 else tf_ref.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = "🔗 " + rt + " "
        r1.font.bold = True
        r1.font.size = Pt(8.2)
        r1.font.color.rgb = DARK_NAVY
        r2 = p.add_run()
        r2.text = rd
        r2.font.size = Pt(7.8)
        r2.font.color.rgb = PRIMARY_BLUE if rurl else TEXT_MUTED
        if rurl:
            r2.font.underline = True

    # Save Presentation
    output_path = os.path.join("presentation", "KaryaSetu_Technical_Presentation.pptx")
    prs.save(output_path)
    print(f"Successfully generated winning presentation with {len(prs.slides)} slides at: {output_path}")

if __name__ == "__main__":
    create_presentation()

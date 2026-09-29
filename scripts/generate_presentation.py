"""Generate the canonical 5-slide SIH Technical Presentation for KaryaSetu AI."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    NAVY = RGBColor(15, 23, 42)       # #0f172a
    CARD_BG = RGBColor(248, 250, 252) # #f8fafc
    CARD_BORDER = RGBColor(203, 213, 225) # #cbd5e1
    PRIMARY_BLUE = RGBColor(2, 132, 199) # #0284c7
    TEXT_DARK = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(71, 85, 105) # #475569
    ACCENT_TEAL = RGBColor(13, 148, 136) # #0d9488
    ACCENT_PURPLE = RGBColor(124, 58, 237) # #7c3aed
    ACCENT_ORANGE = RGBColor(234, 88, 12) # #ea580c
    WHITE = RGBColor(255, 255, 255)

    def add_header(slide, title_text, category_text="SIH 26154 • BLOCKCHAIN & CYBERSECURITY"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_BLUE
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # =========================================================================
    # SLIDE 1 — PROBLEM & SOLUTION
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Title Block
    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(1.8))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    p_tag = tf1.paragraphs[0]
    p_tag.text = "SMART INDIA HACKATHON 2026 • THEME: BLOCKCHAIN & CYBERSECURITY (PS ID: SIH 26154)"
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = PRIMARY_BLUE
    p_tag.space_after = Pt(4)

    p_title = tf1.add_paragraph()
    p_title.text = "KARYASETU AI"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

    p_sub = tf1.add_paragraph()
    p_sub.text = "Gen AI Platform for Automated Content Transformation"
    p_sub.font.size = Pt(16)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ACCENT_TEAL
    p_sub.space_after = Pt(4)

    p_tagline = tf1.add_paragraph()
    p_tagline.text = "One Trusted Source → Seven Governed, Audience-Ready Deliverables"
    p_tagline.font.size = Pt(13)
    p_tagline.font.italic = True
    p_tagline.font.color.rgb = TEXT_MUTED

    # Problem Card (Left)
    add_card(s1, Inches(0.8), Inches(2.9), Inches(5.6), Inches(4.0))
    p_box = s1.shapes.add_textbox(Inches(1.0), Inches(3.1), Inches(5.2), Inches(3.6))
    tf_prob = p_box.text_frame
    tf_prob.word_wrap = True
    p_h = tf_prob.paragraphs[0]
    p_h.text = "THE PROBLEM"
    p_h.font.size = Pt(16)
    p_h.font.bold = True
    p_h.font.color.rgb = ACCENT_ORANGE
    p_h.space_after = Pt(8)

    prob_items = [
        ("Sensitive Data Exposure: ", "Confidential institutional records sent indiscriminately to external cloud LLMs violate data sovereignty regulations."),
        ("Prompt Injection & Manipulation: ", "Untrusted text and malicious instructions can hijack transformation workflows and leak secrets."),
        ("Untrusted & Floating Evidence: ", "Standard RAG models retrieve unverified context, hallucinate citations, and lack factual grounding."),
        ("Cross-Output Fact Drift: ", "Multi-audience collateral (press releases, decks, briefs) diverges in numeric metrics and key findings."),
        ("Manual Transformation Friction: ", "Converting complex source documents into audience-ready outputs requires days of error-prone human rework.")
    ]
    for bold_txt, body_txt in prob_items:
        p = tf_prob.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = body_txt
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED

    # Solution Card (Right)
    add_card(s1, Inches(6.9), Inches(2.9), Inches(5.6), Inches(4.0), bg_color=RGBColor(240, 249, 255), border_color=PRIMARY_BLUE)
    s_box = s1.shapes.add_textbox(Inches(7.1), Inches(3.1), Inches(5.2), Inches(3.6))
    tf_sol = s_box.text_frame
    tf_sol.word_wrap = True
    s_h = tf_sol.paragraphs[0]
    s_h.text = "THE KARYASETU SOLUTION"
    s_h.font.size = Pt(16)
    s_h.font.bold = True
    s_h.font.color.rgb = PRIMARY_BLUE
    s_h.space_after = Pt(8)

    sol_items = [
        ("Policy-Controlled Provider Routing: ", "Deterministic zero-LLM classification (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED). Air-gaps sensitive data."),
        ("Evidence-Grounded RAG: ", "Source chunks anchored via vector embeddings. Synthesizes a unified canonical semantic brief once for all generators."),
        ("7 Audience-Specific Generators: ", "Produces Summary, LinkedIn, Advisory, PPTX deck, X thread, Infographic (PNG/PDF), and Video Package (PDF/SRT)."),
        ("Dual-Layer Fact Verification: ", "Deterministic numeric mismatch, date conflict, and lexical overlap auditing. Bounded schema regeneration on format errors."),
        ("Human Approval & Cryptographic Trust: ", "Human-in-the-loop sign-off before external release, sealed with SHA-256 digests and Ed25519 digital signatures.")
    ]
    for bold_txt, body_txt in sol_items:
        p = tf_sol.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "✓ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = body_txt
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2 — TECHNICAL ARCHITECTURE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "TECHNICAL ARCHITECTURE: 5-TIER MODULAR PLATFORM")

    layers = [
        ("TIER 1: USER ENTRY & DASHBOARD", "Next.js 14 • React • TypeScript • Tailwind CSS", 
         "Stitch enterprise UI console with 4-stage creation workflow (Input Workspace → Configuration → Output Packages → Review & Dispatch). Real-time progress tracking and artifact inspection."),
        ("TIER 2: SECURE INGESTION GATE", "Magic Bytes • ClamAV Scanner • PII Detector", 
         "Validates MIME signatures (%PDF-, PK\\x03\\x04) to prevent type-confusion attacks. Local ClamAV anti-malware scan fails closed. Regex PII scanning redacts sensitive personal identifiers."),
        ("TIER 3: POLICY & CLASSIFICATION ENGINE", "Deterministic Zero-LLM Policy Engine & Router", 
         "Strict governance: 'LLM May Recommend, Policy Engine Must Decide'. Automatically maps data classification (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED) to allowed model routes (Cloud vs Air-Gapped)."),
        ("TIER 4: AI TRANSFORMATION & ORCHESTRATION", "LangGraph Workflow • Multi-Provider Registry", 
         "StateGraph pipeline (load_input → load_canonical → retrieve → brief → plan → generate → validate → verify → finalize). Isolated per-output savepoints ensure partial success tolerance."),
        ("TIER 5: TRUST, GOVERNANCE & PROVENANCE", "Ed25519 Signatures • SHA-256 Digests • Ledger Boundary", 
         "Fact verification checks numeric and date consistency. Human approval gate controls dissemination. Cryptographic integrity envelope sealed with asymmetric Ed25519 signatures.")
    ]

    for i, (title, stack, desc) in enumerate(layers):
        y_pos = Inches(1.6 + i * 0.95)
        add_card(s2, Inches(0.8), y_pos, Inches(8.2), Inches(0.85))
        c_box = s2.shapes.add_textbox(Inches(0.95), y_pos + Inches(0.06), Inches(7.9), Inches(0.73))
        tf = c_box.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r_t = p0.add_run()
        r_t.text = title + "  "
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = PRIMARY_BLUE
        r_s = p0.add_run()
        r_s.text = "[" + stack + "]"
        r_s.font.size = Pt(9.5)
        r_s.font.bold = True
        r_s.font.color.rgb = ACCENT_PURPLE
        
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = TEXT_MUTED

    # Supporting Storage Infrastructure (Right Column)
    add_card(s2, Inches(9.3), Inches(1.6), Inches(3.2), Inches(4.6), bg_color=RGBColor(241, 245, 249), border_color=CARD_BORDER)
    st_box = s2.shapes.add_textbox(Inches(9.45), Inches(1.75), Inches(2.9), Inches(4.3))
    tf_st = st_box.text_frame
    tf_st.word_wrap = True
    p_sh = tf_st.paragraphs[0]
    p_sh.text = "PERSISTENCE & STORAGE"
    p_sh.font.size = Pt(13)
    p_sh.font.bold = True
    p_sh.font.color.rgb = NAVY
    p_sh.space_after = Pt(8)

    storage_items = [
        ("PostgreSQL 16 + pgvector", "Relational persistence for jobs, outputs, verification logs, and 768-dim vector embeddings."),
        ("Redis 7 + RQ Worker", "Asynchronous job queuing, worker task dispatch, and rate-limiting cache."),
        ("S3 / MinIO Object Store", "Binary storage for raw uploaded sources, PPTX presentations, PNGs, and PDF packages."),
        ("Cryptographic Ledger Boundary", "Configuration-ready provenance ledger interface storing immutable SHA-256 digest trees.")
    ]
    for name, s_desc in storage_items:
        p = tf_st.add_paragraph()
        p.space_after = Pt(6)
        r1 = p.add_run()
        r1.text = "• " + name + ": "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = s_desc
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3 — END-TO-END PROCESS WORKFLOW
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "END-TO-END PROCESS WORKFLOW: FROM SOURCE TO SEVEN OUTPUTS")

    # Workflow Steps
    steps = [
        ("1. SOURCE INPUT", "User uploads PDF, DOCX, TXT or raw prompt with target audience, tone, and language directives.", PRIMARY_BLUE),
        ("2. INGESTION & SCAN", "Magic byte verification, ClamAV anti-malware scan, PII detection, text extraction & chunking.", ACCENT_TEAL),
        ("3. CLASSIFICATION & POLICY", "Evaluates PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. Denies cloud processing for sensitive data.", ACCENT_ORANGE),
        ("4. COMPLIANT AI ROUTING", "Routes unclassified data to Cloud AI (Gemini) or air-gapped sensitive data to Private AI (Gemma 3 12B).", ACCENT_PURPLE),
        ("5. EVIDENCE-GROUNDED RAG", "Task-aware vector retrieval formulates top-k citations into an immutable canonical semantic brief.", PRIMARY_BLUE),
        ("6. TRANSFORMATION & GENERATION", "7 isolated output generators execute in parallel with nested savepoints and bounded regeneration.", ACCENT_PURPLE),
        ("7. FACT & SCHEMA VERIFICATION", "Automated fact-checking: claim extraction, numeric consistency, date conflict detection, grounding scores.", ACCENT_TEAL),
        ("8. HUMAN APPROVAL GATE", "Governance review: policy overrides approval. Operators review and approve or reject before release.", ACCENT_ORANGE),
        ("9. DISSEMINATION & SIGNING", "Controlled multi-channel release (LinkedIn, X, PPTX/PDF export). Sealed with SHA-256 and Ed25519.", NAVY)
    ]

    for i, (stitle, sdesc, scolor) in enumerate(steps[:5]):
        y_pos = Inches(1.6 + i * 0.95)
        add_card(s3, Inches(0.8), y_pos, Inches(5.6), Inches(0.82))
        sb = s3.shapes.add_textbox(Inches(0.95), y_pos + Inches(0.04), Inches(5.3), Inches(0.72))
        tf = sb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r1 = p0.add_run()
        r1.text = stitle + "  "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = scolor
        p1 = tf.add_paragraph()
        p1.text = sdesc
        p1.font.size = Pt(9)
        p1.font.color.rgb = TEXT_MUTED

    for i, (stitle, sdesc, scolor) in enumerate(steps[5:]):
        y_pos = Inches(1.6 + i * 1.18)
        add_card(s3, Inches(6.8), y_pos, Inches(5.7), Inches(1.02))
        sb = s3.shapes.add_textbox(Inches(6.95), y_pos + Inches(0.06), Inches(5.4), Inches(0.9))
        tf = sb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        r1 = p0.add_run()
        r1.text = stitle + "  "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = scolor
        p1 = tf.add_paragraph()
        p1.text = sdesc
        p1.font.size = Pt(9)
        p1.font.color.rgb = TEXT_MUTED

    # Highlight 7 outputs at the bottom of left column
    add_card(s3, Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.8), bg_color=RGBColor(240, 253, 244), border_color=RGBColor(34, 197, 94))
    o_box = s3.shapes.add_textbox(Inches(0.95), Inches(6.42), Inches(11.4), Inches(0.65))
    tf_o = o_box.text_frame
    tf_o.word_wrap = True
    p_ot = tf_o.paragraphs[0]
    p_ot.text = "THE 7 PARALLEL OUTPUT PACKAGES:  "
    p_ot.font.bold = True
    p_ot.font.size = Pt(10)
    p_ot.font.color.rgb = RGBColor(22, 101, 52)
    p_or = tf_o.add_paragraph()
    p_or.text = "[1] Executive Summary (Briefing)  •  [2] LinkedIn Post (Social)  •  [3] Policy Advisory (Impact & Risks)  •  [4] Presentation Deck (.pptx)\n[5] X Micro-Copy (Thread)  •  [6] Infographic (PNG + PDF)  •  [7] Video Package (Structured Storyboard PDF + SRT Subtitles — NOT MP4)"
    p_or.font.size = Pt(9)
    p_or.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4 — SECURITY, GOVERNANCE & INNOVATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "SECURITY, GOVERNANCE & INNOVATION HIGHLIGHTS")

    cards = [
        ("POLICY-CONTROLLED AI ROUTING", ACCENT_ORANGE, [
            ("Zero-LLM Authority: ", "Policy engine is pure Python, deterministic, and offline. Never allows LLM to override access rules."),
            ("Information Classification: ", "PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED assigned at ingestion."),
            ("Air-Gapped Sovereign Enforcement: ", "CONFIDENTIAL/RESTRICTED data is strictly forbidden from external cloud LLMs. Fails closed with HTTP 403."),
            ("Dissemination Restrictions: ", "Restricted materials are hard-blocked from public social channels (LinkedIn/X).")
        ]),
        ("EVIDENCE-GROUNDED GENERATION", PRIMARY_BLUE, [
            ("Single Canonical Brief: ", "Extracts facts, claims, statistics, and entities once into CanonicalContent to prevent drift."),
            ("Top-k Citations: ", "RAGService anchors generation to exact source chunk offsets with SHA-256 chunk hashes."),
            ("Bounded Regeneration: ", "Pydantic output schema validation retries on structural errors without prompt re-injection."),
            ("Failure Isolation: ", "Nested DB savepoints isolate output errors so one failure never cancels remaining siblings.")
        ]),
        ("DETERMINISTIC FACT VERIFICATION", ACCENT_TEAL, [
            ("Automated Claim Auditing: ", "Extracts checkable claims from generated outputs and validates them against source chunks."),
            ("Numeric & Date Conflict Checks: ", "Flags metric discrepancies and mismatched timeline dates automatically as warnings/errors."),
            ("Consistency Scoring: ", "Provides quantitative grounding and consistency scores on every completed deliverable."),
            ("On-Demand Verification: ", "Standalone fact verifier assigns explicit SUPPORTED / CONTRADICTED / UNVERIFIED verdicts.")
        ]),
        ("CRYPTOGRAPHIC TRUST & AUDIT LINEAGE", NAVY, [
            ("SHA-256 Storage Digests: ", "Calculates exact cryptographic hashes of all generated binary artifacts (.pptx, .png, .pdf, .srt)."),
            ("Ed25519 Asymmetric Signatures: ", "Authoritative production signing for non-repudiation. Zero private keys exposed in API or logs."),
            ("Human-in-the-Loop Approval: ", "Dissemination policy trumps approval. Operators must sign off before external publication."),
            ("Provenance Ledger Boundary: ", "Pre-built ledger adapter ready for immutable audit tracking (FakeLedger mock in test, RealLedger in prod).")
        ])
    ]

    for idx, (ctitle, ccolor, citems) in enumerate(cards):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 5.95)
        y = Inches(1.6 + row * 2.7)
        add_card(s4, x, y, Inches(5.75), Inches(2.55))
        cb = s4.shapes.add_textbox(x + Inches(0.15), y + Inches(0.12), Inches(5.45), Inches(2.35))
        tf = cb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = ctitle
        p0.font.bold = True
        p0.font.size = Pt(12)
        p0.font.color.rgb = ccolor
        p0.space_after = Pt(6)

        for b_txt, d_txt in citems:
            p = tf.add_paragraph()
            p.space_after = Pt(3)
            r1 = p.add_run()
            r1.text = "• " + b_txt
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = TEXT_DARK
            r2 = p.add_run()
            r2.text = d_txt
            r2.font.size = Pt(9)
            r2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5 — IMPACT, DEPLOYMENT & FUTURE EXTENSIBILITY
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "IMPACT, DEPLOYMENT & STRATEGIC EXTENSIBILITY")

    # Impact Card
    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.75), Inches(5.35))
    i_box = s5.shapes.add_textbox(Inches(0.95), Inches(1.75), Inches(5.45), Inches(5.0))
    tf_i = i_box.text_frame
    tf_i.word_wrap = True
    p_ih = tf_i.paragraphs[0]
    p_ih.text = "QUANTIFIABLE INSTITUTIONAL IMPACT"
    p_ih.font.bold = True
    p_ih.font.size = Pt(14)
    p_ih.font.color.rgb = PRIMARY_BLUE
    p_ih.space_after = Pt(10)

    impacts = [
        ("10x Acceleration in Collateral Synthesis: ", "Transforms 50+ page policy documents or technical whitepapers into 7 audience-tailored formats in under 60 seconds."),
        ("Zero Cloud Leakage Guarantee: ", "Rigid deterministic policy enforcement prevents confidential national or institutional intelligence from leaving sovereign infrastructure."),
        ("Elimination of Multi-Channel Drift: ", "All outputs ground to a single canonical brief, ensuring quantitative metrics remain perfectly aligned across social, executive, and public channels."),
        ("Complete Auditability & Non-Repudiation: ", "Every artifact is sealed with SHA-256 digests and Ed25519 signatures, creating an unforgeable evidentiary chain."),
        ("Drastic Reduction in Human Workload: ", "Automates repetitive document rewriting, slide formatting, infographic structure, and script generation while keeping human review at the release gate.")
    ]
    for b_txt, d_txt in impacts:
        p = tf_i.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = "★ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = d_txt
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_MUTED

    # Deployment Models (Top Right)
    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.75), Inches(2.55), bg_color=RGBColor(240, 253, 250), border_color=ACCENT_TEAL)
    d_box = s5.shapes.add_textbox(Inches(6.95), Inches(1.72), Inches(5.45), Inches(2.35))
    tf_d = d_box.text_frame
    tf_d.word_wrap = True
    p_dh = tf_d.paragraphs[0]
    p_dh.text = "DEPLOYMENT ARCHITECTURE & ENVIRONMENTS"
    p_dh.font.bold = True
    p_dh.font.size = Pt(13)
    p_dh.font.color.rgb = ACCENT_TEAL
    p_dh.space_after = Pt(6)

    deploy_items = [
        ("Hybrid Cloud Deployment: ", "FastAPI backend + Next.js frontend deployed on cloud infrastructure using Gemini 2.5 Flash for public institutional transformation."),
        ("On-Premise / Air-Gapped Deployment: ", "Self-contained Docker Compose stack with local Ollama/vLLM endpoints (Gemma 3 12B) and local ClamAV scanning for sensitive environments."),
        ("Stateless Worker Scalability: ", "Horizontal RQ workers consume Redis transformation queues independently with database-level concurrency locking.")
    ]
    for b_txt, d_txt in deploy_items:
        p = tf_d.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = d_txt
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    # Future Extensibility (Bottom Right)
    add_card(s5, Inches(6.8), Inches(4.4), Inches(5.75), Inches(2.55), bg_color=RGBColor(250, 245, 255), border_color=ACCENT_PURPLE)
    e_box = s5.shapes.add_textbox(Inches(6.95), Inches(4.52), Inches(5.45), Inches(2.35))
    tf_e = e_box.text_frame
    tf_e.word_wrap = True
    p_eh = tf_e.paragraphs[0]
    p_eh.text = "FUTURE ROADMAP & SYSTEM EXTENSIBILITY"
    p_eh.font.bold = True
    p_eh.font.size = Pt(13)
    p_eh.font.color.rgb = ACCENT_PURPLE
    p_eh.space_after = Pt(6)

    ext_items = [
        ("Extended Local Models: ", "Plug-and-play provider registry architecture allows adding fine-tuned multilingual Indic LLMs (Sarvam, Bhashini)."),
        ("Live Blockchain Integration: ", "Active RealLedger boundary designed to plug directly into Hyperledger Fabric or Polygon enterprise nodes for government audit."),
        ("Additional Output Formats: ", "Modular Generator ABC interface easily accommodates interactive dashboards, voice podcasts, and press releases."),
        ("Multi-Agency Dissemination: ", "Configurable policy matrices support custom ministry approval chains and fine-grained department-level access rules.")
    ]
    for b_txt, d_txt in ext_items:
        p = tf_e.add_paragraph()
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = "→ " + b_txt
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        r2 = p.add_run()
        r2.text = d_txt
        r2.font.size = Pt(9)
        r2.font.color.rgb = TEXT_MUTED

    output_path = os.path.join("presentation", "KaryaSetu_Technical_Presentation.pptx")
    prs.save(output_path)
    print(f"Successfully generated presentation with {len(prs.slides)} slides at: {output_path}")

if __name__ == "__main__":
    create_presentation()

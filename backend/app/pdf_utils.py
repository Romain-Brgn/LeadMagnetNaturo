from __future__ import annotations
from datetime import date, datetime
from pathlib import Path
from typing import Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,

)

from app.schemas import AiReport


# ------------------------------------------------------------
# Palette de couleurs 
# ------------------------------------------------------------
C_VERT_DARK = colors.HexColor("#2D5A27")  # Titres
C_TERRE = colors.HexColor("#A67C52")      # Sous-titres
C_GRIS_FOND = colors.HexColor("#F4F7F4")  # Lignes tableau
C_TEXTE = colors.HexColor("#333333")      # Texte principal

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def _safe_get(obj: Any, path: str, default: str = "") -> str:
    cur = obj
    for key in path.split("."):
        if cur is None: return default
        if isinstance(cur, dict): cur = cur.get(key)
        else: cur = getattr(cur, key, None)
    if cur is None: return default
    return str(cur).strip()

def _clean_text(s: str) -> str:
    s = (s or "").replace("\r", "").strip()
    while "\n\n\n" in s: s = s.replace("\n\n\n", "\n\n")
    return s

def _register_font_if_available():
    return "Helvetica"

def _draw_header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, height - 1.2 * cm, "LeadMagnetNaturo • Rapport personnalisé")
    canvas.drawRightString(width - 2 * cm, 1.1 * cm, f"Page {doc.page}")
    canvas.restoreState()

# ------------------------------------------------------------
# Main PDF generator
# ------------------------------------------------------------
def generate_pdf_report(submission: dict, email: str, out_dir: Path, report: AiReport | dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    report_name = f"rapport_{submission['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    out_path = out_dir / report_name
    base_font = _register_font_if_available()
    styles = getSampleStyleSheet()

    # --- STYLES MIS À JOUR ---
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontName=base_font, fontSize=26, textColor=C_VERT_DARK, alignment=1, spaceAfter=20)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName=base_font, fontSize=11, alignment=1, textColor=colors.grey, spaceAfter=18)
    h1_style = ParagraphStyle("H1", parent=styles["Heading2"], fontName=base_font, fontSize=16, leading=20, spaceBefore=18, spaceAfter=10, textColor=C_VERT_DARK)
    h2_style = ParagraphStyle("H2", parent=styles["Heading3"], fontName=base_font, fontSize=12, leading=15, spaceBefore=10, spaceAfter=6, textColor=C_TERRE)
    body_style = ParagraphStyle("Body", parent=styles["BodyText"], fontName=base_font, fontSize=10.5, leading=15, spaceAfter=10, textColor=C_TEXTE, alignment=4)
    small_style = ParagraphStyle("Small", parent=styles["BodyText"], fontName=base_font, fontSize=9.5, leading=13, textColor=colors.grey, spaceAfter=6)

    doc = SimpleDocTemplate(str(out_path), pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # Intro
    story.append(Paragraph("Votre profil hippocratique", title_style))
    story.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", subtitle_style))

    # Data initiales
    top1_list = submission.get("top1", []) or []
    top2_list = submission.get("top2", []) or []
    dominant = " / ".join([t.capitalize() for t in top1_list]) if top1_list else "—"
    subdominant = " / ".join([t.capitalize() for t in top2_list]) if top2_list else "—"

    story.append(Paragraph(f"<b>Profil dominant :</b> <font color='{C_VERT_DARK}'>{dominant}</font>", body_style))
    story.append(Paragraph(f"<b>Profil sous-jacent :</b> <font color='{C_TERRE}'>{subdominant}</font>", body_style))
    story.append(Spacer(1, 10))

    # Tableau stylisé
    story.append(Paragraph("Résultat", h1_style))
    percentages = submission.get("percentages", {}) or {}
    order = ["sanguin", "bilieux", "lymphatique", "nerveux"]
    table_data = [["Tempérament", "Pourcentage"]]
    for k in order:
        v = percentages.get(k, 0)
        table_data.append([k.capitalize(), f"{v}%"])

    t = Table(table_data, colWidths=[9 * cm, 4 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_VERT_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, C_GRIS_FOND]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        ('FONTNAME', (0, 0), (-1, -1), base_font),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph("Les sections suivantes proposent des pistes d'hygiène de vie...", small_style))

    # IA Content 
    report_obj = report
    
    # PORTRAIT
    story.append(Paragraph("Votre portrait", h1_style))
    story.append(Paragraph("Apparence physique", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "portrait.apparence_physique")), body_style))
    story.append(Paragraph("Énergie et sommeil", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "portrait.energie_sommeil")), body_style))
    story.append(Paragraph("Comportement", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "portrait.comportement")), body_style))
    story.append(Paragraph("Qualités et défauts", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "portrait.qualites_defauts")), body_style))
    
    sante = _safe_get(report_obj, "portrait.sante_predispositions") or _safe_get(report_obj, "portrait.sante_generale")
    story.append(Paragraph("Santé générale", h2_style)); story.append(Paragraph(_clean_text(sante), body_style))

    # ALIMENTATION
    story.append(Paragraph("Alimentation", h1_style))
    story.append(Paragraph("Métabolisme", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "alimentation.metabolisme")), body_style))
    story.append(Paragraph("Alimentation optimale", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "alimentation.aliments_conseilles")), body_style))
    story.append(Paragraph("Alimentation à éviter", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "alimentation.aliments_a_eviter")), body_style))

    # ACTIVITÉ
    story.append(Paragraph("Activité physique et psychique", h1_style))
    story.append(Paragraph("Sport recommandé", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "activite.activite_physique_conseillee")), body_style))
    story.append(Paragraph("Régulation du stress", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "activite.regulation_emotionnelle")), body_style))
    story.append(Paragraph("Soutien émotionnel", h2_style)); story.append(Paragraph(_clean_text(_safe_get(report_obj, "activite.tips_soutien_emotionnel")), body_style))

    # REPROGRAMMATION
    story.append(Paragraph("Reprogrammation positive", h1_style))
    story.append(Paragraph(_clean_text(_safe_get(report_obj, "reprogrammation_positive")), body_style))

    # --- TON DISCLAIMER (RÉTABLI ET PROTÉGÉ) ---
    story.append(Spacer(1, 14))
    story.append(Paragraph("Disclaimer", h1_style))
    disclaimer = (
        "Ce rapport est fourni à titre informatif et éducatif uniquement. "
        "Il ne constitue pas un avis médical, un diagnostic, ni une prescription. "
        "Les informations proposées ne remplacent en aucun cas une consultation auprès d'un professionnel "
        "de santé qualifié. En cas de symptômes, de maladie, de traitement en cours, de grossesse ou de toute "
        "situation médicale particulière, rapprochez-vous de votre médecin ou d'un professionnel de santé. "
        "L'auteur et l'éditeur déclinent toute responsabilité quant à l'usage qui pourrait être fait de ce document."
    )
    story.append(Paragraph(_clean_text(disclaimer), body_style))

    doc.build(story, onFirstPage=_draw_header_footer, onLaterPages=_draw_header_footer)
    return out_path
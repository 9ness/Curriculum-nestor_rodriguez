#!/usr/bin/env python3
"""Genera un CV en PDF (A4, 1-2 páginas) a partir de cv/datos.json.

Uso:
    python tools/generar_pdf.py                       # -> web/cv.pdf + cv/CV-Nestor-Rodriguez-Tubio.pdf
    python tools/generar_pdf.py cv/datos.json out.pdf # personalizado

Requiere: pip install reportlab  (puro Python, sin dependencias del sistema).
"""
import json, sys, pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ACCENT = HexColor("#2b57c9")
INK = HexColor("#1a2333")
MUTED = HexColor("#5c6b82")
SOFT = HexColor("#eef2fb")

styles = getSampleStyleSheet()
S = {
    "name": ParagraphStyle("name", parent=styles["Title"], fontName="Helvetica-Bold",
                           fontSize=22, textColor=INK, spaceAfter=2, leading=24, alignment=TA_LEFT if False else 0),
    "titular": ParagraphStyle("titular", fontName="Helvetica-Bold", fontSize=11.5,
                              textColor=ACCENT, spaceAfter=4, leading=14),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.6,
                             textColor=MUTED, spaceAfter=2, leading=12),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, textColor=ACCENT,
                         spaceBefore=10, spaceAfter=3, leading=13),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.3, textColor=INK,
                          leading=12.5, spaceAfter=2),
    "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=10, textColor=INK, leading=12),
    "date": ParagraphStyle("date", fontName="Helvetica", fontSize=8.6, textColor=MUTED,
                          leading=12, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.1, textColor=HexColor("#33404f"),
                            leading=12, spaceAfter=1),
    "stack": ParagraphStyle("stack", fontName="Helvetica-Oblique", fontSize=8, textColor=MUTED,
                           leading=10, spaceAfter=3),
    "skill": ParagraphStyle("skill", fontName="Helvetica", fontSize=9.1, textColor=INK,
                           leading=12.5, spaceAfter=1),
    "hl": ParagraphStyle("hl", fontName="Helvetica", fontSize=9, textColor=INK, leading=12),
}


def section(title):
    return [Paragraph(title.upper(), S["h2"]),
            HRFlowable(width="100%", thickness=0.6, color=HexColor("#dfe4ec"),
                       spaceBefore=1, spaceAfter=4)]


def job_header(role, co, loc, date):
    left = Paragraph(f'<b>{role}</b> · <font color="#2b57c9">{co}</font> — {loc}', S["role"])
    right = Paragraph(date, S["date"])
    t = Table([[left, right]], colWidths=[122*mm, 45*mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(x, S["bullet"]), leftIndent=10, value="•") for x in items],
        bulletType="bullet", start="•", leftIndent=8, bulletFontSize=7,
        bulletColor=ACCENT, spaceBefore=1, spaceAfter=2)


def build(data, out):
    p = data["personal"]
    def link(url, text):
        return f'<a href="{url}" color="#2b57c9">{text}</a>'
    gh = p.get("github", "")
    contact = " &nbsp;·&nbsp; ".join(filter(None, [
        f'{p["ubicacion"]}',
        link("mailto:" + p["email"], p["email"]) if p.get("email") else None,
        p.get("telefono"),
        link(p["linkedin"], "LinkedIn") if p.get("linkedin") else None,
        link(gh, gh.replace("https://", "")) if gh else None,
    ]))
    story = []
    story.append(Paragraph(p["nombre"], S["name"]))
    story.append(Paragraph(p["titular"], S["titular"]))
    story.append(Paragraph(contact, S["contact"]))
    story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=4, spaceAfter=2))

    # Perfil
    story += section("Perfil")
    story.append(Paragraph(data["resumen"], S["body"]))

    # Tecnologías
    story += section("Tecnologías")
    labels = {"lenguajes": "Lenguajes", "frameworks_backend": "Backend & Java",
              "microservicios": "Arquitectura", "ia": "IA / GenAI",
              "bases_de_datos": "Bases de datos", "cloud_devops": "Cloud & DevOps",
              "testing": "Testing", "frontend": "Frontend"}
    sk = data["skills"]
    for key, lab in labels.items():
        if sk.get(key):
            story.append(Paragraph(f'<b>{lab}:</b> ' + " · ".join(sk[key]), S["skill"]))

    # Experiencia
    story += section("Experiencia profesional")
    for e in data["experiencia"]:
        story.append(job_header(e["puesto"], e["empresa"], e["ubicacion"], e["periodo"]))
        story.append(bullets(e["puntos"]))
        if e.get("tecnologias"):
            story.append(Paragraph(" · ".join(e["tecnologias"]), S["stack"]))

    # IA
    ia = data.get("ia")
    if ia:
        story += section(ia.get("titular", "IA generativa"))
        story.append(bullets(ia["puntos"]))

    # Educación + Idiomas + Extra
    story += section("Educación")
    for ed in data["educacion"]:
        story.append(Paragraph(f'<b>{ed["titulo"]}</b> — {ed["periodo"]}', S["skill"]))
        if ed.get("detalle"):
            story.append(Paragraph(ed["detalle"], S["bullet"]))

    story += section("Otros datos relevantes")
    # Destacar el logro estrella en caja
    extra = data.get("extra", [])
    for x in extra:
        story.append(Paragraph("• " + x, S["bullet"]))

    story += section("Idiomas")
    idiomas = " · ".join(f'{i["idioma"]} ({i["nivel"]})' for i in data["idiomas"])
    story.append(Paragraph(idiomas, S["skill"]))

    doc = SimpleDocTemplate(out, pagesize=A4, topMargin=14*mm, bottomMargin=12*mm,
                            leftMargin=16*mm, rightMargin=16*mm,
                            title=f'CV {p["nombre"]}', author=p["nombre"])
    doc.build(story)
    return out


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "cv" / "datos.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    if len(sys.argv) > 2:
        outs = [sys.argv[2]]
    else:
        outs = [str(root / "web" / "cv.pdf"), str(root / "cv" / "CV-Nestor-Rodriguez-Tubio.pdf")]
    for o in outs:
        build(data, o)
        print("PDF generado:", o)

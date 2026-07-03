#!/usr/bin/env python3
"""Genera un CV en PDF minimalista (A4) a partir de cv/datos.json.

Diseño: cabecera + tarjetas de contacto clicables + tarjetas-resumen +
secciones con palabras clave en negrita y poco texto.

Uso:
    python tools/generar_pdf.py                       # -> cv.pdf + cv/CV-Nestor-Rodriguez-Tubio.pdf
    python tools/generar_pdf.py cv/datos.json out.pdf

Requiere: pip install reportlab  (puro Python, sin dependencias del sistema).
"""
import json, sys, re, pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import ParagraphStyle

ACCENT = HexColor("#2b57c9")
INK = HexColor("#1a2333")
MUTED = HexColor("#5c6b82")
SOFT = HexColor("#eef2fb")
CARD = HexColor("#f4f6fa")

PAGE_W, _ = A4
LM = RM = 15 * mm
AVAIL = PAGE_W - LM - RM

S = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=22, textColor=INK, leading=23),
    "titular": ParagraphStyle("titular", fontName="Helvetica-Bold", fontSize=11.5, textColor=ACCENT, leading=14, spaceBefore=1),
    "chip": ParagraphStyle("chip", fontName="Helvetica", fontSize=8.6, textColor=INK, leading=10),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, textColor=ACCENT, leading=12, spaceBefore=6, spaceAfter=2),
    "perfil": ParagraphStyle("perfil", fontName="Helvetica", fontSize=9.6, textColor=INK, leading=12.4),
    "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=10, textColor=INK, leading=12),
    "date": ParagraphStyle("date", fontName="Helvetica", fontSize=8.5, textColor=MUTED, leading=12, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.2, textColor=HexColor("#2c3745"), leading=11.8, leftIndent=9, bulletIndent=0),
    "stack": ParagraphStyle("stack", fontName="Helvetica-Bold", fontSize=8, textColor=ACCENT, leading=10.5, spaceBefore=1),
    "skill": ParagraphStyle("skill", fontName="Helvetica", fontSize=9.2, textColor=INK, leading=12.2),
    "cardbig": ParagraphStyle("cardbig", fontName="Helvetica-Bold", fontSize=10.5, textColor=ACCENT, leading=12, alignment=1),
    "cardsm": ParagraphStyle("cardsm", fontName="Helvetica", fontSize=7.4, textColor=MUTED, leading=8.6, alignment=1),
}

# Palabras clave que se resaltarán en negrita en perfil y experiencia.
KW = ["Spring Boot", "Spring Cloud", "Spring Security", "Spring MVC", "microservicios",
      "IA generativa", "SAP HANA", "SAP BTP", "SAP", "SOAP", "API REST", "OpenAI",
      "Google Gemini", "Gemini", "Claude", "DeepSeek", "Next.js", "Oracle", "MongoDB",
      "RabbitMQ", "Weblogic", "Junta de Andalucía", "Ford", "SERGAS", "VPS", "agentes",
      "prompts", "Java", "LLM", "Kafka", "Docker", "AWS", "Angular"]


def bold_kw(text):
    for kw in sorted(KW, key=len, reverse=True):
        pat = re.compile(r'(?<![\w>])(' + re.escape(kw) + r')(?![\w<])')
        text = pat.sub(r'<b>\1</b>', text)
    return text


def rounded(inner, bg, width=None, pads=(7, 7, 3, 3)):
    t = Table([[inner]], colWidths=[width] if width else None)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("ROUNDEDCORNERS", [5, 5, 5, 5]),
        ("LEFTPADDING", (0, 0), (-1, -1), pads[0]),
        ("RIGHTPADDING", (0, 0), (-1, -1), pads[1]),
        ("TOPPADDING", (0, 0), (-1, -1), pads[2]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pads[3]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def _pack(cells, avail, gap):
    """Coloca celdas (para, width) en filas que quepan en avail."""
    rows, cur, curw = [], [], 0
    for para, w in cells:
        add = w + (gap if cur else 0)
        if cur and curw + add > avail:
            rows.append(cur); cur, curw = [], 0
            add = w
        cur.append((para, w)); curw += add
    if cur:
        rows.append(cur)
    flow = []
    for r in rows:
        c, widths = [], []
        for i, (para, w) in enumerate(r):
            if i:
                c.append(""); widths.append(gap)
            c.append(para); widths.append(w)
        t = Table([c], colWidths=widths)
        t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        flow.append(t)
    return flow


def contact_chips(p):
    def chip(plain, markup, href):
        label = f'<a href="{href}" color="#1a2333">{markup}</a>' if href else markup
        w = stringWidth(plain, "Helvetica", 8.6) + 16
        return (rounded(Paragraph(label, S["chip"]), SOFT, width=w), w)
    items = [chip(f'{p["ubicacion"]}', f'{p["ubicacion"]}', None)]
    if p.get("email"):
        items.append(chip(f'Email  {p["email"]}', f'<b>Email</b>  {p["email"]}', "mailto:" + p["email"]))
    if p.get("telefono"):
        items.append(chip(f'Tel  {p["telefono"]}', f'<b>Tel</b>  {p["telefono"]}', None))
    if p.get("linkedin"):
        items.append(chip('LinkedIn  ver perfil', '<b>LinkedIn</b>  ver perfil', p["linkedin"]))
    gh = p.get("github", "")
    if gh:
        items.append(chip('GitHub  ' + gh.replace("https://", ""), '<b>GitHub</b>  ' + gh.replace("https://", ""), gh))
    return _pack(items, AVAIL, gap=5)


def stat_cards(items):
    n = len(items)
    gap = 6
    cw = (AVAIL - gap * (n - 1)) / n
    cards = []
    for big, small in items:
        inner = [Paragraph(big, S["cardbig"]), Paragraph(small, S["cardsm"])]
        cards.append((rounded(inner, CARD, width=cw, pads=(5, 5, 5, 5)), cw))
    return _pack(cards, AVAIL, gap=gap)


def section(title):
    return [Paragraph(title.upper(), S["h2"]),
            HRFlowable(width="100%", thickness=0.6, color=HexColor("#dbe1ec"), spaceBefore=0, spaceAfter=4)]


def job(e):
    left = Paragraph(f'<b>{e["puesto"]}</b> · <font color="#2b57c9"><b>{e["empresa"]}</b></font> — {e["ubicacion"]}', S["role"])
    right = Paragraph(e["periodo"], S["date"])
    head = Table([[left, right]], colWidths=[AVAIL * 0.72, AVAIL * 0.28])
    head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 3),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    out = [head]
    for pt in e["puntos"][:2]:                     # máximo 2 líneas por trabajo
        out.append(Paragraph("•&nbsp; " + bold_kw(pt), S["bullet"]))
    if e.get("tecnologias"):
        out.append(Paragraph(" · ".join(e["tecnologias"][:8]), S["stack"]))
    return out


def build(data, out):
    p = data["personal"]
    story = [Paragraph(p["nombre"], S["name"]), Paragraph(p["titular"], S["titular"]), Spacer(1, 4)]
    story += contact_chips(p)
    story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=4, spaceAfter=5))

    # Tarjetas-resumen
    story += stat_cards([
        ("6+ años", "Java · Spring Boot · Microservicios"),
        ("IA en producción", "OpenAI · Claude · Gemini · agentes"),
        ("VPS propio", "Despliegue de IA en la nube"),
        ("+5.700 M", "visualizaciones (AR / IA)"),
    ])

    story += section("Perfil")
    story.append(Paragraph(bold_kw(data.get("perfil_corto", data["resumen"])), S["perfil"]))

    story += section("Tecnologías")
    labels = {"frameworks_backend": "Backend & Java", "microservicios": "Arquitectura",
              "ia": "IA / GenAI", "bases_de_datos": "Datos", "cloud_devops": "Cloud & DevOps"}
    sk = data["skills"]
    for key, lab in labels.items():
        if sk.get(key):
            story.append(Paragraph(f'<b>{lab}:</b> ' + " · ".join(sk[key]), S["skill"]))

    story += section("Experiencia")
    for e in data["experiencia"]:
        story += job(e)

    story += section("IA generativa aplicada a producto (desde 2024)")
    for pt in data["ia"]["puntos"][:3]:
        story.append(Paragraph("•&nbsp; " + bold_kw(pt), S["bullet"]))

    story += section("Formación · Idiomas · Extra")
    ed = data["educacion"][0]
    story.append(Paragraph(f'<b>{ed["titulo"]}</b> ({ed["periodo"]})', S["skill"]))
    idiomas = " · ".join(f'{i["idioma"]} ({i["nivel"]})' for i in data["idiomas"])
    story.append(Paragraph(f'<b>Idiomas:</b> {idiomas}', S["skill"]))
    story.append(Paragraph(bold_kw('<b>Extra:</b> Creador de filtros AR (Spark AR) para Instagram con +5.700 M de visualizaciones; certificado React/Redux.'), S["skill"]))

    doc = SimpleDocTemplate(out, pagesize=A4, topMargin=11 * mm, bottomMargin=10 * mm,
                            leftMargin=LM, rightMargin=RM, title=f'CV {p["nombre"]}', author=p["nombre"])
    doc.build(story)
    return out


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "cv" / "datos.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    outs = [sys.argv[2]] if len(sys.argv) > 2 else [str(root / "cv.pdf"), str(root / "cv" / "CV-Nestor-Rodriguez-Tubio.pdf")]
    for o in outs:
        build(data, o)
        print("PDF generado:", o)

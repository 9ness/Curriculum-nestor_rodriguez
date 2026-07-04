#!/usr/bin/env python3
"""Genera el CV en PDF minimalista (A4) + imagen de previsualización (PNG),
a partir de cv/datos.json. Soporta versiones ADAPTADAS a una oferta.

Uso:
    python tools/generar_pdf.py
        -> cv.pdf + cv-preview.png + cv/CV-Nestor-Rodriguez-Tubio.pdf

    python tools/generar_pdf.py --adapt cv/adaptados/cas-training.adapt.json
        -> cv/adaptados/cas-training.pdf + .png (con recuadro de encaje)

Requiere: pip install reportlab pymupdf  (puro Python, sin dependencias del sistema).
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
GREEN = HexColor("#1f9d55")
AMBER = HexColor("#c17d00")
GREY = HexColor("#6b7891")

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
    "pill": ParagraphStyle("pill", fontName="Helvetica-Bold", fontSize=6.8, textColor=HexColor("#ffffff"), leading=8, alignment=1),
    "checkreq": ParagraphStyle("checkreq", fontName="Helvetica", fontSize=8.7, textColor=INK, leading=10.4),
}

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
        ("LEFTPADDING", (0, 0), (-1, -1), pads[0]), ("RIGHTPADDING", (0, 0), (-1, -1), pads[1]),
        ("TOPPADDING", (0, 0), (-1, -1), pads[2]), ("BOTTOMPADDING", (0, 0), (-1, -1), pads[3]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def _pack(cells, avail, gap):
    rows, cur, curw = [], [], 0
    for para, w in cells:
        add = w + (gap if cur else 0)
        if cur and curw + add > avail:
            rows.append(cur); cur, curw = [], 0; add = w
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
    items = [chip(f'{p["ubicacion"]} · Remoto', f'{p["ubicacion"]} · Remoto', None)]
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
    n = len(items); gap = 6
    cw = (AVAIL - gap * (n - 1)) / n
    cards = [(rounded([Paragraph(b, S["cardbig"]), Paragraph(s, S["cardsm"])], CARD, width=cw, pads=(5, 5, 5, 5)), cw)
             for b, s in items]
    return _pack(cards, AVAIL, gap=gap)


def check_cell(c):
    colors = {"cumple": GREEN, "parcial": AMBER, "no": GREY}
    labels = {"cumple": "CUMPLE", "parcial": "PARCIAL", "no": "NO PIDEN"}
    est = c.get("estado", "cumple")
    pill = rounded(Paragraph(labels.get(est, "CUMPLE"), S["pill"]), colors.get(est, GREEN), width=46, pads=(4, 4, 3, 3))
    inner = Table([[pill, Paragraph(c["req"], S["checkreq"])]], colWidths=[46, AVAIL / 2 - 46 - 8])
    inner.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (0, 0), 0),
                               ("LEFTPADDING", (1, 0), (1, 0), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return inner


def check_grid(checks):
    rows = []
    for i in range(0, len(checks), 2):
        pair = checks[i:i + 2]
        rows.append([check_cell(pair[0]), check_cell(pair[1]) if len(pair) > 1 else ""])
    t = Table(rows, colWidths=[AVAIL / 2, AVAIL / 2])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    return [t]


def section(title):
    return [Paragraph(title.upper(), S["h2"]),
            HRFlowable(width="100%", thickness=0.6, color=HexColor("#dbe1ec"), spaceBefore=0, spaceAfter=4)]


def job(e):
    left = Paragraph(f'<b>{e["puesto"]}</b> · <font color="#2b57c9"><b>{e["empresa"]}</b></font> — {e["ubicacion"]}', S["role"])
    head = Table([[left, Paragraph(e["periodo"], S["date"])]], colWidths=[AVAIL * 0.72, AVAIL * 0.28])
    head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 3),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    out = [head]
    for pt in e["puntos"][:2]:
        out.append(Paragraph("•&nbsp; " + bold_kw(pt), S["bullet"]))
    if e.get("tecnologias"):
        out.append(Paragraph(" · ".join(e["tecnologias"][:8]), S["stack"]))
    return out


def build(data, out, adapt=None):
    p = data["personal"]
    titular = adapt["titular"] if adapt and adapt.get("titular") else p["titular"]
    story = [Paragraph(p["nombre"], S["name"]), Paragraph(titular, S["titular"]), Spacer(1, 4)]
    story += contact_chips(p)
    story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=4, spaceAfter=5))

    cards = adapt["cards"] if adapt and adapt.get("cards") else [
        ["6+ años", "Java · Spring Boot · Microservicios"],
        ["IA en producción", "OpenAI · Claude · Gemini · agentes"],
        ["VPS propio", "Despliegue de IA en la nube"],
        ["+5.700 M", "visualizaciones (AR / IA)"],
    ]
    story += stat_cards([tuple(c) for c in cards])

    # Recuadro de encaje (solo versiones adaptadas)
    if adapt and adapt.get("checks"):
        story += section(f'Encaje con la oferta · {adapt.get("puesto","")} @ {adapt.get("empresa","")}')
        story += check_grid(adapt["checks"])

    story += section("Perfil")
    perfil = adapt.get("perfil") if adapt and adapt.get("perfil") else data.get("perfil_corto", data["resumen"])
    story.append(Paragraph(bold_kw(perfil), S["perfil"]))

    story += section("Tecnologías")
    order = adapt.get("skills_order") if adapt and adapt.get("skills_order") else \
        ["frameworks_backend", "microservicios", "ia", "bases_de_datos", "cloud_devops"]
    labels = {"frameworks_backend": "Backend & Java", "microservicios": "Arquitectura",
              "ia": "IA / GenAI", "bases_de_datos": "Datos", "cloud_devops": "Cloud & DevOps"}
    for key in order:
        if data["skills"].get(key):
            story.append(Paragraph(f'<b>{labels[key]}:</b> ' + " · ".join(data["skills"][key]), S["skill"]))

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


def render_preview(pdf_path, png_path, zoom=2.0):
    try:
        import fitz
    except Exception:
        print("  (aviso: pymupdf no disponible, sin imagen de preview)")
        return None
    doc = fitz.open(pdf_path)
    doc[0].get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(png_path)
    doc.close()
    return png_path


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent
    data = json.loads((root / "cv" / "datos.json").read_text(encoding="utf-8"))

    if len(sys.argv) > 2 and sys.argv[1] == "--adapt":
        adapt_path = pathlib.Path(sys.argv[2])
        adapt = json.loads(adapt_path.read_text(encoding="utf-8"))
        base = adapt_path.name.replace(".adapt.json", "")
        pdf = str(adapt_path.parent / f"{base}.pdf")
        build(data, pdf, adapt=adapt)
        render_preview(pdf, str(adapt_path.parent / f"{base}.png"))
        print("PDF adaptado generado:", pdf)
    else:
        for o in [str(root / "cv.pdf"), str(root / "cv" / "CV-Nestor-Rodriguez-Tubio.pdf")]:
            build(data, o)
        render_preview(str(root / "cv.pdf"), str(root / "cv-preview.png"))
        print("PDF base + preview generados: cv.pdf, cv-preview.png")

#!/usr/bin/env python3
"""
Visitenkarten-Generator – Werner Paternoster / 24h Mietwerkstatt.

Erzeugt eine druckfertige, voll vektorbasierte Visitenkarte (Vorder- und
Rueckseite) im Endformat 85 x 55 mm inkl. 3 mm Beschnitt rundum.

Ausgabe:
  druck/vorderseite.svg / .pdf / .png
  druck/rueckseite.svg  / .pdf / .png

Alle Texte, Icons und der QR-Code sind Vektor -> gestochen scharf fuer den Druck.
"""

import math
import os

import qrcode
import qrcode.constants
import cairosvg

# --------------------------------------------------------------------------- #
#  Konfiguration
# --------------------------------------------------------------------------- #
OUT_DIR = "druck"

# Endformat (Trim) und Beschnitt (Bleed)
TRIM_W, TRIM_H = 85.0, 55.0          # mm
BLEED = 3.0                          # mm rundum
SAFE = 4.0                           # mm Sicherheitsabstand innerhalb Trim

PAGE_W = TRIM_W + 2 * BLEED          # 91 mm
PAGE_H = TRIM_H + 2 * BLEED          # 61 mm

# Farben
NAVY = "#0d2b45"                     # Hintergrund dunkelblau
NAVY_BG2 = "#0b2438"                 # leichter Verlauf unten
WATERMARK = "#163a5c"               # dezentes Wasserzeichen
WHITE = "#ffffff"
SOFT = "#d7e0ea"                     # gedaempftes Weiss fuer Fliesstext
BLACK = "#000000"                    # QR – gestochen schwarz

FONT = "Liberation Sans, Arial, DejaVu Sans, sans-serif"

# Kontaktdaten
NAME = "Werner Paternoster"
ADDRESS = "Schwadorf 18, 3100 St. Pölten"
UID = "UID: ATU62142005"
PHONE = "+43 664 5171370"
EMAIL = "Office@w-paternoster.at"

BULLETS = [
    "Hebebühnen bis 5,5t",
    "Werkzeugwagen inklusive",
    "24/7 Zugang nach Einweisung",
    "Trockeneis- & Klimaservice",
    "Reifenhandel",
]

# Inhalt des QR-Codes – vCard, damit Scannen direkt den Kontakt speichert.
QR_CONTENT = (
    "BEGIN:VCARD\r\n"
    "VERSION:3.0\r\n"
    "N:Paternoster;Werner;;;\r\n"
    "FN:Werner Paternoster\r\n"
    "ORG:24h Mietwerkstatt\r\n"
    "ADR;TYPE=WORK:;;Schwadorf 18;St. Pölten;;3100;Österreich\r\n"
    "TEL;TYPE=CELL:+436645171370\r\n"
    "EMAIL;TYPE=WORK:Office@w-paternoster.at\r\n"
    "END:VCARD\r\n"
)

# --------------------------------------------------------------------------- #
#  Icon-Pfade (simple-icons / bootstrap-icons, monochrom)
# --------------------------------------------------------------------------- #
ICON_WHATSAPP = ("M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z")

ICON_TELEGRAM = ("M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z")

ICON_SIGNAL = ("M12 0q-.934 0-1.83.139l.17 1.111a11 11 0 0 1 3.32 0l.172-1.111A12 12 0 0 0 12 0M9.152.34A12 12 0 0 0 5.77 1.742l.584.961a10.8 10.8 0 0 1 3.066-1.27zm5.696 0-.268 1.094a10.8 10.8 0 0 1 3.066 1.27l.584-.962A12 12 0 0 0 14.848.34M12 2.25a9.75 9.75 0 0 0-8.539 14.459c.074.134.1.292.064.441l-1.013 4.338 4.338-1.013a.62.62 0 0 1 .441.064A9.7 9.7 0 0 0 12 21.75c5.385 0 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25m-7.092.068a12 12 0 0 0-2.59 2.59l.909.664a11 11 0 0 1 2.345-2.345zm14.184 0-.664.909a11 11 0 0 1 2.345 2.345l.909-.664a12 12 0 0 0-2.59-2.59M1.742 5.77A12 12 0 0 0 .34 9.152l1.094.268a10.8 10.8 0 0 1 1.269-3.066zm20.516 0-.961.584a10.8 10.8 0 0 1 1.27 3.066l1.093-.268a12 12 0 0 0-1.402-3.383M.138 10.168A12 12 0 0 0 0 12q0 .934.139 1.83l1.111-.17A11 11 0 0 1 1.125 12q0-.848.125-1.66zm23.723.002-1.111.17q.125.812.125 1.66c0 .848-.042 1.12-.125 1.66l1.111.172a12.1 12.1 0 0 0 0-3.662M1.434 14.58l-1.094.268a12 12 0 0 0 .96 2.591l-.265 1.14 1.096.255.36-1.539-.188-.365a10.8 10.8 0 0 1-.87-2.35m21.133 0a10.8 10.8 0 0 1-1.27 3.067l.962.584a12 12 0 0 0 1.402-3.383zm-1.793 3.848a11 11 0 0 1-2.345 2.345l.664.909a12 12 0 0 0 2.59-2.59zm-19.959 1.1L.357 21.48a1.8 1.8 0 0 0 2.162 2.161l1.954-.455-.256-1.095-1.953.455a.675.675 0 0 1-.81-.81l.454-1.954zm16.832 1.769a10.8 10.8 0 0 1-3.066 1.27l.268 1.093a12 12 0 0 0 3.382-1.402zm-10.94.213-1.54.36.256 1.095 1.139-.266c.814.415 1.683.74 2.591.961l.268-1.094a10.8 10.8 0 0 1-2.35-.869zm3.634 1.24-.172 1.111a12.1 12.1 0 0 0 3.662 0l-.17-1.111q-.812.125-1.66.125a11 11 0 0 1-1.66-.125")

# bootstrap hand-thumbs-up-fill (viewBox 16)
ICON_THUMB = ("M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a10 10 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733q.086.18.138.363c.077.27.113.567.113.856s-.036.586-.113.856c-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.2 3.2 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.8 4.8 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z")

# tabler tool/wrench (viewBox 24, stroke)
ICON_WRENCH = "M7 10h3v-3l-3.5 -3.5a6 6 0 0 1 8 8l6 6a2 2 0 0 1 -3 3l-6 -6a6 6 0 0 1 -8 -8l3.5 3.5"


# --------------------------------------------------------------------------- #
#  Hilfsfunktionen
# --------------------------------------------------------------------------- #
def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def icon(path_d: str, x, y, size, color=WHITE, vb=24, stroke=False, sw=2.0):
    """Brand-/Glyph-Icon an Position (x,y) mit Kantenlaenge `size` (mm)."""
    sc = size / vb
    if stroke:
        style = (f'fill="none" stroke="{color}" stroke-width="{sw}" '
                 f'stroke-linecap="round" stroke-linejoin="round"')
    else:
        style = f'fill="{color}"'
    return (f'<g transform="translate({x:.3f},{y:.3f}) scale({sc:.5f})">'
            f'<path d="{path_d}" {style}/></g>')


def approx_text_width(text, size):
    """Grobe Textbreite (Liberation Sans) zur Zentrierung von Mischzeilen."""
    return len(text) * size * 0.53


def arc_text(cx, cy, radius, text, mid_deg, span_deg, size, color,
             bottom=False, weight="bold", spacing=1.0):
    """Setzt Grossbuchstaben gleichmaessig entlang eines Kreisbogens."""
    n = len(text)
    out = []
    # Buchstaben von links nach rechts (unten: Laufrichtung umkehren)
    direction = -1 if bottom else 1
    for i, ch in enumerate(text):
        if n > 1:
            t = (i - (n - 1) / 2) / (n - 1)
        else:
            t = 0.0
        ang = mid_deg + direction * t * span_deg
        rad = math.radians(ang)
        x = cx + radius * math.cos(rad)
        y = cy + radius * math.sin(rad)
        if bottom:
            rot = ang - 90
        else:
            rot = ang + 90
        out.append(
            f'<text x="{x:.3f}" y="{y:.3f}" transform="rotate({rot:.3f} {x:.3f} {y:.3f})" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{spacing}" fill="{color}" text-anchor="middle" '
            f'dominant-baseline="central">{esc(ch)}</text>'
        )
    return "".join(out)


def qr_path(content, x, y, size, quiet=4):
    """Erzeugt den QR-Code als einen schwarzen Vektorpfad innerhalb size x size."""
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,
                       border=0, box_size=10)
    qr.add_data(content)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    total = n + 2 * quiet
    mod = size / total
    d = []
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                px = x + (c + quiet) * mod
                py = y + (r + quiet) * mod
                d.append(f"M{px:.3f} {py:.3f}h{mod:.3f}v{mod:.3f}h{-mod:.3f}z")
    return f'<path d="{"".join(d)}" fill="{BLACK}" shape-rendering="crispEdges"/>', n


# --------------------------------------------------------------------------- #
#  Gemeinsame Bausteine
# --------------------------------------------------------------------------- #
def svg_header():
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{PAGE_W}mm" height="{PAGE_H}mm" '
        f'viewBox="0 0 {PAGE_W} {PAGE_H}">\n'
    )


def background_and_watermark():
    """Dunkelblauer Hintergrund (ueber den Beschnitt) + dezentes Wasserzeichen."""
    out = []
    out.append('<defs>'
               f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0" stop-color="{NAVY}"/>'
               f'<stop offset="1" stop-color="{NAVY_BG2}"/>'
               f'</linearGradient></defs>')
    out.append(f'<rect x="0" y="0" width="{PAGE_W}" height="{PAGE_H}" fill="url(#bg)"/>')

    # Wasserzeichen: gekreuzte Schraubenschluessel, dezent
    cx, cy = PAGE_W * 0.72, PAGE_H * 0.5
    out.append(f'<g opacity="0.5" stroke="none">')
    for rot in (35, -35):
        sc = 1.5
        out.append(
            f'<g transform="translate({cx},{cy}) rotate({rot}) scale({sc}) translate(-12,-12)">'
            + icon(ICON_WRENCH, 0, 0, 24, color=WATERMARK, stroke=True, sw=1.6)
            + '</g>'
        )
    out.append('</g>')
    return "".join(out)


# --------------------------------------------------------------------------- #
#  Vorderseite
# --------------------------------------------------------------------------- #
def build_front():
    s = [svg_header(), background_and_watermark()]

    # ---- Logo-Badge oben links --------------------------------------------
    bx, by, br = BLEED + 12.5, BLEED + 11.5, 10.0
    s.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="none" stroke="{WHITE}" stroke-width="0.5"/>')
    s.append(f'<circle cx="{bx}" cy="{by}" r="{br-1.4}" fill="none" stroke="{WHITE}" stroke-width="0.25"/>')
    # Daumen-hoch zentriert
    th = 9.0
    s.append(icon(ICON_THUMB, bx - th/2, by - th/2 - 0.4, th, color=WHITE, vb=16))
    # Bogentext
    s.append(arc_text(bx, by, br - 2.6, "MACH'S DIR SELBST", mid_deg=-90,
                      span_deg=130, size=1.65, color=WHITE, bottom=False))
    s.append(arc_text(bx, by, br - 2.6, "MIETWERKSTATT", mid_deg=90,
                      span_deg=95, size=1.65, color=WHITE, bottom=True))

    # ---- Name + Adresse ----------------------------------------------------
    tx = bx + br + 4.5
    s.append(f'<text x="{tx}" y="{BLEED+9.5}" font-family="{FONT}" font-size="6.4" '
             f'font-weight="bold" fill="{WHITE}">{esc(NAME)}</text>')
    s.append(f'<text x="{tx}" y="{BLEED+14.6}" font-family="{FONT}" font-size="3.1" '
             f'fill="{SOFT}">{esc(ADDRESS)}</text>')
    s.append(f'<text x="{tx}" y="{BLEED+18.6}" font-family="{FONT}" font-size="3.1" '
             f'fill="{SOFT}">{esc(UID)}</text>')

    # Trennlinie
    s.append(f'<line x1="{BLEED+SAFE}" y1="{BLEED+25}" x2="{PAGE_W-BLEED-SAFE}" y2="{BLEED+25}" '
             f'stroke="{WHITE}" stroke-width="0.25" opacity="0.35"/>')

    # ---- Leistungen (Bullets) ---------------------------------------------
    lx = BLEED + SAFE
    ly = BLEED + 31.5
    step = 5.0
    for i, b in enumerate(BULLETS):
        y = ly + i * step
        s.append(f'<circle cx="{lx+0.9}" cy="{y-1.1}" r="0.85" fill="{WHITE}"/>')
        s.append(f'<text x="{lx+3.2}" y="{y}" font-family="{FONT}" font-size="3.25" '
                 f'fill="{WHITE}">{esc(b)}</text>')

    # ---- QR-Code unten rechts ---------------------------------------------
    panel = 24.0
    px = PAGE_W - BLEED - SAFE - panel
    py = PAGE_H - BLEED - SAFE - panel
    s.append(f'<rect x="{px}" y="{py}" width="{panel}" height="{panel}" rx="1.8" fill="{WHITE}"/>')
    qr_svg, _ = qr_path(QR_CONTENT, px, py, panel, quiet=3)
    s.append(qr_svg)

    # ---- Schnittmarken / Beschnitt-Hinweis (nur Hilfslinien, nicht drucken)
    s.append(trim_guides())

    s.append('</svg>')
    return "".join(s)


# --------------------------------------------------------------------------- #
#  Rueckseite
# --------------------------------------------------------------------------- #
def build_back():
    s = [svg_header(), background_and_watermark()]
    cx = PAGE_W / 2

    def ctext(y, size, parts, fill=WHITE):
        # parts: list of (text, weight). Einzelnes text-Element mit tspans,
        # linksbuendig ab berechnetem Startpunkt -> natuerliche Wortabstaende
        # bei korrekter Zentrierung (umgeht cairosvg-Anchor-Bug bei tspans).
        total = sum(approx_text_width(t, size) * (1.05 if w == "bold" else 1.0)
                    for t, w in parts)
        x = cx - total / 2
        spans = "".join(
            f'<tspan font-weight="{w}">{esc(t)}</tspan>' for t, w in parts
        )
        return (f'<text x="{x:.3f}" y="{y}" font-family="{FONT}" font-size="{size}" '
                f'fill="{fill}" text-anchor="start">{spans}</text>')

    s.append(ctext(BLEED + 9.5, 3.35, [("Anfragen ausschließlich per WhatsApp", "normal")]))
    s.append(ctext(BLEED + 14.3, 3.35, [("oder Telegram / Signal.", "normal")]))
    s.append(ctext(BLEED + 20.6, 3.35, [
        ("Anrufe werden ", "normal"), ("NICHT", "bold"), (" entgegengenommen.", "normal")]))

    # ---- Kontaktzeile: WhatsApp | Nummer | Telegram | Signal --------------
    row_y = BLEED + 30.5
    isz = 5.6                      # Icon-Kantenlaenge
    gap = 2.6
    num_size = 4.0
    num_w = approx_text_width(PHONE, num_size)
    # Reihenfolge + Breiten
    total = isz + gap + num_w + gap + isz + gap + isz
    start = cx - total / 2
    iy = row_y - isz / 2          # Icons vertikal an Textmitte ausrichten

    x = start
    s.append(icon(ICON_WHATSAPP, x, iy, isz, color=WHITE))
    x += isz + gap
    s.append(f'<text x="{x + num_w/2}" y="{row_y + num_size*0.36}" font-family="{FONT}" '
             f'font-size="{num_size}" font-weight="bold" fill="{WHITE}" '
             f'text-anchor="middle">{esc(PHONE)}</text>')
    x += num_w + gap
    s.append(icon(ICON_TELEGRAM, x, iy, isz, color=WHITE))
    x += isz + gap
    s.append(icon(ICON_SIGNAL, x, iy, isz, color=WHITE))

    # ---- E-Mail ------------------------------------------------------------
    s.append(ctext(BLEED + 39.5, 3.35, [(EMAIL, "normal")], fill=SOFT))

    # ---- Hinweis unten -----------------------------------------------------
    s.append(f'<line x1="{cx-22}" y1="{BLEED+44.5}" x2="{cx+22}" y2="{BLEED+44.5}" '
             f'stroke="{WHITE}" stroke-width="0.25" opacity="0.3"/>')
    s.append(ctext(BLEED + 49.5, 3.0, [
        ("24/7 Zugang nach Registrierung und Einweisung.", "normal")], fill=SOFT))

    s.append(trim_guides())
    s.append('</svg>')
    return "".join(s)


# --------------------------------------------------------------------------- #
#  Schnitt-/Beschnitt-Hilfslinien (eigene Ebene, leicht entfernbar)
# --------------------------------------------------------------------------- #
def trim_guides():
    o = ['<g id="trim-guides" opacity="0.0">']  # unsichtbar im Druck-PDF
    o.append(f'<rect x="{BLEED}" y="{BLEED}" width="{TRIM_W}" height="{TRIM_H}" '
             f'fill="none" stroke="#ff00ff" stroke-width="0.1"/>')
    o.append('</g>')
    return "".join(o)


# --------------------------------------------------------------------------- #
#  Export
# --------------------------------------------------------------------------- #
def export(name, svg):
    os.makedirs(OUT_DIR, exist_ok=True)
    svg_path = os.path.join(OUT_DIR, f"{name}.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    cairosvg.svg2pdf(bytestring=svg.encode("utf-8"),
                     write_to=os.path.join(OUT_DIR, f"{name}.pdf"))
    cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                     write_to=os.path.join(OUT_DIR, f"{name}.png"),
                     dpi=600, output_width=int(PAGE_W / 25.4 * 600))
    print(f"  -> {name}: svg, pdf, png")


def main():
    print("Erzeuge Visitenkarte (85 x 55 mm + 3 mm Beschnitt) ...")
    export("vorderseite", build_front())
    export("rueckseite", build_back())
    print("Fertig. Dateien im Ordner:", OUT_DIR)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Flyer-Generator – Werner Paternoster / 24h Mietwerkstatt.

Erzeugt einen druckfertigen, voll vektorbasierten A5-Flyer (Vorder- und
Rueckseite) im gleichen Design wie die Visitenkarte.

Endformat A5: 148 x 210 mm + 3 mm Beschnitt rundum -> 154 x 216 mm.

Ausgabe:
  druck/flyer_vorderseite.svg / .pdf / .png
  druck/flyer_rueckseite.svg  / .pdf / .png
"""

import os

import cairosvg

import generate_card as gc
from generate_card import (
    NAVY, NAVY_BG2, WATERMARK, WHITE, SOFT, BLACK, FONT,
    NAME, ADDRESS, UID, PHONE, EMAIL,
    ICON_WHATSAPP, ICON_TELEGRAM, ICON_SIGNAL, ICON_THUMB, ICON_WRENCH,
    esc, icon, arc_text, qr_path, text_width,
)

# --------------------------------------------------------------------------- #
#  Format
# --------------------------------------------------------------------------- #
OUT_DIR = "druck"
TRIM_W, TRIM_H = 148.0, 210.0       # A5 hoch
BLEED = 3.0
SAFE = 8.0
PAGE_W = TRIM_W + 2 * BLEED          # 154
PAGE_H = TRIM_H + 2 * BLEED          # 216
CX = PAGE_W / 2

PANEL = "#12324f"                    # leicht hellere Box auf Navy
ACCENT = "#7fb2e0"                   # dezenter blauer Akzent

WEBSITE = "https://www.24-stunden-mietwerkstatt.at"
WEBSITE_LABEL = "www.24-stunden-mietwerkstatt.at"

ICON_CHECK = "M5 12.5l4.2 4.2L19 7"  # Haken (stroke, viewBox 24)

TAGLINE = "Mach's dir selbst – deine Werkstatt zur Selbstmiete"

# Leistungen (von der Website), zweispaltig
SERVICES_LEFT = [
    "4 Hebebühnen bis 5,5t",
    "Werkzeugwagen inklusive",
    "24/7 Zugang für Kunden",
    "Klimaservice & Gas",
    "Trockeneis-Reinigung",
    "Reifenservice & -handel",
]
SERVICES_RIGHT = [
    "Unterbodenschutz",
    "Bremsenentlüftung",
    "Diagnosegerät",
    "Werkstattpresse",
    "Spezialwerkzeug",
    "PKW-Aufbereitung",
]


# --------------------------------------------------------------------------- #
#  Bausteine
# --------------------------------------------------------------------------- #
def header():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{PAGE_W}mm" height="{PAGE_H}mm" '
            f'viewBox="0 0 {PAGE_W} {PAGE_H}">\n')


def background():
    out = ['<defs>'
           f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{NAVY}"/>'
           f'<stop offset="1" stop-color="{NAVY_BG2}"/></linearGradient></defs>',
           f'<rect x="0" y="0" width="{PAGE_W}" height="{PAGE_H}" fill="url(#bg)"/>']
    # Wasserzeichen: gekreuzte Schraubenschluessel oben und unten, dezent
    for (wx, wy, sc, op) in ((PAGE_W*0.80, PAGE_H*0.18, 3.2, 0.45),
                             (PAGE_W*0.20, PAGE_H*0.82, 3.6, 0.45)):
        out.append(f'<g opacity="{op}">')
        for rot in (35, -35):
            out.append(
                f'<g transform="translate({wx},{wy}) rotate({rot}) scale({sc}) translate(-12,-12)">'
                + icon(ICON_WRENCH, 0, 0, 24, color=WATERMARK, stroke=True, sw=1.4)
                + '</g>')
        out.append('</g>')
    return "".join(out)


def badge(cx, cy, r):
    s = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{WHITE}" stroke-width="0.9"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r-2.4}" fill="none" stroke="{WHITE}" stroke-width="0.45"/>']
    th = r * 0.92
    s.append(icon(ICON_THUMB, cx - th/2, cy - th/2 - r*0.04, th, color=WHITE, vb=16))
    s.append(arc_text(cx, cy, r - 4.4, "MACH'S DIR SELBST", mid_deg=-90,
                      span_deg=132, size=r*0.155, color=WHITE, bottom=False))
    s.append(arc_text(cx, cy, r - 4.4, "MIETWERKSTATT", mid_deg=90,
                      span_deg=98, size=r*0.155, color=WHITE, bottom=True))
    return "".join(s)


def ctext(y, size, parts, fill=WHITE, cx=CX, letter=None):
    """Zentrierte Zeile mit optional gemischten Schriftschnitten (tspans).
    Breite exakt aus der Schrift gemessen -> sauber mittig."""
    if isinstance(parts, str):
        parts = [(parts, "normal")]
    total = sum(text_width(t, size, w) for t, w in parts)
    nchars = sum(len(t) for t, _ in parts)
    if letter and nchars > 1:
        total += letter * (nchars - 1)
    x = cx - total / 2
    ls = f' letter-spacing="{letter}"' if letter else ""
    spans = "".join(f'<tspan font-weight="{w}">{esc(t)}</tspan>' for t, w in parts)
    return (f'<text x="{x:.3f}" y="{y}" font-family="{FONT}" font-size="{size}"{ls} '
            f'fill="{fill}" text-anchor="start">{spans}</text>')


def divider(y, half=52, cx=CX, op=0.35):
    return (f'<line x1="{cx-half}" y1="{y}" x2="{cx+half}" y2="{y}" '
            f'stroke="{WHITE}" stroke-width="0.4" opacity="{op}"/>')


def contact_row(cx, y, isz=8.0, num_size=6.0, gap=3.4, color=WHITE):
    """WhatsApp | Nummer | Telegram | Signal – zentriert."""
    num_w = text_width(PHONE, num_size, "bold")
    total = isz + gap + num_w + gap + isz + gap + isz
    x = cx - total / 2
    iy = y - isz / 2
    out = [icon(ICON_WHATSAPP, x, iy, isz, color=color)]
    x += isz + gap
    out.append(f'<text x="{x + num_w/2:.3f}" y="{y + num_size*0.36:.3f}" '
               f'font-family="{FONT}" font-size="{num_size}" font-weight="bold" '
               f'fill="{color}" text-anchor="middle">{esc(PHONE)}</text>')
    x += num_w + gap
    out.append(icon(ICON_TELEGRAM, x, iy, isz, color=color))
    x += isz + gap
    out.append(icon(ICON_SIGNAL, x, iy, isz, color=color))
    return "".join(out)


def url_pill(cx, cy, size=6.0):
    """Website-URL als hervorgehobene Pille, vertikal um cy zentriert."""
    w = text_width(WEBSITE_LABEL, size, "bold") + 16
    h = size + 7
    return (f'<rect x="{cx-w/2:.3f}" y="{cy-h/2:.3f}" rx="{h/2}" '
            f'width="{w:.3f}" height="{h:.3f}" fill="{WHITE}"/>'
            f'<text x="{cx}" y="{cy + size*0.36:.3f}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="bold" '
            f'fill="{NAVY}" text-anchor="middle">{esc(WEBSITE_LABEL)}</text>')


# --------------------------------------------------------------------------- #
#  Vorderseite
# --------------------------------------------------------------------------- #
def build_front():
    s = [header(), background()]

    px = BLEED + SAFE                 # linker Inhaltsrand (11)
    pr = PAGE_W - BLEED - SAFE        # rechter Inhaltsrand (143)
    pw = pr - px                      # Inhaltsbreite (132)

    # Hero
    s.append(badge(CX, 28, 15))
    s.append(ctext(49, 10.0, [("24h ", "normal"), ("MIETWERKSTATT", "bold")], letter=0.2))
    s.append(ctext(57, 4.8, f"{NAME} · 3100 St. Pölten", fill=SOFT))
    s.append(ctext(64, 4.2, TAGLINE, fill=ACCENT))
    s.append(divider(70, half=56))

    # Leistungen – zwei Spalten
    s.append(ctext(79, 6.4, [("Unsere Leistungen", "bold")]))
    col_x = (px + 1, CX + 4)          # Icon-Position je Spalte
    fsz = 4.6
    y0 = 90
    step = 9.6
    for col, items in zip(col_x, (SERVICES_LEFT, SERVICES_RIGHT)):
        for i, b in enumerate(items):
            y = y0 + i * step
            s.append(icon(ICON_CHECK, col, y - 5.2, 6.6, color=ACCENT, stroke=True, sw=2.8))
            s.append(f'<text x="{col+8.6}" y="{y}" font-family="{FONT}" font-size="{fsz}" '
                     f'fill="{WHITE}">{esc(b)}</text>')

    # Hinweis
    s.append(divider(151, half=56))
    s.append(ctext(157, 3.5,
                   "Anfragen ausschließlich per WhatsApp, Telegram oder Signal.", fill=SOFT))
    s.append(ctext(162, 3.5,
                   [("Anrufe werden ", "normal"), ("NICHT", "bold"),
                    (" entgegengenommen.", "normal")], fill=SOFT))

    # Footer-Panel: QR + Kontakt (oben) und URL-Pille (unten, ganze Breite)
    py = 166
    ph = 41
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="3" '
             f'fill="{PANEL}" stroke="{WHITE}" stroke-opacity="0.15" stroke-width="0.4"/>')

    # QR links (zeigt auf die Website)
    qp = 26.0
    qx = px + 4
    qy = py + 4
    s.append(f'<rect x="{qx}" y="{qy}" width="{qp}" height="{qp}" rx="1.6" fill="{WHITE}"/>')
    qr_svg, _ = qr_path(WEBSITE, qx, qy, qp, quiet=3)
    s.append(qr_svg)

    # Rechts neben QR: Kontaktblock (mittig in der Restbreite)
    rcx = (qx + qp + px + pw - 4) / 2 + 1
    s.append(ctext(py + 8.5, 3.4, "Termine & Infos – einfach scannen", fill=SOFT, cx=rcx))
    s.append(contact_row(rcx, py + 17.5, isz=5.6, num_size=4.8, gap=2.2))
    s.append(ctext(py + 25.5, 3.9, EMAIL, fill=SOFT, cx=rcx))

    # URL-Pille unten, auf der ganzen Karte zentriert
    s.append(url_pill(CX, py + ph - 5.5, size=5.4))

    s.append('</svg>')
    return "".join(s)


# --------------------------------------------------------------------------- #
#  Rueckseite
# --------------------------------------------------------------------------- #
def build_back():
    s = [header(), background()]

    s.append(badge(CX, 28, 15))
    s.append(ctext(54, 10.0, [("So einfach geht's", "bold")]))
    s.append(divider(62, half=56))

    steps = [
        ("1", "Ersttermin vereinbaren", "Per WhatsApp, Telegram oder Signal anfragen."),
        ("2", "Registrierung & Einweisung", "Vor Ort registrieren + Einweisung erhalten."),
        ("3", "Freischaltung", "Nach ein paar Terminen für 24/7 freigeschaltet."),
        ("4", "24/7 selbst schrauben", "Online buchen – Werkzeug inklusive."),
    ]
    sy = 76
    step_h = 22
    lx = BLEED + 18
    for i, (num, title, desc) in enumerate(steps):
        y = sy + i * step_h
        s.append(f'<circle cx="{lx+5}" cy="{y}" r="6.5" fill="{PANEL}" '
                 f'stroke="{ACCENT}" stroke-width="0.8"/>')
        s.append(f'<text x="{lx+5}" y="{y+2.3}" font-family="{FONT}" font-size="7.5" '
                 f'font-weight="bold" fill="{WHITE}" text-anchor="middle">{num}</text>')
        s.append(f'<text x="{lx+18}" y="{y-1.2}" font-family="{FONT}" font-size="6.0" '
                 f'font-weight="bold" fill="{WHITE}">{esc(title)}</text>')
        s.append(f'<text x="{lx+18}" y="{y+5.4}" font-family="{FONT}" font-size="4.0" '
                 f'fill="{SOFT}">{esc(desc)}</text>')

    # Standort
    s.append(divider(164, half=56))
    s.append(ctext(173, 5.4, [("Standort", "bold")]))
    s.append(ctext(181, 4.6, ADDRESS, fill=SOFT))
    s.append(ctext(187, 3.8, UID, fill=SOFT))

    # Footer: URL prominent
    s.append(url_pill(CX, 196, size=6.0))
    s.append(ctext(209, 3.6,
                   [("24/7 Zugang nach Freischaltung – schrauben wann du willst.", "normal")],
                   fill=SOFT))

    s.append('</svg>')
    return "".join(s)


# --------------------------------------------------------------------------- #
#  Export
# --------------------------------------------------------------------------- #
def export(name, svg):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, f"{name}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    cairosvg.svg2pdf(bytestring=svg.encode("utf-8"),
                     write_to=os.path.join(OUT_DIR, f"{name}.pdf"))
    cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                     write_to=os.path.join(OUT_DIR, f"{name}.png"),
                     dpi=300, output_width=int(PAGE_W / 25.4 * 300))
    print(f"  -> {name}: svg, pdf, png")


def main():
    print("Erzeuge A5-Flyer (148 x 210 mm + 3 mm Beschnitt) ...")
    export("flyer_vorderseite", build_front())
    export("flyer_rueckseite", build_back())
    print("Fertig. Dateien im Ordner:", OUT_DIR)


if __name__ == "__main__":
    main()

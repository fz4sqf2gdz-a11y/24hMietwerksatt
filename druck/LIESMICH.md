# Druckdaten – Werner Paternoster / 24h Mietwerkstatt

Druckfertige **Visitenkarte** und **A5-Flyer** (jeweils Vorder- und Rückseite),
vollständig vektorbasiert – gestochen scharf für die Druckerei.

## Dateien

### Visitenkarte (85 × 55 mm)

| Datei | Zweck |
|-------|-------|
| `vorderseite.pdf` / `rueckseite.pdf` | **Druckdaten** – an die Druckerei geben (Vektor, eingebettete Schriften) |
| `vorderseite.svg` / `rueckseite.svg` | Bearbeitbare Vektorquelle (z. B. in Inkscape/Illustrator) |
| `vorderseite.png` / `rueckseite.png` | Vorschau (600 dpi) |

### Flyer (A5, 148 × 210 mm)

| Datei | Zweck |
|-------|-------|
| `flyer_vorderseite.pdf` / `flyer_rueckseite.pdf` | **Druckdaten** für die Druckerei |
| `flyer_vorderseite.svg` / `flyer_rueckseite.svg` | Bearbeitbare Vektorquelle |
| `flyer_vorderseite.png` / `flyer_rueckseite.png` | Vorschau (300 dpi) |

## Druckspezifikation

- **Visitenkarte:** Endformat 85 × 55 mm + 3 mm Beschnitt → Datenformat **91 × 61 mm**
- **Flyer:** Endformat A5 148 × 210 mm + 3 mm Beschnitt → Datenformat **154 × 216 mm**
- **Sicherheitsabstand:** wichtiger Inhalt bleibt innerhalb des Trims
- **Farben:** Hintergrund Dunkelblau, Texte/Icons Weiß, QR-Code **rein schwarz (#000000)**
- **Schrift:** Liberation Sans (Arial-kompatibel), im PDF eingebettet/als Pfade
- Alles ist Vektor → beliebig skalierbar ohne Qualitätsverlust

> Tipp für die Druckerei: Für satte Tiefe das Dunkelblau als Rich-Black/CMYK
> anlegen. Bei Bedarf liefern wir gern eine CMYK-konvertierte PDF.

## QR-Codes

- **Visitenkarte:** QR als **vCard** – beim Scannen wird direkt der Kontakt
  (Name, Firma, Adresse, Telefon, E-Mail) gespeichert.
- **Flyer:** QR verweist auf die **Website** `https://www.24-stunden-mietwerkstatt.at`.

Beide QR-Codes sind als Vektor erzeugt (gestochen scharf) und wurden getestet
und erfolgreich dekodiert.

## Icons

- Aufgeräumt/angepasst: **WhatsApp, Telegram, Signal**
- Das frühere **SMS-Icon wurde entfernt**
- Hinweis „Anrufe werden **NICHT** entgegengenommen.“

## Neu erzeugen / Inhalte ändern

Alle Texte, Kontaktdaten und QR-Inhalte stehen oben in den Generatoren
`../generate_card.py` (Visitenkarte) und `../generate_flyer.py` (Flyer).
Nach Änderungen einfach neu erzeugen:

```bash
pip install "qrcode[pil]" cairosvg
python generate_card.py
python generate_flyer.py
```

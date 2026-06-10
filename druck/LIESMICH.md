# Visitenkarte – Werner Paternoster / 24h Mietwerkstatt

Druckfertige Visitenkarte (Vorder- und Rückseite), vollständig vektorbasiert –
gestochen scharf für die Druckerei.

## Dateien

| Datei | Zweck |
|-------|-------|
| `vorderseite.pdf` / `rueckseite.pdf` | **Druckdaten** – an die Druckerei geben (Vektor, eingebettete Schriften) |
| `vorderseite.svg` / `rueckseite.svg` | Bearbeitbare Vektorquelle (z. B. in Inkscape/Illustrator) |
| `vorderseite.png` / `rueckseite.png` | Vorschau (600 dpi) |

## Druckspezifikation

- **Endformat (Trim):** 85 × 55 mm
- **Beschnitt (Bleed):** 3 mm rundum → Datenformat **91 × 61 mm**
- **Sicherheitsabstand:** ca. 4 mm zum Rand (wichtiger Inhalt bleibt innen)
- **Farben:** Hintergrund Dunkelblau, Texte/Icons Weiß, QR-Code **rein schwarz (#000000)**
- **Schrift:** Liberation Sans (Arial-kompatibel), im PDF eingebettet/als Pfade
- Alles ist Vektor → beliebig skalierbar ohne Qualitätsverlust

> Tipp für die Druckerei: Für satte Tiefe das Dunkelblau als Rich-Black/CMYK
> anlegen. Bei Bedarf liefern wir gern eine CMYK-konvertierte PDF.

## QR-Code

Der QR-Code ist als **vCard** hinterlegt: beim Scannen wird direkt der Kontakt
(Name, Firma, Adresse, Telefon, E-Mail) gespeichert. Er ist als Vektor erzeugt
und damit gestochen scharf. Geprüft und erfolgreich dekodiert.

## Rückseite

- Icons aufgeräumt/angepasst: **WhatsApp, Telegram, Signal**
- Das frühere **SMS-Icon wurde entfernt**
- Hinweis „Anrufe werden **NICHT** entgegengenommen.“

## Neu erzeugen / Inhalte ändern

Alle Texte, Kontaktdaten und der QR-Inhalt stehen oben im Generator
`../generate_card.py`. Nach Änderungen einfach neu erzeugen:

```bash
pip install "qrcode[pil]" cairosvg
python generate_card.py
```

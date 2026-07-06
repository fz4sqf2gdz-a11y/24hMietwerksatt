# Medien-Guide – Website vs. YouTube

## Kurzantwort

| Wo | Was |
|----|-----|
| **YouTube** | Alle WhatsApp-Videos hochladen (Prozess, Vorher/Nachher, Klima) |
| **Website** | YouTube **einbetten** + Vorher/Nachher-**Fotos** (JPG) |
| **NICHT ins Git** | `.mp4` Dateien (zu groß, langsam) |

---

## Deine WhatsApp-Videos (Downloads)

Original → umbenennen → YouTube → ID in Website eintragen:

| Original (Downloads) | Vorschlag Dateiname | Vermutlich | YouTube-Titel |
|---------------------|---------------------|------------|---------------|
| `WhatsApp Video 2026-06-24 at 13.11.04.mp4` | `01-sandstrahl-start.mp4` | Sandstrahlen | Sandstrahlen Unterboden – Start |
| `WhatsApp Video 2026-06-24 at 13.12.25.mp4` | `02-sandstrahl-prozess.mp4` | Sandstrahlen | Sandstrahlen – in Arbeit |
| `WhatsApp Video 2026-06-24 at 13.13.55.mp4` | `03-sandstrahl-nachher.mp4` | Sandstrahlen | Sandstrahlen – Ergebnis |
| `WhatsApp Video 2026-06-24 at 13.15.03.mp4` | `04-versiegelung.mp4` | Versiegelung | Unterboden Versiegelung |
| `WhatsApp Video 2026-06-24 at 13.17.02.mp4` | `05-trockeneis.mp4` | Trockeneis | Trockeneis Reinigung |
| `WhatsApp Video 2026-06-24 at 14.06.52.mp4` | `06-vorher-nachher.mp4` | Mix / Übersicht | Vorher Nachher Kompilation |
| `WhatsApp Video 2026-06-24 at 17.01.43.mp4` | `07-klimagas.mp4` | Klimaservice | Klimagas Auffüllung |

> **Tipp:** Kurz jede Datei ansehen und Zeile anpassen falls nötig.

---

## Was auf YouTube stellen? (Empfehlung)

### Unbedingt hochladen (SEO + Reichweite)

1. **Klimagas Füllung** (`07-klimagas`) – Saison-Highlight, gut für Google „Klimaservice St. Pölten“
2. **Sandstrahlen Vorher/Nachher** – 1 Video aus 01–03 schneiden oder `06` nutzen
3. **Versiegelung** (`04`) – glänzender schwarzer Unterboden = starkes Ergebnis
4. **Trockeneis** (`05`) – ergänzt bestehende YouTube-Videos

### Als YouTube Shorts (30–60 Sek, vertikal)

- Sandstrahl „Wow“-Moment (Rost weg)
- Versiegelung glänzend
- Klima Auffüllung (rote/blaue Schläuche)

### Bereits auf YouTube (behalten & verlinken)

- `q_X-nAyXZ40` – Motorraum Trockeneis
- `PNSdLFRYj08` – Trockeneis
- `2qb9rLZB5gQ` – Klimaanlage Trockeneis
- `leCB6bQQiNM` – Unterboden Trockeneis

---

## Was auf die Website?

### Fotos (in `images/einblicke/`)

Siehe `images/einblicke/README.md` – Vorher/Nachher-Paare als JPG.

### Videos

Nur **YouTube-Einbettung** in `index.html` → Suche nach `data-yt-placeholder` oder IDs in `#einblicke`.

Nach Upload auf YouTube die Video-ID eintragen:
```
https://youtu.be/ABC123xyz  →  ABC123xyz
```

---

## Setup auf dem Mac (einmalig)

```bash
cd ~/Desktop/"24h mietwerksatt"

# Ordner anlegen
mkdir -p images/einblicke media/import

# Videos kopieren & umbenennen (Pfade anpassen!)
cp ~/Downloads/"WhatsApp Video 2026-06-24 at 13.11.04.mp4" media/import/01-sandstrahl-start.mp4
# … weitere Dateien analog

# Fotos: Vorher/Nachher aus WhatsApp/Galerie nach images/einblicke/ legen
# Siehe images/einblicke/README.md für Dateinamen

git add images/einblicke/
git commit -m "Einblicke Fotos hinzugefügt"
git push origin main
```

**Videos:** Auf YouTube hochladen, dann IDs in `index.html` eintragen (oder Cursor bitten).

---

## YouTube-Kanal Tipp

- Playlist: **„Mietwerkstatt – Reinigung & Service“**
- Beschreibung immer: Adresse, WhatsApp, Link zur Website
- Hashtags: `#trockeneis #sandstrahlen #mietwerkstatt #stpölten`

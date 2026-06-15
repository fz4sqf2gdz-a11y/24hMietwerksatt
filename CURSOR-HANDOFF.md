# Cursor Handoff – 24h Mietwerkstatt

> **Für neue Cursor-Chats:** Diese Datei + `@CURSOR-HANDOFF.md` in den Chat ziehen.

---

## Projekt

| | |
|---|---|
| **Website live** | https://www.24-stunden-mietwerkstatt.at |
| **GitHub (öffentlich!)** | https://github.com/fz4sqf2gdz-a11y/24hMietwerksatt |
| **Lokal (Mac)** | `~/Desktop/24h mietwerksatt` |
| **Inhaber** | Werner Paternoster, Schwadorf 18, 3100 St. Pölten |
| **WhatsApp** | +43 664 5171370 |

---

## Wichtige Pfade (Mac)

```
~/Desktop/24h mietwerksatt/          ← Hauptprojekt (Website)
~/Downloads/                          ← Screen Recordings, Exporte
```

**Screen-Recording Referenz (Design-Vorlage):**
```
~/Downloads/ScreenRecording_06-15-2026 23-06-44_1.MP4
```
→ Per Drag & Drop in Cursor-Chat ziehen, damit der Agent den Stil sieht.

---

## Cursor nutzen

### Lokal (empfohlen für Dateien auf dem Mac)

1. **Cursor** → **File → Open Folder**
2. Ordner: `~/Desktop/24h mietwerksatt`
3. Im Chat: `@index.html`, `@vibe.css` oder Ordner per `@` erwähnen

### Cloud Agent (GitHub)

1. Code per `git push` zu GitHub
2. Agent auf https://cursor.com/agents starten
3. Repo: `24hMietwerksatt`

**Cloud Agent sieht NICHT:** Desktop, Downloads, lokale Videos.

---

## Projektstruktur

```
24h mietwerksatt/
├── index.html          ← Hauptseite
├── style.css           ← Basis-Styles
├── vibe.css            ← Vibe-Coder Layer (Glass, Bento)
├── script.js           ← Nav, Modals, Slider, Scroll-Reveal
├── images/             ← Bilder
├── buchen/
│   ├── index.html      ← Redirect zu Timify
│   ├── .htaccess       ← NUR auf Server (gitignored!)
│   └── .htpasswd       ← NUR auf Server (gitignored!)
├── statistik/          ← Passwortgeschützt (Server only)
├── druck/              ← Visitenkarte + Flyer (Branch/PR)
├── generate_card.py
└── generate_flyer.py
```

---

## Buchungsablauf (NICHT ändern ohne Absprache mit Werner)

1. **Ersttermin** → WhatsApp (+43 664 5171370)
2. **Einweisung & Registrierung** vor Ort
3. **Freischaltung** nach 1. oder mehreren Terminen
4. **Timify-Portal** → `buchen/index.html` → book.timify.com

Texte und Ablauf sind mit dem Geschäftsführer abgestimmt.

---

## Design-Vorgaben

- **Grundfarben behalten:** Gelb `#ffcc00` / Dunkel `#11141a`
- **Stil:** Vibe-Coder / Instagram (Glass, Bento, dezente Animationen)
- **Keine neuen Marketing-Floskeln** ohne Freigabe

### YouTube-Videos (eingebettet)

| ID | Inhalt |
|----|--------|
| `q_X-nAyXZ40` | Motorraum Trockeneis (Shorts) |
| `PNSdLFRYj08` | Trockeneis Reinigung |
| `2qb9rLZB5gQ` | Klimaanlagen Trockeneis |
| `leCB6bQQiNM` | Auto-Unterboden |

---

## Git – Befehle (Mac-Terminal)

```bash
cd ~/Desktop/"24h mietwerksatt"

git status
git pull origin main
git add index.html style.css vibe.css script.js
git commit -m "Beschreibung"
git push origin main
```

Bei Push-Fehler „non-fast-forward“:
```bash
git pull origin main --rebase
git push origin main
```

---

## ⚠️ Sicherheit (öffentliches Repo!)

**NIE committen:**
- `.htpasswd` (Passwort-Dateien)
- `.htaccess` mit echten Server-Pfaden
- `.env`, API-Keys, Private Keys
- `.DS_Store`

**Vorlagen im Repo:** `*.example` Dateien in `buchen/` und `statistik/`

**Passwörter rotieren:** Falls `.htpasswd` jemals in Git war → **sofort neue Passwörter** auf dem Server setzen (Hashes in Git-Historie sind öffentlich einsehbar).

---

## Offene PRs / Branches

| Branch | Inhalt |
|--------|--------|
| `main` | Live-Website-Stand |
| `cursor/website-upgrade-sandstrahl-eaed` | Vibe-Redesign, YouTube, Sandstrahl-Hinweis |
| `cursor/visitenkarte-werner-paternoster-3388` | Druckdaten Visitenkarte + Flyer |

---

## Typische Aufgaben für Cursor

- Design an Screen-Recording anpassen → Video in Chat ziehen
- BMW-Motor-Fotos einbinden → nach `images/einblicke/` legen + pushen
- Preise/Texte ändern → nur mit Werner absprechen
- Druckdaten → `generate_card.py` / `generate_flyer.py`

---

## Chat-Starter (copy & paste)

```
Projekt: 24h Mietwerkstatt St. Pölten
Repo: github.com/fz4sqf2gdz-a11y/24hMietwerksatt
Lokal: ~/Desktop/24h mietwerksatt
Handoff: @CURSOR-HANDOFF.md

Aufgabe: [hier beschreiben]
Grundfarben und Buchungsablauf nicht ändern.
```

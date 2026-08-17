# Checkliste – Redesign 2026 (Ordner `neu/`)

Das Redesign liegt komplett im Ordner **`neu/`** – die alte Website (`index.html` im Hauptordner) ist unverändert. Werner kann beide Versionen vergleichen; erst wenn das Redesign passt, wird es zur Hauptseite gemacht.

## 1. Was Werner anschauen soll

- [ ] **Startseite** `neu/index.html` – im Browser öffnen (Doppelklick reicht). Neu: ruhiges Layout, Hero mit einem Foto, Ablauf in 3 Schritten, Hebebühnen-Animation beim Scrollen, Services als klare Liste statt vieler Karten. **Alle Texte sind wortgleich übernommen.**
- [ ] **Hebebühnen-Animation** – in der dunklen Sektion „Hebebühne mieten – 24/7“ nach unten scrollen: die Bühne hebt das Auto, die Hubhöhe zählt mit.
- [ ] **Wohnwagen-Seite** `neu/wohnwagen/index.html` – neue Verkaufsseite für die Swift Wohnwagen. Dort sind **Platzhalter markiert** (gelb gestrichelt): Modellnamen, Baujahr, ggf. Preise und Fotos fehlen noch – bitte von Werner liefern lassen.
- [ ] **Mobil testen** – Seite am Handy öffnen: schlanke Navigation, unten fixe Leiste mit Buchungslogin + WhatsApp.
- [ ] **Bewusst entfernt** (Inhalte selbst sind alle noch da): Lauftext-Ticker oben, automatisches Sandstrahl-Popup, Floating-WhatsApp-Button (mobil ersetzt durch die Quick-Bar). Wenn etwas davon zurück soll: sagen.

## 2. Offene Punkte / Fragen an Werner

- [ ] **Wohnwagen:** Welche Swift-Modelle stehen zum Verkauf (Name, Baujahr, Zustand)? Sollen Preise auf die Seite? Fotos machen (Außen, Sitzgruppe, **Dusche**, Küche, Schlafbereich) und nach `images/wohnwagen/` legen.
- [ ] **GA4:** Google-Analytics-Konto anlegen und die Measurement-ID in `neu/assets/main.js` eintragen (siehe `neu/ANALYTICS.md`). Vorher Datenschutz-Hinweis klären.
- [ ] **Werkstatt-Fotos:** Ein aktuelles Hallen-/Hero-Foto in guter Auflösung würde dem neuen Design zusätzlich helfen (aktuell wird `images/hero-aerial.jpg` verwendet).

## 3. Live schalten (Cyberduck / FTP) – WICHTIG

`git push` allein ändert die Live-Site **nicht**. Deploy läuft wie bisher über Cyberduck/FTP bzw. cPanel.

**Phase 1 – Vorschau live stellen (ohne Risiko):**

1. Repo am Mac aktualisieren: `git pull origin main` (nach dem Merge des PRs).
2. Per Cyberduck den kompletten Ordner `neu/` in den Webroot hochladen (dorthin, wo die `index.html` der Live-Site liegt).
3. Vorschau ist dann unter `https://www.24-stunden-mietwerkstatt.at/neu/` erreichbar – die alte Seite bleibt die Startseite.

**Phase 2 – Redesign zur Hauptseite machen (erst wenn Werner zufrieden ist):**

1. Backup der alten Live-Dateien ziehen (mindestens `index.html`, `style.css`, `vibe.css`, `script.js`).
2. Inhalt von `neu/` in den Webroot verschieben und dabei die Pfade anpassen: in `neu/index.html` alle `../images/` → `images/`, `../buchen/` → `buchen/`; in `neu/wohnwagen/index.html` alle `../../` → `../`; in `neu/assets/style.css` das `../../images/` → `../images/`.
   (Alternativ: kurz Bescheid geben, dann bereite ich eine fertige Root-Version im Repo vor.)
3. Prüfen: Seitenquelltext → `site-version` muss `20260817` sein.

## 4. SEO – was gemacht wurde

- Title/Description der Startseite auf die stärksten Search-Console-Begriffe ausgerichtet: *Mietwerkstatt St. Pölten, Hebebühne mieten, Trockeneis, Sandstrahlen, Werner Paternoster, Niederösterreich* – ohne Keyword-Stuffing, Werners Texte unangetastet.
- Neue Wohnwagen-Seite mit eigenem Title/Description für „Wohnwagen Swift Österreich / St. Pölten“.
- Strukturierte Daten (JSON-LD `AutoRepair` mit Adresse Schwadorf 18, Öffnungszeiten 24/7, Social-Profile) für Local SEO.
- Sinnvolle Alt-Texte für alle Bilder, klare H1/H2-Hierarchie.
- Noch offen (erst bei Live-Gang an Root sinnvoll): `sitemap.xml` aktualisieren/anlegen und die Wohnwagen-URL in der Search Console einreichen.

# Checkliste – Root-Version (`relaunch/`)

Diese Version ist **fertig als Webroot**: Pfade zeigen auf `images/`, `buchen/`, `wohnwagen/` im selben Ordner. Die alte Website und der Ordner `neu/` bleiben unangetastet.

## 1. Was Werner anschauen soll

- [ ] **Startseite** `index.html` – Hero, Ablauf, Hebebühnen-Animation, Services, Trockeneis, Einblicke, Wohnwagen-Teaser, Preise, Ausstattung, FAQ, Kontakt. Texte von Werner wortgleich.
- [ ] **Hebebühnen-Animation** – in der dunklen Sektion scrollen: Bühne hebt das Auto, Hubhöhe zählt mit.
- [ ] **Wohnwagen** `wohnwagen/index.html` – Platzhalter für Modelle/Preise/Fotos sind gelb markiert.
- [ ] **Mobil** – Navigation, Quick-Bar unten (Buchungslogin + WhatsApp).

## 2. Offene Punkte

- [ ] Swift-Modelle (Name, Baujahr, Zustand) und ob Preise auf die Seite sollen.
- [ ] Fotos nach `images/wohnwagen/` legen und in `wohnwagen/index.html` eintragen.
- [ ] GA4-ID in `assets/main.js` eintragen (siehe `ANALYTICS.md`). Vorher Datenschutz klären.

## 3. Testserver (Cyberduck)

1. Ordner lokal nach `~/Projects/24h-mietwerkstatt-relaunch` kopieren (siehe `README.md`).
2. Inhalt dieses Ordners per FTP auf den **Testserver** hochladen – nicht in den Live-Webroot der alten Site.
3. Prüfen: `site-version` = `20260817`.

Erst wenn Werner zufrieden ist: denselben Ordnerinhalt auf die Live-Domain legen (vorher Backup der alten Live-Dateien).

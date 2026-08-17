# Checkliste – Root-Version (`relaunch/`)

Diese Version ist **fertig als Webroot**: Pfade zeigen auf `images/`, `buchen/`, `wohnwagen/` im selben Ordner. Die alte Website und der Ordner `neu/` bleiben unangetastet.

## 1. Was Werner anschauen soll

- [ ] **Startseite** `index.html` – Hero, Ablauf, Hebebühnen-Animation, Services, Trockeneis, Einblicke, Wohnwagen-Teaser, Preise, Ausstattung, FAQ, Kontakt. Texte von Werner wortgleich.
- [ ] **Hebebühnen-Animation** – in der dunklen Sektion scrollen: Bühne hebt das Auto, Hubhöhe zählt mit.
- [ ] **Wohnwagen** `wohnwagen/index.html` – Platzhalter für Modelle/Preise/Fotos sind gelb markiert.
- [ ] **Mobil** – Navigation, Quick-Bar unten (Buchungslogin + WhatsApp).

## 2. Offene Punkte

- [ ] **Wohnwagen-Videos:** Die zwei WhatsApp-Videos aus Downloads nach `images/wohnwagen/` kopieren und umbenennen: `sprite.mp4` (Swift Sprite) und `bailey.mp4` (Bailey). Sie erscheinen dann automatisch in den Modell-Karten. Achtung: `*.mp4` ist gitignored – per Cyberduck direkt auf den Server laden.
- [ ] **Wohnwagen-Details:** Genaue Modellbezeichnungen, Schlafplätze, Gewicht, Zustand von Werner ergänzen (Platzhalter auf der Seite ist markiert). Preise sind eingetragen: Sprite 23.000 €, Bailey 12.500 €.
- [ ] Fotos (Außen, Bad mit Dusche, Küche, Schlafbereich) nach `images/wohnwagen/` legen und die Platzhalter ersetzen.
- [ ] GA4-ID in `assets/main.js` eintragen (siehe `ANALYTICS.md`). Vorher Datenschutz klären.

## Wichtig: Vorschau immer über einen Server öffnen

Die YouTube-Videos zeigen **„Fehler 153“**, wenn man die `index.html` per Doppelklick öffnet (`file://` sendet keinen Referer an YouTube). Das ist kein Fehler der Seite – auf dem Testserver/Live funktionieren die Videos. Lokal so testen:

```bash
cd ~/Projects/24h-mietwerkstatt-relaunch
python3 -m http.server 8000
# dann http://localhost:8000 öffnen
```

## 3. Testserver (Cyberduck)

1. Ordner lokal nach `~/Projects/24h-mietwerkstatt-relaunch` kopieren (siehe `README.md`).
2. Inhalt dieses Ordners per FTP auf den **Testserver** hochladen – nicht in den Live-Webroot der alten Site.
3. Prüfen: `site-version` = `20260817d`.

Erst wenn Werner zufrieden ist: denselben Ordnerinhalt auf die Live-Domain legen (vorher Backup der alten Live-Dateien).

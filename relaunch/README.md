# Redesign – eigenständiger Webroot

Dieser Ordner **ist die komplette neue Website**. Er hängt nicht an der alten Site.
Den alten Projektordner (`24hMietwerksatt` / `24h mietwerksatt`) **nicht überschreiben**.

```
relaunch/
├── index.html          ← Startseite (Root)
├── wohnwagen/          ← Swift-Verkaufsseite
├── assets/             ← CSS + JS
├── images/             ← alle Fotos (Kopie, unabhängig)
├── buchen/             ← Timify-Redirect
├── ANALYTICS.md
└── CHECKLISTE.md
```

## Auf den Mac holen (neuer Ordner in Projects)

Im bestehenden Repo (nicht den alten Ordner ersetzen):

```bash
cd /Users/ioannisgander/Projects/24hMietwerksatt
git pull origin cursor/redesign-relaunch-10a2

# Neuer, unabhängiger Ordner – die alte Website bleibt unberührt
rm -rf /Users/ioannisgander/Projects/24h-mietwerkstatt-relaunch
cp -R relaunch /Users/ioannisgander/Projects/24h-mietwerkstatt-relaunch
```

Lokal testen:

```bash
cd /Users/ioannisgander/Projects/24h-mietwerkstatt-relaunch
open index.html
# oder: python3 -m http.server 8000  →  http://localhost:8000/
```

## Auf den Testserver (Cyberduck / FTP)

`git push` ändert die Live-Site **nicht**.

1. In Cyberduck zum **Testserver** verbinden (nicht den Live-Webroot der alten Site).
2. Den **Inhalt** von `24h-mietwerkstatt-relaunch` hochladen (also `index.html`, `assets/`, `images/`, `wohnwagen/`, `buchen/` direkt in den Webroot des Testservers).
3. Prüfen: Seitenquelltext → `site-version` muss `20260817b` sein.
4. Wohnwagen-URL: `https://<testserver>/wohnwagen/`

Die Live-Domain `www.24-stunden-mietwerkstatt.at` bleibt die alte Seite, solange dieser Ordner nicht dorthin hochgeladen wird.

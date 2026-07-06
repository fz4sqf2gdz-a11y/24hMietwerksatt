#!/bin/bash
# =============================================================================
# 24h Mietwerkstatt – Dateien fürs Live-Upload vorbereiten
#
# WICHTIG: git push aktualisiert NICHT die Website!
# Die live Site läuft auf einem Webhost – du musst die Dateien hochladen.
#
# Auf dem Mac:
#   cd ~/Desktop/"24h mietwerksatt"
#   git pull origin main
#   bash media/deploy-zum-webserver.sh
#
# Dann ZIP entpacken und per FTP/cPanel in den Webroot hochladen
# (dort wo index.html der Live-Site liegt).
# =============================================================================

set -euo pipefail

PROJECT="${1:-$HOME/Desktop/24h mietwerksatt}"
OUT="$HOME/Desktop/24h-upload-webserver-$(date +%Y%m%d).zip"
TMP="$(mktemp -d)"

cd "$PROJECT"

echo "=== 24h Mietwerkstatt – Upload-Paket bauen ==="
echo "Projekt: $PROJECT"
echo ""

FILES=(
  index.html
  style.css
  vibe.css
  script.js
  images/einblicke/sandstrahl-vorher-01.jpg
  images/einblicke/sandstrahl-vorher-02.jpg
  images/einblicke/sandstrahl-vorher-03.jpg
  images/einblicke/sandstrahl-arbeit-01.jpg
  images/einblicke/sandstrahl-nachher-01.jpg
  images/einblicke/sandstrahl-nachher-02.jpg
  images/einblicke/versiegelung-vorher-01.jpg
  images/einblicke/versiegelung-nachher-01.jpg
  images/einblicke/klima-service-01.jpg
)

MISS=0
for f in "${FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "✗ FEHLT: $f"
    MISS=$((MISS + 1))
  else
    mkdir -p "$TMP/$(dirname "$f")"
    cp "$f" "$TMP/$f"
    echo "✓ $f"
  fi
done

if [[ $MISS -gt 0 ]]; then
  echo ""
  echo "Abbruch – erst git pull origin main, dann erneut starten."
  rm -rf "$TMP"
  exit 1
fi

(cd "$TMP" && zip -rq "$OUT" .)
rm -rf "$TMP"

echo ""
echo "=========================================="
echo "Fertig: $OUT"
echo ""
echo "Nächste Schritte:"
echo "  1. ZIP auf dem Mac doppelklicken (entpacken)"
echo "  2. cPanel Dateimanager oder FTP (FileZilla) öffnen"
echo "  3. In den Ordner der Live-Site gehen (wo index.html liegt)"
echo "  4. Alle Dateien aus dem ZIP hochladen – ÜBERSCHREIBEN bestätigen"
echo "  5. Im Browser: https://www.24-stunden-mietwerkstatt.at"
echo "     Seitenquelltext: site-version muss 20260706 sein"
echo "     Ticker muss SANDSTRAHLEN IN DER HALLE zeigen (nicht BALD DA)"
echo ""
open "$HOME/Desktop" 2>/dev/null || true

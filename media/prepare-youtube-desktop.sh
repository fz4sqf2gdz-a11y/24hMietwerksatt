#!/bin/bash
# =============================================================================
# 24h Mietwerkstatt – YouTube-Videos vorbereiten
# Auf dem Mac ausführen (einmal):
#
#   cd ~/Desktop/"24h mietwerksatt"
#   bash media/prepare-youtube-desktop.sh
#
# Ergebnis: ~/Desktop/24h-mietwerkstatt-youtube/ mit umbenannten Videos
# =============================================================================

set -euo pipefail

DOWNLOADS="$HOME/Downloads"
DESKTOP="$HOME/Desktop/24h-mietwerkstatt-youtube"
PROJECT="${1:-$HOME/Desktop/24h mietwerksatt}"

declare -a MAP=(
  "WhatsApp Video 2026-06-24 at 13.11.04.mp4|01-sandstrahl-unterboden-start.mp4"
  "WhatsApp Video 2026-06-24 at 13.12.25.mp4|02-sandstrahl-unterboden-prozess.mp4"
  "WhatsApp Video 2026-06-24 at 13.13.55.mp4|03-sandstrahl-unterboden-ergebnis.mp4"
  "WhatsApp Video 2026-06-24 at 13.15.03.mp4|04-unterboden-versiegelung.mp4"
  "WhatsApp Video 2026-06-24 at 13.17.02.mp4|05-trockeneis-reinigung.mp4"
  "WhatsApp Video 2026-06-24 at 14.06.52.mp4|06-vorher-nachher-kompilation.mp4"
  "WhatsApp Video 2026-06-24 at 17.01.43.mp4|07-klimagas-auffuellung.mp4"
)

echo "=== 24h Mietwerkstatt – YouTube Ordner ==="
echo ""

mkdir -p "$DESKTOP"
mkdir -p "$DESKTOP/texte-fuer-youtube"

OK=0
MISS=0

for entry in "${MAP[@]}"; do
  IFS='|' read -r src dest <<< "$entry"
  src_path="$DOWNLOADS/$src"
  dest_path="$DESKTOP/$dest"

  if [[ -f "$src_path" ]]; then
    cp "$src_path" "$dest_path"
    size=$(du -h "$dest_path" | cut -f1)
    echo "✓ $dest  ($size)"
    OK=$((OK + 1))
  else
    echo "✗ FEHLT: $src"
    echo "  Erwartet in: $DOWNLOADS/"
    MISS=$((MISS + 1))
  fi
done

# Metadaten-Texte kopieren
if [[ -d "$PROJECT/media/youtube-texte" ]]; then
  cp "$PROJECT/media/youtube-texte/"*.txt "$DESKTOP/texte-fuer-youtube/" 2>/dev/null || true
  echo ""
  echo "✓ YouTube-Texte nach texte-fuer-youtube/ kopiert"
fi

# Upload-Checkliste
cat > "$DESKTOP/LIESMICH.txt" << 'EOF'
24h Mietwerkstatt – YouTube Upload
==================================

Ordner: ~/Desktop/24h-mietwerkstatt-youtube/

VIDEOS (in dieser Reihenfolge hochladen):
  01-sandstrahl-unterboden-start.mp4
  02-sandstrahl-unterboden-prozess.mp4
  03-sandstrahl-unterboden-ergebnis.mp4
  04-unterboden-versiegelung.mp4
  05-trockeneis-reinigung.mp4
  06-vorher-nachher-kompilation.mp4
  07-klimagas-auffuellung.mp4

TITEL + BESCHREIBUNG: siehe Ordner texte-fuer-youtube/

UPLOAD:
  1. https://studio.youtube.com öffnen
  2. „Erstellen“ → „Video hochladen“
  3. Video aus diesem Ordner wählen
  4. Titel/Beschreibung aus passender .txt kopieren
  5. Playlist: „Mietwerkstatt – Reinigung & Service“

SHORTS (optional, vertikal kürzen):
  - 03-sandstrahl (Ergebnis)
  - 04-versiegelung
  - 07-klimagas

Website: Videos NICHT ins Git – nur YouTube-Link später einbetten.
EOF

echo ""
echo "=========================================="
if [[ $MISS -eq 0 ]]; then
  echo "Fertig: $OK Videos in"
  echo "  $DESKTOP"
  echo ""
  echo "Ordner wird geöffnet …"
  open "$DESKTOP" 2>/dev/null || true
  echo ""
  echo "YouTube Studio:"
  echo "  https://studio.youtube.com"
  open "https://studio.youtube.com" 2>/dev/null || true
else
  echo "$OK kopiert, $MISS fehlen."
  echo "Prüfe Downloads-Ordner und Dateinamen."
  exit 1
fi

#!/bin/bash
# Einmal-Skript: WhatsApp-Medien vom Mac ins Projekt kopieren
# Ausführen: bash media/setup-media.sh

set -e
PROJECT="${1:-$HOME/Desktop/24h mietwerksatt}"
DOWNLOADS="$HOME/Downloads"

cd "$PROJECT"
mkdir -p media/import images/einblicke

copy_video() {
  local src="$1" dest="$2"
  if [[ -f "$DOWNLOADS/$src" ]]; then
    cp "$DOWNLOADS/$src" "media/import/$dest"
    echo "✓ $dest"
  else
    echo "– fehlt: $src"
  fi
}

echo "=== Videos nach media/import/ ==="
copy_video "WhatsApp Video 2026-06-24 at 13.11.04.mp4" "01-sandstrahl-start.mp4"
copy_video "WhatsApp Video 2026-06-24 at 13.12.25.mp4" "02-sandstrahl-prozess.mp4"
copy_video "WhatsApp Video 2026-06-24 at 13.13.55.mp4" "03-sandstrahl-nachher.mp4"
copy_video "WhatsApp Video 2026-06-24 at 13.15.03.mp4" "04-versiegelung.mp4"
copy_video "WhatsApp Video 2026-06-24 at 13.17.02.mp4" "05-trockeneis.mp4"
copy_video "WhatsApp Video 2026-06-24 at 14.06.52.mp4" "06-vorher-nachher.mp4"
copy_video "WhatsApp Video 2026-06-24 at 17.01.43.mp4" "07-klimagas.mp4"

echo ""
echo "=== Nächste Schritte ==="
echo "1. Videos auf YouTube hochladen (NICHT ins Git!)"
echo "2. Fotos nach images/einblicke/ legen (siehe README dort)"
echo "3. YouTube-IDs in index.html eintragen (#einblicke)"
echo "4. git add images/einblicke/ && git commit && git push"

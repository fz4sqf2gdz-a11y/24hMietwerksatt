#!/bin/bash
# =============================================================================
# 24h Mietwerkstatt – Fotos vorbereiten (Vorher/Nachher)
# Auf dem Mac ausführen:
#
#   cd ~/Desktop/"24h mietwerksatt"
#   bash media/prepare-fotos-desktop.sh
#
# Optional – nur WhatsApp-Bilder vom 24.06. automatisch zuordnen:
#   bash media/prepare-fotos-desktop.sh --auto
#
# Ergebnis:
#   ~/Desktop/24h-mietwerkstatt-fotos/     (Kopie zum Prüfen)
#   ~/Desktop/24h mietwerksatt/images/einblicke/  (für Website + Git)
# =============================================================================

set -euo pipefail

DOWNLOADS="$HOME/Downloads"
DESKTOP_OUT="$HOME/Desktop/24h-mietwerkstatt-fotos"
DEFAULT_PROJECT="$HOME/Desktop/24h mietwerksatt"
AUTO_MODE=0
PROJECT="$DEFAULT_PROJECT"

for arg in "$@"; do
  if [[ "$arg" == "--auto" ]]; then
    AUTO_MODE=1
  elif [[ "$arg" != --* ]]; then
    PROJECT="$arg"
  fi
done

OUT_DIR="$PROJECT/images/einblicke"

# Wenn du exakte Dateinamen in Downloads kennst, hier eintragen:
# Format: "Originalname|ziel-dateiname.jpg"
declare -a MAP=(
  # Beispiel:
  # "WhatsApp Image 2026-06-24 at 12.01.00.jpeg|sandstrahl-vorher-01.jpg"
)

declare -a TARGETS=(
  "sandstrahl-vorher-01.jpg|Unterboden mit Rost (Gesamtansicht)"
  "sandstrahl-vorher-02.jpg|Aufhängung / Unterboden mit Rost"
  "sandstrahl-vorher-03.jpg|Fahrwerk / Stoßdämpfer mit Rost"
  "sandstrahl-arbeit-01.jpg|Sandstrahlen in der Halle"
  "sandstrahl-nachher-01.jpg|Unterboden aufbereitet"
  "sandstrahl-nachher-02.jpg|Fahrwerk aufbereitet"
  "versiegelung-vorher-01.jpg|Vor Versiegelung"
  "versiegelung-nachher-01.jpg|Versiegelter Unterboden"
  "klima-service-01.jpg|Klimaservice (Gerät oder Motorraum)"
)

copy_and_convert() {
  local src="$1"
  local dest="$2"
  local ext="${dest##*.}"

  if [[ ! -f "$src" ]]; then
    return 1
  fi

  mkdir -p "$(dirname "$dest")"

  if [[ "${src##*.}" =~ ^([Hh][Ee][Ii][Cc])$ ]]; then
    sips -s format jpeg "$src" --out "$dest" >/dev/null 2>&1
  else
    cp "$src" "$dest"
  fi

  if command -v sips >/dev/null 2>&1; then
    sips -Z 1920 "$dest" >/dev/null 2>&1 || true
  fi
  return 0
}

echo "=== 24h Mietwerkstatt – Fotos vorbereiten ==="
echo ""

mkdir -p "$DESKTOP_OUT"
mkdir -p "$OUT_DIR"

OK=0
MISS=0

# --- 1) Explizite Zuordnung ---
if [[ ${#MAP[@]} -gt 0 ]]; then
  echo "--- Bekannte Dateinamen ---"
  for entry in "${MAP[@]}"; do
    [[ -z "$entry" || "$entry" == \#* ]] && continue
    IFS='|' read -r src dest <<< "$entry"
    src_path="$DOWNLOADS/$src"
    if copy_and_convert "$src_path" "$DESKTOP_OUT/$dest" && \
       copy_and_convert "$src_path" "$OUT_DIR/$dest"; then
      echo "✓ $dest"
      OK=$((OK + 1))
    else
      echo "✗ FEHLT: $src"
      MISS=$((MISS + 1))
    fi
  done
  echo ""
fi

# --- 2) Auto-Modus: WhatsApp/IMG aus Downloads nach Zeit sortiert ---
if [[ $AUTO_MODE -eq 1 ]]; then
  echo "--- Auto-Modus: Bilder aus Downloads ---"
  TMP_LIST="$(mktemp)"
  find "$DOWNLOADS" -maxdepth 1 -type f \( \
    -iname 'WhatsApp Image*.jpeg' -o \
    -iname 'WhatsApp Image*.jpg' -o \
    -iname 'IMG_*.JPG' -o \
    -iname 'IMG_*.jpeg' -o \
    -iname '*.HEIC' -o \
    -iname '*.heic' \
  \) -newermt '2026-06-01' 2>/dev/null | sort > "$TMP_LIST"

  COUNT=$(wc -l < "$TMP_LIST" | tr -d ' ')
  echo "Gefunden: $COUNT Bilder (ab Juni 2026)"
  echo ""

  i=0
  while IFS= read -r src_path && [[ $i -lt ${#TARGETS[@]} ]]; do
    IFS='|' read -r dest desc <<< "${TARGETS[$i]}"
    dest_path="$DESKTOP_OUT/$dest"

    if [[ -f "$dest_path" ]]; then
      echo "– übersprungen (existiert): $dest"
      i=$((i + 1))
      continue
    fi

    if copy_and_convert "$src_path" "$DESKTOP_OUT/$dest" && \
       copy_and_convert "$src_path" "$OUT_DIR/$dest"; then
      echo "✓ $dest  ←  $(basename "$src_path")"
      echo "    ($desc)"
      OK=$((OK + 1))
    fi
    i=$((i + 1))
  done < "$TMP_LIST"

  rm -f "$TMP_LIST"
  echo ""
  echo "⚠️  Auto-Modus mappt nur nach Datei-Datum – immer im Finder prüfen!"
  echo "    Screenshots und falsche Bilder manuell entfernen."
  echo ""
fi

# --- LIESMICH ---
cat > "$DESKTOP_OUT/LIESMICH.txt" << EOF
24h Mietwerkstatt – Fotos für Website
=====================================

Ziel-Dateinamen (images/einblicke/):

$(for t in "${TARGETS[@]}"; do
  IFS='|' read -r f d <<< "$t"
  echo "  $f  –  $d"
done)

Website-Ordner:
  $OUT_DIR

Nächste Schritte:
  1. Fotos im Finder prüfen (Vorher/Nachher stimmt?)
  2. Im Projektordner:
     cd "$PROJECT"
     git add images/einblicke/
     git commit -m "Einblicke Fotos Vorher/Nachher"
     git push origin main
  3. index.html auf Webserver aktualisieren (git pull)

Tipp: Einzelne Bilder manuell umbenennen und nach
  images/einblicke/
kopieren – Dateinamen exakt wie oben.
EOF

cp "$DESKTOP_OUT/LIESMICH.txt" "$OUT_DIR/LIESMICH.txt" 2>/dev/null || true
# LIESMICH nicht ins Git committen
rm -f "$OUT_DIR/LIESMICH.txt" 2>/dev/null || true

echo "=========================================="
echo "Fertig: $OK Bilder vorbereitet"
echo ""
echo "  Prüfen:  $DESKTOP_OUT"
echo "  Website: $OUT_DIR"
echo ""

if [[ $AUTO_MODE -eq 0 && ${#MAP[@]} -eq 0 ]]; then
  echo "Hinweis: Keine festen Dateinamen hinterlegt."
  echo "Starte mit Auto-Zuordnung:"
  echo "  bash media/prepare-fotos-desktop.sh --auto"
  echo ""
fi

if [[ $OK -gt 0 ]]; then
  echo "Git push:"
  echo "  cd \"$PROJECT\""
  echo "  git add images/einblicke/"
  echo "  git commit -m \"Einblicke Fotos\""
  echo "  git push origin main"
  echo ""
  open "$DESKTOP_OUT" 2>/dev/null || true
fi

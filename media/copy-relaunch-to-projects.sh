#!/usr/bin/env bash
# Kopiert die eigenständige Root-Version nach ~/Projects/24h-mietwerkstatt-relaunch
# Der alte Projektordner bleibt unberührt.
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)/relaunch"
DEST="${HOME}/Projects/24h-mietwerkstatt-relaunch"

if [ ! -d "$SRC" ]; then
  echo "Quelle nicht gefunden: $SRC"
  echo "Zuerst ins Repo wechseln und git pull machen."
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
echo "Fertig: $DEST"
echo "Lokal öffnen:  open \"$DEST/index.html\""
echo "Testserver:    Inhalt dieses Ordners per Cyberduck hochladen (nicht die Live-Site)."

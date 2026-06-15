# Sicherheitshinweise

Dieses Repository ist **öffentlich**. Behandle alles in Git als von jedem einsehbar.

## Sofort-Maßnahme

Falls `buchen/.htpasswd` oder `statistik/.htpasswd` jemals committed waren:

1. **Neue Passwörter** für alle geschützten Bereiche setzen
2. Auf dem Server neue `.htpasswd` erzeugen:
   ```bash
   htpasswd -c .htpasswd neuer_benutzername
   ```
3. Alte Hashes gelten als kompromittiert (auch nach Löschung aus Git – Historie bleibt)

## Was nicht ins Repo gehört

| Datei | Grund |
|-------|--------|
| `.htpasswd` | Passwort-Hashes |
| `.htaccess` (mit echtem Server-Pfad) | Hosting-Account erkennbar |
| `.env` | Secrets |
| Große private Videos | Besser YouTube oder lokal |

## Server-Setup (nur auf dem Webserver)

```bash
# buchen/
cp .htaccess.example .htaccess   # Pfad anpassen!
htpasswd -c .htpasswd benutzer

# statistik/
cp .htaccess.example .htaccess
htpasswd -c .htpasswd benutzer
```

Diese Dateien liegen nur auf dem Server, nicht in Git.

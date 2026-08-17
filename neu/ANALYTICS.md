# Analytics – GA4 Einrichtung & Events

## GA4 aktivieren

1. In [Google Analytics](https://analytics.google.com) eine Property anlegen (falls noch nicht vorhanden) und die **Measurement-ID** kopieren (Format `G-XXXXXXXXXX`).
2. In `neu/assets/main.js` ganz oben die ID eintragen:

```js
const GA4_MEASUREMENT_ID = 'G-XXXXXXXXXX'; // <<< HIER GA4-ID EINTRAGEN
```

**Solange der Platzhalter drinsteht, wird GA4 nicht geladen** – kein Tracking, keine Fehler. Die Seite funktioniert normal.

## Welche Events feuern wo

Alle Events werden in `neu/assets/main.js` zentral über die Funktion `track()` gesendet. Die Zuordnung passiert über `data-`Attribute im HTML – kein Event ist fest verdrahtet.

| Event | Parameter | Wann |
|---|---|---|
| `cta_click` | `cta`, `cta_location` | Klick auf jeden Button/Link mit `data-ga-cta` (WhatsApp, Buchungslogin, Timify, Sandstrahlen, Wohnwagen-Anfrage, Preise). `cta_location` sagt, wo auf der Seite geklickt wurde (z.B. `hero`, `header`, `preise`, `quickbar`). |
| `cta_click` mit `cta: whatsapp_formular` | `form_id` | Absenden eines WhatsApp-Formulars (Kontakt-Sektion, Modal, Wohnwagen-Seite). |
| `nav_click` | `target` | Klick auf Navigations-Links mit `data-ga-nav` – aktuell der Link **Wohnwagen/Swift** in Header und Footer. |
| `section_view` | `section` | Eine Sektion mit `data-ga-section` wird zu 30 % sichtbar (einmal pro Seitenaufruf). Getrackt: `ablauf`, `hebebuehne`, `angebote`, `trockeneis`, `einblicke`, `wohnwagen_teaser`, `preise`, `ausstattung`, `kontakt` sowie die Sektionen der Wohnwagen-Seite. |
| `scroll_depth` | `percent` (25/50/75/100) | Scroll-Tiefe, jede Marke einmal pro Seitenaufruf. |
| `video_impression` | `video_title` | Ein YouTube-Embed wird zu 50 % sichtbar (einmal pro Video und Seitenaufruf). |

## Was man damit beantworten kann

- **Was gefällt den Leuten?** → `section_view` + `scroll_depth`: Wie weit scrollen Besucher, welche Sektionen (Einblicke, Preise, Trockeneis, Wohnwagen) werden gesehen?
- **Welche Videos ziehen?** → `video_impression` pro Videotitel.
- **Was konvertiert?** → `cta_click` nach `cta` und `cta_location` aufschlüsseln: Kommen WhatsApp-Klicks eher aus dem Hero, den Preisen oder der Quickbar?
- **Zieht das Wohnwagen-Angebot?** → `nav_click` mit `target: wohnwagen` + Seitenaufrufe von `/wohnwagen/` + `cta_click` mit `cta: wohnwagen_anfrage`.

## Hinweis zu Video-Interaktion

Echte Play/Pause-Events der YouTube-Embeds bräuchten die YouTube IFrame API (zusätzliches Script pro Video). Bewusst weggelassen, um die Seite schlank zu halten – `video_impression` zeigt, welche Videos überhaupt gesehen werden. Bei Bedarf nachrüstbar.

## Datenschutz

- GA4 wird mit `anonymize_ip: true` konfiguriert.
- Wenn GA4 live geht, sollte ein Datenschutz-Hinweis (und je nach Auslegung ein Cookie-Consent-Banner) ergänzt werden. Das ist bewusst noch nicht eingebaut – bitte mit Werner klären, bevor die ID eingetragen wird.

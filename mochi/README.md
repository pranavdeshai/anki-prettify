# mochi
Anki flashcard template based on the flashcard app - Mochi

## Features
### Minimal
Minimises distractions without affecting important elements of the card.

### Responsive
Works on both Anki (desktop) and AnkiDroid (Android).
Haven't tested on the Anki Mobile (iOS).

### Night mode
Easy on the eyes for the night-owls.

### Fully customizable
CSS variables for reusability and maintenance.

## Instructions
### Direct download (quick and easy)
1. Download the [demo deck](https://github.com/pranavdeshai23/anki-templates/blob/main/mochi/anki-mochi.apkg)
2. The new note type (`demo-mochi-cloze`) should be created automatically
3. Use the note type as it is or clone it to suit your needs

### Manual method (if you don't like downloading stuff online)
1. Create a new note type
2. Rename the `Back Extra` field to `Extra` (as this is the field name used in the template)
3. Copy the contents of `front.html` and `back.html` into the front and back templates of the note (Can be accessed by clicking on `Cards` when in browser mode)
4. Copy the contents of `style.css` into the styling section of the note
5. You can now use the new note type in your collection

## Requirements
- Anki 2.1 or higher (2.1.x) is required for CSS flexbox to render properly
- No addons required ([WebView inspector addon](https://ankiweb.net/shared/info/31746032) is recommended for debugging and customizing)

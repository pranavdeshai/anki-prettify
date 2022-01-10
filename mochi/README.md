# mochi

Anki flashcard template based on the flashcard app - Mochi

## Features

-   **Minimal**: Minimises distractions without affecting important elements of the card
-   **Responsive design**: Works on both Anki 2.1+ (desktop) and AnkiDroid (Android)
-   **Dark theme**: Easy on the eyes for the night-owls
-   **Fully customizable**: CSS variables for reusability and maintenance
-   **Tags**: for quick context
-   **Includes [basic](./mochi-basic) and [cloze](./mochi-cloze) note types**

## Instructions

### Direct download (quick and easy)

1. Download the demo deck (`mochi-basic` or `mochi-cloze` in the respective sub-folders)
2. The new note type (`demo-mochi-...`) should be created automatically
3. Use the note type as it is or _clone_ it to suit your needs

### Manual method (if you don't like downloading stuff online)

1. Create a new note type
2. Copy the contents of `front.html` and `back.html` into the front and back templates of the note (Can be accessed by clicking on `Cards` when in browser mode)

> **Note**: For cloze notes, you have to rename the field `Back Extra` to `Extra` (this is the field name used in the template because it's simpler)

3. Copy the contents of `style.css` into the styling section of the note 4. You can now use the new note type in your collection

## Requirements

-   Anki 2.1 or higher (2.1.x) is required for CSS flexbox to render properly
-   No addons required ([WebView inspector addon](https://ankiweb.net/shared/info/31746032) is recommended for debugging and customizing)

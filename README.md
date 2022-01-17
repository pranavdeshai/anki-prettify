# Anki Templates

Collection of customizable Anki flashcard templates with modern and clean themes.

- [Features](#features)
- [Themes](#themes)
- [Instructions](#instructions)
- [Add-on support](#add-on-support)
- [Compatibility](#compatibility)
- [Requirements](#requirements)

## Features

-   Automatic dark and night theme switching
-   Responsive design - fully support for desktop and mobile apps
-   Customizable color palette
-   Support for Basic and Cloze note types
-   Tags for quick context
-   Click and hold to expand images
-   Preferences for tweaking optional features

## Themes

### [Minimal](./src/minimal)

## Instructions

### Direct download

1. Download the demo deck file (`{theme}-basic.apkg` or `{theme}-cloze.apkg`)
2. Open Anki and click on `Import File`
3. Select the downloaded deck file
4. The new note type (`basic-{theme}` or `cloze-{theme}`) should be created automatically
5. Use the note type as it is or [clone it](https://docs.ankiweb.net/editing.html#adding-a-note-type)

### Manual method

1. Create a new note type (See [Adding a note type](https://docs.ankiweb.net/editing.html#adding-a-note-type))
2. Click on `Cards` in browser mode
3. Copy the contents of `front.html` and `back.html` into the Front and back templates of the note type

    > **Important**: For cloze notes, the field `Back Extra` should be renamed to `Extra` (this is the name used in the template)

4. Copy the content of `style.css` into the _Styling_ section
5. You can now use the new note type in your collection

## Add-on support

The following add-ons are currently supported

-   [Clickable Tags](https://ankiweb.net/shared/info/1739176371)
-   [Edit Field During Review (Cloze)](https://ankiweb.net/shared/info/385888438)

> **Note**: Add-ons are optional and not necessary. The templates work as expected _with or without_ the addons.

## Compatibility

Tested on

-   Desktop: Anki 2.1.49 (Mac)
-   Mobile: AnkiDroid 2.15 (Can someone test on iOS?)
-   Browsers (AnkiWeb): Chrome(97.0.4692.71), Safari(15.0)

## Requirements

-   Anki 2.1 or higher (should work with even Anki 2.0)

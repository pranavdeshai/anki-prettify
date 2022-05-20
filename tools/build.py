# Automate building demo packages from source code

import json
import os
import re
import sys
from pathlib import Path
from random import randrange

import genanki
import requests

FONTS = {
    "minimal": "Inter",
    "nord": "Rubik",
    "dracula": "Source Sans Pro",
}

# Field contents for each note type
NOTE_FIELDS = {
    "basic": [
        "What is <b>Anki</b>?",
        "<b>Anki</b>&nbsp;is a <u>free and open-source</u>&nbsp;flashcard&nbsp;program using&nbsp;<i>spaced repetition</i>, a technique from&nbsp;cognitive science&nbsp;for fast and long-lasting memorization.<br><br><img src='https://upload.wikimedia.org/wikipedia/commons/9/9a/Anki_2.1.6_screenshot.png'><br>Anki 2.1.6 screenshot (<a href='https://en.wikipedia.org/wiki/Anki_(software)'>https://en.wikipedia.org/wiki/Anki_(software)</a>)",
    ],
    "basic_reverse": [
        "What is <b>Anki</b>?",
        "<b>Anki</b>&nbsp;is a <u>free and open-source</u>&nbsp;flashcard&nbsp;program using&nbsp;<i>spaced repetition</i>, a technique from&nbsp;cognitive science&nbsp;for fast and long-lasting memorization.<br><br><img src='https://upload.wikimedia.org/wikipedia/commons/9/9a/Anki_2.1.6_screenshot.png'><br>Anki 2.1.6 screenshot (<a href='https://en.wikipedia.org/wiki/Anki_(software)'>https://en.wikipedia.org/wiki/Anki_(software)</a>)",
    ],
    "cloze": [
        "<b>Anki</b>&nbsp;is a <u>free and open-source</u>&nbsp;{{c1::flashcard}}&nbsp;program using&nbsp;<i>spaced repetition</i>, a technique from&nbsp;cognitive science&nbsp;for fast and long-lasting memorization.<br><br><img src='https://upload.wikimedia.org/wikipedia/commons/9/9a/Anki_2.1.6_screenshot.png'>",
        "Anki 2.1.6 screenshot (<a href='https://en.wikipedia.org/wiki/Anki_(software)'>https://en.wikipedia.org/wiki/Anki_(software)</a>)",
    ],
}

# Store the root path for future use
root = Path(f"{__file__}/../..").resolve()

semver_regex = re.compile(
    r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
)

# Get latest version release number
try:
    last_rel_ver = requests.get(
        "https://api.github.com/repos/pranavdeshai/anki-prettify/releases/latest"
    ).json()["tag_name"]
except KeyError:
    with open(
        root / "src" / "templates" / "default" / "basic" / "basic-front.html"
    ) as f:
        s = f.read()
    last_rel_ver = semver_regex.search(s).group()  # type:ignore

# Get the new version number
try:
    new_ver = sys.argv[1]
    if re.fullmatch(semver_regex, new_ver) is None:
        print(
            f"Warning: Invalid version number. Using latest release version: {last_rel_ver}"
        )
    else:
        print(f"Building with version {new_ver}")
except IndexError:
    print(
        f"Warning: New version not provided. Using latest release version: {last_rel_ver}"
    )
    new_ver = last_rel_ver  # Default to last release version if not provided

# Update version number in SCSS files
if new_ver != last_rel_ver:
    for x in root.glob("**/scss/*.scss"):
        with x.open("r+") as f:
            s = f.read()
            s = re.sub(semver_regex, new_ver, s)
            f.seek(0)
            f.write(s)
    print("Updated version in SCSS files")

# Compile SCSS to CSS
os.system(
    f"sass --no-source-map {str(root / 'src' / 'styles' / 'scss')}:{str(root / 'src' / 'styles' / 'css')}"
)
print("Compiled SCSS to CSS")

# Update genanki IDs
with open(root / "tools" / "ids.json", "r+") as ids_file:
    ids = json.load(ids_file)
    ids_file.seek(0)

    for i in root.glob("**/css/*.css"):
        theme = i.stem

        if not theme in ids:
            ids[theme] = {}
            print(f"Added new theme to IDs: {theme}")

        for j in root.glob("**/templates/default/*"):
            if j.is_dir():
                notetype = j.stem

                if notetype not in ids[theme]:
                    ids[theme][notetype] = {
                        "model_id": randrange(1 << 30, 1 << 31),
                        "deck_id": randrange(1 << 30, 1 << 31),
                        "note_id": randrange(1 << 30, 1 << 31),
                    }
                    print(f"Added new notetype to IDs: {notetype}")

    json.dump(ids, ids_file, indent=4)
    print("Updated ids.json")


# Generate deck packages
decks = {}

for t in ids:
    for n in ids[t]:
        with open(
            (root / "src" / "templates" / "default" / n / f"{n}-front.html"),
            "r+",
        ) as f1, open(
            (root / "src" / "templates" / "default" / n / f"{n}-back.html"), "r+"
        ) as f2, open(
            (root / "src" / "styles" / "css" / f"{t}.css")
        ) as f3:
            front_html = f1.read()
            back_html = f2.read()
            css = f3.read()

            # Update version number in templates
            if new_ver != last_rel_ver:
                front_html = re.sub(semver_regex, new_ver, front_html)
                back_html = re.sub(semver_regex, new_ver, back_html)

                f1.seek(0)
                f2.seek(0)

                f1.write(front_html)
                f2.write(back_html)

        if n == "basic_reverse":
            # Basic reverse requires two card templates
            templates = [
                {
                    "name": "Card 1",
                    "qfmt": front_html,
                    "afmt": back_html,
                },
                {
                    "name": "Card 2",
                    "qfmt": front_html.replace("{{edit:Front}}", "{{edit:Back}}"),
                    "afmt": back_html.replace(
                        "{{edit:Back}}", "{{edit:Front}}"
                    ).replace("{{edit:Front}}", "{{edit:Back}}", 1),
                },
            ]
        else:
            templates = [
                {
                    "name": "Card 1",
                    "qfmt": front_html,
                    "afmt": back_html,
                }
            ]

        model_fields = [
            {
                # Cloze note types have different field names
                "name": "Text" if n == "cloze" else "Front",
                "font": FONTS[t],
            },
            {
                "name": "Back Extra" if n == "cloze" else "Back",
                "font": FONTS[t],
            },
        ]

        model = genanki.Model(
            model_id=ids[t][n]["model_id"],
            name=f"prettify-{t}-{n}",
            fields=model_fields,
            templates=templates,
            css=css,
            model_type=genanki.Model.CLOZE
            if n == "cloze"
            else genanki.Model.FRONT_BACK,
        )

        deck = genanki.Deck(
            ids[t][n]["deck_id"],
            f"Prettify::{t.capitalize()}::{n.capitalize().replace('_',' ')}",
        )

        note = genanki.Note(
            guid=ids[t][n]["note_id"],
            fields=NOTE_FIELDS[n],
            model=model,
            tags=["prettify", f"prettify::{t}", f"prettify::{t}::{n}"],
        )

        deck.add_model(model)
        deck.add_note(note)

        # Note type-wise packages
        genanki.Package(deck).write_to_file(
            root / "themes" / t / "notetypes" / f"prettify-{t}-{n}.apkg"
        )

        if t not in decks:
            decks[t] = []

        decks[t].append(deck)

    # Theme-wise packages
    genanki.Package(decks[t]).write_to_file(root / "themes" / t / f"prettify-{t}.apkg")

# Master package with all the themes
genanki.Package([d for x in decks.values() for d in x]).write_to_file(
    root / "prettify.apkg"
)

print("Generated all packages successfully")

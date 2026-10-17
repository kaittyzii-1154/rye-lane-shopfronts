# Rye Lane interactive site

Open index.html or run python3 -m http.server 8000 in this folder.

## Photo replacement

Each region has a permanent photo number, 01–13. The black placeholders are assets/photo-01.svg through assets/photo-13.svg. Replace an image by putting a JPG, PNG or WebP in assets/ and changing the corresponding image path in hover-cards.json. The title and text fields control the reverse side. Current text is explicitly illustrative, not a record of observed events.

After editing hover-cards.json, run python3 source/build.py to refresh the embedded content in index.html. Source SVG files and the DOCX are read from the original project folder.

## Pages

- index.html: interactive market, one-second hover cards, title and embedded paper.
- paper.html: first chapter; the paper has eight main chapters.
- scenes.html: five other SVG scenes; scene-01.html through scene-05.html are their viewers.
- source/build.py: main page generator.
- source/camera.js: zoom and title transition.
- source/hover-cards.js: delayed photo and flip behaviour.
- source/build-paper.py: complete paper and chapter navigation.

## Photo numbers

- 01: Street bollard — assets/photo-01.svg
- 02: Canopy and supports — assets/photo-02.svg
- 03: Hanging fruit — assets/photo-03.svg
- 04: Fruit display — assets/photo-04.svg
- 05: Display racks — assets/photo-05.svg
- 06: Alley plant — assets/photo-06.svg
- 07: Upper window plant — assets/photo-07.svg
- 08: Lower window plant — assets/photo-08.svg
- 09: Right window plant — assets/photo-09.svg
- 10: Climbing plants — assets/photo-10.svg
- 11: Right and middle buildings — assets/photo-11.svg
- 12: Left wall and middle details — assets/photo-12.svg
- 13: Pavement and drain — assets/photo-13.svg


The website editor has been removed. Layout changes are maintained in source.

## Scene interactions

Street overview is featured first, followed by the fruit shop and Street study 01–03. Each scene has semantic region masks, delayed photo cards and reversible text faces. Photo IDs use O-, F-, S01-, S02- and S03- prefixes. The mappings and example stories are in scene-regions.json. Build scene pages with python3 source/build-scenes.py.

The embedded paper expands to its chapter content height and uses the outer page for scrolling, including wheel and keyboard input. The title layer appears only after the moving marks have completed their letter shapes.

## Font Studio

Open fonts.html to preview title, paper-heading and body fonts. The independent font-only tool saves choices in browser storage and exports CSS. Local file browser storage can vary by browser; previewed pages receive settings directly. Export CSS for permanent publishing. Restore default fonts removes font overrides. The plugin is source/font-settings.js; the layout editor remains disabled.

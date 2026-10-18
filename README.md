# Rye Lane interactive research website

## Local preview
Open `index.html` in a browser. The finished pages are static and require no build step to view.

## Pages
- `index.html`: interactive street drawing, project/contact panels, photo cards and embedded research paper.
- `paper.html` and `paper-02.html`–`paper-10.html`: research chapters and compatibility redirects.
- `scenes.html`: scene gallery.
- `scene-02.html`: Street overview, bounded zoom and links to the four studies.
- `scene-01.html`, `scene-03.html`, `scene-04.html`, `scene-05.html`: Street studies; photo popups are currently disabled.

## Editable sources
- `hover-cards.json`: homepage photo cards, text, addresses and links.
- `source/user-settings/regions-*.json`: scene boundaries and overview link targets.
- `source/build.py`: rebuild homepage, using the source SVG in the original MA ISD UNIT3 folder.
- `source/build-scenes.py`: rebuild scene pages from `assets/scene-*.svg` and saved boundaries.
- `source/build-paper.py`: rebuild paper pages from the source document in the original project folder.
- `source/camera.js`, `source/scene-camera.js`, `source/hover-cards.js`: camera and card interactions.
- `source/font-settings.js`: runtime font normalization; keep this to preserve the chosen heading and body fonts.
- `source/optimize_assets.py`: SVG optimization required by the generators.

Original SVG and DOCX inputs referenced by the generators remain in the original project folder; retain that folder for future rebuilds.

Photo assignments are recorded in `photo-number-map.json` and `悬停弹窗编号对照表.md`. IDs are internal to each page; visible names may replace numbers.

## Publishing
Current work is local only. Upload to GitHub only when requested. Before replacing a published folder, keep the canonical website and staging copy synchronized.

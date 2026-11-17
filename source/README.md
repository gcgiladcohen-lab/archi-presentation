# Source of the deck

Build (from `source/web`):

```
python3 data.py && python3 fixes.py && python3 build3.py
```

- `data.py` builds `slides.json` from `deck/order.json` + `v2/slides5.json` (+ `mj.json` image map).
- `fixes.py` applies every client correction on top (renumbering, wording, prices, creatives, merges). Edit here.
- `deck3_src.html` is the template: renderers, CSS, motion (GSAP), progressive reveal.
- `build3.py` injects data + Matador fonts and writes the repo-root `index.html` (served by GitHub Pages).

QC (needs `npm i` in `source/web`): `node check3.js` (overlap check, must print CLEAN),
`node shot3.js all` (screenshots to `s3/`), `node shotpdf.js all` (all steps revealed, for PDF).

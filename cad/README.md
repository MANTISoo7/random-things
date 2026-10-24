# Desk Organizer CAD

Front-opening under-shelf organizer, 53″ × 9″ × 6″.
Parametric in `src/*.py` — edit `L`, `H`, `D`, `T` and rerun.

## Build

Uses the `cadgen` plugin from
[earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad).

```bash
cd src
uvx --from cadgen==0.7.26 python organizer_D_hybrid.py
uvx --from cadgen==0.7.26 python organizer_B_tilt.py
uvx --from cadgen==0.7.26 python render_preview.py
```

Outputs: `STEP/*.step`, `STL/*.stl`, `images/*.png`.

## Open the STEP

Any CAD app opens `.step`: FreeCAD (free), Fusion 360, SolidWorks,
Onshape, CAD Viewer. STL opens in any 3D-print slicer or mesh viewer.

## Options

- **D — Hybrid.** Zones for scissors/pens, cutters+tilt-bins, four card
  slots, open stapler cubby, notebook + drawer face.
- **B — Tilt-forward bins.** Two full-length rows: flat compartments on
  top (scissors, pens, markers, cutters, stapler, notebook), tilt bins
  on bottom (bands, clips, 5 card slots, misc) with a short front lip.

Dimensions are provisional — update constants in `src/*.py` once the
desk is measured.

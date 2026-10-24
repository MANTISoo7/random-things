"""Engineering drawing for Option D hybrid organizer.

Produces a one-page A3 PDF with four views (top, front, right, iso),
overall dimensions, zone widths, and shelf heights.
"""
from pathlib import Path

import cadgen
from cadgen.eng_drawing import Sheet, eng_drawing

from organizer_D_hybrid import L, H, D, T, BZ


@eng_drawing(out="../PDF/organizer_D_hybrid_drawing.pdf")
def drawing():
    part = cadgen.read_step(
        Path(__file__).parent / "../STEP/organizer_D_hybrid.step"
    )
    sheet = Sheet(
        "A2",
        scale=0.2,
        title="DESK ORGANIZER - OPTION D (HYBRID)",
        part_number="ORG-D-001",
        material="MDF 12 mm (or 6 mm acrylic)",
        author="S. Bansal",
        revision="A",
        general_tolerance="±1 mm",
        notes=[
            "ALL DIMENSIONS IN MILLIMETRES.",
            "WALL AND DIVIDER THICKNESS 12 mm.",
            "FRONT FACE OPEN; FITS UNDER MONITOR SHELF.",
            "FINISH: SEAL EDGES, PRIME, PAINT (MDF).",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True)

    # ---- TOP VIEW: overall L and D, plus zone boundaries along the length.
    top.overall()
    # Zone boundary dimensions along X (from left end of part).
    # The part is centred on X=0, so left end is at -L/2.
    x0 = -L / 2
    y_floor = -D / 2
    y_back = D / 2
    for i, b in enumerate(BZ[1:], start=1):
        top.dim(
            (x0, y_back, 0),
            (x0 + b, y_back, 0),
            orientation="h",
        )

    # ---- FRONT VIEW: overall H, and the mid-shelf height.
    front.overall()
    # Shelf (horizontal panel at mid-height of the box).
    front.dim(
        (-L / 2, 0, -H / 2),
        (-L / 2, 0, 0),
        orientation="v",
    )

    # ---- RIGHT (end) VIEW: overall D and H (what's seen from the side).
    right.overall()
    right.dim(
        (L / 2, -D / 2, -H / 2),
        (L / 2, D / 2, -H / 2),
        orientation="h",
    )

    # Zone labels on the top view (less crowded than front view).
    zone_names = [
        "1: SCISSORS/PENS",
        "2: CUTTERS/BANDS/CLIPS",
        "3: CARDS",
        "4: STAPLER/TAPE",
        "5: NOTEBOOK/DRAWER",
    ]
    for i, name in enumerate(zone_names):
        cx = (BZ[i] + BZ[i + 1]) / 2 - L / 2
        top.note(name, (cx, 0, 0), offset=(0, 45 + 10 * (i % 2)))

    return sheet


if __name__ == "__main__":
    drawing()

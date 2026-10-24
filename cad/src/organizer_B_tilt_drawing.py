"""Engineering drawing for Option B tilt-forward-bins organizer."""
from pathlib import Path

import cadgen
from cadgen.eng_drawing import Sheet, eng_drawing

from organizer_B_tilt import L, H, D, T, IN, TOP_W, BOT_W


@eng_drawing(out="../PDF/organizer_B_tilt_drawing.pdf")
def drawing():
    part = cadgen.read_step(
        Path(__file__).parent / "../STEP/organizer_B_tilt.step"
    )
    sheet = Sheet(
        "A2",
        scale=0.2,
        title="DESK ORGANIZER - OPTION B (TILT BINS)",
        part_number="ORG-B-001",
        material="MDF 12 mm (or 6 mm acrylic)",
        author="S. Bansal",
        revision="A",
        general_tolerance="±1 mm",
        notes=[
            "ALL DIMENSIONS IN MILLIMETRES.",
            "WALL AND DIVIDER THICKNESS 12 mm.",
            "FRONT FACE OPEN; FITS UNDER MONITOR SHELF.",
            "TOP ROW: FLAT COMPARTMENTS; BOTTOM ROW: TILT BINS WITH FRONT LIP.",
        ],
    )
    top, front, right, iso = sheet.three_views(part, iso=True)

    # ---- TOP VIEW: overall L, and top-row compartment widths.
    top.overall()
    x_cursor = 0.0
    y_back = D / 2
    for w in TOP_W[:-1]:
        x_cursor += w * IN
        top.dim(
            (-L / 2, y_back, 0),
            (-L / 2 + x_cursor, y_back, 0),
            orientation="h",
        )

    # ---- FRONT VIEW: overall H, shelf height, and bottom-row (tilt-bin) widths.
    front.overall()
    front.dim(
        (-L / 2, 0, -H / 2),
        (-L / 2, 0, 0),
        orientation="v",
    )
    x_cursor = 0.0
    for w in BOT_W[:-1]:
        x_cursor += w * IN
        front.dim(
            (-L / 2, -D / 2, -H / 2),
            (-L / 2 + x_cursor, -D / 2, -H / 2),
            orientation="h",
        )

    # ---- RIGHT VIEW: depth and height.
    right.overall()
    right.dim(
        (L / 2, -D / 2, -H / 2),
        (L / 2, D / 2, -H / 2),
        orientation="h",
    )

    # Labels on top view.
    top_labels = ["SCISSORS", "PENS", "CUTTERS", "MARKERS",
                  "STAPLER+TAPE", "NOTEBOOK"]
    x_cursor = 0.0
    for i, (w, name) in enumerate(zip(TOP_W, top_labels)):
        cx = -L / 2 + x_cursor + w * IN / 2
        top.note(name, (cx, 0, 0), offset=(0, 20 + 8 * (i % 2)))
        x_cursor += w * IN

    # Labels on front view (bottom row).
    bot_labels = ["BANDS", "CLIPS", "CARDS: OURS", "PARTNER A/B",
                  "PARTNER C/D", "PARTNER E", "MISC"]
    x_cursor = 0.0
    for i, (w, name) in enumerate(zip(BOT_W, bot_labels)):
        cx = -L / 2 + x_cursor + w * IN / 2
        front.note(name, (cx, -D / 2, -H / 2), offset=(0, -14 - 6 * (i % 2)))
        x_cursor += w * IN

    return sheet


if __name__ == "__main__":
    drawing()

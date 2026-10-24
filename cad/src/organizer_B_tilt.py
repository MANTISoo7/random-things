"""Desk organizer, Option B (tilt-forward bins).

Front-opening box. Two horizontal rows:
  TOP ROW (flat compartments, items lay horizontally):
    1. Scissors   8.4"
    2. Pens       5.7"
    3. Cutters    5.0"
    4. Markers    5.0"
    5. Stapler+tape 10.5"
    6. Notebook   18.4"

  BOTTOM ROW (tilt-forward bins, back wall taller than front wall):
    1. Rubber bands        7.8"
    2. Paper clips / pins  6.7"
    3. Cards OURS          6.7"
    4. Cards Partner A/B   6.7"
    5. Cards Partner C/D   6.7"
    6. Cards Partner E     9.6"
    7. Loose misc          8.8"

Units: millimetres.
"""

from cadgen import build123d as bd
from cadgen import step, stl

IN = 25.4
L = 53 * IN
H = 9 * IN
D = 6 * IN
T = 12.0

# Row split: top row ~44% of interior height, bottom row the rest.
TOP_FRAC = 0.44

# Top-row compartment widths (inches) and bottom-row widths (inches).
TOP_W = [8.4, 5.7, 5.0, 5.0, 10.5, 18.4]   # sums to 53.0
BOT_W = [7.8, 6.7, 6.7, 6.7, 6.7, 9.6, 8.8]  # sums to 53.0

# Height of the SHORT front lip of each tilt bin (fraction of bottom row).
TILT_FRONT_FRAC = 0.35


def _carcase():
    outer = bd.Box(L, D, H)
    cavity = bd.Box(L - 2 * T, D, H - 2 * T)
    cavity = bd.Pos(0, -T, 0) * cavity
    return outer - cavity


def tilt_organizer():
    body = _carcase()
    iD = D - T
    iH = H - 2 * T
    top_h = iH * TOP_FRAC
    bot_h = iH - top_h
    # Horizontal shelf splitting top and bottom rows.
    shelf = bd.Box(L - 2 * T, iD, T)
    # Shelf top surface is at Z = -iH/2 + bot_h, centre at that - T/2.
    shelf_cz = -iH / 2 + bot_h - T / 2
    body = body + bd.Pos(0, -T / 2, shelf_cz) * shelf

    # ---- Top row vertical dividers.
    x_cursor = 0.0
    for w in TOP_W[:-1]:
        x_cursor += w * IN
        x = x_cursor - L / 2
        div = bd.Box(T, iD, top_h - T)
        # Top-row interior spans Z = shelf_top_z to iH/2 - T/2 (top wall at iH/2+T/2).
        shelf_top_z = -iH / 2 + bot_h
        div_cz = shelf_top_z + (top_h - T) / 2
        body = body + bd.Pos(x, -T / 2, div_cz) * div

    # ---- Bottom row vertical dividers (full bottom-row height).
    x_cursor = 0.0
    for w in BOT_W[:-1]:
        x_cursor += w * IN
        x = x_cursor - L / 2
        div = bd.Box(T, iD, bot_h - T)
        div_cz = -iH / 2 + (bot_h - T) / 2
        body = body + bd.Pos(x, -T / 2, div_cz) * div

    # ---- Short front lip across each bottom-row bin (tilt pocket).
    lip_h = bot_h * TILT_FRONT_FRAC
    # One continuous lip across the whole bottom row; dividers break it visually.
    lip = bd.Box(L - 2 * T, T, lip_h)
    lip_cz = -iH / 2 + lip_h / 2
    body = body + bd.Pos(0, -D / 2 + T / 2, lip_cz) * lip

    body.label = "organizer_B_tilt"
    return body


@step(out="../STEP/organizer_B_tilt.step")
@stl(out="../STL/organizer_B_tilt.stl")
def model():
    return tilt_organizer()


if __name__ == "__main__":
    model()

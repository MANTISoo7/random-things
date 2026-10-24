"""Desk organizer, Option D (hybrid).

Front-opening box that tucks under a monitor-shelf.
Zones along length (left to right):
  1. Scissors cubby (top) + pens trough (bottom)
  2. Cutters cubby (top) + two tilt bins (bottom: bands, clips)
  3. Four tilted card slots (OURS + partner A/B/C)
  4. Open cubby (stapler + tape)
  5. Notebook cubby (top) + drawer face (bottom)

Units: millimetres. All dimensions parametric at the top.
"""

from cadgen import build123d as bd
from cadgen import step, stl

IN = 25.4
L = 53 * IN          # overall length (X)
H = 9 * IN           # overall height (Z)
D = 6 * IN           # overall depth (Y). Open face is -Y.
T = 12.0             # wall / divider thickness (~1/2" MDF)

# Zone boundaries along X, from the left end, in mm.
BZ = [0.0, 10 * IN, 16 * IN, 30 * IN, 42 * IN, 53 * IN]


def _carcase():
    """Hollow outer shell, open on the front (-Y face)."""
    outer = bd.Box(L, D, H)
    cavity = bd.Box(L - 2 * T, D, H - 2 * T)
    # Shift cavity by -T in Y so it cuts through the front face and
    # leaves a back wall of thickness T.
    cavity = bd.Pos(0, -T, 0) * cavity
    return outer - cavity


def hybrid_organizer():
    body = _carcase()

    iD = D - T               # interior depth
    iH = H - 2 * T           # interior height

    # Full-height vertical dividers at interior zone boundaries.
    for b in BZ[1:-1]:
        x = b - L / 2
        div = bd.Box(T, iD, iH)
        div = bd.Pos(x, -T / 2, 0) * div
        body = body + div

    def zone_center_and_inner_w(i):
        cx = (BZ[i] + BZ[i + 1]) / 2 - L / 2
        iw = (BZ[i + 1] - BZ[i]) - T  # subtract shared divider thickness
        return cx, iw

    # Zone 1: horizontal shelf at mid-height (scissors on top, pens on bottom).
    cx, iw = zone_center_and_inner_w(0)
    shelf = bd.Box(iw, iD, T)
    body = body + bd.Pos(cx, -T / 2, 0) * shelf

    # Zone 2: shelf + a vertical sub-divider in the bottom for 2 tilt bins.
    cx, iw = zone_center_and_inner_w(1)
    shelf2 = bd.Box(iw, iD, T)
    body = body + bd.Pos(cx, -T / 2, 0) * shelf2
    sub2 = bd.Box(T, iD, iH / 2 - T / 2)
    body = body + bd.Pos(cx, -T / 2, -iH / 4 - T / 4) * sub2
    # Short front lip across the two tilt bins (so stuff doesn't fall out).
    lip_h = iH / 2 * 0.5
    lip2 = bd.Box(iw, T, lip_h)
    body = body + bd.Pos(
        cx, -D / 2 + T / 2, -iH / 2 + lip_h / 2
    ) * lip2

    # Zone 3: three interior tilt-slot dividers plus front short lip.
    z3_w = BZ[3] - BZ[2]
    sub_w3 = z3_w / 4
    for i in range(1, 4):
        x_div = BZ[2] + i * sub_w3 - L / 2
        d3 = bd.Box(T, iD, iH)
        body = body + bd.Pos(x_div, -T / 2, 0) * d3
    cx3, iw3 = zone_center_and_inner_w(2)
    lip3_h = iH * 0.35
    lip3 = bd.Box(iw3, T, lip3_h)
    body = body + bd.Pos(
        cx3, -D / 2 + T / 2, -iH / 2 + lip3_h / 2
    ) * lip3

    # Zone 4: open cubby. Nothing to add.

    # Zone 5: horizontal shelf (notebook on top, drawer below).
    cx5, iw5 = zone_center_and_inner_w(4)
    shelf5 = bd.Box(iw5, iD, T)
    body = body + bd.Pos(cx5, -T / 2, 0) * shelf5
    # Drawer face: an inset panel sitting slightly proud of the front.
    df = bd.Box(iw5 - 6, T, iH / 2 - 6)
    body = body + bd.Pos(
        cx5, -D / 2 - T / 2, -iH / 4 - T / 2
    ) * df

    body.label = "organizer_D_hybrid"
    return body


@step(out="../STEP/organizer_D_hybrid.step")
@stl(out="../STL/organizer_D_hybrid.stl")
def model():
    return hybrid_organizer()


if __name__ == "__main__":
    model()

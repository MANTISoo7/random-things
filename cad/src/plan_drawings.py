"""Color-coded presentation drawings for both organizer options.

Produces one landscape A3 PDF per design with:
  - Big front view (color-coded zones, labeled)
  - Top view (color-coded, with dimensions)
  - Isometric wireframe (from STL)
  - Legend keyed to zone colors
  - Title block, notes, dimensions
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

IN = 25.4
L = 53 * IN
H = 9 * IN
D = 6 * IN
T = 12.0

# --- A3 landscape sheet in inches (matplotlib figsize).
SHEET_W, SHEET_H = 16.54, 11.69

# Soft, print-friendly palette.
PALETTE_D = {
    "z1": "#CB7B82",   # scissors / pens
    "z2": "#D4A373",   # cutters / bands / clips
    "z3": "#7FA989",   # cards
    "z4": "#6B98B5",   # stapler / tape
    "z5": "#9381A6",   # notebook / drawer
    "ink": "#2A2520",
    "wood": "#F0E6D2",
    "wood_edge": "#9A7E55",
    "muted": "#7A736A",
    "paper": "#FAF7F0",
    "panel": "#FFFFFF",
    "rule": "#D9D1C3",
}

PALETTE_B_TOP = ["#CB7B82", "#D4A373", "#C09A4E", "#B98060",
                 "#6B98B5", "#9381A6"]
PALETTE_B_BOT = ["#D4A373", "#C9A86B", "#7FA989", "#6FA38C",
                 "#5F9D8F", "#4F978F", "#9381A6"]

# ---------- Common sheet frame ----------
def _sheet(title, subtitle, part_no, material):
    fig = plt.figure(figsize=(SHEET_W, SHEET_H),
                     facecolor=PALETTE_D["paper"])
    # Outer frame
    frame = fig.add_axes([0.015, 0.015, 0.97, 0.97], frameon=False)
    frame.set_xlim(0, 1)
    frame.set_ylim(0, 1)
    frame.axis("off")
    frame.add_patch(Rectangle((0, 0), 1, 1, fill=False,
                              edgecolor=PALETTE_D["ink"], lw=1.4))
    frame.add_patch(Rectangle((0.005, 0.005), 0.99, 0.99, fill=False,
                              edgecolor=PALETTE_D["ink"], lw=0.6))

    # Title bar
    frame.text(0.02, 0.965, title, fontsize=20, fontweight="bold",
               color=PALETTE_D["ink"], va="top")
    frame.text(0.02, 0.935, subtitle, fontsize=11,
               color=PALETTE_D["muted"], va="top", style="italic")

    # Title block (bottom-right)
    tb_x, tb_y, tb_w, tb_h = 0.70, 0.015, 0.285, 0.09
    frame.add_patch(Rectangle((tb_x, tb_y), tb_w, tb_h, fill=True,
                              facecolor=PALETTE_D["panel"],
                              edgecolor=PALETTE_D["ink"], lw=0.8))
    rows = [
        ("PART NO.", part_no),
        ("MATERIAL", material),
        ("UNITS", "mm (inches in parentheses)"),
        ("SCALE", "varies per view (not to scale)"),
        ("DRAWN BY", "S. BANSAL"),
    ]
    for i, (k, v) in enumerate(rows):
        y = tb_y + tb_h - (i + 1) * (tb_h / len(rows)) + 0.004
        frame.text(tb_x + 0.008, y, k, fontsize=7, color=PALETTE_D["muted"],
                   fontweight="bold", va="bottom")
        frame.text(tb_x + 0.08, y, v, fontsize=9, color=PALETTE_D["ink"],
                   va="bottom")
    return fig, frame


def _add_dim_bar(ax, x0, x1, y, label, color=PALETTE_D["ink"],
                 lw=0.8, tick=4):
    ax.plot([x0, x1], [y, y], color=color, lw=lw)
    ax.plot([x0, x0], [y - tick, y + tick], color=color, lw=lw)
    ax.plot([x1, x1], [y - tick, y + tick], color=color, lw=lw)
    ax.text((x0 + x1) / 2, y + 8, label, ha="center", va="bottom",
            fontsize=8, color=color)


def _add_vdim_bar(ax, y0, y1, x, label, color=PALETTE_D["ink"],
                  lw=0.8, tick=4):
    ax.plot([x, x], [y0, y1], color=color, lw=lw)
    ax.plot([x - tick, x + tick], [y0, y0], color=color, lw=lw)
    ax.plot([x - tick, x + tick], [y1, y1], color=color, lw=lw)
    ax.text(x + 8, (y0 + y1) / 2, label, ha="left", va="center",
            fontsize=8, color=color, rotation=90)


# ---------- Design D (hybrid) ----------
def draw_D():
    BZ = [0, 10 * IN, 16 * IN, 30 * IN, 42 * IN, 53 * IN]
    iH = H - 2 * T

    fig, frame = _sheet(
        "DESK ORGANIZER  —  OPTION D  (hybrid)",
        "53″ × 9″ × 6″ · open front · fits under monitor shelf · 5 zones",
        "ORG-D-001", "12 mm MDF  or  6 mm acrylic")

    # ---------- FRONT VIEW (top of page) ----------
    fv = fig.add_axes([0.03, 0.52, 0.75, 0.36])
    fv.set_aspect("equal")
    fv.axis("off")
    fv.set_title("FRONT VIEW  (looking at the open face)",
                 fontsize=11, color=PALETTE_D["muted"], loc="left",
                 pad=10)

    # Carcase outline (external rectangle)
    fv.add_patch(Rectangle((0, 0), L, H, facecolor=PALETTE_D["wood"],
                           edgecolor=PALETTE_D["wood_edge"], lw=1.6))
    # Inner cavity bounds (interior top/bottom lines)
    fv.plot([T, L - T], [T, T], color=PALETTE_D["wood_edge"], lw=0.6)
    fv.plot([T, L - T], [H - T, H - T], color=PALETTE_D["wood_edge"], lw=0.6)

    def _z_rect(x0, x1, z0, z1, color, label, sub=None):
        fv.add_patch(Rectangle(
            (x0, z0), x1 - x0, z1 - z0,
            facecolor=color, edgecolor=PALETTE_D["ink"],
            lw=0.9, alpha=0.75))
        fv.text((x0 + x1) / 2, (z0 + z1) / 2 + 4, label,
                ha="center", va="center", fontsize=9,
                color=PALETTE_D["ink"], fontweight="bold")
        if sub:
            fv.text((x0 + x1) / 2, (z0 + z1) / 2 - 10, sub,
                    ha="center", va="center", fontsize=7.5,
                    color=PALETTE_D["ink"], style="italic")

    # Zone 1: scissors (top), pens (bottom)
    _z_rect(T, BZ[1], T + iH / 2, H - T, PALETTE_D["z1"], "SCISSORS")
    _z_rect(T, BZ[1], T, T + iH / 2, PALETTE_D["z1"], "PENS",
            "(lay horizontal)")
    fv.plot([T, BZ[1]], [T + iH / 2, T + iH / 2],
            color=PALETTE_D["ink"], lw=0.9)

    # Zone 2: cutters (top), bands + clips (bottom, with lip)
    _z_rect(BZ[1], BZ[2], T + iH / 2, H - T, PALETTE_D["z2"], "CUTTERS")
    sub_mid = (BZ[1] + BZ[2]) / 2
    _z_rect(BZ[1], sub_mid, T, T + iH / 2, PALETTE_D["z2"], "BANDS")
    _z_rect(sub_mid, BZ[2], T, T + iH / 2, PALETTE_D["z2"], "CLIPS")
    fv.plot([BZ[1], BZ[2]], [T + iH / 2, T + iH / 2],
            color=PALETTE_D["ink"], lw=0.9)
    # Short lip across bottom (visual: dashed outline on front edge, suggests short wall)
    lip2_h = iH / 2 * 0.5
    fv.add_patch(Rectangle((BZ[1], T), BZ[2] - BZ[1], lip2_h,
                           facecolor="none",
                           edgecolor=PALETTE_D["ink"], lw=1.4,
                           linestyle=(0, (3, 2))))

    # Zone 3: cards (4 slots)
    sub_w3 = (BZ[3] - BZ[2]) / 4
    card_labels = ["OURS", "PARTNER A", "PARTNER B", "PARTNER C+"]
    for i, lbl in enumerate(card_labels):
        x0 = BZ[2] + i * sub_w3
        x1 = BZ[2] + (i + 1) * sub_w3
        _z_rect(x0, x1, T, H - T, PALETTE_D["z3"], lbl)
    lip3_h = iH * 0.35
    fv.add_patch(Rectangle((BZ[2], T), BZ[3] - BZ[2], lip3_h,
                           facecolor="none",
                           edgecolor=PALETTE_D["ink"], lw=1.4,
                           linestyle=(0, (3, 2))))

    # Zone 4: stapler + tape (open)
    _z_rect(BZ[3], BZ[4], T, H - T, PALETTE_D["z4"],
            "STAPLER  +  TAPE", "open cubby, full height")

    # Zone 5: notebook (top), drawer (bottom)
    _z_rect(BZ[4], BZ[5] - T, T + iH / 2, H - T, PALETTE_D["z5"],
            "NOTEBOOK")
    _z_rect(BZ[4], BZ[5] - T, T, T + iH / 2, PALETTE_D["z5"],
            "DRAWER", "(pull-out)")
    fv.plot([BZ[4], BZ[5] - T], [T + iH / 2, T + iH / 2],
            color=PALETTE_D["ink"], lw=0.9)
    # Drawer-face suggestion: small handle hole
    df_y = (T + iH / 4 + T / 2)
    fv.add_patch(plt.Circle(((BZ[4] + BZ[5] - T) / 2, df_y - 6),
                            3.5, facecolor="none",
                            edgecolor=PALETTE_D["ink"], lw=0.9))

    # Divider lines (vertical) between zones for clarity
    for b in BZ[1:-1]:
        fv.plot([b, b], [T, H - T], color=PALETTE_D["ink"], lw=1.0)

    # Dimensions on the front view
    _add_dim_bar(fv, 0, L, H + 25, f"{L:.0f} mm  ({L/IN:.0f}\")",
                 color=PALETTE_D["ink"])
    _add_vdim_bar(fv, 0, H, -40, f"{H:.0f} mm  ({H/IN:.0f}\")",
                  color=PALETTE_D["ink"])

    # Zone-width dimensions below
    for i in range(5):
        _add_dim_bar(fv, BZ[i], BZ[i + 1], -22,
                     f"{(BZ[i+1]-BZ[i]):.0f}  ({(BZ[i+1]-BZ[i])/IN:.1f}\")",
                     color=PALETTE_D["muted"], lw=0.6, tick=3)

    fv.set_xlim(-80, L + 60)
    fv.set_ylim(-55, H + 55)

    # ---------- TOP VIEW ----------
    tv = fig.add_axes([0.03, 0.26, 0.75, 0.17])
    tv.set_aspect("equal")
    tv.axis("off")
    tv.set_title("TOP VIEW  (looking down into the open front)",
                 fontsize=11, color=PALETTE_D["muted"], loc="left",
                 pad=8)
    # Carcase outline from above
    tv.add_patch(Rectangle((0, 0), L, D, facecolor=PALETTE_D["wood"],
                           edgecolor=PALETTE_D["wood_edge"], lw=1.6))
    # Back wall line
    tv.plot([T, L - T], [D - T, D - T],
            color=PALETTE_D["wood_edge"], lw=0.6)
    # Front edge of box
    tv.plot([T, L - T], [T, T],
            color=PALETTE_D["wood_edge"], lw=0.6)
    # Zone fills (lighter, since cards show from above as 4 slots etc.)
    def _tv_fill(x0, x1, color, label):
        tv.add_patch(Rectangle((x0, T), x1 - x0, D - 2 * T,
                               facecolor=color, alpha=0.5,
                               edgecolor=PALETTE_D["ink"], lw=0.6))
        tv.text((x0 + x1) / 2, D / 2, label, ha="center", va="center",
                fontsize=9, color=PALETTE_D["ink"], fontweight="bold")

    _tv_fill(T, BZ[1], PALETTE_D["z1"], "1 · PENS / SCISSORS")
    _tv_fill(BZ[1], BZ[2], PALETTE_D["z2"], "2 · CUTTERS / BANDS·CLIPS")
    _tv_fill(BZ[2], BZ[3], PALETTE_D["z3"], "3 · CARDS")
    _tv_fill(BZ[3], BZ[4], PALETTE_D["z4"], "4 · STAPLER + TAPE")
    _tv_fill(BZ[4], BZ[5] - T, PALETTE_D["z5"], "5 · NOTEBOOK / DRAWER")

    # Depth dimension
    _add_vdim_bar(tv, 0, D, -40, f"{D:.0f} mm  ({D/IN:.0f}\")",
                  color=PALETTE_D["ink"])

    tv.set_xlim(-80, L + 60)
    tv.set_ylim(-15, D + 25)

    # ---------- ISOMETRIC (hand-drawn, color-coded) ----------
    iso = fig.add_axes([0.80, 0.52, 0.18, 0.36])
    iso.set_aspect("equal")
    iso.axis("off")
    iso.set_title("ISOMETRIC", fontsize=10,
                  color=PALETTE_D["muted"], loc="left", pad=4)
    # Simple oblique projection of the carcase. We don't need to be
    # precise; the point is to communicate "this is a long shallow box".
    sx, sy = 1.0, 0.5
    def _iso(x, y, z):
        return (x + y * sx * 0.5, z + y * sy * 0.5)
    def _poly(pts, color, alpha=0.9, ec=PALETTE_D["ink"]):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        iso.add_patch(Polygon(list(zip(xs, ys)), facecolor=color,
                              edgecolor=ec, lw=0.8, alpha=alpha))

    # Front face (shows all zones)
    front_pts = [_iso(0, 0, 0), _iso(L, 0, 0), _iso(L, 0, H), _iso(0, 0, H)]
    _poly(front_pts, PALETTE_D["wood"], 0.3,
          ec=PALETTE_D["wood_edge"])
    # Front edges / top & right faces
    top_pts = [_iso(0, 0, H), _iso(L, 0, H), _iso(L, D, H), _iso(0, D, H)]
    _poly(top_pts, PALETTE_D["wood_edge"], 0.9)
    right_pts = [_iso(L, 0, 0), _iso(L, D, 0), _iso(L, D, H), _iso(L, 0, H)]
    _poly(right_pts, PALETTE_D["wood"], 0.9)
    # Color strips on front face per zone
    for i in range(5):
        c = [PALETTE_D["z1"], PALETTE_D["z2"], PALETTE_D["z3"],
             PALETTE_D["z4"], PALETTE_D["z5"]][i]
        pts = [_iso(BZ[i], 0, T), _iso(BZ[i + 1], 0, T),
               _iso(BZ[i + 1], 0, H - T), _iso(BZ[i], 0, H - T)]
        _poly(pts, c, 0.75)

    all_x = [p[0] for p in (front_pts + top_pts + right_pts)]
    all_y = [p[1] for p in (front_pts + top_pts + right_pts)]
    pad = 20
    iso.set_xlim(min(all_x) - pad, max(all_x) + pad)
    iso.set_ylim(min(all_y) - pad, max(all_y) + pad)

    # ---------- LEGEND / CONTENTS KEY ----------
    lg = fig.add_axes([0.80, 0.14, 0.18, 0.33])
    lg.axis("off")
    lg.set_xlim(0, 1)
    lg.set_ylim(0, 1)
    lg.text(0.02, 0.97, "ZONE KEY", fontsize=11, fontweight="bold",
            color=PALETTE_D["ink"], va="top")
    entries = [
        ("1", PALETTE_D["z1"], "Scissors (shelf)\nPens (trough)"),
        ("2", PALETTE_D["z2"], "Cutters (shelf)\nBands + clips (2 tilt bins)"),
        ("3", PALETTE_D["z3"], "Cards: ours\n+ 3 partner slots"),
        ("4", PALETTE_D["z4"], "Stapler + tape\n(open cubby)"),
        ("5", PALETTE_D["z5"], "Notebook (shelf)\nDrawer (bottom)"),
    ]
    for i, (num, color, text) in enumerate(entries):
        y = 0.88 - i * 0.17
        lg.add_patch(FancyBboxPatch((0.02, y - 0.08), 0.11, 0.11,
                                    boxstyle="round,pad=0.005",
                                    facecolor=color,
                                    edgecolor=PALETTE_D["ink"], lw=0.8))
        lg.text(0.075, y - 0.025, num, ha="center", va="center",
                fontsize=14, fontweight="bold", color=PALETTE_D["ink"])
        lg.text(0.18, y - 0.025, text, va="center", fontsize=8,
                color=PALETTE_D["ink"])

    # ---------- NOTES (bottom-left) ----------
    nt = fig.add_axes([0.03, 0.02, 0.65, 0.20])
    nt.axis("off")
    nt.set_xlim(0, 1)
    nt.set_ylim(0, 1)
    nt.text(0.0, 0.95, "NOTES", fontsize=11, fontweight="bold",
            color=PALETTE_D["ink"], va="top")
    notes = [
        "1.  All interior dividers and shelves are 12 mm thick (same as walls).",
        "2.  Front face is fully open — the box tucks under the monitor shelf, so the only access is from the front.",
        "3.  'Short front lip' (dashed) means a half-height wall across the front; keeps bands, clips and cards from falling out while still letting you see in from above.",
        "4.  Zone 5 drawer is a shallow pull-out behind the drawer face; add drawer runners when building.",
        "5.  Dimensions are provisional — refresh when the shelf clearance and desk width are measured.",
        "6.  For acrylic, drop wall thickness to 6 mm and use slot-and-tab joinery with Weld-On 4 cement.",
    ]
    for i, n in enumerate(notes):
        nt.text(0.0, 0.82 - i * 0.13, n, fontsize=8.5,
                color=PALETTE_D["ink"], va="top", wrap=True)

    out = Path(__file__).parent.parent / "PDF" / "organizer_D_hybrid_plan.pdf"
    fig.savefig(out, dpi=200, facecolor=PALETTE_D["paper"])
    plt.close(fig)
    print(f"wrote {out}")


# ---------- Design B (tilt bins) ----------
def draw_B():
    TOP_W = [8.4, 5.7, 5.0, 5.0, 10.5, 18.4]
    BOT_W = [7.8, 6.7, 6.7, 6.7, 6.7, 9.6, 8.8]
    iH = H - 2 * T
    top_h = iH * 0.44
    bot_h = iH - top_h

    fig, frame = _sheet(
        "DESK ORGANIZER  —  OPTION B  (tilt-forward bins)",
        "53″ × 9″ × 6″ · open front · fits under monitor shelf · top row flat / bottom row tilt",
        "ORG-B-001", "12 mm MDF  or  6 mm acrylic")

    # ---------- FRONT VIEW ----------
    fv = fig.add_axes([0.03, 0.52, 0.75, 0.36])
    fv.set_aspect("equal")
    fv.axis("off")
    fv.set_title("FRONT VIEW  (looking at the open face)",
                 fontsize=11, color=PALETTE_D["muted"], loc="left",
                 pad=10)

    fv.add_patch(Rectangle((0, 0), L, H, facecolor=PALETTE_D["wood"],
                           edgecolor=PALETTE_D["wood_edge"], lw=1.6))

    shelf_z = T + bot_h  # top of bottom row (= bottom of shelf)
    fv.plot([T, L - T], [shelf_z, shelf_z], color=PALETTE_D["ink"], lw=1.0)

    # Top row compartments
    top_labels = ["SCISSORS", "PENS", "CUTTERS", "MARKERS",
                  "STAPLER + TAPE", "NOTEBOOK"]
    x_cur = T
    for i, (w_in, lbl) in enumerate(zip(TOP_W, top_labels)):
        w = w_in * IN
        if i == 0:
            w -= T  # first compartment loses left wall
        if i == len(TOP_W) - 1:
            w -= T  # last loses right wall
        x1 = x_cur + w
        fv.add_patch(Rectangle(
            (x_cur, shelf_z + T), w, H - T - (shelf_z + T),
            facecolor=PALETTE_B_TOP[i], alpha=0.75,
            edgecolor=PALETTE_D["ink"], lw=0.9))
        fv.text((x_cur + x1) / 2, shelf_z + T + (H - T - shelf_z - T) / 2,
                lbl, ha="center", va="center",
                fontsize=8, color=PALETTE_D["ink"], fontweight="bold")
        x_cur = x1 + T

    # Bottom row (tilt bins)
    bot_labels = ["BANDS", "CLIPS", "CARDS: OURS",
                  "PARTNER A/B", "PARTNER C/D", "PARTNER E", "MISC"]
    x_cur = T
    lip_h = bot_h * 0.35
    for i, (w_in, lbl) in enumerate(zip(BOT_W, bot_labels)):
        w = w_in * IN
        if i == 0:
            w -= T
        if i == len(BOT_W) - 1:
            w -= T
        x1 = x_cur + w
        fv.add_patch(Rectangle(
            (x_cur, T), w, bot_h - T,
            facecolor=PALETTE_B_BOT[i], alpha=0.75,
            edgecolor=PALETTE_D["ink"], lw=0.9))
        fv.text((x_cur + x1) / 2, T + bot_h / 2 + 2, lbl,
                ha="center", va="center", fontsize=8,
                color=PALETTE_D["ink"], fontweight="bold")
        x_cur = x1 + T
    # Single lip across the full bottom row
    fv.add_patch(Rectangle((T, T), L - 2 * T, lip_h,
                           facecolor="none",
                           edgecolor=PALETTE_D["ink"], lw=1.4,
                           linestyle=(0, (3, 2))))

    # Overall dimensions
    _add_dim_bar(fv, 0, L, H + 25, f"{L:.0f} mm  ({L/IN:.0f}\")",
                 color=PALETTE_D["ink"])
    _add_vdim_bar(fv, 0, H, -40, f"{H:.0f} mm  ({H/IN:.0f}\")",
                  color=PALETTE_D["ink"])

    fv.set_xlim(-80, L + 90)
    fv.set_ylim(-30, H + 50)

    # ---------- TOP VIEW ----------
    tv = fig.add_axes([0.03, 0.26, 0.75, 0.17])
    tv.set_aspect("equal")
    tv.axis("off")
    tv.set_title("TOP VIEW  (looking down)",
                 fontsize=11, color=PALETTE_D["muted"], loc="left",
                 pad=8)
    tv.add_patch(Rectangle((0, 0), L, D, facecolor=PALETTE_D["wood"],
                           edgecolor=PALETTE_D["wood_edge"], lw=1.6))
    # Draw top-row compartment outlines from above (each compartment visible)
    x_cur = T
    for i, w_in in enumerate(TOP_W):
        w = w_in * IN
        if i == 0:
            w -= T
        if i == len(TOP_W) - 1:
            w -= T
        tv.add_patch(Rectangle(
            (x_cur, T), w, D - 2 * T,
            facecolor=PALETTE_B_TOP[i], alpha=0.5,
            edgecolor=PALETTE_D["ink"], lw=0.6))
        x_cur += w + T
    _add_vdim_bar(tv, 0, D, -40, f"{D:.0f} mm  ({D/IN:.0f}\")",
                  color=PALETTE_D["ink"])
    tv.set_xlim(-80, L + 90)
    tv.set_ylim(-15, D + 25)

    # ---------- ISO ----------
    iso = fig.add_axes([0.80, 0.52, 0.18, 0.36])
    iso.set_aspect("equal")
    iso.axis("off")
    iso.set_title("ISOMETRIC", fontsize=10,
                  color=PALETTE_D["muted"], loc="left", pad=4)
    sx, sy = 1.0, 0.5
    def _iso(x, y, z):
        return (x + y * sx * 0.5, z + y * sy * 0.5)
    def _poly(pts, color, alpha=0.9, ec=PALETTE_D["ink"]):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        iso.add_patch(Polygon(list(zip(xs, ys)), facecolor=color,
                              edgecolor=ec, lw=0.8, alpha=alpha))
    front_pts = [_iso(0, 0, 0), _iso(L, 0, 0), _iso(L, 0, H), _iso(0, 0, H)]
    _poly(front_pts, PALETTE_D["wood"], 0.3,
          ec=PALETTE_D["wood_edge"])
    top_pts = [_iso(0, 0, H), _iso(L, 0, H), _iso(L, D, H), _iso(0, D, H)]
    _poly(top_pts, PALETTE_D["wood_edge"], 0.9)
    right_pts = [_iso(L, 0, 0), _iso(L, D, 0), _iso(L, D, H), _iso(L, 0, H)]
    _poly(right_pts, PALETTE_D["wood"], 0.9)
    # Color strips: top row + bottom row
    x_cur = T
    shelf_z_iso = T + bot_h
    for i, w_in in enumerate(TOP_W):
        w = w_in * IN
        if i == 0: w -= T
        if i == len(TOP_W) - 1: w -= T
        pts = [_iso(x_cur, 0, shelf_z_iso + T),
               _iso(x_cur + w, 0, shelf_z_iso + T),
               _iso(x_cur + w, 0, H - T),
               _iso(x_cur, 0, H - T)]
        _poly(pts, PALETTE_B_TOP[i], 0.8)
        x_cur += w + T
    x_cur = T
    for i, w_in in enumerate(BOT_W):
        w = w_in * IN
        if i == 0: w -= T
        if i == len(BOT_W) - 1: w -= T
        pts = [_iso(x_cur, 0, T + lip_h),
               _iso(x_cur + w, 0, T + lip_h),
               _iso(x_cur + w, 0, shelf_z_iso),
               _iso(x_cur, 0, shelf_z_iso)]
        _poly(pts, PALETTE_B_BOT[i], 0.8)
        x_cur += w + T

    all_x = [p[0] for p in (front_pts + top_pts + right_pts)]
    all_y = [p[1] for p in (front_pts + top_pts + right_pts)]
    pad = 20
    iso.set_xlim(min(all_x) - pad, max(all_x) + pad)
    iso.set_ylim(min(all_y) - pad, max(all_y) + pad)

    # ---------- LEGEND ----------
    lg = fig.add_axes([0.80, 0.08, 0.18, 0.39])
    lg.axis("off")
    lg.set_xlim(0, 1)
    lg.set_ylim(0, 1)
    lg.text(0.02, 0.98, "KEY", fontsize=11, fontweight="bold",
            color=PALETTE_D["ink"], va="top")
    lg.text(0.02, 0.945, "Top row (flat compartments)",
            fontsize=8, color=PALETTE_D["muted"], va="top",
            style="italic")
    for i, (lbl, col) in enumerate(zip(top_labels, PALETTE_B_TOP)):
        y = 0.90 - i * 0.055
        lg.add_patch(Rectangle((0.03, y - 0.025), 0.08, 0.035,
                               facecolor=col, alpha=0.8,
                               edgecolor=PALETTE_D["ink"], lw=0.6))
        lg.text(0.14, y - 0.005, lbl, fontsize=7.5,
                color=PALETTE_D["ink"], va="center")
    lg.text(0.02, 0.52, "Bottom row (tilt bins)",
            fontsize=8, color=PALETTE_D["muted"], va="top",
            style="italic")
    for i, (lbl, col) in enumerate(zip(bot_labels, PALETTE_B_BOT)):
        y = 0.47 - i * 0.055
        lg.add_patch(Rectangle((0.03, y - 0.025), 0.08, 0.035,
                               facecolor=col, alpha=0.8,
                               edgecolor=PALETTE_D["ink"], lw=0.6))
        lg.text(0.14, y - 0.005, lbl, fontsize=7.5,
                color=PALETTE_D["ink"], va="center")

    # ---------- NOTES ----------
    nt = fig.add_axes([0.03, 0.02, 0.65, 0.20])
    nt.axis("off")
    nt.set_xlim(0, 1)
    nt.set_ylim(0, 1)
    nt.text(0.0, 0.95, "NOTES", fontsize=11, fontweight="bold",
            color=PALETTE_D["ink"], va="top")
    notes = [
        "1.  All interior dividers and shelves are 12 mm thick.",
        "2.  Front face fully open — fits under monitor shelf, front access only.",
        "3.  Bottom row is a continuous short-front-lip tray that visually reads as 7 tilt bins; the lip (dashed in front view) is ~1\" tall and runs the full length.",
        "4.  Top row stores items horizontally (laid flat): scissors, pens, markers, cutters, stapler, notebook. Easy swipe-to-grab.",
        "5.  Dimensions are provisional — refresh when the shelf clearance and desk width are measured.",
        "6.  For acrylic, drop wall thickness to 6 mm and use slot-and-tab joinery with Weld-On 4 cement.",
    ]
    for i, n in enumerate(notes):
        nt.text(0.0, 0.82 - i * 0.13, n, fontsize=8.5,
                color=PALETTE_D["ink"], va="top")

    out = Path(__file__).parent.parent / "PDF" / "organizer_B_tilt_plan.pdf"
    fig.savefig(out, dpi=200, facecolor=PALETTE_D["paper"])
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    draw_D()
    draw_B()

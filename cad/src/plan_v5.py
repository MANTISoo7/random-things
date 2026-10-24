"""Shop counter organizer v5 - varied compartment shapes.

Items are not labelled per-zone anymore - you fill each shape however
you want. The design decision is now the SHAPE and MECHANISM of each
zone, not the specific items.

Zones (left to right):
  1. Recessed card slot        (full height, 3 horizontal slots, scalloped front)
  2. Cross-divided tray         (upper tier, + divider = 4 sub-pockets)
  3. Stapler stack              (upper drawer for pins, lower OPEN bay for staplers)
  4. Pen-over-coin stack        (upper OPEN shelf, lower drawer for coins)
  5. Mixing tray                (lower open with light partitions, upper OPEN)
  6. Damper floor zone          (full open column, damper sits on the floor)
  7. Label pull-out             (small upper tray)
  8. Calculator stack           (full height, 3 stacked rectangles)
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Rectangle, Polygon, FancyBboxPatch,
                                 Circle, Arc, PathPatch)
from matplotlib.path import Path as MplPath

IN = 25.4
L = 53 * IN
H = 5 * IN
D = 6 * IN
T = 10.0
SHEET_W, SHEET_H = 16.54, 11.69

PAPER = "#FAF7F0"
INK = "#2A2520"
MUTED = "#7A736A"
WOOD = "#F0E6D2"
WOOD_EDGE = "#9A7E55"
PANEL = "#FFFFFF"
LOOSE = "#EADFC5"
DRAWER_FACE = "#C9D7E3"
DRAWER_EDGE = "#6B8AA0"

CARDS_C   = "#7FA989"
CROSS_C   = "#CB7B82"
STAPLER_C = "#AF8359"
PENS_C    = "#D4A373"
MIX_C     = "#C9A86B"
DAMP_C    = "#9381A6"
LABEL_C   = "#8E90B9"
CALCS_C   = "#6B98B5"

# (width_in, type, color, label)
ZONES = [
    (4,  "cards-recessed", CARDS_C,   "VISITING CARDS\n3 recessed slots"),
    (8,  "cross-tray",     CROSS_C,   "CROSS TRAY\n4 sub-pockets"),
    (7,  "stapler-stack",  STAPLER_C, "upper: PIN DRAWER\nlower: open bay (staplers)"),
    (10, "pen-coin-stack", PENS_C,    "upper: open shelf (pens)\nlower: COIN DRAWER"),
    (8,  "mix-tray",       MIX_C,     "MIXING TRAY\nloose stuff, soft partitions"),
    (4,  "floor-damper",   DAMP_C,    "DAMPER\nsits on the floor"),
    (4,  "label-tray",     LABEL_C,   "LABEL PULL-OUT"),
    (8,  "calc-stack",     CALCS_C,   "CALCULATORS\n(stacked ×3)"),
]


def _sheet():
    fig = plt.figure(figsize=(SHEET_W, SHEET_H), facecolor=PAPER)
    frame = fig.add_axes([0.015, 0.015, 0.97, 0.97], frameon=False)
    frame.set_xlim(0, 1); frame.set_ylim(0, 1); frame.axis("off")
    frame.add_patch(Rectangle((0, 0), 1, 1, fill=False,
                              edgecolor=INK, lw=1.4))
    frame.add_patch(Rectangle((0.005, 0.005), 0.99, 0.99, fill=False,
                              edgecolor=INK, lw=0.6))
    frame.text(0.02, 0.965,
               "SHOP COUNTER ORGANIZER  —  v5  (varied shapes)",
               fontsize=19, fontweight="bold", color=INK, va="top")
    frame.text(0.02, 0.935,
               '53" × 5" × 6"  ·  '
               'shapes, not items  ·  '
               'cross tray, recessed cards, drawers, floor zone  ·  '
               'widths provisional',
               fontsize=10.5, color=MUTED, va="top", style="italic")
    tb_x, tb_y, tb_w, tb_h = 0.70, 0.015, 0.285, 0.09
    frame.add_patch(Rectangle((tb_x, tb_y), tb_w, tb_h, fill=True,
                              facecolor=PANEL, edgecolor=INK, lw=0.8))
    rows = [
        ("PART NO.", "ORG-D-005"),
        ("MATERIAL", "12 mm MDF carcase; 6 mm trays/drawers"),
        ("UNITS",    "mm  (inches in parentheses)"),
        ("SCALE",    "not to scale  ·  shape over size"),
        ("DRAWN BY", "S. BANSAL"),
    ]
    for i, (k, v) in enumerate(rows):
        y = tb_y + tb_h - (i + 1) * (tb_h / len(rows)) + 0.004
        frame.text(tb_x + 0.008, y, k, fontsize=7, color=MUTED,
                   fontweight="bold", va="bottom")
        frame.text(tb_x + 0.08, y, v, fontsize=9, color=INK, va="bottom")
    return fig, frame


def _dim_h(ax, x0, x1, y, label, color=INK, lw=0.8, tick=4, fs=8):
    ax.plot([x0, x1], [y, y], color=color, lw=lw)
    ax.plot([x0, x0], [y - tick, y + tick], color=color, lw=lw)
    ax.plot([x1, x1], [y - tick, y + tick], color=color, lw=lw)
    ax.text((x0 + x1) / 2, y + 6, label, ha="center", va="bottom",
            fontsize=fs, color=color)


def _dim_v(ax, y0, y1, x, label, color=INK, lw=0.8, tick=4, fs=8):
    ax.plot([x, x], [y0, y1], color=color, lw=lw)
    ax.plot([x - tick, x + tick], [y0, y0], color=color, lw=lw)
    ax.plot([x - tick, x + tick], [y1, y1], color=color, lw=lw)
    ax.text(x + 6, (y0 + y1) / 2, label, ha="left", va="center",
            fontsize=fs, color=color, rotation=90)


# ---------- zone renderers ----------
def render_cards_recessed(ax, x0, w, color, label, inner_z0, inner_z1):
    # Base
    ax.add_patch(Rectangle((x0, inner_z0), w, inner_z1 - inner_z0,
                           facecolor=color, alpha=0.75,
                           edgecolor=INK, lw=0.9))
    # 2 horizontal dividers (3 slots)
    for k in (1, 2):
        yz = inner_z0 + (inner_z1 - inner_z0) * k / 3
        ax.plot([x0, x0 + w], [yz, yz], color=INK, lw=0.7)
    # Scalloped recess at the front: show a shallow U cut in each slot's front
    # (we render this as 3 small arcs at the front face of each slot)
    for k in range(3):
        y_mid = inner_z0 + (inner_z1 - inner_z0) * (k + 0.5) / 3
        # Draw a semicircular notch into the front (visual on front view)
        notch_w = w * 0.5
        notch_h = (inner_z1 - inner_z0) / 3 * 0.35
        cx = x0 + w / 2
        ax.add_patch(FancyBboxPatch(
            (cx - notch_w / 2, y_mid - notch_h / 2),
            notch_w, notch_h,
            boxstyle="round,pad=0,rounding_size=4",
            facecolor=PAPER, edgecolor=INK, lw=0.6))
        ax.text(cx, y_mid, f"slot {k+1}", ha="center", va="center",
                fontsize=6.0, color=INK)
    ax.text(x0 + w / 2, inner_z1 + 3, "VISITING CARDS · recessed",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


def render_cross_tray(ax, x0, w, color, label, inner_z0, inner_z1):
    # One tray with + dividers forming 4 sub-pockets
    ax.add_patch(FancyBboxPatch(
        (x0 + 2, inner_z0 + 2), w - 4, inner_z1 - inner_z0 - 4,
        boxstyle="round,pad=0.3",
        facecolor=color, alpha=0.85, edgecolor=INK, lw=0.9))
    # finger hole on front face (shown at centre top)
    cx = x0 + w / 2
    cy = (inner_z0 + inner_z1) / 2
    # Cross dividers (horizontal and vertical through the pocket)
    ax.plot([x0 + 3, x0 + w - 3], [cy, cy], color=INK, lw=0.9,
            linestyle=(0, (3, 2)))
    ax.plot([cx, cx], [inner_z0 + 3, inner_z1 - 3], color=INK, lw=0.9,
            linestyle=(0, (3, 2)))
    # Four tiny labels in each quadrant
    for (sx, sy) in [(-0.25, 0.25), (0.25, 0.25),
                     (-0.25, -0.25), (0.25, -0.25)]:
        ax.text(cx + sx * (w - 8), cy + sy * (inner_z1 - inner_z0 - 8),
                "□", ha="center", va="center",
                fontsize=10, color=INK, alpha=0.4)
    # finger hole
    ax.add_patch(Circle((cx, inner_z0 + 6), 3,
                        facecolor=PAPER, edgecolor=INK, lw=0.6))
    ax.text(x0 + w / 2, inner_z1 + 3, "CROSS TRAY · 4 pockets · pull-out",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


def render_stapler_stack(ax, x0, w, color, label, inner_z0, inner_z1):
    # upper = drawer (face shown with handle), lower = open bay for staplers
    mid_z = (inner_z0 + inner_z1) / 2
    # upper drawer face
    ax.add_patch(FancyBboxPatch(
        (x0 + 2, mid_z + 2), w - 4, (inner_z1 - mid_z) - 4,
        boxstyle="round,pad=0.3",
        facecolor=DRAWER_FACE, edgecolor=DRAWER_EDGE, lw=1.2))
    # handle - small horizontal bar
    hb_w = w * 0.35; hb_h = 2
    ax.add_patch(Rectangle(
        (x0 + (w - hb_w) / 2, mid_z + (inner_z1 - mid_z) / 2 - hb_h / 2),
        hb_w, hb_h, facecolor=DRAWER_EDGE, edgecolor=INK, lw=0.6))
    ax.text(x0 + w / 2, mid_z + (inner_z1 - mid_z) * 0.80,
            "PIN DRAWER", ha="center", va="center",
            fontsize=6.5, color=INK, fontweight="bold")
    # shelf line
    ax.plot([x0, x0 + w], [mid_z, mid_z], color=INK, lw=1.0)
    # lower open bay
    ax.add_patch(Rectangle(
        (x0, inner_z0), w, mid_z - inner_z0,
        facecolor=color, alpha=0.60, edgecolor=INK, lw=0.6))
    # stapler glyph (simple)
    sx = x0 + w * 0.25; sy = inner_z0 + (mid_z - inner_z0) * 0.45
    ax.add_patch(Rectangle((sx, sy), w * 0.5, 4,
                           facecolor=INK, alpha=0.6, edgecolor=INK, lw=0.5))
    ax.text(x0 + w / 2, inner_z0 + (mid_z - inner_z0) * 0.80,
            "OPEN BAY → staplers",
            ha="center", va="center",
            fontsize=6.5, color=INK, fontweight="bold")
    ax.text(x0 + w / 2, -1000,
            "STAPLER STACK · drawer over open bay",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


def render_pen_coin_stack(ax, x0, w, color, label, inner_z0, inner_z1):
    # upper = open shelf (pens laying forward), lower = coin drawer
    mid_z = (inner_z0 + inner_z1) / 2
    # upper open bay
    ax.add_patch(Rectangle(
        (x0, mid_z), w, inner_z1 - mid_z,
        facecolor=color, alpha=0.60, edgecolor=INK, lw=0.6))
    # 4 stylised pens lying across
    for i in range(4):
        py = mid_z + (inner_z1 - mid_z) * (i + 1) / 5 - 1
        ax.plot([x0 + 6, x0 + w - 6], [py, py], color=INK,
                lw=1.5, alpha=0.6, solid_capstyle="round")
    ax.text(x0 + w / 2, mid_z + (inner_z1 - mid_z) * 0.86,
            "OPEN SHELF → pens / misc",
            ha="center", va="center", fontsize=6.5,
            color=INK, fontweight="bold")
    # shelf line
    ax.plot([x0, x0 + w], [mid_z, mid_z], color=INK, lw=1.0)
    # lower drawer face
    ax.add_patch(FancyBboxPatch(
        (x0 + 2, inner_z0 + 2), w - 4, (mid_z - inner_z0) - 4,
        boxstyle="round,pad=0.3",
        facecolor=DRAWER_FACE, edgecolor=DRAWER_EDGE, lw=1.2))
    hb_w = w * 0.35; hb_h = 2
    ax.add_patch(Rectangle(
        (x0 + (w - hb_w) / 2,
         inner_z0 + (mid_z - inner_z0) / 2 - hb_h / 2),
        hb_w, hb_h, facecolor=DRAWER_EDGE, edgecolor=INK, lw=0.6))
    ax.text(x0 + w / 2, inner_z0 + (mid_z - inner_z0) * 0.85,
            "COIN DRAWER", ha="center", va="center",
            fontsize=6.5, color=INK, fontweight="bold")
    ax.text(x0 + w / 2, -1000,
            "OPEN SHELF over COIN DRAWER",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


def render_mix_tray(ax, x0, w, color, label, inner_z0, inner_z1):
    # Lower open mixing area; upper = empty shelf
    mid_z = (inner_z0 + inner_z1) / 2
    # upper empty
    ax.add_patch(Rectangle(
        (x0, mid_z), w, inner_z1 - mid_z,
        facecolor=WOOD, edgecolor=INK, lw=0.5, alpha=0.5))
    ax.text(x0 + w / 2, mid_z + (inner_z1 - mid_z) * 0.5,
            "empty shelf (optional tray)",
            ha="center", va="center", fontsize=5.8,
            color=MUTED, style="italic")
    # shelf line
    ax.plot([x0, x0 + w], [mid_z, mid_z], color=INK, lw=1.0)
    # lower open
    ax.add_patch(Rectangle(
        (x0, inner_z0), w, mid_z - inner_z0,
        facecolor=LOOSE, edgecolor=INK, lw=0.6))
    # 2 soft partitions
    for k in (1, 2):
        xp = x0 + w * k / 3
        ax.plot([xp, xp], [inner_z0 + 2, mid_z - 2],
                color=INK, lw=0.5, linestyle=(0, (2, 2)))
    ax.text(x0 + w / 2, inner_z0 + (mid_z - inner_z0) * 0.5,
            "MIXING TRAY · drop stuff in",
            ha="center", va="center", fontsize=6.3,
            color=INK)
    ax.text(x0 + w / 2, -1000,
            "MIX TRAY · lower open with soft partitions",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


def render_floor_damper(ax, x0, w, color, label, inner_z0, inner_z1):
    # Open full-height column with damper on the floor
    ax.add_patch(Rectangle(
        (x0, inner_z0), w, inner_z1 - inner_z0,
        facecolor=WOOD, edgecolor=INK, lw=0.6, alpha=0.6))
    # damper = short cylinder with spindle poking up (two circles stacked)
    cx = x0 + w / 2
    # Base disc stack
    ax.add_patch(Rectangle(
        (cx - w * 0.30, inner_z0 + 3), w * 0.60, 7,
        facecolor=color, edgecolor=INK, lw=0.6))
    ax.add_patch(Circle((cx, inner_z0 + 10 + 4), 3,
                        facecolor=color, edgecolor=INK, lw=0.6))
    # spindle up
    ax.plot([cx, cx], [inner_z0 + 14, inner_z0 + 24],
            color=INK, lw=1.5)
    ax.text(cx, inner_z0 + 28, "finger damper",
            ha="center", va="bottom", fontsize=6.3,
            color=INK, fontweight="bold")
    ax.text(cx, inner_z1 - 6, "open above",
            ha="center", va="top", fontsize=6.0,
            color=MUTED, style="italic")
    ax.text(x0 + w / 2, -1000,
            "FLOOR ZONE · damper sits on the floor",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


def render_label_tray(ax, x0, w, color, label, inner_z0, inner_z1):
    # Simple upper pull-out tray + lower empty
    mid_z = (inner_z0 + inner_z1) / 2
    ax.add_patch(FancyBboxPatch(
        (x0 + 2, mid_z + 2), w - 4, (inner_z1 - mid_z) - 4,
        boxstyle="round,pad=0.3",
        facecolor=color, alpha=0.85, edgecolor=INK, lw=0.9))
    ax.add_patch(Circle(
        (x0 + w / 2, mid_z + (inner_z1 - mid_z) / 2),
        3, facecolor=PAPER, edgecolor=INK, lw=0.6))
    ax.text(x0 + w / 2, mid_z + (inner_z1 - mid_z) * 0.80,
            "LABELS", ha="center", va="center",
            fontsize=6.5, color=INK, fontweight="bold")
    ax.plot([x0, x0 + w], [mid_z, mid_z], color=INK, lw=1.0)
    ax.add_patch(Rectangle(
        (x0, inner_z0), w, mid_z - inner_z0,
        facecolor=LOOSE, edgecolor=INK, lw=0.6))
    ax.text(x0 + w / 2, inner_z0 + (mid_z - inner_z0) * 0.5,
            "open", ha="center", va="center",
            fontsize=6.0, color=MUTED, style="italic")
    ax.text(x0 + w / 2, -1000,
            "SIMPLE PULL-OUT · small tray",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


def render_calc_stack(ax, x0, w, color, label, inner_z0, inner_z1):
    ax.add_patch(Rectangle(
        (x0, inner_z0), w, inner_z1 - inner_z0,
        facecolor=color, alpha=0.80, edgecolor=INK, lw=0.9))
    for k in (1, 2):
        yz = inner_z0 + (inner_z1 - inner_z0) * k / 3
        ax.plot([x0 + 3, x0 + w - 3], [yz, yz], color=INK,
                lw=0.6, linestyle=(0, (3, 2)))
    ax.text(x0 + w / 2, (inner_z0 + inner_z1) / 2,
            "CALCULATORS\n(stacked ×3)", ha="center",
            va="center", fontsize=8, color=INK, fontweight="bold")
    ax.text(x0 + w / 2, -1000,
            "FULL COLUMN · stack of 3",
            ha="center", va="bottom", fontsize=7,
            color=MUTED, style="italic")


RENDERERS = {
    "cards-recessed":  render_cards_recessed,
    "cross-tray":      render_cross_tray,
    "stapler-stack":   render_stapler_stack,
    "pen-coin-stack":  render_pen_coin_stack,
    "mix-tray":        render_mix_tray,
    "floor-damper":    render_floor_damper,
    "label-tray":      render_label_tray,
    "calc-stack":      render_calc_stack,
}


def draw():
    fig, frame = _sheet()

    # ---------- FRONT VIEW ----------
    fv = fig.add_axes([0.03, 0.44, 0.94, 0.42])
    fv.set_aspect("equal"); fv.axis("off")
    fv.set_title("FRONT VIEW  (open face, 8 zones with varied shapes)",
                 fontsize=11, color=MUTED, loc="left", pad=10)

    fv.add_patch(Rectangle((0, 0), L, H, facecolor=WOOD,
                           edgecolor=WOOD_EDGE, lw=1.6))
    inner_z0 = T
    inner_z1 = H - T

    # Walk zones
    boundaries = []
    x_cursor = T
    for i, (w_in, kind, color, label) in enumerate(ZONES):
        w = w_in * IN
        if i == 0:
            x0 = T
        else:
            x0 = x_cursor
        if i == len(ZONES) - 1:
            x1 = L - T
        else:
            x1 = x0 + w
        RENDERERS[kind](fv, x0, x1 - x0, color, label, inner_z0, inner_z1)
        if i < len(ZONES) - 1:
            fv.plot([x1, x1], [T, H - T], color=INK, lw=1.0)
            x_cursor = x1 + T
        boundaries.append((x0, x1))

    # Overall dimensions
    _dim_h(fv, 0, L, H + 32, f"{L:.0f} mm  (53\")", color=INK)
    _dim_v(fv, 0, H, -40, f"{H:.0f} mm  (5\")", color=INK)

    # Zone width callouts under
    for i, ((x0, x1), (w_in, *_)) in enumerate(zip(boundaries, ZONES)):
        _dim_h(fv, x0, x1, -12, f'{w_in}"', color=MUTED,
               lw=0.6, tick=3, fs=7)

    fv.set_xlim(-80, L + 50)
    fv.set_ylim(-30, H + 55)

    # ---------- MECHANISM KEY (bottom) ----------
    mk = fig.add_axes([0.03, 0.02, 0.94, 0.36])
    mk.axis("off"); mk.set_xlim(0, 1); mk.set_ylim(0, 1)
    mk.text(0.0, 0.98, "MECHANISM KEY",
            fontsize=12, fontweight="bold", color=INK, va="top")

    items = [
        ("Recessed card slot", CARDS_C,
         "Full-height column, 2 horizontal dividers = 3 stacks.\n"
         "Front has a scalloped cut-out at each slot so you can grab the\n"
         "top card without digging in with fingers."),
        ("Cross-divided tray", CROSS_C,
         "One pull-out tray with a + divider inside = 4 sub-pockets.\n"
         "You decide what goes in each pocket (pens, pencils, small tools);\n"
         "the shape just gives you four grouped bins in one tray."),
        ("Drawer over open bay (stapler)", STAPLER_C,
         "Upper = small drawer with handle (sliding front panel) for\n"
         "stapler pins. Lower = open bay you can reach into for staplers.\n"
         "Drawer hides mess; open bay = grab-and-go."),
        ("Open shelf over drawer (coins)", PENS_C,
         "Reverse of above: upper = open shelf (pens or anything), lower =\n"
         "small drawer for coins. Keeps the loose heavy stuff tucked out of\n"
         "sight but easy to open."),
        ("Mixing tray", MIX_C,
         "Lower = open area with soft partitions (half-height walls).\n"
         "Upper = empty shelf, optional removable tray. Rake things forward."),
        ("Floor zone", DAMP_C,
         "Full-height open column. Thing sits on the floor of the box\n"
         "(no shelf above). Used for the finger damper or anything tall-ish\n"
         "that needs headroom."),
        ("Simple pull-out tray", LABEL_C,
         "Just the plain pull-out tray with finger-hole. Open bay below.\n"
         "Catch-all shape when you don't need anything fancier."),
        ("Stacked column", CALCS_C,
         "Full-height open column with no shelves. Items stack naturally.\n"
         "Used for the 3 calculators; same shape works for notebooks."),
    ]
    cols = 4
    rows = 2
    cw = 1.0 / cols
    rh = 0.90 / rows
    for i, (name, col, desc) in enumerate(items):
        r = i // cols; c = i % cols
        x = c * cw + 0.005
        y = 0.90 - r * rh
        # colour chip
        mk.add_patch(Rectangle((x, y - 0.03), 0.035, 0.045,
                               facecolor=col, alpha=0.9,
                               edgecolor=INK, lw=0.6))
        mk.text(x + 0.045, y - 0.005, name, fontsize=8.5,
                fontweight="bold", color=INK, va="center")
        mk.text(x + 0.005, y - 0.07, desc, fontsize=6.8,
                color=INK, va="top")

    out = Path(__file__).parent.parent / "PDF" / "organizer_v5_plan.pdf"
    fig.savefig(out, dpi=200, facecolor=PAPER)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    draw()

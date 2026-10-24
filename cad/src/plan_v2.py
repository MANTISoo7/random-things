"""Color-coded plan drawing v2 — Design D (hybrid) with revised dimensions.

Dimensions updated to measured values (53" L x 5" H x 6" D).
Item list expanded; shallow box forces most items to lay horizontally.
Small loose items (coins, keys, pins, toothpicks, U-clips, pin boxes)
share compartments with internal sub-bins.

Compartments (left to right, 53" total):
  1. Pens + highlighters       12"   2 sub-bins
  2. Visiting cards             4"
  3. Small-item grid A          6"   2x2 (coins, keys, toothpicks, pushpins)
  4. Small-item strip B         6"   3 bins (U-clips, pin box 1, pin box 2)
  5. Pin box 3 + glue           3"   2 sub-bins
  6. Staplers                   8"   2 sub-bins
  7. Calculators                8"   3 sub-bins (upright)
  8. Coasters (stacked)         3"
  9. Damper + misc              3"
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch

IN = 25.4
L = 53 * IN            # 1346.2 mm
H = 5 * IN             # 127.0  mm  (was 9"; measured value)
D = 6 * IN             # 152.4  mm
T = 12.0               # wall thickness (12 mm MDF)

SHEET_W, SHEET_H = 16.54, 11.69  # A3 landscape, inches

# Soft, print-friendly palette.
PAPER = "#FAF7F0"
INK = "#2A2520"
MUTED = "#7A736A"
WOOD = "#F0E6D2"
WOOD_EDGE = "#9A7E55"
PANEL = "#FFFFFF"

# One colour per compartment group.
COLORS = {
    "pens":    "#CB7B82",
    "cards":   "#D4A373",
    "smallA":  "#C9A86B",
    "smallB":  "#B98060",
    "pinglue": "#AF8359",
    "staplers":"#7FA989",
    "calcs":   "#6B98B5",
    "coasters":"#8E90B9",
    "damper":  "#9381A6",
}

# Compartment list: (width_in, label, color_key, sub_labels, sub_layout)
# sub_layout: None | "h" (horizontal split) | "v" (vertical split) | (rows, cols) grid
COMPS = [
    (12, "PENS + HIGHLIGHTERS", "pens",
         ["PENS",  "HIGHLIGHTERS"], "h"),
    (4,  "VISITING CARDS",       "cards",
         None, None),
    (6,  "SMALL ITEMS · A", "smallA",
         ["COINS", "KEYS", "TOOTHPICKS", "PUSHPINS"], (2, 2)),
    (6,  "SMALL ITEMS · B", "smallB",
         ["U-CLIPS", "PIN BOX 1", "PIN BOX 2"], "h"),
    (3,  "PIN BOX 3 + GLUE",      "pinglue",
         ["PIN BOX 3", "GLUE"], "h"),
    (8,  "STAPLERS",               "staplers",
         ["STAPLER 1", "STAPLER 2"], "h"),
    (8,  "CALCULATORS (upright)",  "calcs",
         ["CALC 1", "CALC 2", "CALC 3"], "h"),
    (3,  "COASTERS (stacked)",     "coasters",
         None, None),
    (3,  "DAMPER / MISC",          "damper",
         None, None),
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
               "DESK ORGANIZER  —  OPTION D v2  (hybrid, revised)",
               fontsize=19, fontweight="bold", color=INK, va="top")
    frame.text(0.02, 0.935,
               '53" × 5" × 6"  (1346 × 127 × 152 mm)  ·  '
               'open front  ·  fits under monitor shelf  ·  9 compartments',
               fontsize=11, color=MUTED, va="top", style="italic")

    tb_x, tb_y, tb_w, tb_h = 0.70, 0.015, 0.285, 0.09
    frame.add_patch(Rectangle((tb_x, tb_y), tb_w, tb_h, fill=True,
                              facecolor=PANEL, edgecolor=INK, lw=0.8))
    rows = [
        ("PART NO.", "ORG-D-002"),
        ("MATERIAL", "12 mm MDF  or  6 mm acrylic"),
        ("UNITS",    "mm  (inches in parentheses)"),
        ("SCALE",    "not to scale  ·  revise after measurement"),
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
    ax.text((x0 + x1) / 2, y + 8, label, ha="center", va="bottom",
            fontsize=fs, color=color)


def _dim_v(ax, y0, y1, x, label, color=INK, lw=0.8, tick=4, fs=8):
    ax.plot([x, x], [y0, y1], color=color, lw=lw)
    ax.plot([x - tick, x + tick], [y0, y0], color=color, lw=lw)
    ax.plot([x - tick, x + tick], [y1, y1], color=color, lw=lw)
    ax.text(x + 8, (y0 + y1) / 2, label, ha="left", va="center",
            fontsize=fs, color=color, rotation=90)


def _draw_compartment_front(ax, x0, w_mm, color, label, subs, layout):
    """Render one compartment on the front view, from x0 to x0+w_mm."""
    inner_z0 = T
    inner_z1 = H - T
    # Base fill
    ax.add_patch(Rectangle(
        (x0, inner_z0), w_mm, inner_z1 - inner_z0,
        facecolor=color, alpha=0.75, edgecolor=INK, lw=0.9))

    if subs is None:
        # Narrow compartments: show number only inside, label below in key.
        narrow = w_mm < 100
        ax.text(x0 + w_mm / 2, (inner_z0 + inner_z1) / 2, label,
                ha="center", va="center",
                fontsize=6.5 if narrow else 8,
                color=INK, fontweight="bold",
                rotation=90 if narrow else 0)
        return

    if layout == "h":
        n = len(subs)
        sw = w_mm / n
        for i, s in enumerate(subs):
            if i < n - 1:
                sx = x0 + (i + 1) * sw
                ax.plot([sx, sx], [inner_z0, inner_z1],
                        color=INK, lw=0.6, linestyle=(0, (2, 2)))
            ax.text(x0 + sw * (i + 0.5), (inner_z0 + inner_z1) / 2,
                    s, ha="center", va="center",
                    fontsize=6.6, color=INK, fontweight="bold")
        return

    if isinstance(layout, tuple):
        rows, cols = layout
        rh = (inner_z1 - inner_z0) / rows
        cw = w_mm / cols
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                if idx >= len(subs):
                    break
                cx = x0 + cw * (c + 0.5)
                cz = inner_z1 - rh * (r + 0.5)
                ax.text(cx, cz, subs[idx],
                        ha="center", va="center",
                        fontsize=6.3, color=INK, fontweight="bold")
        for r in range(1, rows):
            z = inner_z1 - r * rh
            ax.plot([x0, x0 + w_mm], [z, z],
                    color=INK, lw=0.6, linestyle=(0, (2, 2)))
        for c in range(1, cols):
            x = x0 + c * cw
            ax.plot([x, x], [inner_z0, inner_z1],
                    color=INK, lw=0.6, linestyle=(0, (2, 2)))


def draw():
    fig, frame = _sheet()

    # ---------- FRONT VIEW ----------
    fv = fig.add_axes([0.03, 0.50, 0.75, 0.38])
    fv.set_aspect("equal"); fv.axis("off")
    fv.set_title("FRONT VIEW  (looking at the open face)",
                 fontsize=11, color=MUTED, loc="left", pad=10)
    # Carcase
    fv.add_patch(Rectangle((0, 0), L, H, facecolor=WOOD,
                           edgecolor=WOOD_EDGE, lw=1.6))

    # Walk compartments
    boundaries = [0]
    x_cursor = T  # start inside the left wall
    for i, (w_in, label, ckey, subs, layout) in enumerate(COMPS):
        w = w_in * IN
        # First and last compartments reach to the carcase ends (no wall there)
        if i == 0:
            x0 = T
        else:
            x0 = x_cursor
        if i == len(COMPS) - 1:
            x1 = L - T
        else:
            x1 = x0 + w
        _draw_compartment_front(fv, x0, x1 - x0,
                                COLORS[ckey], label, subs, layout)
        if i < len(COMPS) - 1:
            # Divider line
            fv.plot([x1, x1], [T, H - T], color=INK, lw=1.0)
            x_cursor = x1 + T  # advance past divider thickness
        boundaries.append(x1)

    # Overall dimensions
    _dim_h(fv, 0, L, H + 18, f"{L:.0f} mm  ({L/IN:.0f}\")", color=INK)
    _dim_v(fv, 0, H, -40, f"{H:.0f} mm  ({H/IN:.0f}\")", color=INK)

    # Compartment-width callouts under each
    for i, (w_in, *_rest) in enumerate(COMPS):
        x0 = boundaries[i]
        x1 = boundaries[i + 1]
        _dim_h(fv, x0, x1, -14, f'{w_in:.0f}"', color=MUTED,
               lw=0.6, tick=3, fs=7)

    fv.set_xlim(-80, L + 50)
    fv.set_ylim(-30, H + 42)

    # ---------- TOP VIEW ----------
    tv = fig.add_axes([0.03, 0.28, 0.75, 0.17])
    tv.set_aspect("equal"); tv.axis("off")
    tv.set_title("TOP VIEW  (looking down into the open front)",
                 fontsize=11, color=MUTED, loc="left", pad=8)
    tv.add_patch(Rectangle((0, 0), L, D, facecolor=WOOD,
                           edgecolor=WOOD_EDGE, lw=1.6))
    for i, (w_in, label, ckey, _subs, _layout) in enumerate(COMPS):
        x0 = boundaries[i]
        x1 = boundaries[i + 1]
        tv.add_patch(Rectangle((x0, T), x1 - x0, D - 2 * T,
                               facecolor=COLORS[ckey], alpha=0.55,
                               edgecolor=INK, lw=0.6))
        narrow = (x1 - x0) < 100
        short = label.split(" ")[0] if " " in label else label
        tv.text((x0 + x1) / 2, D / 2,
                str(i + 1) if narrow else short,
                ha="center", va="center",
                fontsize=8, color=INK, fontweight="bold")
    _dim_v(tv, 0, D, -40, f"{D:.0f} mm  ({D/IN:.0f}\")", color=INK)
    tv.set_xlim(-80, L + 50); tv.set_ylim(-15, D + 25)

    # ---------- ISOMETRIC ----------
    iso = fig.add_axes([0.80, 0.50, 0.18, 0.38])
    iso.set_aspect("equal"); iso.axis("off")
    iso.set_title("ISOMETRIC", fontsize=10,
                  color=MUTED, loc="left", pad=4)
    sx, sy = 1.0, 0.5
    def _iso(x, y, z):
        return (x + y * sx * 0.5, z + y * sy * 0.5)
    def _poly(pts, color, alpha=0.9, ec=INK):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        iso.add_patch(Polygon(list(zip(xs, ys)), facecolor=color,
                              edgecolor=ec, lw=0.8, alpha=alpha))
    front_pts = [_iso(0, 0, 0), _iso(L, 0, 0),
                 _iso(L, 0, H), _iso(0, 0, H)]
    _poly(front_pts, WOOD, 0.25, ec=WOOD_EDGE)
    top_pts = [_iso(0, 0, H), _iso(L, 0, H),
               _iso(L, D, H), _iso(0, D, H)]
    _poly(top_pts, WOOD_EDGE, 0.9)
    right_pts = [_iso(L, 0, 0), _iso(L, D, 0),
                 _iso(L, D, H), _iso(L, 0, H)]
    _poly(right_pts, WOOD, 0.9)
    for i, (_, _l, ckey, _s, _la) in enumerate(COMPS):
        x0 = boundaries[i]; x1 = boundaries[i + 1]
        pts = [_iso(x0, 0, T), _iso(x1, 0, T),
               _iso(x1, 0, H - T), _iso(x0, 0, H - T)]
        _poly(pts, COLORS[ckey], 0.75)
    all_x = [p[0] for p in (front_pts + top_pts + right_pts)]
    all_y = [p[1] for p in (front_pts + top_pts + right_pts)]
    pad = 20
    iso.set_xlim(min(all_x) - pad, max(all_x) + pad)
    iso.set_ylim(min(all_y) - pad, max(all_y) + pad)

    # ---------- LEGEND / KEY ----------
    lg = fig.add_axes([0.80, 0.14, 0.18, 0.33])
    lg.axis("off"); lg.set_xlim(0, 1); lg.set_ylim(0, 1)
    lg.text(0.02, 0.98, "COMPARTMENT KEY", fontsize=10,
            fontweight="bold", color=INK, va="top")

    key_rows = []
    for i, (w_in, label, ckey, subs, _layout) in enumerate(COMPS):
        text = label
        if subs:
            text = text + "  (" + " / ".join(subs) + ")"
        key_rows.append((i + 1, COLORS[ckey], text, f"{w_in}\""))

    row_h = 0.93 / len(key_rows)
    for row_i, (num, color, text, w) in enumerate(key_rows):
        y = 0.93 - row_i * row_h
        lg.add_patch(Rectangle(
            (0.02, y - row_h * 0.78), 0.07, row_h * 0.72,
            facecolor=color, edgecolor=INK, lw=0.5))
        lg.text(0.055, y - row_h * 0.42, str(num), ha="center",
                va="center", fontsize=7.5, fontweight="bold", color=INK)
        lg.text(0.11, y - row_h * 0.30, text, va="center",
                fontsize=6.0, color=INK)
        lg.text(0.11, y - row_h * 0.62, w, va="center",
                fontsize=5.6, color=MUTED, style="italic")

    # ---------- NOTES ----------
    nt = fig.add_axes([0.03, 0.02, 0.65, 0.22])
    nt.axis("off"); nt.set_xlim(0, 1); nt.set_ylim(0, 1)
    nt.text(0.0, 0.96, "NOTES", fontsize=11, fontweight="bold",
            color=INK, va="top")
    notes = [
        "1.  All interior dividers 12 mm thick (same as walls); sub-dividers inside a compartment may be 6 mm for lighter touch.",
        "2.  Front face fully open — the box tucks under the monitor shelf, so the only access is from the front.",
        "3.  Dashed internal lines show sub-bins within one compartment (shared walls, no structural separation).",
        "4.  Shallow (5\") box means almost everything lays flat; only visiting cards (slot) and calculators (upright) use the full height.",
        "5.  Small-item grid A uses a 2×2 sub-grid for coins/keys/toothpicks/pushpins; add a thin removable tray to lift them to the lip for easier grab.",
        "6.  Width sums to 53\" nominally; actual compartment widths shrink by the divider thickness between them.",
        "7.  All dimensions provisional — refresh when exact shelf clearance and desk width are measured.",
    ]
    for i, n in enumerate(notes):
        nt.text(0.0, 0.86 - i * 0.11, n, fontsize=8.3,
                color=INK, va="top")

    out = Path(__file__).parent.parent / "PDF" / "organizer_D_v2_plan.pdf"
    fig.savefig(out, dpi=200, facecolor=PAPER)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    draw()

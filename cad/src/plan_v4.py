"""Shop counter organizer v4 — layered shelf with pull-out trays.

Structure:
  - Full height (5") at the LEFT end: visiting cards (upright slot).
  - Full height at the RIGHT end: calculators (stacked x3).
  - MIDDLE section is a 2-tier shelf:
      upper tier (~2") = pull-out trays (pens, markers, highlighters,
                         fine pens, damper, labels, stapler+glue,
                         pin boxes + U-clips)
      lower tier (~2.5") = one open tray with light partitions for
                           loose stuff (coins, keys, bands, pushpins,
                           toothpicks, coasters)

Access is purely from the front: pull a tray out, use it, slide it back.
Lower tier scoops out so you can rake things forward.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, Circle

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

PENS      = "#CB7B82"
MARKERS   = "#D47A5A"
HILI      = "#D4A373"
FINE      = "#B98060"
DAMPER    = "#9381A6"
LABELS    = "#8E90B9"
STAPLER   = "#AF8359"
PINBOX    = "#C9A86B"
CARDS     = "#7FA989"
CALCS     = "#6B98B5"

# Full-height end zones
END_LEFT_W  = 4.0   # inches, visiting cards
END_RIGHT_W = 8.0   # inches, calculators

# Middle pull-out trays (upper tier). (width_in, label, color)
PULLOUTS = [
    (5.5, "PENS",         PENS),
    (5.5, "MARKERS",      MARKERS),
    (5.5, "HIGHLIGHTERS", HILI),
    (5.0, "FINE PENS",    FINE),
    (3.5, "DAMPER",       DAMPER),
    (3.5, "LABELS",       LABELS),
    (5.0, "STAPLER+GLUE", STAPLER),
    (4.0, "PIN BOX / U-CLIPS", PINBOX),
]

# Lower-tier open-tray partitions (light walls). (width_in, label)
LOWER = [
    (10, "COINS · KEYS · MISC"),
    (10, "BANDS · PUSHPINS · TOOTHPICKS · U-CLIPS"),
    (10, "COASTERS · OPEN SPACE"),
    (11, "OPEN SPACE"),
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
               "SHOP COUNTER ORGANIZER  —  v4  (layered shelf)",
               fontsize=19, fontweight="bold", color=INK, va="top")
    frame.text(0.02, 0.935,
               '53" × 5" × 6"  ·  open front  ·  '
               '2-tier middle section  ·  pull-out trays over an '
               'open tray  ·  cards left, calculators right',
               fontsize=10.5, color=MUTED, va="top", style="italic")

    tb_x, tb_y, tb_w, tb_h = 0.70, 0.015, 0.285, 0.09
    frame.add_patch(Rectangle((tb_x, tb_y), tb_w, tb_h, fill=True,
                              facecolor=PANEL, edgecolor=INK, lw=0.8))
    rows = [
        ("PART NO.", "ORG-D-004"),
        ("MATERIAL", "12 mm MDF carcase; 6 mm trays"),
        ("UNITS",    "mm  (inches in parentheses)"),
        ("SCALE",    "not to scale  ·  widths are provisional"),
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


def draw():
    fig, frame = _sheet()

    # ---------- FRONT VIEW ----------
    fv = fig.add_axes([0.03, 0.46, 0.75, 0.40])
    fv.set_aspect("equal"); fv.axis("off")
    fv.set_title("FRONT VIEW  (looking at the open face)",
                 fontsize=11, color=MUTED, loc="left", pad=10)
    fv.add_patch(Rectangle((0, 0), L, H, facecolor=WOOD,
                           edgecolor=WOOD_EDGE, lw=1.6))

    end_l = END_LEFT_W * IN
    end_r = END_RIGHT_W * IN

    # LEFT: visiting cards (full height upright slot)
    x0 = T; x1 = end_l
    fv.add_patch(Rectangle((x0, T), x1 - x0, H - 2 * T,
                           facecolor=CARDS, alpha=0.80,
                           edgecolor=INK, lw=0.9))
    fv.text((x0 + x1) / 2, (T + H - T) / 2, "VISITING\nCARDS",
            ha="center", va="center", fontsize=8.5,
            color=INK, fontweight="bold")

    # Divider between left-end zone and middle
    fv.plot([x1, x1], [T, H - T], color=INK, lw=1.0)

    # RIGHT: calculators stack
    xr0 = L - end_r; xr1 = L - T
    fv.add_patch(Rectangle((xr0, T), xr1 - xr0, H - 2 * T,
                           facecolor=CALCS, alpha=0.80,
                           edgecolor=INK, lw=0.9))
    # 3 stacked calculator rectangles (horizontal lines)
    for i in range(1, 3):
        yz = T + (H - 2 * T) * i / 3
        fv.plot([xr0 + 4, xr1 - 4], [yz, yz], color=INK,
                lw=0.5, linestyle=(0, (3, 2)))
    fv.text((xr0 + xr1) / 2, (T + H - T) / 2,
            "CALCULATORS\n(stacked ×3)",
            ha="center", va="center", fontsize=8.5,
            color=INK, fontweight="bold")

    fv.plot([xr0, xr0], [T, H - T], color=INK, lw=1.0)

    # MIDDLE: 2-tier
    mid_x0 = end_l + T   # just inside left divider
    mid_x1 = xr0 - T     # just inside right divider
    mid_w = mid_x1 - mid_x0

    shelf_z = T + (H - 2 * T) * 0.45   # mid-shelf position
    # Horizontal shelf line
    fv.plot([mid_x0, mid_x1], [shelf_z, shelf_z],
            color=INK, lw=1.2)

    # ----- UPPER TIER: pull-out trays
    tier_top = H - T
    tier_bot = shelf_z + 1
    inner_top = tier_top - tier_bot
    # Compute scaled widths from PULLOUTS to fill mid_w
    total_w_in = sum(w for w, *_ in PULLOUTS)
    px = mid_x0
    for (win, lbl, col) in PULLOUTS:
        pw = (win / total_w_in) * mid_w
        # tray body
        fv.add_patch(FancyBboxPatch(
            (px + 1, tier_bot + 1), pw - 2, inner_top - 2,
            boxstyle="round,pad=0.3",
            facecolor=col, alpha=0.85,
            edgecolor=INK, lw=0.8))
        # finger-hole
        fv.add_patch(Circle(
            (px + pw / 2, tier_bot + inner_top / 2),
            inner_top * 0.18, facecolor=WOOD, edgecolor=INK, lw=0.6))
        # label above the hole
        fv.text(px + pw / 2, tier_bot + inner_top * 0.80,
                lbl, ha="center", va="top", fontsize=6.0,
                color=INK, fontweight="bold")
        px += pw

    # Tier label above (centred on middle section)
    fv.text((mid_x0 + mid_x1) / 2, tier_top + 5,
            "UPPER TIER — pull-out trays (grab the finger hole, slide out)",
            ha="center", va="bottom", fontsize=7.5,
            color=MUTED, style="italic")

    # ----- LOWER TIER: open tray with soft partitions
    low_top = shelf_z - 1
    low_bot = T
    fv.add_patch(Rectangle((mid_x0, low_bot), mid_w, low_top - low_bot,
                           facecolor=LOOSE, edgecolor=INK, lw=0.9))
    # Light partitions
    total_lw_in = sum(w for w, *_ in LOWER)
    lx = mid_x0
    for i, (win, lbl) in enumerate(LOWER):
        lw_mm = (win / total_lw_in) * mid_w
        if i < len(LOWER) - 1:
            x_part = lx + lw_mm
            fv.plot([x_part, x_part], [low_bot + 2, low_top - 1],
                    color=INK, lw=0.5, linestyle=(0, (2, 2)))
        fv.text(lx + lw_mm / 2, (low_bot + low_top) / 2,
                lbl, ha="center", va="center", fontsize=5.8,
                color=INK)
        lx += lw_mm

    # Tier label below (centred on middle section)
    fv.text((mid_x0 + mid_x1) / 2, low_bot - 6,
            "LOWER TIER — open tray; low partitions, no lids (rake things forward with your hand)",
            ha="center", va="top", fontsize=7.5,
            color=MUTED, style="italic")

    # Overall dimensions
    _dim_h(fv, 0, L, H + 18, f"{L:.0f} mm  (53\")", color=INK)
    _dim_v(fv, 0, H, -40, f"{H:.0f} mm  (5\")", color=INK)

    fv.set_xlim(-80, L + 50)
    fv.set_ylim(-32, H + 48)

    # ---------- TOP VIEW with one tray pulled out ----------
    tv = fig.add_axes([0.03, 0.24, 0.75, 0.17])
    tv.set_aspect("equal"); tv.axis("off")
    tv.set_title("TOP VIEW  (one tray shown pulled out to show the slide-out action)",
                 fontsize=11, color=MUTED, loc="left", pad=8)
    tv.add_patch(Rectangle((0, 0), L, D, facecolor=WOOD,
                           edgecolor=WOOD_EDGE, lw=1.6))

    # ends
    tv.add_patch(Rectangle((T, T), end_l - T, D - 2 * T,
                           facecolor=CARDS, alpha=0.5,
                           edgecolor=INK, lw=0.5))
    tv.text((T + end_l) / 2, D / 2, "CARDS",
            ha="center", va="center", fontsize=8,
            color=INK, fontweight="bold")
    tv.add_patch(Rectangle((xr0, T), end_r - T, D - 2 * T,
                           facecolor=CALCS, alpha=0.5,
                           edgecolor=INK, lw=0.5))
    tv.text((xr0 + xr1) / 2, D / 2, "CALC",
            ha="center", va="center", fontsize=8,
            color=INK, fontweight="bold")

    # pull-out trays as top-view rectangles (seen through open front)
    px = mid_x0
    pull_index = 2  # which tray to render as "pulled out"
    for i, (win, lbl, col) in enumerate(PULLOUTS):
        pw = (win / total_w_in) * mid_w
        if i == pull_index:
            # pulled forward by half the depth
            dy = -D * 0.5
            tv.add_patch(FancyBboxPatch(
                (px + 1, T + dy), pw - 2, D - 2 * T,
                boxstyle="round,pad=0.3",
                facecolor=col, alpha=0.9,
                edgecolor=INK, lw=0.9))
            # arrow
            tv.annotate("", xy=(px + pw / 2, T + dy - 2),
                        xytext=(px + pw / 2, T + 4),
                        arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
            tv.text(px + pw / 2, T + dy - 10, lbl + "  (pulled out)",
                    ha="center", va="top", fontsize=6.5,
                    color=INK, fontweight="bold")
        else:
            tv.add_patch(FancyBboxPatch(
                (px + 1, T + 1), pw - 2, D - 2 * T - 2,
                boxstyle="round,pad=0.2",
                facecolor=col, alpha=0.55,
                edgecolor=INK, lw=0.4))
            tv.text(px + pw / 2, D / 2, lbl[:4],
                    ha="center", va="center", fontsize=5.5,
                    color=INK)
        px += pw

    _dim_v(tv, 0, D, -40, f"{D:.0f} mm  (6\")", color=INK)
    tv.set_xlim(-80, L + 50)
    tv.set_ylim(-D * 0.6, D + 20)

    # ---------- SIDE / CROSS-SECTION ----------
    sv = fig.add_axes([0.80, 0.46, 0.18, 0.40])
    sv.set_aspect("equal"); sv.axis("off")
    sv.set_title("CROSS-SECTION  (through the middle)",
                 fontsize=9.5, color=MUTED, loc="left", pad=4)
    # Depth across x, height across z. Section at the middle zone.
    sv.add_patch(Rectangle((0, 0), D, H, facecolor=WOOD,
                           edgecolor=WOOD_EDGE, lw=1.6))
    # mid shelf
    sv.add_patch(Rectangle((T, shelf_z - 1), D - 2 * T, 2,
                           facecolor=WOOD_EDGE, edgecolor=INK, lw=0.5))
    # upper tray showing finger hole
    sv.add_patch(FancyBboxPatch(
        (T + 1, shelf_z + 2), D - 2 * T - 2, (H - T) - shelf_z - 3,
        boxstyle="round,pad=0.3",
        facecolor=PENS, alpha=0.75, edgecolor=INK, lw=0.8))
    sv.add_patch(Circle(
        (T + (D - 2 * T) * 0.15, shelf_z + 2 + ((H - T) - shelf_z - 3) / 2),
        2.5, facecolor=WOOD, edgecolor=INK, lw=0.5))
    sv.text(D / 2, (shelf_z + H - T) / 2 + 1, "pull-out tray",
            ha="center", va="center", fontsize=6.5,
            color=INK, fontweight="bold")
    # lower open tray
    sv.add_patch(Rectangle((T, T), D - 2 * T, shelf_z - T - 1,
                           facecolor=LOOSE, edgecolor=INK, lw=0.6))
    sv.text(D / 2, (T + shelf_z) / 2, "open tray",
            ha="center", va="center", fontsize=6.5,
            color=INK, fontweight="bold")
    # arrow showing pull direction
    sv.annotate("pull →",
                xy=(-10, (shelf_z + H - T) / 2),
                xytext=(T + 2, (shelf_z + H - T) / 2),
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8),
                fontsize=7, color=INK, va="center")
    _dim_h(sv, 0, D, -8, '6"', color=MUTED, lw=0.5, tick=3, fs=6)
    _dim_v(sv, 0, H, -14, '5"', color=MUTED, lw=0.5, tick=3, fs=6)
    sv.set_xlim(-25, D + 10)
    sv.set_ylim(-16, H + 12)

    # ---------- KEY ----------
    lg = fig.add_axes([0.80, 0.06, 0.18, 0.37])
    lg.axis("off"); lg.set_xlim(0, 1); lg.set_ylim(0, 1)
    lg.text(0.02, 0.98, "KEY", fontsize=10,
            fontweight="bold", color=INK, va="top")
    lg.text(0.02, 0.945, "Full height (ends)",
            fontsize=7.5, color=MUTED, va="top", style="italic")
    for i, (lbl, col) in enumerate([("VISITING CARDS", CARDS),
                                     ("CALCULATORS (stacked ×3)", CALCS)]):
        y = 0.90 - i * 0.045
        lg.add_patch(Rectangle((0.03, y - 0.022), 0.08, 0.030,
                               facecolor=col, alpha=0.8,
                               edgecolor=INK, lw=0.5))
        lg.text(0.14, y - 0.007, lbl, fontsize=7, color=INK, va="center")

    lg.text(0.02, 0.79, "Upper tier — pull-out trays",
            fontsize=7.5, color=MUTED, va="top", style="italic")
    for i, (_w, lbl, col) in enumerate(PULLOUTS):
        y = 0.75 - i * 0.038
        lg.add_patch(Rectangle((0.03, y - 0.018), 0.08, 0.024,
                               facecolor=col, alpha=0.85,
                               edgecolor=INK, lw=0.5))
        lg.text(0.14, y - 0.005, lbl, fontsize=6.5, color=INK, va="center")

    lg.text(0.02, 0.42, "Lower tier — open tray",
            fontsize=7.5, color=MUTED, va="top", style="italic")
    lg.add_patch(Rectangle((0.03, 0.355), 0.08, 0.024,
                           facecolor=LOOSE, edgecolor=INK, lw=0.5))
    lg.text(0.14, 0.367, "LOOSE MIX (soft partitions)",
            fontsize=6.5, color=INK, va="center")
    lg.text(0.03, 0.32,
            "coins, keys, bands, pushpins, toothpicks,\nU-clips, coasters — just drop them in",
            fontsize=6.3, color=INK, va="top")

    # ---------- NOTES ----------
    nt = fig.add_axes([0.03, 0.02, 0.75, 0.19])
    nt.axis("off"); nt.set_xlim(0, 1); nt.set_ylim(0, 1)
    nt.text(0.0, 0.96, "NOTES", fontsize=11, fontweight="bold",
            color=INK, va="top")
    notes = [
        "1.  LAYERED structure in the middle: a horizontal shelf splits the central section into upper and lower tiers. Full-height on both ends only.",
        "2.  UPPER TIER = removable pull-out trays. Each tray has a finger-hole on the front; grab it, slide the tray straight toward you to use, slide it back when done. Trays are open-top boxes with no lids.",
        "3.  LOWER TIER = one open tray running the full middle length. Only light partitions (half-height), no lids. For small loose items that don't earn a dedicated tray (coins, keys, bands, pushpins, toothpicks, U-clips, coasters). Rake things forward with your hand.",
        "4.  LEFT END = full-height upright slot for visiting cards. RIGHT END = full-height column for the 3 stacked calculators.",
        "5.  Pull-out trays slide on wooden rails inside the carcase. Each tray is 6 mm MDF (or 3 mm acrylic). Carcase and shelf are 12 mm MDF.",
        "6.  Widths are provisional. Build a cardboard mock-up and let the trays find their final widths through use.",
    ]
    for i, n in enumerate(notes):
        nt.text(0.0, 0.86 - i * 0.14, n, fontsize=8.2,
                color=INK, va="top")

    out = Path(__file__).parent.parent / "PDF" / "organizer_v4_plan.pdf"
    fig.savefig(out, dpi=200, facecolor=PAPER)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    draw()

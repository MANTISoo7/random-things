"""Multi-view PNG renders of each STL (front + top + two zoomed iso)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def load_stl(path):
    with open(path, "rb") as f:
        f.read(80)
        count = int.from_bytes(f.read(4), "little")
        data = f.read(count * 50)
    tri = np.zeros((count, 3, 3), dtype=np.float32)
    buf = np.frombuffer(data, dtype=np.uint8).reshape(count, 50)
    verts = buf[:, 12:48].copy().view(np.float32).reshape(count, 3, 3)
    tri[:] = verts
    return tri


def _draw(ax, tris, elev, azim, bounds, title):
    poly = Poly3DCollection(tris, linewidths=0.08,
                            edgecolor=(0.3, 0.25, 0.2),
                            facecolor=(0.88, 0.74, 0.56), alpha=1.0)
    ax.add_collection3d(poly)
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)
    ax.set_box_aspect([xmax - xmin, ymax - ymin, zmax - zmin])
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=10, pad=4)


def render(stl_path, out_png, title):
    tris = load_stl(stl_path)
    pts = tris.reshape(-1, 3)
    mins, maxs = pts.min(0), pts.max(0)
    full = [(mins[0], maxs[0]), (mins[1], maxs[1]), (mins[2], maxs[2])]
    # Zoomed section: just the right third (last ~18")
    xcut = mins[0] + (maxs[0] - mins[0]) * 0.65
    right = [(xcut, maxs[0]), (mins[1], maxs[1]), (mins[2], maxs[2])]
    # Zoomed section: left third
    xcut2 = mins[0] + (maxs[0] - mins[0]) * 0.35
    left = [(mins[0], xcut2), (mins[1], maxs[1]), (mins[2], maxs[2])]

    fig = plt.figure(figsize=(16, 12), dpi=130,
                     facecolor=(0.96, 0.95, 0.93))
    fig.suptitle(title, fontsize=15, y=0.98)

    # Row 1: full front view (looking at open -Y face), tall thin
    ax1 = fig.add_subplot(3, 1, 1, projection="3d")
    _draw(ax1, tris, elev=0, azim=-90, bounds=full,
          title='Full front view (open face)')

    # Row 2: full top-down view
    ax2 = fig.add_subplot(3, 1, 2, projection="3d")
    _draw(ax2, tris, elev=89, azim=-90, bounds=full,
          title='Top view (looking down into open front)')

    # Row 3: two zoomed iso details
    ax3 = fig.add_subplot(3, 2, 5, projection="3d")
    _draw(ax3, tris, elev=25, azim=-65, bounds=left,
          title='Left end detail (iso)')

    ax4 = fig.add_subplot(3, 2, 6, projection="3d")
    _draw(ax4, tris, elev=25, azim=-65, bounds=right,
          title='Right end detail (iso)')

    plt.tight_layout()
    plt.savefig(out_png, dpi=130, bbox_inches="tight",
                facecolor=(0.96, 0.95, 0.93))
    plt.close(fig)
    print(f"wrote {out_png}")


if __name__ == "__main__":
    pairs = [
        ("../STL/organizer_D_hybrid.stl",
         "../images/organizer_D_hybrid.png",
         'Option D — Hybrid organizer   53" × 9" × 6"   (open front, under-shelf)'),
        ("../STL/organizer_B_tilt.stl",
         "../images/organizer_B_tilt.png",
         'Option B — Tilt-forward bins   53" × 9" × 6"   (open front, under-shelf)'),
    ]
    for stl_path, png_path, title in pairs:
        render(stl_path, png_path, title)

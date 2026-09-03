# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SCPN Magnetic Cusp Core — repository header artwork generator

"""Generate the three README header images (1280x640) for this repository.

Every image is original generated artwork derived from this repository's
own domain surface — the spindle cusp with its defining central field
null, the two owned coil classes, and the minimum-B magnitude map. The
cusp field is computed from an opposed two-dimensional dipole pair, not
hand-drawn. The right-hand text panel states only facts backed by the
repository itself.

Outputs (written next to this script):

- ``repo_header.png`` — the spindle cusp with streamlines, the central
  null and the point/line cusps (used by ``README.md``).
- ``repo_header_cusp_classes.png`` — spindle pair versus the
  picket-fence alternating array.
- ``repo_header_minimum_b.png`` — the minimum-B magnitude map around
  the central null.

Generation-time tooling only: requires ``numpy`` and ``matplotlib``,
which are deliberately not part of the pinned development lock. Run as
``python3 docs/assets/generate_header.py`` from the repository root.
The output is deterministic (fixed geometry, no random input).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

OUT_DIR = Path(__file__).resolve().parent

BG = "#00050a"
CYAN = "#00ccff"
MAGENTA = "#ff00ff"
STEEL = "#334466"
PROBE = "#66aaff"
RED = "#ff3366"

WIDTH_IN, HEIGHT_IN, DPI = 12.8, 6.4, 100

TITLE_METRICS: list[tuple[str, str]] = [
    ("Device Configuration", "cusp · spindle + picket_fence classes"),
    ("Hard Invariant", "opposed neighbour currents · central null"),
    ("Class Rules", "spindle = 2 coils · picket even, >= 4"),
    ("Spindle Window", "separation/radius outside window flagged"),
    ("Plan Envelope", "v1.1.0 · synthetic · review-only"),
    ("Quality Gates", "100% branch cov · mypy --strict"),
]


def _pyplot() -> Any:
    """Return pyplot configured for headless Agg rendering."""
    import matplotlib as mpl

    mpl.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def _glow_cmap() -> Any:
    """Build the family glow colormap (deep navy to cyan)."""
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list(
        "scpn_glow",
        ["#00050a", "#001428", "#002d55", "#005588", "#0088bb", "#00ccff"],
    )


def spindle_field(
    nx: int = 240,
    nz: int = 240,
    span_x: float = 2.6,
    span_z: float = 2.6,
    separation: float = 1.35,
) -> tuple[Any, Any, Any, Any]:
    """Return the field of two opposed two-dimensional dipoles."""
    x = np.linspace(-span_x, span_x, nx)
    z = np.linspace(-span_z, span_z, nz)
    mesh_x, mesh_z = np.meshgrid(x, z)

    def dipole(z_centre: float, sign: float) -> tuple[Any, Any]:
        dx, dz = mesh_x, mesh_z - z_centre
        r2 = dx**2 + dz**2 + 0.04
        return sign * 2 * dx * dz / r2**2, sign * (dz**2 - dx**2) / r2**2

    bx1, bz1 = dipole(+separation, +1.0)
    bx2, bz2 = dipole(-separation, -1.0)
    return mesh_x, mesh_z, bx1 + bx2, bz1 + bz2


def _text_panel(fig: Any, subtitle: str) -> None:
    """Draw the family right-hand text panel onto ``fig``."""
    ax = fig.add_axes([0.62, 0.0, 0.38, 1.0], facecolor=BG)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(
        0.08,
        0.84,
        "SCPN",
        color="white",
        fontsize=36,
        fontweight="bold",
        fontfamily="monospace",
        alpha=0.95,
    )
    ax.text(
        0.08,
        0.74,
        "MAGNETIC CUSP",
        color="white",
        fontsize=25,
        fontweight="bold",
        fontfamily="monospace",
        alpha=0.95,
    )
    ax.text(
        0.08,
        0.69,
        "CORE",
        color="white",
        fontsize=25,
        fontweight="bold",
        fontfamily="monospace",
        alpha=0.95,
    )
    ax.text(
        0.08,
        0.63,
        subtitle,
        color=CYAN,
        fontsize=11,
        fontfamily="monospace",
        alpha=0.85,
    )
    ax.plot([0.08, 0.85], [0.59, 0.59], color=STEEL, lw=0.8, alpha=0.5)
    y = 0.53
    for label, value in TITLE_METRICS:
        ax.text(
            0.08,
            y,
            f"▸ {label}",
            color="#6688aa",
            fontsize=9,
            fontfamily="monospace",
            alpha=0.9,
        )
        ax.text(
            0.10,
            y - 0.030,
            value,
            color="#99bbdd",
            fontsize=8,
            fontfamily="monospace",
            alpha=0.7,
        )
        y -= 0.072
    ax.text(
        0.08,
        0.06,
        "© 1996–2026 Miroslav Šotek",
        color="#445566",
        fontsize=7,
        fontfamily="monospace",
        alpha=0.6,
    )
    ax.text(
        0.08,
        0.03,
        "anulum.li | AGPL-3.0",
        color="#445566",
        fontsize=7,
        fontfamily="monospace",
        alpha=0.5,
    )


def _art_axes(fig: Any) -> Any:
    """Return the borderless left-hand art axes of ``fig``."""
    ax = fig.add_axes([0.0, 0.0, 0.68, 1.0], facecolor=BG)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    return ax


def _save(fig: Any, plt: Any, name: str) -> None:
    """Save ``fig`` to ``name`` inside the assets directory and close it."""
    target = OUT_DIR / name
    fig.savefig(target, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"generated {target}")


def generate_spindle_cusp() -> None:
    """Generate ``repo_header.png``: the spindle cusp with streamlines."""
    plt = _pyplot()
    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI, facecolor=BG)
    ax = _art_axes(fig)
    ax.set_xlim(-2.9, 2.9)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal")

    mesh_x, mesh_z, b_x, b_z = spindle_field(
        nx=320, nz=200, span_x=2.9, span_z=1.45, separation=0.85
    )
    magnitude = np.sqrt(b_x**2 + b_z**2)
    ax.contourf(
        mesh_x,
        mesh_z,
        np.log10(magnitude + 1e-3),
        levels=30,
        cmap=_glow_cmap(),
        alpha=0.8,
    )
    ax.streamplot(
        mesh_x,
        mesh_z,
        b_x,
        b_z,
        color=CYAN,
        linewidth=0.6,
        density=1.1,
        arrowsize=0.6,
    )

    for coil_z, marks in [(+0.85, ("x", "o")), (-0.85, ("o", "x"))]:
        for coil_x, mark in zip((-0.62, 0.62), marks, strict=True):
            ax.plot(
                coil_x,
                coil_z,
                mark,
                color=MAGENTA,
                ms=9,
                mew=2.0,
                alpha=0.95,
            )
    ax.text(
        -1.15,
        0.85,
        "opposed coil pair",
        color=MAGENTA,
        fontsize=8,
        fontfamily="monospace",
        ha="right",
        alpha=0.9,
    )

    ax.plot(0, 0, "o", color="white", ms=6, mfc="none", mew=1.5, alpha=0.95)
    ax.text(
        0.12,
        -0.16,
        "B = 0",
        color="white",
        fontsize=8.5,
        fontfamily="monospace",
        alpha=0.9,
    )

    for cusp_z in (1.32, -1.32):
        ax.annotate(
            "",
            xy=(0, cusp_z),
            xytext=(0, cusp_z - np.sign(cusp_z) * 0.3),
            arrowprops={"arrowstyle": "->", "color": RED, "lw": 1.2, "alpha": 0.85},
        )
    ax.text(
        0.16,
        1.18,
        "point cusp",
        color=RED,
        fontsize=7.5,
        fontfamily="monospace",
        alpha=0.9,
    )
    for cusp_x in (2.45, -2.45):
        ax.annotate(
            "",
            xy=(cusp_x + np.sign(cusp_x) * 0.32, 0),
            xytext=(cusp_x, 0),
            arrowprops={"arrowstyle": "->", "color": RED, "lw": 1.2, "alpha": 0.85},
        )
    ax.text(
        1.95,
        0.14,
        "line cusp",
        color=RED,
        fontsize=7.5,
        fontfamily="monospace",
        alpha=0.9,
    )

    ax.text(
        0,
        -1.36,
        "spindle cusp · defining central field null (Berkowitz et al., 1958)",
        color="#445566",
        fontsize=7.5,
        fontfamily="monospace",
        ha="center",
    )
    _text_panel(fig, "Opposed Currents, Central Null")
    _save(fig, plt, "repo_header.png")


def generate_cusp_classes() -> None:
    """Generate ``repo_header_cusp_classes.png``: the two coil classes."""
    plt = _pyplot()
    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI, facecolor=BG)
    ax = _art_axes(fig)
    ax.set_xlim(0, 10)
    ax.set_ylim(-3.2, 3.2)

    mesh_x, mesh_z, b_x, b_z = spindle_field(
        nx=170, nz=200, span_x=2.35, span_z=3.4, separation=0.8
    )
    magnitude = np.sqrt(b_x**2 + b_z**2)
    ax.contourf(
        mesh_x + 2.4,
        mesh_z,
        np.log10(magnitude + 1e-3),
        levels=24,
        cmap=_glow_cmap(),
        alpha=0.75,
    )
    for coil_z, mark in [(+1.12, "x"), (-0.72, "o")]:
        for coil_x in (-0.71, 0.71):
            resolved = mark if coil_x < 0 else ("o" if mark == "x" else "x")
            ax.plot(
                2.4 + coil_x,
                coil_z,
                resolved,
                color=MAGENTA,
                ms=8,
                mew=1.9,
                alpha=0.95,
            )
    ax.plot(2.4, 0.2, "o", color="white", ms=5, mfc="none", mew=1.3, alpha=0.95)
    ax.text(
        2.4,
        2.0,
        "spindle · exactly one opposed pair",
        color="#99bbdd",
        fontsize=8.5,
        fontfamily="monospace",
        ha="center",
        alpha=0.95,
    )
    ax.text(
        2.4,
        -2.5,
        "separation/radius window checked",
        color="#445566",
        fontsize=7.5,
        fontfamily="monospace",
        ha="center",
    )

    coil_positions = np.linspace(5.8, 8.8, 6)
    for index, coil_x in enumerate(coil_positions):
        mark = "x" if index % 2 == 0 else "o"
        ax.plot(coil_x, 1.05, mark, color=MAGENTA, ms=8, mew=1.9, alpha=0.95)
        ax.plot(
            coil_x,
            -1.05,
            "o" if mark == "x" else "x",
            color=MAGENTA,
            ms=8,
            mew=1.9,
            alpha=0.95,
        )
    for index in range(len(coil_positions) - 1):
        midpoint = (coil_positions[index] + coil_positions[index + 1]) / 2
        along = np.linspace(-1, 1, 100)
        for sign in (+1, -1):
            ax.plot(
                midpoint + sign * 0.28 * np.sinh(1.4 * along) / np.sinh(1.4),
                along * 0.95,
                color=CYAN,
                lw=0.8,
                alpha=0.6,
            )
    ax.text(
        7.3,
        2.0,
        "picket_fence · even array (>= 4)",
        color="#99bbdd",
        fontsize=8.5,
        fontfamily="monospace",
        ha="center",
        alpha=0.95,
    )
    ax.text(
        7.3,
        -2.5,
        "opposed neighbour currents · hard invariant",
        color="#445566",
        fontsize=7.5,
        fontfamily="monospace",
        ha="center",
    )

    ax.plot([4.75, 4.75], [-2.4, 2.4], color=STEEL, lw=0.8, alpha=0.4)
    _text_panel(fig, "Two Cusp Classes, One Owner")
    _save(fig, plt, "repo_header_cusp_classes.png")


def generate_minimum_b() -> None:
    """Generate ``repo_header_minimum_b.png``: the magnitude map."""
    plt = _pyplot()
    fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI, facecolor=BG)
    ax = _art_axes(fig)
    ax.set_xlim(-2.9, 2.9)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal")

    mesh_x, mesh_z, b_x, b_z = spindle_field(
        nx=360, nz=220, span_x=2.9, span_z=1.45, separation=0.85
    )
    magnitude = np.sqrt(b_x**2 + b_z**2)
    ax.contourf(
        mesh_x,
        mesh_z,
        np.log10(magnitude + 3e-3),
        levels=40,
        cmap=_glow_cmap(),
        alpha=0.95,
    )
    ax.contour(
        mesh_x,
        mesh_z,
        np.log10(magnitude + 3e-3),
        levels=10,
        colors=PROBE,
        linewidths=0.5,
        alpha=0.4,
    )

    ax.plot(0, 0, "o", color="white", ms=7, mfc="none", mew=1.6, alpha=0.95)
    ax.annotate(
        "minimum-B · stability by geometry",
        xy=(0.05, -0.05),
        xytext=(-2.75, -1.0),
        color="white",
        fontsize=8.5,
        fontfamily="monospace",
        alpha=0.9,
        arrowprops={"arrowstyle": "->", "color": "white", "lw": 0.9, "alpha": 0.6},
    )
    for coil_z, mark in [(+0.85, "x"), (-0.85, "o")]:
        for coil_x in (-0.62, 0.62):
            resolved = mark if coil_x < 0 else ("o" if mark == "x" else "x")
            ax.plot(
                coil_x,
                coil_z,
                resolved,
                color=MAGENTA,
                ms=9,
                mew=2.0,
                alpha=0.95,
            )

    ax.text(
        0,
        -1.36,
        "|B| rises away from the null in every direction · declared "
        "drive, derived null",
        color="#445566",
        fontsize=7.5,
        fontfamily="monospace",
        ha="center",
    )
    _text_panel(fig, "The Null Is The Device")
    _save(fig, plt, "repo_header_minimum_b.png")


if __name__ == "__main__":
    generate_spindle_cusp()
    generate_cusp_classes()
    generate_minimum_b()

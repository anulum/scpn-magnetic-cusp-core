# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SCPN Magnetic Cusp Core — parameter model tests

"""Every validation branch of the magnetic-cusp parameter model.

All parameter sets in this module are synthetic fixtures; none describes
any real machine.
"""

from __future__ import annotations

import math
from typing import Any

import pytest

from scpn_magnetic_cusp_core.errors import DeviceConfigurationError
from scpn_magnetic_cusp_core.parameters import (
    MU0,
    CoilDrive,
    CuspGeometry,
    loop_axis_field_t,
    require_finite,
    require_positive,
)


def synthetic_geometry(**overrides: Any) -> CuspGeometry:
    """Build a valid synthetic spindle geometry with optional overrides."""
    values: dict[str, Any] = {
        "kind": "spindle",
        "coil_count": 2,
        "coil_radius_m": 0.4,
        "coil_separation_m": 0.6,
    }
    values.update(overrides)
    return CuspGeometry(**values)


def test_require_finite_accepts_and_rejects() -> None:
    """The finite guard returns the value and rejects NaN and infinity."""
    assert require_finite("x", 1.5) == 1.5
    for bad in (math.nan, math.inf, -math.inf):
        with pytest.raises(DeviceConfigurationError, match="x: must be finite"):
            require_finite("x", bad)


def test_require_positive_accepts_and_rejects() -> None:
    """The positive guard returns the value and rejects zero and below."""
    assert require_positive("x", 0.1) == 0.1
    for bad in (0.0, -2.0):
        with pytest.raises(DeviceConfigurationError, match="strictly positive"):
            require_positive("x", bad)
    with pytest.raises(DeviceConfigurationError, match="must be finite"):
        require_positive("x", math.nan)


def test_loop_axis_field_formula() -> None:
    """The loop field follows the standard on-axis formula."""
    value = loop_axis_field_t(10.0, 0.4, 0.3)
    expected = MU0 * 10.0e3 * 0.4**2 / (2.0 * (0.4**2 + 0.3**2) ** 1.5)
    assert value == pytest.approx(expected)
    centre = loop_axis_field_t(10.0, 0.4, 0.0)
    assert centre == pytest.approx(MU0 * 10.0e3 / (2.0 * 0.4))


def test_loop_axis_field_rejects_bad_arguments() -> None:
    """The loop-field helper validates its arguments."""
    with pytest.raises(DeviceConfigurationError, match="current_ka"):
        loop_axis_field_t(0.0, 0.4, 0.0)
    with pytest.raises(DeviceConfigurationError, match="radius_m"):
        loop_axis_field_t(10.0, -0.4, 0.0)
    with pytest.raises(DeviceConfigurationError, match="axial_m"):
        loop_axis_field_t(10.0, 0.4, math.nan)


def test_valid_geometries_and_ratio() -> None:
    """Both cusp classes construct and derive the separation ratio."""
    spindle = synthetic_geometry()
    fence = synthetic_geometry(kind="picket_fence", coil_count=6)
    assert spindle.separation_ratio == pytest.approx(1.5)
    assert fence.coil_count == 6


@pytest.mark.parametrize(
    ("overrides", "fragment"),
    [
        ({"kind": "ring"}, "kind"),
        ({"coil_count": 3}, "spindle requires exactly"),
        ({"kind": "picket_fence", "coil_count": 2}, "picket_fence requires"),
        ({"kind": "picket_fence", "coil_count": 5}, "picket_fence requires"),
        ({"coil_radius_m": 0.0}, "coil_radius_m"),
        ({"coil_separation_m": -1.0}, "coil_separation_m"),
    ],
)
def test_invalid_geometry_is_rejected(overrides: dict[str, Any], fragment: str) -> None:
    """Each cusp-geometry violation is rejected with its field name."""
    with pytest.raises(DeviceConfigurationError, match=fragment):
        synthetic_geometry(**overrides)


def test_valid_drive_constructs() -> None:
    """A valid opposed-current drive constructs unchanged."""
    drive = CoilDrive(coil_current_ka=10.0, opposed_neighbour_currents=True)
    assert drive.coil_current_ka == 10.0


def test_invalid_drive_is_rejected() -> None:
    """Non-positive current and co-directed currents are rejected."""
    with pytest.raises(DeviceConfigurationError, match="coil_current_ka"):
        CoilDrive(coil_current_ka=0.0, opposed_neighbour_currents=True)
    with pytest.raises(DeviceConfigurationError, match="opposed"):
        CoilDrive(coil_current_ka=10.0, opposed_neighbour_currents=False)

# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SCPN Magnetic Cusp Core — cusp parameter model

"""Validated parameter objects of a magnetic-cusp configuration.

The derived quantity implements one standard result and nothing more:
the on-axis field of a circular current loop
``B(z) = mu0 I R^2 / (2 (R^2 + z^2)^{3/2})`` (standard magnetostatics),
used to evaluate the spindle-pair field at a coil plane. It is a rough
consistency instrument with documented applicability bounds; no claim
about any real machine follows from it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

from scpn_magnetic_cusp_core.errors import DeviceConfigurationError

CUSP_KINDS: Final = ("picket_fence", "spindle")
SPINDLE_COIL_COUNT: Final = 2
PICKET_FENCE_MIN_COILS: Final = 4
MU0: Final = 4.0e-7 * math.pi


def require_finite(name: str, value: float) -> float:
    """Return ``value`` when finite, otherwise fail closed.

    Parameters
    ----------
    name
        Field name reported in the rejection message.
    value
        Value under validation.

    Returns
    -------
    float
        The validated value.

    Raises
    ------
    DeviceConfigurationError
        If ``value`` is NaN or infinite; non-finite input is rejected,
        never clamped.
    """
    if not math.isfinite(value):
        raise DeviceConfigurationError(f"{name}: must be finite, got {value!r}")
    return value


def require_positive(name: str, value: float) -> float:
    """Return ``value`` when finite and strictly positive.

    Parameters
    ----------
    name
        Field name reported in the rejection message.
    value
        Value under validation.

    Returns
    -------
    float
        The validated value.

    Raises
    ------
    DeviceConfigurationError
        If ``value`` is non-finite or not strictly positive.
    """
    require_finite(name, value)
    if value <= 0.0:
        raise DeviceConfigurationError(
            f"{name}: must be strictly positive, got {value!r}"
        )
    return value


def loop_axis_field_t(current_ka: float, radius_m: float, axial_m: float) -> float:
    """On-axis field of one circular loop.

    Parameters
    ----------
    current_ka
        Loop current in kiloamperes; strictly positive.
    radius_m
        Loop radius in metres; strictly positive.
    axial_m
        Axial distance from the loop plane in metres; finite.

    Returns
    -------
    float
        ``B(z) = mu0 I R^2 / (2 (R^2 + z^2)^{3/2})`` in tesla.

    Raises
    ------
    DeviceConfigurationError
        If an argument violates its bound.
    """
    require_positive("current_ka", current_ka)
    require_positive("radius_m", radius_m)
    require_finite("axial_m", axial_m)
    current_a = current_ka * 1.0e3
    denominator = 2.0 * math.pow(radius_m**2 + axial_m**2, 1.5)
    return MU0 * current_a * radius_m**2 / denominator


@dataclass(frozen=True, slots=True)
class CuspGeometry:
    """Coil geometry of a magnetic-cusp configuration.

    Parameters
    ----------
    kind
        Cusp class: ``spindle`` (one opposed coil pair) or
        ``picket_fence`` (an even alternating array).
    coil_count
        Number of coils; exactly two for ``spindle``, an even count of
        at least four for ``picket_fence``.
    coil_radius_m
        Coil radius in metres; strictly positive.
    coil_separation_m
        Separation of neighbouring coil planes in metres; strictly
        positive.

    Raises
    ------
    DeviceConfigurationError
        If the kind is unknown or a class invariant is violated.
    """

    kind: str
    coil_count: int
    coil_radius_m: float
    coil_separation_m: float

    def __post_init__(self) -> None:
        """Validate the cusp-geometry class invariants.

        Raises
        ------
        DeviceConfigurationError
            If the kind is unknown or a class invariant is violated.
        """
        if self.kind not in CUSP_KINDS:
            raise DeviceConfigurationError(
                f"kind: must be one of {CUSP_KINDS!r}, got {self.kind!r}"
            )
        if self.kind == "spindle" and self.coil_count != SPINDLE_COIL_COUNT:
            raise DeviceConfigurationError(
                f"coil_count: spindle requires exactly {SPINDLE_COIL_COUNT} "
                f"coils, got {self.coil_count!r}"
            )
        if self.kind == "picket_fence" and (
            self.coil_count < PICKET_FENCE_MIN_COILS or self.coil_count % 2 != 0
        ):
            raise DeviceConfigurationError(
                "coil_count: picket_fence requires an even count of at "
                f"least {PICKET_FENCE_MIN_COILS}, got {self.coil_count!r}"
            )
        require_positive("coil_radius_m", self.coil_radius_m)
        require_positive("coil_separation_m", self.coil_separation_m)

    @property
    def separation_ratio(self) -> float:
        """Separation-to-radius ratio of neighbouring coils.

        Returns
        -------
        float
            ``d / R`` of the validated geometry.
        """
        return self.coil_separation_m / self.coil_radius_m


@dataclass(frozen=True, slots=True)
class CoilDrive:
    """Coil-drive parameters of a magnetic-cusp configuration.

    Parameters
    ----------
    coil_current_ka
        Current per coil in kiloamperes; strictly positive.
    opposed_neighbour_currents
        Must be true — the central field null produced by opposed
        neighbouring currents is the defining property of cusp
        confinement.

    Raises
    ------
    DeviceConfigurationError
        If the current is non-positive or the currents are not opposed.
    """

    coil_current_ka: float
    opposed_neighbour_currents: bool

    def __post_init__(self) -> None:
        """Validate the coil-drive invariants.

        Raises
        ------
        DeviceConfigurationError
            If the current is non-positive or the currents are not
            opposed.
        """
        require_positive("coil_current_ka", self.coil_current_ka)
        if not self.opposed_neighbour_currents:
            raise DeviceConfigurationError(
                "opposed_neighbour_currents: must be true — the cusp field "
                "null exists only for opposed neighbouring currents"
            )

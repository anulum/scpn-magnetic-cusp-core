# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SCPN Magnetic Cusp Core — device configuration container

"""Device configuration container bound to the SPO reactor registry.

A :class:`DeviceConfiguration` composes validated cusp geometry and coil
drive under the single registry identifier this repository owns. Opposed
neighbouring currents are a hard invariant (they create the defining
central field null; J. Berkowitz et al., 1958), the spindle class
carries exactly one opposed pair, and a spindle arrangement far from the
canonical separation-to-radius window is flagged. Serialisation is
canonical (sorted keys, no NaN or infinity accepted anywhere) and the
SHA-256 digest of those bytes identifies the exact parameter set. The
registry binding is a data pin only — this package never imports SCPN
Phase Orchestrator code.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Final

from scpn_magnetic_cusp_core.errors import DeviceConfigurationError
from scpn_magnetic_cusp_core.parameters import (
    CoilDrive,
    CuspGeometry,
    loop_axis_field_t,
)

OWNED_CONFIGURATIONS: Final = ("cusp",)
SPINDLE_RATIO_BOUNDS: Final = (0.5, 4.0)
HEX_DIGEST: Final = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class RegistryBinding:
    """Pin to one SPO reactor registry release.

    Parameters
    ----------
    version
        Registry release version; non-empty.
    digest_sha256
        Registry digest as 64 lowercase hexadecimal characters.

    Raises
    ------
    DeviceConfigurationError
        If either pin component is malformed.
    """

    version: str
    digest_sha256: str

    def __post_init__(self) -> None:
        """Validate the registry pin.

        Raises
        ------
        DeviceConfigurationError
            If either pin component is malformed.
        """
        if not self.version:
            raise DeviceConfigurationError("registry.version: must be non-empty")
        if HEX_DIGEST.fullmatch(self.digest_sha256) is None:
            raise DeviceConfigurationError(
                "registry.digest_sha256: must be 64 lowercase hexadecimal "
                f"characters, got {self.digest_sha256!r}"
            )


@dataclass(frozen=True, slots=True)
class ConsistencyFinding:
    """One internal-consistency finding on a device configuration.

    Parameters
    ----------
    field
        Dotted field path the finding refers to.
    message
        Human-readable statement of the inconsistency.
    """

    field: str
    message: str


@dataclass(frozen=True, slots=True)
class DeviceConfiguration:
    """Validated magnetic-cusp device configuration.

    Parameters
    ----------
    identifier
        SPO registry configuration identifier; must be ``cusp``.
    geometry
        Validated cusp geometry.
    drive
        Validated coil drive.
    registry
        Pin to the SPO reactor registry release the identifier belongs
        to.

    Raises
    ------
    DeviceConfigurationError
        If the identifier is not owned by this repository.
    """

    identifier: str
    geometry: CuspGeometry
    drive: CoilDrive
    registry: RegistryBinding

    def __post_init__(self) -> None:
        """Validate identifier ownership.

        Raises
        ------
        DeviceConfigurationError
            If the identifier is not owned by this repository.
        """
        if self.identifier not in OWNED_CONFIGURATIONS:
            raise DeviceConfigurationError(
                f"identifier: {self.identifier!r} is not owned by "
                f"SCPN-MAGNETIC-CUSP-CORE; owned: {OWNED_CONFIGURATIONS!r}"
            )

    def spindle_coil_plane_field_t(self) -> float:
        """Net on-axis field at one coil plane of the spindle pair.

        Returns
        -------
        float
            Own-loop field minus the opposed partner-loop contribution,
            both from the standard loop formula.

        Raises
        ------
        DeviceConfigurationError
            If the geometry is not the spindle class.
        """
        if self.geometry.kind != "spindle":
            raise DeviceConfigurationError(
                "geometry.kind: the coil-plane field helper applies to the "
                f"spindle class only, got {self.geometry.kind!r}"
            )
        own = loop_axis_field_t(
            self.drive.coil_current_ka, self.geometry.coil_radius_m, 0.0
        )
        partner = loop_axis_field_t(
            self.drive.coil_current_ka,
            self.geometry.coil_radius_m,
            self.geometry.coil_separation_m,
        )
        return own - partner

    def consistency_report(self) -> tuple[ConsistencyFinding, ...]:
        """Report physics-consistency findings without failing.

        Returns
        -------
        tuple of ConsistencyFinding
            Advisory findings from the documented bounds; empty when
            the declared geometry sits in the canonical arrangement.
            Findings are advisory instruments, not machine claims.
        """
        findings: list[ConsistencyFinding] = []
        if self.geometry.kind == "spindle":
            low, high = SPINDLE_RATIO_BOUNDS
            ratio = self.geometry.separation_ratio
            if not low <= ratio <= high:
                findings.append(
                    ConsistencyFinding(
                        field="geometry.coil_separation_m",
                        message=(
                            f"separation-to-radius ratio {ratio:.3f} is "
                            f"outside [{low}, {high}]; the arrangement "
                            "departs from the canonical spindle cusp"
                        ),
                    )
                )
        return tuple(findings)

    def to_record(self) -> dict[str, Any]:
        """Project the configuration to a JSON-serialisable record.

        Returns
        -------
        dict[str, Any]
            Nested record with every declared parameter.
        """
        return {
            "identifier": self.identifier,
            "geometry": {
                "kind": self.geometry.kind,
                "coil_count": self.geometry.coil_count,
                "coil_radius_m": self.geometry.coil_radius_m,
                "coil_separation_m": self.geometry.coil_separation_m,
            },
            "drive": {
                "coil_current_ka": self.drive.coil_current_ka,
                "opposed_neighbour_currents": (self.drive.opposed_neighbour_currents),
            },
            "registry": {
                "version": self.registry.version,
                "digest_sha256": self.registry.digest_sha256,
            },
        }

    def canonical_bytes(self) -> bytes:
        """Serialise the configuration canonically.

        Returns
        -------
        bytes
            UTF-8 JSON with sorted keys, minimal separators, and a
            trailing newline; NaN and infinity are never emitted.
        """
        text = json.dumps(
            self.to_record(),
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        return (text + "\n").encode("utf-8")

    def digest_sha256(self) -> str:
        """Identify the exact parameter set.

        Returns
        -------
        str
            SHA-256 digest of :meth:`canonical_bytes` as lowercase hex.
        """
        return hashlib.sha256(self.canonical_bytes()).hexdigest()


def _require_mapping(record: dict[str, Any], field: str) -> dict[str, Any]:
    """Return one required mapping field of a record.

    Parameters
    ----------
    record
        Parent mapping under inspection.
    field
        Key that must hold a mapping.

    Returns
    -------
    dict[str, Any]
        The nested mapping.

    Raises
    ------
    DeviceConfigurationError
        If the field is missing or not a mapping.
    """
    value = record.get(field)
    if not isinstance(value, dict):
        raise DeviceConfigurationError(f"{field}: must be an object")
    return value


def _number(record: dict[str, Any], field: str) -> float:
    """Return one required real-number field of a record.

    Parameters
    ----------
    record
        Mapping under inspection.
    field
        Key that must hold a real number.

    Returns
    -------
    float
        The numeric value; booleans are rejected.

    Raises
    ------
    DeviceConfigurationError
        If the field is missing or not a real number.
    """
    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise DeviceConfigurationError(f"{field}: must be a number, got {value!r}")
    return float(value)


def _integer(record: dict[str, Any], field: str) -> int:
    """Return one required integer field of a record.

    Parameters
    ----------
    record
        Mapping under inspection.
    field
        Key that must hold an integer.

    Returns
    -------
    int
        The integer value; booleans are rejected.

    Raises
    ------
    DeviceConfigurationError
        If the field is missing or not an integer.
    """
    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, int):
        raise DeviceConfigurationError(f"{field}: must be an integer, got {value!r}")
    return value


def _boolean(record: dict[str, Any], field: str) -> bool:
    """Return one required boolean field of a record.

    Parameters
    ----------
    record
        Mapping under inspection.
    field
        Key that must hold a boolean.

    Returns
    -------
    bool
        The boolean value.

    Raises
    ------
    DeviceConfigurationError
        If the field is missing or not a boolean.
    """
    value = record.get(field)
    if not isinstance(value, bool):
        raise DeviceConfigurationError(f"{field}: must be a boolean, got {value!r}")
    return value


def _string(record: dict[str, Any], field: str) -> str:
    """Return one required string field of a record.

    Parameters
    ----------
    record
        Mapping under inspection.
    field
        Key that must hold a string.

    Returns
    -------
    str
        The string value.

    Raises
    ------
    DeviceConfigurationError
        If the field is missing or not a string.
    """
    value = record.get(field)
    if not isinstance(value, str):
        raise DeviceConfigurationError(f"{field}: must be a string, got {value!r}")
    return value


def configuration_from_record(record: Any) -> DeviceConfiguration:
    """Build a validated configuration from a decoded record.

    Parameters
    ----------
    record
        Decoded JSON object in the shape produced by
        :meth:`DeviceConfiguration.to_record`.

    Returns
    -------
    DeviceConfiguration
        The fully validated configuration.

    Raises
    ------
    DeviceConfigurationError
        If the record shape or any value violates the model.
    """
    if not isinstance(record, dict):
        raise DeviceConfigurationError("record: must be an object")
    known = {"identifier", "geometry", "drive", "registry"}
    unknown = sorted(set(record) - known)
    if unknown:
        raise DeviceConfigurationError(f"record: unknown fields {unknown!r}")
    geometry = _require_mapping(record, "geometry")
    drive = _require_mapping(record, "drive")
    registry = _require_mapping(record, "registry")
    return DeviceConfiguration(
        identifier=_string(record, "identifier"),
        geometry=CuspGeometry(
            kind=_string(geometry, "kind"),
            coil_count=_integer(geometry, "coil_count"),
            coil_radius_m=_number(geometry, "coil_radius_m"),
            coil_separation_m=_number(geometry, "coil_separation_m"),
        ),
        drive=CoilDrive(
            coil_current_ka=_number(drive, "coil_current_ka"),
            opposed_neighbour_currents=_boolean(drive, "opposed_neighbour_currents"),
        ),
        registry=RegistryBinding(
            version=_string(registry, "version"),
            digest_sha256=_string(registry, "digest_sha256"),
        ),
    )


def configuration_from_bytes(data: bytes) -> DeviceConfiguration:
    """Build a validated configuration from canonical JSON bytes.

    Parameters
    ----------
    data
        UTF-8 JSON document; NaN and infinity literals are rejected.

    Returns
    -------
    DeviceConfiguration
        The fully validated configuration.

    Raises
    ------
    DeviceConfigurationError
        If the document is not valid strict JSON or violates the model.
    """

    def _reject_constant(literal: str) -> float:
        raise DeviceConfigurationError(
            f"record: non-finite JSON literal {literal!r} is rejected"
        )

    try:
        record = json.loads(data.decode("utf-8"), parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DeviceConfigurationError(f"record: invalid JSON document: {exc}") from exc
    return configuration_from_record(record)

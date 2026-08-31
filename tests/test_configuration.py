# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SCPN Magnetic Cusp Core — device configuration container tests

"""Every branch of the device configuration container and its parsers.

All parameter sets in this module are synthetic fixtures; none describes
any real machine.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pytest

from scpn_magnetic_cusp_core.configuration import (
    DeviceConfiguration,
    RegistryBinding,
    configuration_from_bytes,
    configuration_from_record,
)
from scpn_magnetic_cusp_core.errors import DeviceConfigurationError
from scpn_magnetic_cusp_core.parameters import (
    CoilDrive,
    CuspGeometry,
    loop_axis_field_t,
)

REGISTRY = RegistryBinding(version="1.0.0", digest_sha256="0" * 64)


def synthetic_configuration(
    identifier: str = "cusp",
    kind: str = "spindle",
    coil_count: int = 2,
    coil_separation_m: float = 0.6,
) -> DeviceConfiguration:
    """Build a valid synthetic configuration with optional overrides."""
    return DeviceConfiguration(
        identifier=identifier,
        geometry=CuspGeometry(
            kind=kind,
            coil_count=coil_count,
            coil_radius_m=0.4,
            coil_separation_m=coil_separation_m,
        ),
        drive=CoilDrive(coil_current_ka=10.0, opposed_neighbour_currents=True),
        registry=REGISTRY,
    )


def test_registry_binding_rejects_bad_pins() -> None:
    """Malformed registry pins are rejected."""
    with pytest.raises(DeviceConfigurationError, match=r"registry\.version"):
        RegistryBinding(version="", digest_sha256="0" * 64)
    with pytest.raises(DeviceConfigurationError, match=r"registry\.digest_sha256"):
        RegistryBinding(version="1.0.0", digest_sha256="ZZ")


def test_owned_identifier_constructs() -> None:
    """The owned identifier constructs for both cusp classes."""
    assert synthetic_configuration().identifier == "cusp"
    fence = synthetic_configuration(kind="picket_fence", coil_count=6)
    assert fence.geometry.kind == "picket_fence"


def test_unowned_identifier_is_rejected() -> None:
    """Identifiers outside this repository's ownership are rejected."""
    with pytest.raises(DeviceConfigurationError, match="not owned"):
        synthetic_configuration("levitated_dipole")


def test_spindle_coil_plane_field() -> None:
    """The spindle helper subtracts the opposed partner contribution."""
    configuration = synthetic_configuration()
    own = loop_axis_field_t(10.0, 0.4, 0.0)
    partner = loop_axis_field_t(10.0, 0.4, 0.6)
    assert configuration.spindle_coil_plane_field_t() == pytest.approx(own - partner)


def test_spindle_helper_rejects_picket_fence() -> None:
    """The coil-plane helper applies to the spindle class only."""
    fence = synthetic_configuration(kind="picket_fence", coil_count=6)
    with pytest.raises(DeviceConfigurationError, match="spindle class only"):
        fence.spindle_coil_plane_field_t()


def test_consistency_report_clean_and_finding() -> None:
    """The report is empty in the canonical window and precise outside."""
    assert synthetic_configuration().consistency_report() == ()
    stretched = synthetic_configuration(coil_separation_m=2.0)
    findings = stretched.consistency_report()
    assert len(findings) == 1
    assert "canonical spindle" in findings[0].message
    fence = synthetic_configuration(
        kind="picket_fence", coil_count=6, coil_separation_m=2.0
    )
    assert fence.consistency_report() == ()


def test_canonical_round_trip_and_digest() -> None:
    """Canonical bytes round-trip losslessly and digest deterministically."""
    configuration = synthetic_configuration()
    data = configuration.canonical_bytes()
    assert data.endswith(b"\n")
    restored = configuration_from_bytes(data)
    assert restored == configuration
    expected = hashlib.sha256(data).hexdigest()
    assert configuration.digest_sha256() == expected


def test_from_record_round_trip_both_classes() -> None:
    """Both cusp classes round-trip through records."""
    for configuration in (
        synthetic_configuration(),
        synthetic_configuration(kind="picket_fence", coil_count=6),
    ):
        assert configuration_from_record(configuration.to_record()) == configuration


@pytest.mark.parametrize(
    ("mutate", "fragment"),
    [
        (lambda _: "not-a-dict", "record: must be an object"),
        (lambda r: {**r, "extra": 1}, "unknown fields"),
        (lambda r: {**r, "geometry": None}, "geometry: must be an object"),
        (lambda r: {**r, "drive": []}, "drive: must be an object"),
        (lambda r: {**r, "registry": 7}, "registry: must be an object"),
        (lambda r: {**r, "identifier": 3}, "identifier: must be a string"),
    ],
)
def test_from_record_shape_violations(mutate: Any, fragment: str) -> None:
    """Each record-shape violation is rejected with a precise message."""
    record = synthetic_configuration().to_record()
    with pytest.raises(DeviceConfigurationError, match=fragment):
        configuration_from_record(mutate(record))


def test_from_record_field_type_violations() -> None:
    """Nested field-type violations name the offending field."""
    record = synthetic_configuration().to_record()
    record["geometry"]["kind"] = 5
    with pytest.raises(DeviceConfigurationError, match="kind: must be a string"):
        configuration_from_record(record)
    record = synthetic_configuration().to_record()
    record["geometry"]["coil_count"] = 2.5
    with pytest.raises(DeviceConfigurationError, match="coil_count: must be"):
        configuration_from_record(record)
    record = synthetic_configuration().to_record()
    record["geometry"]["coil_count"] = True
    with pytest.raises(DeviceConfigurationError, match="coil_count: must be"):
        configuration_from_record(record)
    record = synthetic_configuration().to_record()
    record["drive"]["coil_current_ka"] = True
    with pytest.raises(DeviceConfigurationError, match="coil_current_ka: must be"):
        configuration_from_record(record)
    record = synthetic_configuration().to_record()
    record["drive"]["opposed_neighbour_currents"] = "yes"
    with pytest.raises(
        DeviceConfigurationError, match="opposed_neighbour_currents: must be"
    ):
        configuration_from_record(record)
    record = synthetic_configuration().to_record()
    record["registry"]["version"] = None
    with pytest.raises(DeviceConfigurationError, match="version: must be a string"):
        configuration_from_record(record)


def test_from_bytes_rejects_invalid_documents() -> None:
    """Invalid UTF-8, invalid JSON, and non-finite literals are rejected."""
    with pytest.raises(DeviceConfigurationError, match="invalid JSON document"):
        configuration_from_bytes(b"\xff\xfe")
    with pytest.raises(DeviceConfigurationError, match="invalid JSON document"):
        configuration_from_bytes(b"{not json")
    record = synthetic_configuration().to_record()
    text = json.dumps(record).replace("0.4", "NaN", 1)
    with pytest.raises(DeviceConfigurationError, match="non-finite JSON literal"):
        configuration_from_bytes(text.encode("utf-8"))


def test_integer_accepted_where_number_expected() -> None:
    """Integral JSON numbers are accepted for real-valued fields."""
    record = synthetic_configuration().to_record()
    record["drive"]["coil_current_ka"] = 10
    restored = configuration_from_record(record)
    assert restored.drive.coil_current_ka == 10.0

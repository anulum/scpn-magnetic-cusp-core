# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SCPN Magnetic Cusp Core — device configuration model package

"""Device configuration model of the SCPN magnetic-cusp device family.

Public surface of the ``device_configuration_model`` capability at
``computational_prototype`` maturity: validated parameter objects,
documented consistency estimates, canonical serialisation with SHA-256
digests, and a data-only pin to the SPO reactor registry. No claim about
any real machine is made anywhere in this package.
"""

from __future__ import annotations

from typing import Final

from scpn_magnetic_cusp_core.configuration import (
    OWNED_CONFIGURATIONS,
    SPINDLE_RATIO_BOUNDS,
    ConsistencyFinding,
    DeviceConfiguration,
    RegistryBinding,
    configuration_from_bytes,
    configuration_from_record,
)
from scpn_magnetic_cusp_core.errors import DeviceConfigurationError
from scpn_magnetic_cusp_core.parameters import (
    CUSP_KINDS,
    MU0,
    PICKET_FENCE_MIN_COILS,
    SPINDLE_COIL_COUNT,
    CoilDrive,
    CuspGeometry,
    loop_axis_field_t,
)

__version__: Final = "0.1.0.dev0"

__all__ = [
    "CUSP_KINDS",
    "MU0",
    "OWNED_CONFIGURATIONS",
    "PICKET_FENCE_MIN_COILS",
    "SPINDLE_COIL_COUNT",
    "SPINDLE_RATIO_BOUNDS",
    "CoilDrive",
    "ConsistencyFinding",
    "CuspGeometry",
    "DeviceConfiguration",
    "DeviceConfigurationError",
    "RegistryBinding",
    "__version__",
    "configuration_from_bytes",
    "configuration_from_record",
    "loop_axis_field_t",
]

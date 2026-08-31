# SPDX-License-Identifier: AGPL-3.0-or-later
# Commercial license available
# © Concepts 1996–2026 Miroslav Šotek. All rights reserved.
# © Code 2020–2026 Miroslav Šotek. All rights reserved.
# ORCID: 0009-0009-3560-0851
# Contact: www.anulum.li | protoscience@anulum.li
# SCPN Magnetic Cusp Core — device capability package

"""Device capability models of the SCPN magnetic-cusp device family.

Public surface of the ``device_configuration_model`` and
``diagnostic_clock_semantics`` capabilities at
``computational_prototype`` maturity: validated parameter objects,
synthetic diagnostic and clock declarations aligned with the pinned SPO
observability catalogue, documented consistency estimates, canonical
serialisation with SHA-256 digests, and data-only pins to the SPO
registries. No claim about any real machine or diagnostic is made
anywhere in this package.
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
from scpn_magnetic_cusp_core.errors import DeviceConfigurationError, DiagnosticPlanError
from scpn_magnetic_cusp_core.observability import (
    APPLICABLE_CANDIDATES,
    CATALOGUE_BINDING,
    CandidateProfile,
    ClockKind,
    ClockModel,
    ClockRelation,
    DeferredCandidate,
    DiagnosticChannelPlan,
    DiagnosticPlan,
    FrameKind,
    ObservabilityBinding,
    ObservabilityClass,
    ReferenceFrame,
    SemanticCarrier,
    plan_from_bytes,
    plan_from_record,
)
from scpn_magnetic_cusp_core.parameters import (
    CUSP_KINDS,
    MU0,
    PICKET_FENCE_MIN_COILS,
    SPINDLE_COIL_COUNT,
    CoilDrive,
    CuspGeometry,
    loop_axis_field_t,
)
from scpn_magnetic_cusp_core.plan_envelope import (
    PlanEnvelope,
    envelope_for_plan,
    envelope_from_bytes,
    envelope_from_record,
    verify_envelope,
)

__version__: Final = "0.1.0.dev0"

__all__ = [
    "APPLICABLE_CANDIDATES",
    "CATALOGUE_BINDING",
    "CUSP_KINDS",
    "MU0",
    "OWNED_CONFIGURATIONS",
    "PICKET_FENCE_MIN_COILS",
    "SPINDLE_COIL_COUNT",
    "SPINDLE_RATIO_BOUNDS",
    "CandidateProfile",
    "ClockKind",
    "ClockModel",
    "ClockRelation",
    "CoilDrive",
    "ConsistencyFinding",
    "CuspGeometry",
    "DeferredCandidate",
    "DeviceConfiguration",
    "DeviceConfigurationError",
    "DiagnosticChannelPlan",
    "DiagnosticPlan",
    "DiagnosticPlanError",
    "FrameKind",
    "ObservabilityBinding",
    "ObservabilityClass",
    "PlanEnvelope",
    "ReferenceFrame",
    "RegistryBinding",
    "SemanticCarrier",
    "__version__",
    "configuration_from_bytes",
    "configuration_from_record",
    "envelope_for_plan",
    "envelope_from_bytes",
    "envelope_from_record",
    "loop_axis_field_t",
    "plan_from_bytes",
    "plan_from_record",
    "verify_envelope",
]

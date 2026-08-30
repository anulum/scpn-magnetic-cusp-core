<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SCPN Magnetic Cusp Core — ADR 0001: repository boundary
-->

# ADR 0001 — Repository boundary and ownership

**Status:** accepted (2026-08-30)  
**Deciders:** project owner; SCPN Reactor Systems Research Group standard

## Context

The SCPN reactor portfolio assigns every built-in configuration of the SCPN
Phase Orchestrator reactor registry (version `1.0.0`, 32 configurations) to
exactly one device-family repository. The `cusp` configuration shares the
`magnetic_open` registry family with mirrors and the levitated dipole, and
shares field topology with the electrostatic Polywell; a boundary decision
was needed on all three edges.

## Decision

1. `SCPN-MAGNETIC-CUSP-CORE` owns exactly one registry configuration:
   `cusp` (magnetic cusp).
2. The repository owns device-level truth only: cusp-boundary
   configuration policy (spindle and picket-fence realisations,
   point/line-cusp loss apertures), lifecycle semantics with beta-collapse
   hazard records, cusp-frame diagnostic and clock declarations,
   actuator-response model boundaries, the safety-envelope declaration,
   and the device-owned CONTROL adapter specification.
3. The Polywell stays with `SCPN-IEC-CORE`: although the registry
   classifies it under the magnetic-open family for its cusp topology, the
   portfolio standard intentionally assigns it to the electrostatic owner
   because its device-level energy and reaction workflow is an
   electrostatic potential well. This repository owns purely magnetic cusp
   confinement.
4. Solver mathematics remains in `SCPN-FUSION-CORE` until an exact surface
   passes the family migration gate. No solver code is copied here.
5. Typed semantics remain in `SCPN-PHASE-ORCHESTRATOR` (review-only).
   Admission and `ControlAction` formation remain exclusively in
   `SCPN-CONTROL`. Machine protection remains independent with the final
   veto. Presentation remains in `SCPN-STUDIO`; this project is
   `not_federated`.
6. The repository starts, and remains until evidenced otherwise, at
   `architecture_only` with empty capability and claim inventories.

## Alternatives considered

- **Folding the cusp into the mirror repository** (both `magnetic_open`):
  rejected — the cusp's defining physics is the everywhere-convex
  opposed-field boundary with sheath-scale point/line loss apertures, not
  the axial mirror-force loss cone; drivers and diagnostics differ on
  surfaces 1, 2, and 4.
- **Owning the Polywell here** (shared cusp topology): rejected — the
  portfolio standard's explicit decision places device-level electrostatic
  workflow with `SCPN-IEC-CORE`; duplicating it here would give one
  registry configuration two owners.
- **Absorbing solver code at scaffold time**: rejected — violates the
  migration gate.

## Consequences

- Downstream consumers get one stable identity for magnetic-cusp
  confinement and a manifest to bind against.
- The validator fails on any capability or claim entry while maturity is
  `architecture_only`.
- Boundary changes require a portfolio-level map change first; a future
  ADR records any such change here.

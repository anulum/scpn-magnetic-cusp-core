<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SCPN Magnetic Cusp Core — Architecture summary
-->

# Architecture summary

`SCPN-MAGNETIC-CUSP-CORE` is the device-family owner for magnetic-cusp
systems inside the SCPN Reactor Systems Research Group. The repository holds two implemented capabilities at
`computational_prototype` — the device configuration model (ADR 0002)
and the diagnostic and clock semantics model (ADR 0003), both in
`src/scpn_magnetic_cusp_core/` — alongside the device boundary, its
ecosystem contracts, and the validation tooling that enforces both.

The authoritative architecture record is
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). The ownership decision and
its consequences are fixed in
[`docs/adr/0001-repository-boundary.md`](docs/adr/0001-repository-boundary.md).

Boundary in one paragraph: this repository owns magnetic-cusp plant and
experiment truth — configuration policy for opposed-field devices whose
point and line cusps form an everywhere-convex stable boundary with
sheath-scale loss apertures, lifecycle semantics with beta-collapse
records, cusp-frame diagnostic and clock declarations, actuator-response
boundaries, safety-envelope declarations, and the device-owned CONTROL
adapter specification. The electrostatic Polywell belongs to
`SCPN-IEC-CORE` by the portfolio standard's explicit decision; solver
mathematics stays in `SCPN-FUSION-CORE`; typed semantics stay in
`SCPN-PHASE-ORCHESTRATOR` (review-only); admitted control actions are
formed only by `SCPN-CONTROL`; independent machine protection keeps the
final veto; portfolio presentation belongs to `SCPN-STUDIO`, towards which
this project is `not_federated`.

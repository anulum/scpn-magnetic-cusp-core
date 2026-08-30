<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SCPN Magnetic Cusp Core — Architecture
-->

# Architecture

## Purpose and evidence state

`SCPN-MAGNETIC-CUSP-CORE` is the device-family owner for magnetic-cusp
systems in the SCPN Reactor Systems Research Group portfolio. The
repository is `architecture_only`: every section below describes boundaries
and contracts, not implemented capability. The capability and claim
inventories are empty; both derived artefacts are generated and
drift-checked.

## The five-surface boundary

1. **Governing confinement physics** — the `cusp` (magnetic cusp): plasma
   confined by opposed magnetic fields whose point and line cusps form an
   everywhere-convex, magnetohydrodynamically favourable boundary. The
   defining physics is the trade between that intrinsic stability and the
   cusp loss channels: narrow sheath-scale apertures at the point and line
   cusps whose effective width (ion-gyroradius versus hybrid-scale) sets
   confinement, with high-beta interior operation sharpening the boundary.
   Spindle-cusp and picket-fence realisations are configuration facets.
   Mirror machines (axial mirror-force confinement without opposed-field
   null regions), the electrostatic Polywell (potential-well confinement
   assisted by a cusp field), and the levitated dipole fail this sharing
   test and are excluded.
2. **Primary driver and energy delivery** — opposed-coil systems
   establishing the cusp field, with plasma-gun or gas-breakdown filling
   and auxiliary heating as configuration facets.
3. **Plant and shot lifecycle** — pulsed to quasi-steady lifecycle: field
   energisation, filling, confined high-beta phase governed by cusp-loss
   balance, and termination. Device-level hazard semantics cover
   beta-collapse (loss of the sharp-boundary regime) and coil-force
   excursions.
4. **Diagnostic, reference-frame, and clock model** — cusp-axis and
   midplane conventions, loss-aperture flux instrumentation at point and
   line cusps, boundary-sharpness (beta-regime) indicators, and
   pulse-relative clock identities.
5. **Solver, evidence, and control-contract boundary** — versioned seams
   towards `SCPN-FUSION-CORE`, review-only semantics towards
   `SCPN-PHASE-ORCHESTRATOR`, and the device-owned CONTROL adapter
   specification towards `SCPN-CONTROL`.

## Position in the SCPN ecosystem

```text
SCPN-MAGNETIC-CUSP-CORE (device truth: cusp-boundary policy, loss-aperture
                         semantics, lifecycle, safety envelope, adapter spec)
   │  optional versioned solver seams (none active)
   ├──────────────► SCPN-FUSION-CORE      (solver mathematics, evidence)
   │  typed review-only semantics
   ├──────────────► SCPN-PHASE-ORCHESTRATOR (semantics, comparability)
   │  device-owned adapter (specification only; no implementation)
   ├──────────────► SCPN-CONTROL          (admission; sole ControlAction author)
   │  derived portfolio descriptor (not_federated)
   └──────────────► SCPN-STUDIO           (catalogue, evidence UI, gating)

SCPN-CONTROL ──admitted ControlAction──► independent machine protection
                                          (final veto) ─► plant actuators
```

## Repository layout

| Path | Role |
|---|---|
| `reactor-domain.json` | portable source of project identity and contracts |
| `studio/portfolio-descriptor.json` | derived Studio descriptor, `not_federated` |
| `capability-inventory.json` | generated, truthfully empty inventory |
| `docs/CONTROL_ADAPTER_SPECIFICATION.md` | device-owned adapter contract |
| `docs/THREAT_MODEL.md` | assets, trust boundaries, misuse paths |
| `docs/adr/0001-repository-boundary.md` | boundary decision record |
| `tools/` | validators, derivation tools, preflight orchestrator |
| `tests/` | statement- and branch-complete tests for `tools/` |
| `.github/workflows/` | read-only CI definitions (no publication) |

## Contract surfaces and versioning

- `reactor-domain.json` follows schema `scpn.reactor-domain.v1`; unknown
  schemas are rejected by consumers.
- The Studio descriptor is derived deterministically and embeds the
  manifest's SHA-256; manual edits are detected as drift.
- The CONTROL adapter contract is specification-only at `0.1.0-spec`.
- SPO binding is fixed to reactor registry `1.0.0`, digest
  `786d9542ce76c56dd7748fa948b17efed6c073525e527ce90e6d5e29a2d00090`.

## Registry-family note

The registry classifies `cusp` under `magnetic_open`, and this repository
adopts that family. The neighbouring `polywell` shares the cusp topology in
the registry but is assigned to `SCPN-IEC-CORE` by the portfolio standard
because its device-level workflow is electrostatic; the machine-readable
map records this intentional distinction.

## What would change this architecture

Acceptance of a FUSION solver seam through the family migration gate,
ratification of an SPO `ControlIntent`-class contract, or Studio federation
after a real capability passes producer and consumer gates — each recorded
as a versioned contract change in a new ADR.

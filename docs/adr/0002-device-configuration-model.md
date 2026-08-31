<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Commercial license available
© Concepts 1996–2026 Miroslav Šotek. All rights reserved.
© Code 2020–2026 Miroslav Šotek. All rights reserved.
ORCID: 0009-0009-3560-0851
Contact: www.anulum.li | protoscience@anulum.li
SCPN Magnetic Cusp Core — ADR 0002: device configuration model
-->

# ADR 0002 — Device configuration model and evidence-maturity semantics

**Status:** accepted (2026-08-31)

**Deciders:** project owner; SCPN Reactor Systems Research Group standard

## Context

The repository was established architecture-only (ADR 0001). The first
capability lane is the device configuration model for the single
registry configuration this repository owns (`cusp`). The claim
boundary and repository-level `evidence_maturity` semantics follow the
family pilot.

## Decision

1. The package `scpn_magnetic_cusp_core` implements the device
   configuration model as frozen, strictly typed value objects: cusp
   geometry (spindle or picket-fence class with coil counts and
   dimensions) and the coil drive.
2. Claim boundary — identical to the family pilot: internal-consistency
   validation, cited textbook estimates with documented bounds,
   canonical serialisation with SHA-256 digest, and the data-only SPO
   registry pin. No claim about any real machine; every exercised
   parameter set is a synthetic test fixture.
3. Hard class invariants: opposed neighbouring coil currents are
   required — the central field null they produce is the defining
   property of cusp confinement (J. Berkowitz et al., Proc. 2nd UN
   Int. Conf. Peaceful Uses of Atomic Energy 31 (1958) 171). The
   `spindle` class requires exactly two coils; the `picket_fence`
   class requires an even count of at least four (alternating
   currents close only on even arrays).
4. Derived quantity with citation: the on-axis field of a circular
   loop ``B(z) = mu0 I R^2 / (2 (R^2 + z^2)^{3/2})`` (standard
   magnetostatics) used by the spindle-pair helper. Advisory finding,
   reported by `consistency_report()` and never clamped: a spindle
   separation-to-radius ratio outside ``[0.5, 4]`` departs from the
   canonical spindle-cusp arrangement (documented model bound).
5. Repository-level `evidence_maturity` = the highest state claimed by
   any capability entry; per-capability states are the authoritative
   claim surface.
6. Everything else is unchanged: review-only/non-actionable SPO
   profile, no adapter implementation, empty solver seams,
   `not_federated` Studio state, independent machine-protection veto,
   all non-claims.

## Consequences

- The Studio descriptor's `capabilities` array carries its first item
  (schema 1.1.0 data change only).
- The reactor-domain validator gains the populated-capabilities branch
  with the ceiling rule.
- Later lanes (loss-flux diagnostic semantics, safety envelope) build
  on these types; maturity advances per capability only with the
  evidence the family standard requires.

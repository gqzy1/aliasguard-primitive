# Design rationale

Entity resolution often uses fuzzy name scores followed by an unconditional union operation. A mistaken bridge can then merge two explicitly distinct objects. AliasGuard makes the difference between a pairwise identity finding, inferred sameness and a publishable partition explicit.

Natural-language descriptions can identify the same object using a nickname and a namespaced asset tag. The semantic boundary needs GenLayer because byte equality cannot determine that identity claim. Independent validators must agree on every pair's interpretation. The graph algorithm then enforces equivalence consistency without asking a model to choose groups or resolve contradictions. Other contracts or applications can consume the immutable partition and verify its commitment without running their own inference server.

## Relationship to adjacent primitives

The design was compared against the accessible connected GenLayer repository catalogue and its mechanism documentation on 2026-10-27, including the standalone FitCert, TermFence and RatioRail releases. This is a bounded repository comparison, not a claim that entity resolution or graph consistency was invented here.

| Existing mechanism | AliasGuard difference |
| --- | --- |
| FitCert: bipartite compatibility, maximum matching and allocation optimality | No resource assignment, matching, capacities or Hall witness; an identity partition is accepted only when equality closure and explicit inequality are consistent |
| VOLTA: prerequisite graph and admissible execution order | Undirected identity equivalence, not direction, ordering, task scheduling or cycle freedom |
| Evidence Independence Matrix / EchoMap: provenance dependence and maximum independent subset | Individual-object identity, transitive equality and inequality contradictions; no source acquisition provenance or independent-set optimization |
| Grant Overlap / GrantWeave: expense duplicate detection with funding caps and reservations | Complete catalogue partition and contradiction paths; no expense activation, ledger capacity, approval or reservation |
| ClauseMesh / Handshake Map: two-party clause reconciliation matrix | Single sealed collection of individual objects, equivalence closure and terminal entity groups; no clause agreement core or counterpart consent |
| AccordSpace / Jijing: finite-world condition compilation and unanimous plan approval | No configurable variables, feasible-world search, waivers or negotiated commitment |
| RatioRail: exact rational conversion graph | No quantities, unit conversion, rational edge multiplication or numerical cycle products |
| TermFence / PatchDebt: material preservation or migration instruction coverage | No shortened candidate, source-unit preservation vector or change-to-guide coverage |
| ContextPass, BallotSeal, PolicyDrift | No delegated attestation, acknowledgement epochs or changing-source semantic history |
| RecallScope, SampleScope / CoreRelay, ErrataScope | No external policy/recall/notice lookup or applicability gates |
| Splice, Story Guardian, EvidenceCourt / Greybox, BriefProof | No creative generation, game strategy proof or multimodal deliverable acceptance |
| ANTHER: sourced flowering seasons; AFTERHOURS: activity coexistence with room-capacity reservations; BLOOMBOUND: theme membership and concept novelty scoring | Individual physical-object identity, not seasonal planning, co-location capacity, synonym novelty or game territory |

Generic patterns such as canonical JSON, caller namespaces, revision guards and fixed-runner headers are ordinary infrastructure. The standalone identity protocol, graph proof, fixtures and tests are implemented here; no earlier business mechanism or frontend is repackaged.

## Conservative publication

A contradiction is a business result, not a consensus execution failure. CONFLICT and UNRESOLVED are stored successfully but cannot publish. Semantic/model/format/consensus errors instead abort before persistence. Publishing recomputes the graph from accepted labels; it never trusts a caller's grouping or proof. Every published member appears exactly once, and every group representative is its lowest input index.

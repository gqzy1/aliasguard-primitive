# AliasGuard protocol

`aliasguard-1` uses zero-based entry indexes. One sealed catalogue has 2–6 distinct descriptions, each 10–600 characters, and a 10–600 character scope. Payload JSON has exactly `scope` and `entries`; its maximum length is 6,000 characters. Strings retain their exact content; leading/trailing whitespace, control characters and invalid UTF-8 are rejected. JSON duplicate keys are rejected.

## Consensus boundary

The full fixed prompt is in `contracts/alias_guard.py::RULES`. It distinguishes individual identity from shared names, models and batches. A positive shared individual identifier supports SAME. Explicit incompatible individual identifiers in the same namespace support DIFFERENT. Insufficient or contradictory evidence yields UNKNOWN. Labels for every unordered pair are independently evaluated using only that pair and scope; no third-record inference is permitted in the semantic stage.

Leader and each validator independently call `gl.nondet.exec_prompt` with the sealed input. The custom `gl.vm.run_nondet_unsafe` validator checks Return type, strict schema, exact pair count and every independent relation label. A disagreement on any pair rejects, including a pair that does not change the aggregate state. Errors and malformed responses fail closed; they never become UNKNOWN. Only accepted semantic decisions leave this boundary. No storage object is captured in the callbacks.

## Deterministic graph

Pairs are `(0,1),(0,2),...,(n-2,n-1)`. Undirected SAME edges form connected components. For each DIFFERENT pair inside a component, the proof includes the pair and a shortest SAME-edge path joining it. This is an explicit contradiction; the contract never silently chooses which assertion wins.

UNKNOWN inside a component is recorded separately as a transitive inference with a SAME path. UNKNOWN across components remains unresolved. A catalogue is READY only if no contradictory edge exists and every cross-component pair is explicitly DIFFERENT. This ensures that no unresolved pair can silently alter the published partition.

| State | Transition / effect |
| --- | --- |
| SEALED, revision 0 | Exact immutable input; one assessment permitted |
| CONFLICT, revision 1 | At least one DIFFERENT edge contradicts a SAME path; publication blocked |
| UNRESOLVED, revision 1 | No contradiction, but cross-component UNKNOWN remains; publication blocked |
| READY, revision 1 | Consistent and fully separated components; owner may publish |
| PUBLISHED, revision 2 | Terminal canonical groups and certificate hash |

CONFLICT takes priority over UNRESOLVED. Components are ordered by their minimum entry index. Members are ascending. That minimum is the canonical representative; it is a local deterministic choice, not a claim that one name is authoritative. BFS chooses shortest witness paths with ascending neighbours as the tie-break. There is no model-selected grouping, administrator repair, editing, deletion, retry method or override. A corrected catalogue must use a new slug.

## API

Constructor: no arguments. All methods return strings.

| Method | Arguments | Authorization / return |
| --- | --- | --- |
| seal | slug, payload | Any actual sender; returns lowercase-owner + `:` + slug |
| assess | record_id, expected_revision | Owner; SEALED only; accepted record JSON |
| publish | record_id, expected_revision | Owner; READY only; terminal record JSON |
| get_record | record_id | Public; stored JSON, empty string if absent |
| protocol | none | Public; version, bounds and exact semantic rules |

Slugs use 3–32 lowercase ASCII letters, digits or hyphens. Each owner can seal 16 catalogues. The same owner/slug/input returns the existing ID without new inference; changed input fails. Quotas are per address, not Sybil resistance. Wrong owner, stale revision, failed consensus and ineligible publication fail before storage mutation. SDK tests and real evidence have separate scopes.

Commitments are SHA256 of UTF-8 canonical JSON: sorted object keys, compact separators, `ensure_ascii=False`, array order retained. Input hashes include protocol version. Assessment hashes bind the input hash, full relation vector and graph proof. Publication certificates bind record identity, input and assessment hashes, canonical representatives and all members. `tools/verify_record.py` independently recomputes them. Hashes prove integrity, not factual truth.

## Official references

- [Stable network configuration](https://docs.genlayer.com/developers/networks)
- [Independent validation and equivalence](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle)
- [SDK contract methods](https://docs.genlayer.com/api-references/genlayer-js/contracts)
- [GenVM linter](https://docs.genlayer.com/api-references/genlayer-linter)

Current documentation also covers newer consensus deployments. This release's actual compatibility evidence is the pinned source, genlayer-js 1.1.8, Stable RPC ABI parse, source readback and recorded live receipts; no Studio-dev or Bradbury compatibility is claimed.

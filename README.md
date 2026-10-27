# AliasGuard

A standalone GenLayer Intelligent Contract for **entity alias consolidation with contradiction witnesses**.

“North projector” and “Hall beamer” may describe the same tagged object. A third similar projector may be a different unit. AliasGuard independently interprets each pair, then uses deterministic code to create consistent identity groups. A SAME path that joins an explicitly DIFFERENT pair produces a blocking witness instead of silently merging the records.

**Deployed:** [Stable Studionet contract](https://explorer-studio.genlayer.com/address/0xc27b9497801E01BAeB02B294c6124724e0333da9). The verified example is PUBLISHED, with groups `[0,1]` and `[2]`. [Receipts and readback](EVIDENCE.md) include the initial unsuccessful consensus attempt.

## Mechanism

1. `seal` fixes a catalogue scope and 2–6 individual-object descriptions in the sender's namespace.
2. `assess` asks the leader and validators to independently classify every unordered pair as SAME, DIFFERENT or UNKNOWN. Every label must agree, including pairs that do not change the final state.
3. Deterministic graph code computes SAME components, shortest contradiction paths, unresolved cross-group pairs and separately labelled transitive inferences.
4. Only READY catalogues can `publish`. Publication recomputes the proof and freezes canonical groups with an integrity certificate.

A fixed namespace asset identity and an informal alias can refer to one object without identical wording. A shared model or name alone proves neither equality nor difference. The model does not choose the partition or override contradictions. [Protocol](PROTOCOL.md) · [Design and adjacent mechanisms](DESIGN.md) · [Security](SECURITY.md).

## Use

Deploy the complete single-file [contract](contracts/alias_guard.py), no constructor arguments, on **Stable Studionet, chain ID 61999**, RPC `https://studio.genlayer.com/api`. Use full consensus. The exact Python SDK runner is pinned in the first source line. JavaScript examples use `genlayer-js@1.1.8`.

Pass the contents of `examples/equipment-explicit.json` as the payload string:

```text
seal("equipment-explicit", payload)
assess("<lowercase-sender>:equipment-explicit", 0)
publish("<lowercase-sender>:equipment-explicit", 1)
get_record("<lowercase-sender>:equipment-explicit")
```

Wait for each successful finalized receipt and matching readback before the next write. `tools/calls.mjs` provides signer-independent helpers; no key should be pasted into chat. No paid API, backend, token, frontend or mainnet transaction is required.

## Verification

[Deployment and real evidence](EVIDENCE.md). Offline tests use explicitly scripted responses and are distinct from live consensus:

```sh
python -m unittest discover -s tests -v
python -m pip install -r requirements-dev.txt
genvm-lint check contracts/alias_guard.py --json
python tools/sdk_check.py
python tools/verify_record.py evidence/published-record.json
sha256sum -c SOURCE_SHA256.txt
```

The 27 unit tests include all 729 four-entry relation graphs, contradiction witnesses, unresolved publication guards, malformed output, independent validator disagreement, namespaces, revision guards and terminal state. The official SDK check uses the GenVM v0.2.16 archive and actual SDK storage/calldata with a mocked model; it is not a network node or real consensus test.

## Boundaries

Identity descriptions are unverified public claims. Consensus does not establish physical existence, custody or ownership. SAME is transitive by protocol: inferred pairs are exposed separately. All cross-group uncertainty blocks publication. There is no global asset uniqueness, cross-catalogue inventory, administrator repair, deletion or real-world merge action. Use non-sensitive catalogues. Model errors and correlated errors remain possible.

MIT licensed.

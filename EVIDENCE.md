# Stable Studionet verification

Network: **61999**, RPC `https://studio.genlayer.com/api`. SDK: `genlayer-js@1.1.8`. All sends used full consensus, zero value and zero configured rotation retries. Preflight returned `eth_chainId = 0xf22f`, `eth_gasPrice = 0x0`; the dedicated example address had zero balance. No faucet funding, paid API or user wallet key was used.

Contract: [`0xc27b9497801E01BAeB02B294c6124724e0333da9`](https://explorer-studio.genlayer.com/address/0xc27b9497801E01BAeB02B294c6124724e0333da9).

Canonical source: `contracts/alias_guard.py`, SHA256 `5986b7cee7637323c21dbd4dd451d601dbde9c699d571576926e6838412ad673`. The RPC-returned source matches, with CRLF/LF normalization permitted by the comparison; the returned raw digest also equals this digest. [Source check](evidence/source-check.json) · [Deployment metadata](deployment.json).

## Transactions

The successful published example uses `examples/equipment-explicit.json`. The initial fixture and its unsuccessful assessment are retained separately. A failed assessment was investigated before any further write; its transaction was not resent or appealed. The later request has a new slug and a more explicit identity-scope declaration, and uses the same unchanged contract.

| Operation | Transaction | Result |
| --- | --- | --- |
| Deploy | [08585772…](https://explorer-studio.genlayer.com/tx/0x08585772de936b5f1d4d5c9fb63c3d87d83ffedfa06e6a702b33ade3d7684e49) | FINALIZED / MAJORITY_AGREE / SUCCESS |
| Seal original example | [864b2372…](https://explorer-studio.genlayer.com/tx/0x864b2372210e01c6b0c0b8b030ca94013c212b80d85b9203f2ed7a0ebdf96ae0) | FINALIZED / MAJORITY_AGREE / SUCCESS |
| Assess original example | [60fff431…](https://explorer-studio.genlayer.com/tx/0x60fff431c1a101039d70c4c4a06db071fb072635e7e27c0ad439dd22a7e2f542) | UNDETERMINED / MAJORITY_DISAGREE; no assessment persisted |
| Seal explicit example | [8587e678…](https://explorer-studio.genlayer.com/tx/0x8587e67874365c1c64dc9a02de32857727ce03bcea6685f6a12343581677cf05) | FINALIZED / MAJORITY_AGREE / SUCCESS |
| Assess explicit example | [eb208b76…](https://explorer-studio.genlayer.com/tx/0xeb208b760c73b591fa99600577842ab7a4b1e0fce53a43c3c52b68f1359d642f) | FINALIZED / MAJORITY_AGREE / SUCCESS |
| Publish explicit example | [b8ecb9c6…](https://explorer-studio.genlayer.com/tx/0xb8ecb9c6638fe8be06b0007070c3ca801a551e1bdd741339e69433b2beb2ca89) | FINALIZED / MAJORITY_AGREE / SUCCESS |

The original leader proposed `[SAME, DIFFERENT, UNKNOWN]`. Final recorded votes were 2 agree and 3 disagree; validator runtime results were SUCCESS, so this was semantic disagreement rather than a parser or VM failure. The original record remains `SEALED`, revision 0 ([readback](evidence/original-record.json)). Candidate state in a leader receipt is not accepted chain state.

The explicit assessment accepted `[SAME, DIFFERENT, DIFFERENT]`, with 3 agree, 1 disagree and 1 idle. The readback is READY with components `[[0,1],[2]]` and no conflicts or unresolved pairs. Five configured validators does not mean five agreeing independent organizations. Some receipts include an extra cancelled/idle execution after quorum; `CONSENSUS_VALIDATOR_QUORUM_REACHED` is not a failed leader execution. Raw receipts preserve those fields.

Published record: `0xb560a20855fafb5110824ef1bd3e2d1ebab0ef1e:equipment-explicit`, revision **2**, state **PUBLISHED**. Certificate SHA256: `bfa0e2bf9f5caf0d8d53924dc9863478dd7fd04f190deab74adf1eaac8505eda`. Independent commitment verification passed.

## Evidence files

`evidence/transactions.json` holds the six returned transaction hashes. Compact receipt projections expose status, votes, execution and equivalence outputs; `evidence/raw-receipts.json.gz` retains the full captured SDK responses, including cancelled/idle executions and the unsuccessful assessment. Projections are labelled as projections, not raw responses. `evidence/published-record.json` is the latest-final terminal readback. `tools/verify_record.py` recomputes input, relation-graph, assessment and publication commitments locally without a model or SDK.

## Offline checks and coverage limits

- **27 unit tests passed**, including exhaustive reference comparison for all **729 four-entry relation vectors** and path-witness validation. The host and model are scripted; the production validator is explicitly invoked by that harness.
- **GenVM lint and ABI validation passed** with `genvm-linter==0.11.0`. The I200 notice reports a newer available runner; this source retains its explicit, live-compatible runner.
- **Official SDK direct check passed** using `genlayer-test==0.29.2`, actual SDK storage/calldata and callback serialization with `vm.check_pickling=True`. The archive is GenVM `v0.2.16`; no Localnet or alternate network was started. Inference and consensus are mocked in this check.
- Stable RPC parsed all five public methods, then deployed the exact source. [ABI](evidence/contract-schema.json) · [Unit output](evidence/unit-tests.txt) · [Lint output](evidence/lint.json) · [SDK result](evidence/sdk-check.txt).

Live coverage establishes one successful semantic partition and publication, plus rejection of one differing semantic proposal. CONFLICT witnesses, transitive UNKNOWN inference, UNRESOLVED publication blocking, owner denial, stale revisions, quotas, and malformed model output are offline-tested only. `examples/contradiction.json` is a synthetic input illustration, not a claimed live consensus result. This evidence does not prove universal accuracy, injection immunity, authenticated asset identity or distributed operator independence.

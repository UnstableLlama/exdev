# 306/002 post-author blob-link recovery

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Stopped run: `.teacher/runs/commit-000306-002`; packet `.teacher/retrieval/000306-002`. The fresh assisted teacher completed and wrote a draft, transcript and provenance. Post-author validation failed at the blob-link check, before replay. Queue is stopped_failure, no active session; 307 approval remains unrecorded pending approved306.

My administrative `shutil.copytree` copied packet blobs into separate inodes. The previous packet comparison checked bytes but omitted shared-store identity. The audit checks all 4390 blobs: every packet/store hash matches its filename, all are regular/read-only, but 3769 packet blobs are not shared-store hard links. Current305-ancestor approval selection verifies. The original packet and all authored artifacts remain unchanged.

Please authorize the bound one-off script to restore only those 3769 byte-identical links atomically through existing blob_store.put, then run unchanged validate_run with the accepted sparse adapter. It verifies the audit, authorization, manifest and every authored artifact, holds the cycle lock, and performs no author invocation. A host process check must first confirm no cycle remains. Only after successful full validation does it complete the existing failed reservation once under the queue lock, using existing finish after guarded rearming; it binds your authorization and original failure in recovery_log and retains retry_awaiting_verdict. No new reservation, attempt, changed bytes, source change or stop bypass. Original failure result/log are retained. If validation fails again, stop and report.

This asks for transport/validation recovery of completed002, not a third teacher attempt or entry approval. The draft now explicitly traces residual x from Embedding's float default, half attention addition and float MLP addition through block return/next normalization, compares the earlier Llama entry and labels source versus unexecuted mixed-dtype semantics. It carries the existing odd-tail finding. This is an administrative inspection, not a claim the entry passes review. After recovery, file the normal full request with the validation, recovery audit and artifact hashes. No308 launch; canonical/training false. No implementation edits, commit or push; latest accepted tests20 focused/337 full. Awaiting authorization before relinking or completing the failed reservation.

## SHA256

- reports/commit-000306-prepared-002.result.json: `424b7e3522398d7430c02eb4b5b7d92b8cf2bd900dcf2f646321bc1b0fced9dc`
- reports/commit-000306-prepared-002.log: `c2f62805a4df5d0eb0210c036446efbc1653d258c8fb580dda8cd6a9a5186254`
- reports/commit-000306-link-recovery-002.json: `0110cff761ba82ca7f464d703a8326de2c2ebd8712a3b25715feead45a6487cf`
- reports/commit-000306-link-recovery-002.py: `13b53a9267d348ab74661f6b297cfaef158dffe4ff59df89062b27d5341d6b7e`
- reviews/verdicts/commit-000306-retry-recovery-002.md: `a8bb4a10bd21b92a5bb09781200f5d62a0e7feae3b050c8d3190b5ba9082ce6e`
- .teacher/retrieval/000306-002/manifest.json: `1d371a7eb98805c935d1e23158309fb7acdcae9582c4ea9004858a4ced5aa940`
- teacher/cycle.py: `9e6f7eb484cc727cebfc40b1e1c6d926ae29423b90e0fe31abfeadac4e9344de`
- teacher/blob_store.py: `0552562b4ccfccd3ab25808b7413b25e3f45da6f861f3f50a2d863ba6df81bda`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
- .teacher/runs/commit-000306-002/raw-transcript.json: `b339bc38bdb698b9259a7916f4008f1426be55d1e118bbdba1df22317b3a8f1b`
- .teacher/runs/commit-000306-002/provenance.json: `334d182acd1a57b08feedad15dca9acab50166398de1df28d368647ee384f1af`
- .teacher/runs/commit-000306-002/draft.json: `d565bca3d37071dfd4c19aef4a8bf38370e8b9c911f70bdce4f18aa77e9442f7`
- .teacher/runs/commit-000306-002/review.json: `fbc4354734bd202b73f69fe2a36028cc67acbc8c3d3b0f1e3d792e8f7a46bed6`
- .teacher/runs/commit-000306-002/coverage.json: `15bedab9ce8ad4836cdd6153781d5c9682d7455fd323ef813ebd81cb8b7b0586`
- .teacher/runs/commit-000306-002/draft.md: `ec5c55d67810b3c6ddabc7468cfcb49dd388274ec718863ca91c5af7f83fff32`
- .teacher/runs/commit-000306-002/status.json: `537aede7f1404a612d0c5308704be156b3fda5620ed602c450f7ccc9a849682d`

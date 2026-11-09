# Source modification inventory

The ordered patches distribute modifications to Apache-2.0 TensorFold source at the pinned public revision. Each diff section identifies its modified file. The exact recorded source bytes are preserved for hash verification. These changes combine prior retained work with the November 7 repairs and the November 8 compact-Store recency correction; they are not presented as isolated new changes. Retain the base source notices when applying or redistributing them.

Apply `tested-stack.patch`, `cache-cut-in.patch`, `full-prefix-backing.patch`, then `prefix-recency.patch`. The last three touch only `lanes.zig`, `model.zig` and `prompt_cache.zig`, already present in the inventory below, so the total remains 53 modified files and seven additions. The cut-in guard refuses unsafe cached cut-ins before placement; complete backing preserves the packed prefix independently of reusable working rows and updates both peers' save/restore protocol. The fourth patch adds `o.used >= e.used` to the compact Store's superseded preference, preserving a recently resumed short checkpoint against an older deeper snapshot. It changes no budget or peer protocol. Both executables must still come from the same updated build because the retained full-prefix repair changes peer frames.

The v0.3.0 recency core is `8210b249…` and its 1,117-file closure is `aa0f3dcd…`. The saved UI trial qualified the exact artifacts. A separate fresh startup verified equivalence and persistent selection of those artifacts. Historical v0.1 and v0.2 closures and build identities are available separately. Current public TP2 source uses newer branch-point policy protection and needs its own reproduction for a recency port. PRs #54, #55 and #56 track separate fixes. [Ordered patch hashes and intermediate closures](../data/patch-series.json) · [final artifact hashes](../data/source-modifications.json) · [results](../data/recency-results.json).

| Change | File |
| --- | --- |
| added | `zig/src/core/cache_refresh_borrow_test.zig` |
| modified | `zig/src/core/engine_api.zig` |
| modified | `zig/src/core/lane_host.zig` |
| modified | `zig/src/core/lane_host_reuse_test.zig` |
| modified | `zig/src/core/lane_host_test.zig` |
| added | `zig/src/core/lanes/call_gate.zig` |
| modified | `zig/src/core/lanes/config.zig` |
| modified | `zig/src/core/lanes/engine.zig` |
| modified | `zig/src/core/lanes/fake.zig` |
| modified | `zig/src/core/lanes/stream.zig` |
| modified | `zig/src/core/lanes/windows.zig` |
| modified | `zig/src/core/prompt_cache.zig` |
| modified | `zig/src/core/template/template.zig` |
| modified | `zig/src/core/tokenizer/model.zig` |
| modified | `zig/src/core/tokenizer/steps.zig` |
| modified | `zig/src/core/tokenizer/tokenizer.zig` |
| modified | `zig/src/families/dsv41/draft.zig` |
| modified | `zig/src/families/dsv41/dsv41.zig` |
| modified | `zig/src/families/dsv41/engram.zig` |
| modified | `zig/src/families/dsv41/engram_aio.zig` |
| modified | `zig/src/families/dsv41/engram_io.zig` |
| modified | `zig/src/families/dsv41/exl3_experts.zig` |
| modified | `zig/src/families/dsv41/exl3_experts2d.zig` |
| added | `zig/src/families/dsv41/graph_fallback.zig` |
| added | `zig/src/families/dsv41/graph_fallback_test.zig` |
| modified | `zig/src/families/dsv41/lanes.zig` |
| modified | `zig/src/families/dsv41/lanes_main.zig` |
| modified | `zig/src/families/dsv41/link.zig` |
| modified | `zig/src/families/dsv41/model.zig` |
| modified | `zig/src/families/dsv41/native.zig` |
| modified | `zig/src/families/dsv41/pil.zig` |
| modified | `zig/src/families/dsv41/prompt.zig` |
| modified | `zig/src/families/dsv41/prompt2d.zig` |
| modified | `zig/src/families/dsv41/rdma.zig` |
| modified | `zig/src/families/dsv41/round.zig` |
| modified | `zig/src/families/dsv41/tri_markov.zig` |
| modified | `zig/src/native/cuda.zig` |
| modified | `zig/src/server/anthropic.zig` |
| modified | `zig/src/server/anthropic_translate.zig` |
| modified | `zig/src/server/chat.zig` |
| modified | `zig/src/server/cli.zig` |
| added | `zig/src/server/gap_regression.zig` |
| modified | `zig/src/server/hf_text.zig` |
| modified | `zig/src/server/late_system_test.zig` |
| modified | `zig/src/server/messages.zig` |
| modified | `zig/src/server/metrics.zig` |
| modified | `zig/src/server/model_text.zig` |
| modified | `zig/src/server/openai.zig` |
| added | `zig/src/server/prepare_gate.zig` |
| modified | `zig/src/server/prompt.zig` |
| modified | `zig/src/server/reply_text.zig` |
| modified | `zig/src/server/root.zig` |
| modified | `zig/src/server/serve.zig` |
| modified | `zig/src/server/server.zig` |
| modified | `zig/src/server/sse.zig` |
| modified | `zig/src/server/status_routes.zig` |
| modified | `zig/src/server/stream_preflight_test.zig` |
| modified | `zig/src/server/tokens.zig` |
| modified | `zig/src/server/tool_stream.zig` |
| added | `zig/tests/server/pressure_serve.zig` |

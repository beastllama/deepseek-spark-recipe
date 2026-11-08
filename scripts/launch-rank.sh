#!/usr/bin/env bash
# Native argv adapter for this recipe. It does not create containers or supervise a pair.
set -euo pipefail
rank=${1:?Usage: bash launch-rank.sh head|worker runtime.env}
set -a
source "${2:?An operator-owned runtime.env is required}"
set +a
[[ "$rank" == head || "$rank" == worker ]] || { echo 'Expected head or worker' >&2; exit 2; }
: "${BIN_ROOT:?}" "${MODEL_DIR:?}" "${CHECKPOINT_DIR:?}" "${RANK_CACHE_DIR:?}"
: "${TF_TP_MASTER:?}" "${TF_TP_PORT:?}" "${TF_RDMA_DEVICES:?}"
: "${TF_RDMA_GID_INDEX:?}" "${TF_DS_KIT:?}" "${TF_DS_ENGRAM:?}" "${TF_DS_TOKEN_MAP:?}"
: "${TF_DS_ROUND_MS:?}" "${NCCL_SOCKET_IFNAME:?}"
export TF_TP_WORLD=2 TF_DS_REPLAY_FLOOR=1 TF_DS_STREAMS=32 HF_HUB_OFFLINE=1
export TF_DS_PREFILL_INTERLEAVE_MS=250 TENSORFOLD_MEMORY_RESERVE_GIB=12.2
export TF_FILL_CHUNKS=1 TF_FILL_CUT_IN=8192 TF_DS_ROUND_ROWS=64
export NCCL_NET_PLUGIN=spcx NCCL_IB_HCA="$TF_RDMA_DEVICES" NCCL_IB_GID_INDEX="$TF_RDMA_GID_INDEX"
export TF_DS_GRAPHS=1 TF_DS_HC_SIDE=1 TF_DS_L2_PREFETCH=1 TF_DS_ENGRAM_AIO=1
export TENSORFOLD_CUDA_KERNELS="$TF_DS_KIT/aot"
if [[ "$rank" == worker ]]; then
  exec "$BIN_ROOT/bin/tf-dsv41-lanes" "$CHECKPOINT_DIR" "$RANK_CACHE_DIR" 1 2 \
    "$TF_TP_MASTER" "$TF_TP_PORT" "$TF_DS_KIT" --engram "$TF_DS_ENGRAM" \
    --token-map "$TF_DS_TOKEN_MAP" --pool 524288 --streams 32 --drafts 1 \
    --graphs 1 --side 1 --prefetch 1 --aio 1 --rdma "$TF_RDMA_DEVICES" \
    --round-rows 64 --round-ms "$TF_DS_ROUND_MS"
fi
export TF_DS_RANK_CACHE="$RANK_CACHE_DIR" TF_DS_FINE_SNAPSHOT_128=1 TF_AI_OPS_SPANS=1
api_host=${API_HOST:-127.0.0.1}
auth=()
if [[ -n "${API_KEY_FILE:-}" ]]; then
  [[ -f "$API_KEY_FILE" ]] || { echo 'API_KEY_FILE is missing' >&2; exit 2; }
  auth=(--api-key-file "$API_KEY_FILE")
elif [[ "$api_host" != 127.0.0.1 && "$api_host" != ::1 ]]; then
  echo 'A non-loopback API_HOST requires API_KEY_FILE' >&2
  exit 2
fi
exec "$BIN_ROOT/native/bin/tensorfold-native" serve "$MODEL_DIR" --backend cuda \
  --host "$api_host" --port "${API_PORT:-8888}" --name DeepSeek-V4.1-Flash-1017 \
  --context 524288 --parallel 8 --max-tokens 32768 --temperature 1.0 --top-p 0.95 \
  --top-k 20 --thinking --reasoning-effort high --prompt-cache-gib 1.0 "${auth[@]}"

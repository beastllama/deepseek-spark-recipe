# Packing KV allocations into the smallest fitting gap

One matched SparkDash trial on two DGX Sparks cut a large request’s queue time from **208.3 s to 57.0 s**. It finished **145.3 s earlier**. The full job took **4.8 s longer**. This is an experimental placement patch. The bounded short-request scheduler remains the selected recipe.

| Metric | Original | Tightest fit |
| --- | ---: | ---: |
| Large request queue time | 208.3 s | 57.0 s |
| Large request completion | 272.4 s | 127.1 s |
| Fragmented allocation failures for the large request | 146 | 0 |
| Six-request wave | 798.1 s | 803.1 s |
| Full job including the primer | 838.5 s | 843.3 s |
| Total output tokens across measured requests | 69,863 | 69,863 |

The original had 272,384 KV rows free. Its largest contiguous block held 180,224 rows, and the queued request needed 215,040. The patch puts a new reservation into the smallest aligned gap that fits when no unbacked retained snapshots need protection. This preserved a 229,376-row block and let the large request start while the same three requests held reservations. Context-retry time fell from 150.9 s to zero. The remaining 56.3 s tagged as ineligible for cached cut-in accounted for nearly all of its remaining queue wait.

The cold request took 45.9 s longer in the patched wave. The same 31,647-token stream finished last in both arms. Weights, High reasoning, 524,288 logical context, 32,768 output allowance, eight lanes, 786,432 shared KV rows and cache policy matched. All seven reply token hashes and cache counts matched, including the separate primer. Each of the five warm measured requests reused 94,080 tokens. One matched synthetic wave establishes this allocation behavior for the tested layout. Other arrival orders and real job dependencies can change the result. [Per-request measurements](data/kv-placement-trial.json)

## Source and test

Start with the [bounded short-request recipe](BOUNDED-SHORT-ADMISSION.md), including the numeric admission observations. The 1,120-file published source manifest matches the original source used in this trial. In the Linux checkout, verify that closure, apply the optional allocator patch and verify the candidate closure.

```sh
python3 scripts/verify-source.py tensorfold --manifest data/source-manifest-bounded-short.json
git -C tensorfold apply --check ../patches/kv-placement-tight-fit.patch
git -C tensorfold apply ../patches/kv-placement-tight-fit.patch
python3 scripts/verify-source.py tensorfold --manifest data/source-manifest-kv-placement-tight-fit.json
```

The patch changes one DSV4.1 allocator source file. Its CPU fixture creates live extents at `[112,176)` and `[264,384)` in 2,048-row blocks. Allocate 67 blocks, then request 105. The original uses the first gap for the 67-block request. Tightest fit uses the second gap and leaves the first available for the larger allocation. The measured ARM64 head built and passed its loader check with the same 21 GPU fatbins and compatible worker. [Allocator patch](patches/kv-placement-tight-fit.patch)

The live comparison used a local SparkDash 2.90.1 collector. It primed a shared prefix, admitted four requests with reservations of 112, 64, 88 and 120 blocks in order, then let the first and third finish. It submitted a cold 67-block request before the warm 105-block request. Native logs verified the reserve sizes, which streams were live, and whether the largest free block could fit the last request. One arm used the original head and one used the tightest-fit head. The stock SparkDash collector cannot stage this sequence. The patch and numeric results are available for review, and an independent live reproduction remains open.

This builds on DeepSeek, Ash Hart and the TensorFold contributors, Albert Lee and BertholomusAI’s native Spark work, Mia’s AI Lab’s EAQ recipe and SparkDash, drowzeys’ matching Keys, and turboderp’s EXL3 work. [Full credits and upstream licenses](CREDITS.md)

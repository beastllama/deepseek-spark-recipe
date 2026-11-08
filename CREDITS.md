# Credits and provenance

The model, engine, quantization, kernels, serving recipes and measurement tools were made by their respective authors. This repository adds a record of one deployment, its source overlay, a configurable native-argv adapter and reproduction notes. No endorsement is implied.

| Work | Attribution and source |
| --- | --- |
| DeepSeek-V4.1-Flash-1017, draft blocks, Engram and reference inference | [DeepSeek](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/tree/1bae0e1088993b9b82de08f59de5be5a34e42170) |
| TensorFold native engine and server | [Ash Hart and TensorFold contributors](https://github.com/ashhart/TensorFold) |
| DeepSeek native family, TP2, RDMA and kernel kit | [BertholomusAI / Albert Lee and contributors](https://github.com/bertholomus/TensorFold/tree/fbbc97132cd004237d9887b8d3185896efaedc5c) |
| EAQ v1 EXL3 quantization, chat template, Spark recipe and patch integration | [Mia's AI Lab and recipe contributors](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks/tree/0e7d421eb4797d98dc781dad764b8f86d34118ae) |
| Matching Keys overlay and application work | [drowzeys](https://huggingface.co/drowzeys/keys-DeepSeek-V4.1-Flash-1017-Abliterated/tree/de412d2249632903dace23399526e00a145aada5) |
| EXL3 format and quantizer | [turboderp / ExLlamaV3](https://github.com/turboderp-org/exllamav3) |
| SparkDash UI and native benchmark collectors | [Mia's AI Lab / sparkDash and contributors](https://github.com/MiaAI-Lab/sparkDash) |

The retained source also carries work attributed in [Mia's pinned credits](https://github.com/MiaAI-Lab/DeepSeek-v4.1-Flash-1017-2x-DGX-Sparks/blob/0e7d421eb4797d98dc781dad764b8f86d34118ae/CREDITS.md), including eleata's engine rebase, Hector Isaza's Engram failure handling, Coinupbtc's interleave/tool work, Robert Wojciechowski and BadAd84's memory/cache work, and Jay Leaton's UTF-8 JSON-writer repair. That upstream credit inventory remains authoritative for their contributions; this overlay does not claim their work as new.

Related community work includes [OsakaTX's short-prompt fill/drain PR #51](https://github.com/bertholomus/TensorFold/pull/51) and [Jay Leaton's Spark recipe](https://github.com/jayleaton/deepseek-v41-tensorfold-spark). They are useful related work, not an attribution of this benchmark's settings or numbers to their recipes. [LibertAI's DeepSeek EXL3 releases](https://huggingface.co/LibertAIDAI) are part of the surrounding quantization ecosystem; this measurement used the specifically pinned Mia EAQ pack, not a LibertAI checkpoint.

TensorFold and Mia's recipe state Apache-2.0 for their code. Their notices are preserved under [LICENSES](LICENSES), with the repository [LICENSE](LICENSE) and [NOTICE](NOTICE). The original model and EAQ metadata state MIT. The public Keys metadata at the tested pin states MIT and gated access; a separate `LICENSE` URL at that pin returned 404 when checked, so this repository does not claim to replace the model card or access conditions. See [license-check.json](data/license-check.json). No model, sidecar, packed rank, binary, container or GPU bundle is redistributed here.

NVIDIA's container and CUDA components, the kit's Triton/PyTorch/CUTLASS components and the compiler retain their own terms. Preserve the authors' notices when acquiring or building them; the engine's Apache license is not a blanket license for those assets.

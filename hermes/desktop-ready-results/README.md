# Finished child reports in Hermes Desktop

A parent in one of my swarms asked for subagent status after all three children had finished. Hermes reported zero live children. The full reports reached the parent **37 minutes 2 seconds later**.

I enabled a small plugin on the default Hermes gateway serving Desktop. When the parent already calls `delegate_task(action="list")`, the reply can now include excerpts of its own finished reports that are awaiting delivery. Hermes still delivers the full reports normally. The plugin adds no model tools or polling and makes no generation requests.

| Check | Result |
| --- | --- |
| Original recorded status reply | 0 finished findings |
| Same reply with the pending state reconstructed, through the installed plugin | 3 finished findings |
| A different conversation, then a repeat lookup by the original parent | 0 excerpts in each check |
| Live gateway readback | Version 1.0.0 enabled, one hook registered |

This measures when information could reach the parent. The effect on total project time has not been measured. The test used Hermes 0.23.2, source `f753c4b8086f0a2019ec92e2d9184dde98cb3f87`. The engine, weights and cache settings are independent of this plugin.

## Install on the machine that runs the Desktop backend

From a clone of this recipe, use the Hermes CLI and profile that own the Desktop sessions. The commands below target the default profile on macOS or Linux. If the destination directory already exists, the install stops so it can be reviewed.

```sh
(
  set -eu
  src=hermes/desktop-ready-results
  dest="${HERMES_HOME:-$HOME/.hermes}/plugins/desktop-ready-results"
  hermes plugins validate "$src" --json
  mkdir -p "$(dirname "$dest")"
  mkdir "$dest"
  cp "$src/__init__.py" "$src/plugin.yaml" "$dest/"
  hermes plugins enable --no-allow-tool-override desktop-ready-results
)
```

Hermes's activation response says whether the running gateway loaded the hook. To turn it off, run `hermes plugins disable desktop-ready-results` in the same profile.

The hook checks the profile, parent session and Desktop UI session. It considers up to eight recent pending batches and returns at most four excerpts of 600 characters, using Hermes’s own redaction. It leaves active children, official delivery state and historical messages alone. Hosted sandboxes and compute-only workers are excluded. [Plugin source](__init__.py)

The implementation builds on Nous Research and the Hermes Agent contributors’ tool-result hooks, redaction and durable delegation ledger. TurgutKural’s busy-turn proposal informed the use of an existing tool reply to reach a working parent. This plugin handles the explicit Desktop status check. [Hermes Agent](https://github.com/NousResearch/hermes-agent) · [TurgutKural’s proposal](https://github.com/NousResearch/hermes-agent/pull/136708)

"""Surface already-finished child reports during an explicit Hermes Desktop status check."""

from collections import deque
from contextlib import closing
import json
import sqlite3
from threading import Lock

from agent.runtime_session_store import is_worker_process
from gateway.session_context import get_session_env
from hermes_constants import get_hermes_home
from tools.delegation_redaction import redact_child_result
from tools.environments.sandbox_scope import current_sandbox_key


_seen = deque(maxlen=256)
_lock = Lock()


def _pending_excerpts(session_id, ui):
    path = get_hermes_home() / "state.db"
    try:
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=0)) as db:
            rows = db.execute(
                """SELECT d.delegation_id, d.result_json FROM async_delegations AS d
                   JOIN sessions AS s ON s.id=d.parent_session_id
                   WHERE d.delivery_state='pending' AND d.state='completed'
                     AND s.source='desktop' AND d.parent_session_id=? AND d.origin_session=?
                     AND d.origin_ui_session_id=?
                   ORDER BY d.completed_at DESC LIMIT 8""",
                (session_id, session_id, ui),
            ).fetchall()
    except (sqlite3.Error, ValueError):
        return []

    ready = []
    remaining = 4
    for uid, raw in rows:
        try:
            result = json.loads(raw) if raw else {}
        except (ValueError, TypeError):
            continue
        if not isinstance(result, dict):
            continue
        children = result.get("results", [result])
        if not isinstance(children, list):
            continue
        excerpts = []
        for i, child in enumerate(children):
            if not isinstance(child, dict) or child.get("status") != "completed":
                continue
            summary = child.get("summary")
            if not isinstance(summary, str) or not summary:
                continue
            summary = redact_child_result({"summary": summary}).get("summary")
            if not isinstance(summary, str) or not summary:
                continue
            key = (path, session_id, ui, uid, i)
            with _lock:
                if key in _seen:
                    continue
                _seen.append(key)
            index = child.get("task_index")
            excerpts.append({
                "task_index": index if type(index) is int else i,
                "summary": summary[:600],
                "truncated": bool(child.get("truncated") or len(summary) > 600),
            })
            remaining -= 1
            if not remaining:
                break
        if excerpts:
            ready.append({"delegation_id": uid, "total_children": len(children), "previews": excerpts})
        if not remaining:
            break
    return ready


def _on_result(*, tool_name="", args=None, result=None, session_id="", **_):
    if tool_name != "delegate_task" or not isinstance(args, dict) or args.get("action") != "list":
        return None
    if not session_id or not isinstance(result, str) or is_worker_process() or current_sandbox_key():
        return None
    ui = get_session_env("HERMES_UI_SESSION_ID")
    if not ui:
        return None
    try:
        listing = json.loads(result)
    except ValueError:
        return None
    if (not isinstance(listing, dict) or listing.get("action") != "list"
            or not isinstance(listing.get("subagents"), list) or "error" in listing
            or "completed_pending_delivery" in listing):
        return None
    ready = _pending_excerpts(session_id, ui)
    if not ready:
        return None
    listing["completed_pending_delivery"] = ready
    listing["note"] = "These are excerpts of finished child reports. Hermes will deliver the full reports normally."
    return json.dumps(listing, ensure_ascii=False)


def register(ctx):
    ctx.register_hook("transform_tool_result", _on_result)

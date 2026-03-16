#!/usr/bin/env python3
"""Parse alpha agent container logs into a swimlane timeline view.

Usage:
    docker logs <container> 2>&1 | python scripts/swimlane.py
"""
import json
import sys


def main():
    events = []
    for line in sys.stdin:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue

        ts = d.get("ts", "")[:19]
        ev = d.get("event", "")
        msg = d.get("msg", "")
        agent = d.get("agent", "main")
        agent_id = d.get("agent_id", "")
        data = d.get("data", {}) if isinstance(d.get("data"), dict) else {}
        subtype = data.get("subtype", "")

        # Step start
        if "step.start" in msg:
            name = msg.split("name=")[1].split(" ")[0] if "name=" in msg else "?"
            events.append((ts, "main", f"STEP START: {name}", "step"))

        # Subagent spawn
        elif ev == "subagent.start":
            sub = d.get("subagent", "")
            prompt = d.get("prompt", "")
            axis = ""
            for part in ["Axis 1", "Axis 2", "Axis 3", "Axis 4"]:
                if part in prompt:
                    axis = part
                    break
            sid = d.get("subagent_id", "")[:12]
            events.append((ts, "main", f"SPAWN {sub} [{axis}] ({sid})", "spawn"))

        # Task lifecycle
        elif subtype == "task_started":
            tid = str(data.get("task_id", ""))[:12]
            events.append((ts, "main", f"TASK_STARTED ({tid})", "task"))
        elif subtype == "task_completed":
            tid = str(data.get("task_id", ""))[:12]
            events.append((ts, "main", f"TASK_DONE ({tid})", "task"))

        # DA progress (from subagents)
        elif subtype == "task_progress" and agent_id:
            desc = str(data.get("description", ""))[:50]
            aid = agent_id[:12]
            events.append((ts, f"DA:{aid}", f"progress: {desc}", "progress"))
        elif ev == "tool.call" and agent_id:
            tool = d.get("tool", "")
            inp = d.get("input", {})
            detail = ""
            if tool == "Bash":
                detail = str(inp.get("description", ""))[:30]
            elif tool == "Write":
                fp = str(inp.get("file_path", ""))
                detail = fp.split("/")[-1] if fp else ""
            elif tool == "Read":
                fp = str(inp.get("file_path", ""))
                detail = fp.split("/")[-1] if fp else ""
            aid = agent_id[:12]
            events.append((ts, f"DA:{aid}", f"{tool} {detail}", "tool"))

        # Main agent messages (brief)
        elif ev == "agent.message" and agent == "main" and not agent_id:
            text = d.get("text", "")[:60]
            if text:
                events.append((ts, "main", f"MSG: {text}", "msg"))

    # Deduplicate consecutive progress events on same lane
    filtered = []
    for e in events:
        if e[3] == "tool" and filtered and filtered[-1][1] == e[1] and filtered[-1][3] == "tool":
            filtered[-1] = e  # replace with latest
        else:
            filtered.append(e)

    # Print
    lanes = []
    for e in filtered:
        if e[1] not in lanes:
            lanes.append(e[1])

    print()
    print(f"{'TIME':<14} {'LANE':<25} EVENT")
    print("-" * 80)
    prev_ts = ""
    for ts, lane, desc, _ in filtered:
        ts_short = ts[11:] if ts != prev_ts else ""
        prev_ts = ts
        print(f"{ts_short:<14} {lane:<25} {desc}")
    print("-" * 80)
    print(f"\nTotal events: {len(filtered)} | Lanes: {', '.join(lanes)}")


if __name__ == "__main__":
    main()

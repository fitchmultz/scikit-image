#!/usr/bin/env python3
"""Render a PR-ready scikit-image change brief as Markdown and HTML."""

from __future__ import annotations

import argparse
import html
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", default="Scoped scikit-image change")
    parser.add_argument("--plan", default="See engineering notes and changed files below.")
    parser.add_argument("--summary", default="See changed files and commit details below.")
    parser.add_argument("--test", action="append", default=[])
    parser.add_argument("--qa-note", action="append", default=[])
    parser.add_argument("--devops-note", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--out-dir", default=".cursor/acme-sdk-accelerator")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    status = git("status", "--short")
    stat = git("diff", "--stat") if status else git("diff", "--stat", "HEAD~1..HEAD")
    data = {
        "request": args.request,
        "plan": args.plan,
        "summary": args.summary,
        "branch": git("branch", "--show-current"),
        "commit": git("rev-parse", "--short", "HEAD"),
        "status": status or "clean",
        "stat": stat,
        "tests": args.test or ["Validation evidence pending"],
        "qa": args.qa_note or ["Verify changed behavior and any edge cases named in the tests."],
        "devops": args.devops_note or ["Run the normal scikit-image CI gates before merge."],
        "risks": args.risk or ["Residual risk: none recorded."],
    }

    md = markdown(data)
    (out_dir / "change-brief.md").write_text(md)
    (out_dir / "change-brief.html").write_text(to_html(data, md))
    print(out_dir / "change-brief.md")
    print(out_dir / "change-brief.html")
    return 0


def git(*args: str) -> str:
    try:
        p = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
    except OSError:
        return ""
    return p.stdout.strip() if p.returncode == 0 else ""


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def fenced(value: str) -> str:
    return f"```text\n{value}\n```" if value else "```text\n(none)\n```"


def markdown(d: dict) -> str:
    return f"""# PR-ready change brief

## Request

{d['request']}

## Plan

{d['plan']}

## PM summary

{d['summary']}

## Engineering notes

- Branch: `{d['branch'] or 'unknown'}`
- Commit: `{d['commit'] or 'unknown'}`
- AI disclosure: Cursor Agent assisted with this change; author remains responsible for review.

### Changed files

{fenced(d['stat'])}

## QA notes

{bullets(d['qa'])}

## DevOps / CI notes

{bullets(d['devops'])}

## Validation

{bullets(d['tests'])}

## Residual risk

{bullets(d['risks'])}

## Local git status

{fenced(d['status'])}
"""


def to_html(d: dict, md: str) -> str:
    sections = []
    current_title = None
    current_lines: list[str] = []
    for line in md.splitlines():
        if line.startswith("## "):
            if current_title:
                sections.append((current_title, current_lines))
            current_title = line[3:]
            current_lines = []
        elif current_title and not line.startswith("# "):
            current_lines.append(line)
    if current_title:
        sections.append((current_title, current_lines))

    cards = "\n".join(
        f"<section class='card'><h2>{html.escape(title)}</h2>{render_lines(lines)}</section>"
        for title, lines in sections
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>PR-ready change brief</title>
<style>
:root {{ color-scheme: light dark; --bg: #f7f7f4; --fg: #171717; --card: #fff; --muted: #5f6368; --accent: #5b6cff; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #111; --fg: #eee; --card: #1c1c1c; --muted: #aaa; }} }}
body {{ margin: 0; padding: 32px; background: var(--bg); color: var(--fg); font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
main {{ max-width: 960px; margin: 0 auto; }}
h1 {{ margin: 0 0 8px; font-size: 34px; }}
.subtitle {{ color: var(--muted); margin-bottom: 24px; }}
.grid {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
.card {{ background: var(--card); border: 1px solid color-mix(in srgb, var(--fg) 12%, transparent); border-radius: 14px; padding: 18px; box-shadow: 0 1px 6px color-mix(in srgb, #000 10%, transparent); }}
h2 {{ color: var(--accent); margin-top: 0; font-size: 18px; }}
pre {{ overflow: auto; padding: 12px; border-radius: 10px; background: color-mix(in srgb, var(--fg) 8%, transparent); }}
code {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
ul {{ padding-left: 20px; }}
</style>
</head>
<body>
<main>
<h1>PR-ready change brief</h1>
<p class="subtitle">Generated for Engineering, PM, QA, and DevOps from one Cursor Agent run.</p>
<div class="grid">{cards}</div>
</main>
</body>
</html>
"""


def render_lines(lines: list[str]) -> str:
    out: list[str] = []
    in_pre = False
    list_open = False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            if in_pre:
                out.append("</code></pre>")
            else:
                if list_open:
                    out.append("</ul>")
                    list_open = False
                out.append("<pre><code>")
            in_pre = not in_pre
            continue
        if in_pre:
            out.append(html.escape(line) + "\n")
        elif line.startswith("### "):
            if list_open:
                out.append("</ul>")
                list_open = False
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            if not list_open:
                out.append("<ul>")
                list_open = True
            out.append(f"<li>{inline(line[2:])}</li>")
        elif line:
            if list_open:
                out.append("</ul>")
                list_open = False
            out.append(f"<p>{inline(line)}</p>")
    if list_open:
        out.append("</ul>")
    if in_pre:
        out.append("</code></pre>")
    return "\n".join(out)


def inline(text: str) -> str:
    escaped = html.escape(text)
    return re_code(escaped)


def re_code(text: str) -> str:
    parts = text.split("`")
    for i in range(1, len(parts), 2):
        parts[i] = f"<code>{parts[i]}</code>"
    return "".join(parts)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def _append_event(novel_dir: Path, event: str, **payload: object) -> None:
    path = novel_dir / "tmp" / "run-metadata" / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": _utc_now(), "event": event, **payload}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        return ""


def _find_chapter_path(novel_dir: Path, episode: int) -> Path | None:
    chapters_dir = novel_dir / "chapters"
    if not chapters_dir.exists():
        return None
    matches = sorted(chapters_dir.glob(f"**/chapter-{episode:02d}.md"))
    return matches[0] if matches else None


def _has_heading_with_bullets(text: str, headings: tuple[str, ...]) -> bool:
    if not text:
        return False
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() not in headings:
            continue
        bullet_count = 0
        for inner in lines[idx + 1 :]:
            stripped = inner.strip()
            if stripped.startswith("## "):
                break
            if stripped.startswith(("- ", "* ")):
                bullet_count += 1
        if bullet_count > 0:
            return True
    return False


def _mentions_episode(text: str, episode: int) -> bool:
    if not text:
        return False
    patterns = (
        rf"\bchapter-{episode:02d}\b",
        rf"(?<!\d){episode}화(?!\d)",
        rf"episode[- ]?{episode:02d}\b",
    )
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--novel-dir", required=True)
    parser.add_argument("--episode", required=True, type=int)
    args = parser.parse_args(argv[1:])

    novel_dir = Path(args.novel_dir)
    episode = args.episode

    required_files = {
        "summaries/running-context.md": novel_dir / "summaries" / "running-context.md",
        "summaries/episode-log.md": novel_dir / "summaries" / "episode-log.md",
        "summaries/character-tracker.md": novel_dir
        / "summaries"
        / "character-tracker.md",
        "summaries/action-log.md": novel_dir / "summaries" / "action-log.md",
    }

    chapter_path = _find_chapter_path(novel_dir, episode)
    reasons: list[str] = []

    if chapter_path is None:
        reasons.append(f"missing_chapter_{episode:02d}")
        chapter_text = ""
    else:
        chapter_text = _read_text(chapter_path)
        if not chapter_text:
            reasons.append("chapter_unreadable")
        if "### EPISODE_META" not in chapter_text:
            reasons.append("missing_episode_meta")

    loaded = {label: _read_text(path) for label, path in required_files.items()}
    for label, text in loaded.items():
        if not text:
            reasons.append(f"missing_required={label}")

    running_context = loaded["summaries/running-context.md"]
    action_log = loaded["summaries/action-log.md"]
    episode_log = loaded["summaries/episode-log.md"]

    if running_context and not _has_heading_with_bullets(
        running_context,
        ("## Immediate Carry-Forward", "## 직전 화 직결 상태"),
    ):
        reasons.append("missing_carry_forward_section")

    if action_log and not _mentions_episode(action_log, episode):
        reasons.append(f"action_log_missing_episode_{episode:02d}")

    if episode_log and not _mentions_episode(episode_log, episode):
        reasons.append(f"episode_log_missing_episode_{episode:02d}")

    if reasons:
        _append_event(
            novel_dir,
            "writer_done_gate_failed",
            episode=episode,
            reasons=reasons,
        )
        print("GATE_FAIL " + " ".join(reasons))
        return 1

    _append_event(
        novel_dir,
        "writer_done_gate_passed",
        episode=episode,
        chapter=str(chapter_path.relative_to(novel_dir)) if chapter_path else "",
    )
    print(
        f"GATE_OK episode={episode:02d} "
        f"chapter={chapter_path.relative_to(novel_dir) if chapter_path else ''}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

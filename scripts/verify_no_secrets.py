#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

PATTERNS = {
    "github_classic_pat": re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    "github_fine_grained_pat": re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    "huggingface_token": re.compile(r"hf_[A-Za-z0-9]{20,}"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "literal_qwen_api_key": re.compile(
        r"QWEN3VL_API_KEY\s*=\s*['\"](?!<|\$|\{)[^'\"\s]{8,}['\"]"
    ),
}

SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", "results", ".venv"}
TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".toml", ".yml", ".yaml", ".json", ".cff",
    ".sh", ".gitignore", ".gitattributes", ".editorconfig",
}


def is_candidate(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name in {"LICENSE", ".gitignore", ".gitattributes", ".editorconfig"}:
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def main() -> None:
    findings: list[str] = []
    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or not is_candidate(path.relative_to(ROOT)):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path.relative_to(ROOT)}:{line}: {name}")

    if findings:
        print("SECRET_SCAN=FAIL")
        for finding in findings:
            print(finding)
        raise SystemExit(1)
    print(f"SECRET_SCAN=PASS files_scanned={scanned}")


if __name__ == "__main__":
    main()

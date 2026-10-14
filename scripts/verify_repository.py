from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

required = [
    'LICENSE', 'LICENSE.vi.md', 'MODEL_LICENSE.md', 'MODEL_LICENSE.vi.md',
    'LICENSE-NOTES.md', 'LICENSE-NOTES.vi.md', 'LICENSE-SOURCES.md', 'LICENSE-SOURCES.vi.md',
    'THIRD_PARTY_LICENSES/QWEN3-VL-APACHE-2.0.txt',
    '.github/CODEOWNERS', '.github/workflows/ci.yml', '.github/workflows/repository-audit.yml',
]
for rel in required:
    if not (ROOT / rel).is_file():
        errors.append(f'missing required file: {rel}')

if (ROOT / 'docs/superpowers').exists():
    errors.append('internal planning directory docs/superpowers must not be public')
if (ROOT / 'IMPLEMENTATION-ASSET-NOTES.md').exists():
    errors.append('internal implementation notes must not be public')

# Public Markdown is bilingual. English files use NAME.md; Vietnamese files use NAME.vi.md.
skip = set()
for p in ROOT.rglob('*.md'):
    if any(part in {'.git', '.pytest_cache', 'results'} for part in p.parts):
        continue
    rel = p.relative_to(ROOT)
    if p.name == 'LICENSE.vi.md':
        en = ROOT / 'LICENSE'
        if not en.exists():
            errors.append('missing English legal LICENSE for LICENSE.vi.md')
    elif p.name.endswith('.vi.md'):
        en = p.with_name(p.name[:-6] + '.md')
        if not en.exists():
            errors.append(f'missing English pair for {rel}')
    else:
        vi = p.with_name(p.stem + '.vi.md')
        if not vi.exists():
            errors.append(f'missing Vietnamese pair for {rel}')
    head = p.read_text(encoding='utf-8', errors='replace')[:2500]
    if 'Language / Ngôn ngữ:' not in head:
        errors.append(f'missing language switch: {rel}')

license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8') if (ROOT/'LICENSE').exists() else ''
if 'Đăng Khoa <i.am@dangkhoa.dev>' not in license_text:
    errors.append('MIT LICENSE missing required author/email')

model_text = (ROOT / 'MODEL_LICENSE.md').read_text(encoding='utf-8') if (ROOT/'MODEL_LICENSE.md').exists() else ''
for token in ('Qwen/Qwen3-VL-8B-Instruct', 'Apache License 2.0', 'redistribute'):
    if token.lower() not in model_text.lower():
        errors.append(f'MODEL_LICENSE.md missing: {token}')

if errors:
    for e in errors: print(f'REPOSITORY_AUDIT_ERROR={e}')
    raise SystemExit(1)
print('REPOSITORY_AUDIT=PASS')
print(f'PUBLIC_MARKDOWN_FILES={sum(1 for p in ROOT.rglob("*.md") if "results" not in p.parts and ".git" not in p.parts)}')

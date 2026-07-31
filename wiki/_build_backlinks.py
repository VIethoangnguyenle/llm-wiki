"""
Build backlinks index for Second Brain wiki, and audit vault health.

Scans all .md files in wiki/, extracts [[wikilinks]], builds a reverse index.
Output: wiki/_backlinks.json

Usage:
    python wiki/_build_backlinks.py            # build _backlinks.json
    python wiki/_build_backlinks.py --check    # build + audit, exit 1 if broken links

The --check mode is what /cleanup runs. It reports mechanically verifiable
problems (broken links, size guardrails, index drift) so the audit does not
depend on the agent remembering to look.
"""
import json
import re
import os
import sys
from datetime import date
from pathlib import Path

WIKI_DIR = Path(__file__).parent
VAULT_DIR = WIKI_DIR.parent
BACKLINKS_FILE = WIKI_DIR / "_backlinks.json"

# Meta files — scanned for links, but never counted as articles
META_FILES = {"_index.md", "_glossary.md", "_dashboard.md", "_ops_log.md", "overview.md"}

MIN_LINES, MAX_LINES = 15, 120   # Article Size Guardrails (AGENTS.md)
MIN_LINKS = 2                    # each article links to >= 2 others (AGENTS.md)

CODE_BLOCK = re.compile(r'```.*?```', re.S)
CODE_SPAN = re.compile(r'`[^`\n]*`')
WIKILINK = re.compile(r'\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]')
FRONTMATTER = re.compile(r'^---\n.*?\n---\n', re.S)


def strip_code(text: str) -> str:
    """Drop fenced blocks and inline spans — `[[wikilinks]]` in code is not a link."""
    return CODE_SPAN.sub('', CODE_BLOCK.sub('', text))


def link_name(target: str) -> str:
    """Normalize a link target to the note name Obsidian would resolve."""
    name = target.strip().split('/')[-1]
    return name[:-3] if name.endswith('.md') else name


def md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob('*.md') if p.is_file())


def load_vault():
    """Return (articles, meta, notes) where notes maps note-name -> path."""
    articles, meta = {}, {}
    for p in md_files(WIKI_DIR):
        (meta if p.name in META_FILES or p.name.startswith('_') else articles)[p.stem] = p
    notes = {p.stem: p for p in md_files(VAULT_DIR)}
    return articles, meta, notes


def build_backlinks(articles: dict, meta: dict) -> dict:
    """Backlinks count only article->article links.

    Meta files (_index, _glossary) link to everything by construction; counting them
    would give every article a backlink and make orphan detection meaningless. Their
    links are still returned in `forward` so the audit can validate them.
    """
    forward = {}
    for name, path in {**articles, **meta}.items():
        text = strip_code(path.read_text(encoding='utf-8'))
        forward[name] = [link_name(t) for t in WIKILINK.findall(text)]

    backlinks: dict[str, list[str]] = {}
    for source, targets in forward.items():
        if source not in articles:
            continue
        for target in targets:
            refs = backlinks.setdefault(target, [])
            if source not in refs:
                refs.append(source)

    ranked = dict(sorted(backlinks.items(), key=lambda kv: len(kv[1]), reverse=True))
    return {
        "description": "Reverse link index. Maps article -> list of articles linking TO it.",
        "last_updated": date.today().isoformat(),
        "total_articles": len(articles),
        "total_links": sum(len(v) for v in ranked.values()),
        "backlinks": ranked,
    }, forward


def audit(articles: dict, meta: dict, notes: dict, forward: dict, backlinks: dict) -> dict:
    broken, stubs, oversize, thin, orphans = {}, [], [], [], []

    for source, targets in forward.items():
        for target in targets:
            if target not in notes:
                broken.setdefault(target, []).append(source)

    for name, path in articles.items():
        text = path.read_text(encoding='utf-8')
        body = FRONTMATTER.sub('', text)
        lines = [ln for ln in body.splitlines() if ln.strip()]
        if len(lines) < MIN_LINES:
            stubs.append((name, len(lines)))
        elif len(lines) > MAX_LINES:
            oversize.append((name, len(lines)))
        outbound = {t for t in forward.get(name, []) if t in articles and t != name}
        if len(outbound) < MIN_LINKS:
            thin.append((name, len(outbound)))
        if not backlinks.get(name):
            orphans.append(name)

    index_text = (WIKI_DIR / '_index.md').read_text(encoding='utf-8')
    unindexed = sorted(n for n in articles if f'[[{n}]]' not in index_text)

    unlogged = []
    log_path = WIKI_DIR / '_absorb_log.json'
    if log_path.exists():
        logged = set(json.loads(log_path.read_text(encoding='utf-8')).get('sources', {}))
        raw_dir = VAULT_DIR / 'raw'
        for p in md_files(raw_dir) if raw_dir.exists() else []:
            if p.name.startswith('_'):
                continue
            if str(p.relative_to(VAULT_DIR)) not in logged:
                unlogged.append(str(p.relative_to(VAULT_DIR)))

    return {
        "broken_links": broken,
        "stubs": sorted(stubs, key=lambda x: x[1]),
        "oversize": sorted(oversize, key=lambda x: -x[1]),
        "under_linked": sorted(thin, key=lambda x: x[1]),
        "orphans": sorted(orphans),
        "missing_from_index": unindexed,
        "raw_not_in_absorb_log": sorted(unlogged),
    }


def report(a: dict) -> int:
    def section(title, items, fmt=str):
        print(f"\n{'✅' if not items else '⚠️ '} {title}: {len(items)}")
        for it in items[:20] if isinstance(items, list) else list(items)[:20]:
            print(f"     {fmt(it)}")
        extra = len(items) - 20
        if extra > 0:
            print(f"     … và {extra} mục nữa")

    print(f"\n{'=' * 60}\n  WIKI HEALTH CHECK\n{'=' * 60}")
    broken = a["broken_links"]
    print(f"\n{'✅' if not broken else '❌'} Wikilink hỏng: {len(broken)}")
    for target, sources in broken.items():
        print(f"     [[{target}]]  <- {', '.join(sorted(set(sources)))}")

    section("Bài stub (< %d dòng)" % MIN_LINES, a["stubs"], lambda x: f"{x[0]} ({x[1]} dòng)")
    section("Bài quá dài (> %d dòng)" % MAX_LINES, a["oversize"], lambda x: f"{x[0]} ({x[1]} dòng)")
    section("Bài link ra < %d bài khác" % MIN_LINKS, a["under_linked"], lambda x: f"{x[0]} ({x[1]} link)")
    section("Bài không ai trỏ tới (orphan)", a["orphans"])
    section("Bài thiếu trong _index.md", a["missing_from_index"])
    section("Raw chưa có trong _absorb_log.json", a["raw_not_in_absorb_log"])

    if broken:
        print(f"\n❌ FAIL — {len(broken)} wikilink không resolve được.\n")
        return 1
    print("\n✅ PASS — không có wikilink hỏng.\n")
    return 0


if __name__ == "__main__":
    check = "--check" in sys.argv
    articles, meta, notes = load_vault()
    result, forward = build_backlinks(articles, meta)

    BACKLINKS_FILE.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ Backlinks: {len(result['backlinks'])} targets, "
          f"{result['total_links']} links, {result['total_articles']} articles")
    print(f"📄 {BACKLINKS_FILE}")

    if not check:
        print("\n📊 Top linked:")
        for target, sources in list(result['backlinks'].items())[:10]:
            print(f"  {target}: {len(sources)}")
        sys.exit(0)

    sys.exit(report(audit(articles, meta, notes, forward, result['backlinks'])))

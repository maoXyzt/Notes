#!/usr/bin/env python3

"""
This script generates a structured representation of markdown files
in the 'docs' directory.

It builds a hierarchical structure of groups and pages, ignoring certain
files and drafts.

The structure is saved as a JSON file and a Table of Contents (TOC) is
generated in markdown format.
"""

import fnmatch
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import frontmatter
from pydantic_settings import BaseSettings
from rich import print

from .utils.constants import INDEX_FILENAMES
from .utils.structure import CJSONEncoder, GroupInfo, PageInfo
from .utils.tools import custom_quote

ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / 'docs'


class Settings(BaseSettings):
    indent_size: int = 2  # indent with 2 spaces
    includes: tuple[str, ...] = ('*.md',)
    # NOTE: `excludes` patterns are matched via fnmatch against paths of the
    # form `./relative/path.md`. A leading `./` therefore anchors the match to
    # the docs root — `./index.md` only excludes the root index, NOT nested
    # `index.md` files (which are intentionally kept so that
    # `PageInfo.build_page` can convert them into directory links). To
    # exclude at any depth, use `*/index.md` or similar.
    excludes: tuple[str, ...] = ('./index.md', './toc.md')
    structure_json_output: Path = DOCS_ROOT / 'structure.json'
    toc_md_output: Path = DOCS_ROOT / 'toc.md'
    # TOC title
    toc_title: str = 'Table of Contents'
    max_header_level: int = 3  # level higher than this will be formatted as list
    min_level: int = 0  # level less than this will be ignored in TOC
    recent_updates_title: str = '最近更新'
    recent_updates_count: int = 10
    recent_updates_excerpt_lines: int = 3
    recent_updates_excerpt_fallback_scan_lines: int = 200
    recent_updates_excerpt_max_line_length: int = 120


settings = Settings()


@dataclass
class RecentNote:
    title: str
    link: str
    modified: datetime
    modified_raw: str
    excerpt_lines: list[str]


def main() -> None:
    """Analyse the directory structure and generate `toc.md` and `structure.json`."""
    assert DOCS_ROOT.exists()

    if not settings.toc_md_output.exists():
        print(
            '[bold yellow]Warning:[/bold yellow] '
            + f'{settings.toc_md_output} does not exist. Creating a new one...'
        )

    # print(json.dumps(build_structure(root), indent=2, cls=MyJSONEncoder))
    root_info = build_from_root(DOCS_ROOT)
    order_group_by_num_of_children(root_info)
    root_info.prefix_title_index(max_header_level=settings.max_header_level - 1)
    with settings.structure_json_output.open('w+', encoding='utf8', newline='\n') as f:
        json.dump(root_info.items, f, indent=2, cls=CJSONEncoder, ensure_ascii=False)

    # file_paths = find_markdowns(root)
    # side_bars_list = create_sidebar(file_paths)

    # with (root / "_sidebar.md").open("w+", encoding="utf8") as f:
    #     f.write("\n".join(side_bars_list))

    toc_lines = make_toc_content(
        root_info,
        min_level=settings.min_level,
        max_header_level=settings.max_header_level,
    )
    toc_lines = toc_lines[1:]  # remove the root title
    toc_lines = _format_toc(toc_lines)
    print('[bold]Table of Contents:[/bold]')
    print('\n'.join(toc_lines))

    lines = ['<!-- TOC -->', *toc_lines, '<!-- /TOC -->']
    if settings.toc_md_output.exists():
        old_lines = settings.toc_md_output.read_text(encoding='utf8').splitlines()
        lines = _replace_section_by_markers(
            old_lines=old_lines,
            section_lines=toc_lines,
            start_marker='<!-- TOC -->',
            end_marker='<!-- /TOC -->',
        )

    recent_notes = build_recent_notes(DOCS_ROOT)
    recent_updates_section = make_recent_updates_content(recent_notes)
    lines = _replace_recent_updates_section(lines, recent_updates_section)
    settings.toc_md_output.write_text('\n'.join(lines), encoding='utf8', newline='\n')
    print('[bold green]Done![/bold green]')

    for x in root_info.items:
        print(x.model_dump())


def build_from_root(root: Path) -> GroupInfo:
    """Build a structure of the directory.

    Args:
        root: The root directory.
    """
    root_group = GroupInfo.build_group(
        folder=root, root=root, includes=settings.includes, excludes=settings.excludes
    )
    root_group.text = settings.toc_title
    return root_group


def order_group_by_num_of_children(
    group: GroupInfo,
    add_title_index: bool = True,
) -> None:
    """Recursively sort a group and its children by the number of children."""

    def sum_items(item: GroupInfo | PageInfo) -> int:
        if isinstance(item, GroupInfo):
            return sum([sum_items(child) for child in item.items])
        else:
            return 1

    def _sort_key(item: GroupInfo | PageInfo):
        if isinstance(item, GroupInfo):
            return sum_items(item)
        else:
            return math.inf

    for item in group.items:
        if isinstance(item, GroupInfo) and item.items:
            order_group_by_num_of_children(item)

    group.items.sort(key=_sort_key, reverse=True)
    return


def make_toc_content(
    item: GroupInfo | PageInfo,
    lines: list[str] | None = None,
    level: int = 0,
    min_level: int = 0,
    max_header_level: int = 3,
) -> list[str]:
    """Generate Table of Contents (TOC) for a group recursively."""
    if lines is None:
        lines = []

    if level >= min_level:
        if line_content := _make_line(item):
            indent = _get_indented_prefix(
                level,
                max_header_level=max_header_level,
                has_children=bool(getattr(item, 'items', None)),
            )
            lines.append(f'{indent} {line_content}')
    if isinstance(item, GroupInfo):
        for c in item.items:
            make_toc_content(
                c,
                lines,
                level=level + 1,
                min_level=settings.min_level,
                max_header_level=max_header_level,
            )
    return lines


def _get_indented_prefix(
    level: int,
    max_header_level: int = 3,
    has_children: bool = False,
) -> str:
    if level < max_header_level:
        if has_children:
            # should be formatted as header
            return '#' * (level + 1)
        else:
            return '*'
    else:
        # should be formatted as list
        return ' ' * settings.indent_size * (level - max_header_level) + '*'


def _make_line(item: PageInfo | GroupInfo) -> str:
    """Make a line for TOC content."""
    if isinstance(item, GroupInfo):
        return item.text
    # PageInfo whose link points at a directory comes from an index/atlas file.
    # Its `text` is the parent folder name, which duplicates the enclosing
    # group's title — show it as a generic "overview" link instead.
    text = '📖 概览' if item.link.endswith('/') else item.text
    return f'[{text}](.{custom_quote(item.link, safe="/")})'


def _format_toc(lines: list[str]) -> list[str]:
    """Format the TOC content.

    Rules:
    - Insert a blank line between headers and contents.
    """
    insert_blank_lines_idx: list[int] = []
    for i in range(len(lines) - 1):
        l1, l2 = lines[i], lines[i + 1]
        l1 = l1.strip()
        l2 = l2.strip()
        if (
            (l1.startswith('#') and l2.startswith('#'))
            or (l1.startswith('#') and l2)
            or (l1 and l2.startswith('#'))
        ):
            print(l1[:5], '\t', l2[:5])
            insert_blank_lines_idx.append(i + 1)
    for idx in reversed(insert_blank_lines_idx):
        lines.insert(idx, '')
    return lines


def _replace_section_by_markers(
    old_lines: list[str],
    section_lines: list[str],
    start_marker: str,
    end_marker: str,
    section_header: str | None = None,
) -> list[str]:
    start, end = None, None
    for i, line in enumerate(old_lines):
        if line.strip().startswith(start_marker):
            start = i
        elif line.strip().startswith(end_marker):
            end = i
    if start is not None and end is not None and start < end:
        return old_lines[: start + 1] + section_lines + old_lines[end:]

    if not old_lines:
        return [start_marker, *section_lines, end_marker]

    append_lines = []
    if old_lines[-1].strip():
        append_lines.append('')
    if section_header:
        append_lines.extend([section_header, ''])
    append_lines.extend([start_marker, *section_lines, end_marker])
    return old_lines + append_lines


def _replace_recent_updates_section(
    old_lines: list[str],
    section_lines: list[str],
) -> list[str]:
    start_marker = '<!-- RECENT_UPDATES -->'
    end_marker = '<!-- /RECENT_UPDATES -->'
    section_header = f'## {settings.recent_updates_title}'
    toc_start_marker = '<!-- TOC -->'

    start, end = None, None
    for i, line in enumerate(old_lines):
        if line.strip().startswith(start_marker):
            start = i
        elif line.strip().startswith(end_marker):
            end = i
    lines = old_lines
    if start is not None and end is not None and start < end:
        # Remove existing recent-updates block (and optional heading/blank lines before it),
        # then reinsert it before TOC for stable ordering.
        block_start = start
        if start >= 2 and lines[start - 1] == '' and lines[start - 2] == section_header:
            block_start = start - 2
        elif start >= 1 and lines[start - 1] == section_header:
            block_start = start - 1
        block_end = end
        if end + 1 < len(lines) and lines[end + 1] == '':
            block_end = end + 1
        lines = lines[:block_start] + lines[block_end + 1 :]

    toc_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(toc_start_marker):
            toc_start = i
            break

    block = [section_header, '', start_marker, *section_lines, end_marker, '']
    if toc_start is not None:
        return lines[:toc_start] + block + lines[toc_start:]

    if not lines:
        return [start_marker, *section_lines, end_marker]

    append_lines: list[str] = []
    if lines[-1].strip():
        append_lines.append('')
    append_lines.extend(block[:-1])
    return lines + append_lines


def build_recent_notes(root: Path) -> list[RecentNote]:
    notes: list[RecentNote] = []
    for filepath in root.rglob('*.md'):
        if filepath.name in INDEX_FILENAMES:
            continue
        rel_p = filepath.relative_to(root)
        rel_p_str = f'./{rel_p.as_posix()}'
        if not any(
            fnmatch.fnmatch(rel_p_str, pattern) for pattern in settings.includes
        ):
            continue
        if any(fnmatch.fnmatch(rel_p_str, pattern) for pattern in settings.excludes):
            continue

        post = frontmatter.load(filepath.as_posix())
        if post.get('NoteStatus') == 'draft':
            continue

        modified_raw = post.get('modified')
        if not isinstance(modified_raw, str):
            continue
        modified = _parse_modified_datetime(modified_raw)
        if modified is None:
            continue

        title = filepath.stem

        link = f'./{custom_quote(rel_p.as_posix(), safe="/")}'
        excerpt_lines = _extract_excerpt_lines(post.content)
        notes.append(
            RecentNote(
                title=title,
                link=link,
                modified=modified,
                modified_raw=modified_raw,
                excerpt_lines=excerpt_lines,
            )
        )

    notes.sort(key=lambda x: x.modified, reverse=True)
    return notes[: settings.recent_updates_count]


def _extract_excerpt_lines(content: str) -> list[str]:
    strict_lines: list[str] = []
    fallback_lines: list[str] = []
    in_code_block = False
    for idx, raw_line in enumerate(content.splitlines()):
        if idx >= settings.recent_updates_excerpt_fallback_scan_lines:
            break
        line = raw_line.strip()
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not line or line.startswith('#') or line.startswith('>'):
            continue

        normalized = _truncate_excerpt_line(_strip_markdown_links(line))
        if _is_noisy_excerpt_line(line):
            # Keep as fallback candidates when clean prose is insufficient.
            fallback_lines.append(normalized)
            continue

        strict_lines.append(normalized)
        if len(strict_lines) >= settings.recent_updates_excerpt_lines:
            break

    if len(strict_lines) >= settings.recent_updates_excerpt_lines:
        return strict_lines[: settings.recent_updates_excerpt_lines]

    remaining = settings.recent_updates_excerpt_lines - len(strict_lines)
    return strict_lines + fallback_lines[:remaining]


_unordered_list_re = re.compile(r'^[-*+]\s+')
_ordered_list_re = re.compile(r'^\d+\.\s+')
_markdown_image_re = re.compile(r'!\[([^\]]*)\]\([^)]*\)')
_markdown_link_re = re.compile(r'\[([^\]]+)\]\([^)]*\)')
_wikilink_re = re.compile(r'\[\[([^\]]+)\]\]')


def _is_noisy_excerpt_line(line: str) -> bool:
    # Skip list/meta heavy lines in the primary excerpt selection.
    return (
        bool(_unordered_list_re.match(line))
        or bool(_ordered_list_re.match(line))
        or line.startswith('![')
        or line.startswith('|')
        or line.startswith('---')
        or line.startswith('***')
        or line.startswith('```')
        or line.startswith('<!--')
    )


def _strip_markdown_links(line: str) -> str:
    # Excerpts get embedded into toc.md as blockquotes; relative paths written
    # inside source files would otherwise resolve against docs root and trip
    # VitePress' dead-link check. Wikilinks survive linkage but read poorly in
    # a summary. Downgrade all link/image syntax to plain display text.
    line = _markdown_image_re.sub(r'\1', line)
    line = _markdown_link_re.sub(r'\1', line)
    line = _wikilink_re.sub(_wikilink_display_text, line)
    return line


def _wikilink_display_text(match: re.Match[str]) -> str:
    inner = match.group(1)
    # Obsidian alias form: [[target|display]] — prefer the display text.
    if '|' in inner:
        inner = inner.split('|', 1)[1]
    # Drop heading anchor if no alias was provided: [[target#section]] -> target.
    elif '#' in inner:
        inner = inner.split('#', 1)[0]
    return inner.strip()


def _truncate_excerpt_line(line: str) -> str:
    max_len = settings.recent_updates_excerpt_max_line_length
    if len(line) <= max_len:
        return line
    return line[: max_len - 3].rstrip() + '...'


def make_recent_updates_content(notes: list[RecentNote]) -> list[str]:
    if not notes:
        return ['暂无符合条件的最近更新文档。']

    lines: list[str] = []
    for note in notes:
        lines.append(
            f'- [{note.title}]({note.link}) · {_format_modified_datetime(note.modified)}'
        )
        if note.excerpt_lines:
            lines.extend(f'  > {excerpt}' for excerpt in note.excerpt_lines)
            lines.append('  > ...')
        else:
            lines.append('  > （暂无可展示摘要）')
    return lines


def _format_modified_datetime(dt: datetime) -> str:
    """Format datetime into a readable local string."""
    return dt.strftime('%Y-%m-%d %H:%M')


def _parse_modified_datetime(raw: str) -> datetime | None:
    text = raw.strip()
    if not text:
        return None
    if text.endswith('Z'):
        text = text[:-1] + '+00:00'

    # 1) Try fromisoformat first: handles many ISO variants.
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        pass

    # 2) Fallback common explicit formats.
    formats = (
        '%Y-%m-%dT%H:%M:%S.%f%z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S.%f%z',
        '%Y-%m-%d %H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
    )
    dt = None
    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            break
        except ValueError:
            continue
    return dt


if __name__ == '__main__':
    main()

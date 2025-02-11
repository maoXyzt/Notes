#!/usr/bin/env python3

"""
This script generates a structured representation of markdown files
in the 'docs' directory.

It builds a hierarchical structure of groups and pages, ignoring certain
files and drafts.

The structure is saved as a JSON file and a Table of Contents (TOC) is
generated in markdown format.
"""

import json
from pathlib import Path
from urllib.parse import quote

from pydantic_settings import BaseSettings
from rich import print

from .utils.structure import CJSONEncoder, GroupInfo, PageInfo

ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / 'docs'


class Settings(BaseSettings):
    indent_size: int = 2  # indent with 2 spaces
    includes: tuple[str, ...] = ('*.md',)
    excludes: tuple[str, ...] = ('./index.md', './toc.md')
    structure_json_output: Path = DOCS_ROOT / 'structure.json'
    toc_md_output: Path = DOCS_ROOT / 'toc.md'
    # TOC title
    toc_title: str = 'Table of Contents'
    max_header_level: int = 3  # level higher than this will be formatted as list
    min_level: int = 0  # level less than this will be ignored in TOC


settings = Settings()


def main():
    """Analyse the directory structure and generate `toc.md` and `structure.json`."""
    assert DOCS_ROOT.exists()

    if not settings.toc_md_output.exists():
        print(
            '[bold yellow]Warning:[/bold yellow] '
            f'{settings.toc_md_output} does not exist. Creating a new one...'
        )

    # print(json.dumps(build_structure(root), indent=2, cls=MyJSONEncoder))
    root_info = build_from_root(DOCS_ROOT)
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
    toc_lines = _format_toc(toc_lines)
    print('[bold]Table of Contents:[/bold]')
    print('\n'.join(toc_lines))

    lines = ['<!-- TOC -->', *toc_lines, '<!-- /TOC -->']
    if settings.toc_md_output.exists():
        old_lines = settings.toc_md_output.read_text(encoding='utf8').splitlines()
        start, end = None, None
        for i, line in enumerate(old_lines):
            if line.strip().startswith('<!-- TOC -->'):
                start = i
            elif line.strip().startswith('<!-- /TOC -->'):
                end = i
        if start is not None and end is not None:
            lines = old_lines[: start + 1] + toc_lines + old_lines[end:]
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
            indent = _get_indented_prefix(level, max_header_level=max_header_level)
            lines.append(f'{indent} {line_content}')
    if children := getattr(item, 'items', None):
        for c in children:
            make_toc_content(
                c,
                lines,
                level=level + 1,
                min_level=settings.min_level,
                max_header_level=max_header_level,
            )
    return lines


def _get_indented_prefix(level: int, max_header_level: int = 3) -> str:
    if level < max_header_level:
        # should be formatted as header
        return '#' * (level + 1)
    else:
        # should be formatted as list
        return ' ' * settings.indent_size * (level - max_header_level) + '*'


def _make_line(item: PageInfo | GroupInfo) -> str:
    """Make a line for TOC content."""
    if isinstance(item, GroupInfo):
        return item.text
    else:
        return f'[{item.text}]({quote(item.link)})'


def _format_toc(lines: list[str]) -> list[str]:
    """Format the TOC content.

    Rules:
    - Insert a blank line between headers and contents.
    """
    insert_blank_lines_idx = []
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


if __name__ == '__main__':
    main()

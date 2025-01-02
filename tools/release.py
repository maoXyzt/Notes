"""
This script generates a structured representation of markdown files in the 'docs' directory.
It builds a hierarchical structure of groups and pages, ignoring certain files and drafts.
The structure is saved as a JSON file and a Table of Contents (TOC) is generated in markdown format.

Functions:
- build_structure(root: Path) -> GroupInfo: Builds the directory structure starting from the root.
- build_group(d: Path, root: Path, depth: int = 0) -> GroupInfo: Recursively builds groups for directories.
- _get_sort_key(p: Path) -> str: Generates a sort key for sorting files and directories.
- build_page(p: Path, root: Path) -> Optional[PageInfo]: Creates a PageInfo instance for markdown files.
- make_toc(group: GroupInfo, level: int = 0) -> List[str]: Generates a TOC for the given group.
- main(): Main function to execute the script.
"""

#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote

import frontmatter
from pypinyin import Style, lazy_pinyin

from .constants import NoteStatus

ROOT = Path(__file__).resolve().parents[1] / "docs"
INDENT = " " * 4
IGNORES = (
    "index.md",
    "readme.md",
    "toc.md",
)


class BasicItem(ABC):
    text: str


@dataclass
class PageInfo(BasicItem):
    text: str
    link: str


@dataclass
class GroupInfo(BasicItem):
    text: str
    collapsed: bool
    items: List[BasicItem]


class _MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (PageInfo, GroupInfo)):
            return o.__dict__
        return super().default(o)


def build_structure(root: Path) -> GroupInfo:
    """Build a structure of the directory.

    Args:
        root: The root directory.
    """
    root_group = build_group(root, root, depth=0)
    root_group.text = "root"
    return root_group


def build_group(d: Path, root: Path, depth: int = 0) -> GroupInfo:
    collapsed = depth > 1
    group = GroupInfo(text=d.name, collapsed=collapsed, items=[])
    for p in sorted(
        d.iterdir(),
        key=_get_sort_key,
    ):
        if p.name.startswith("."):
            # skip hidden files and directories
            continue
        if p.is_dir():
            item = build_group(p, root, depth=depth + 1)
            if item.items:
                group.items.append(item)
        elif p.is_file():
            item = build_page(p, root)
            if item:
                group.items.append(item)
    return group


def _get_sort_key(p: Path) -> str:
    text = p.name
    # convert alphabets to uppercase to make them sorted before Chinese characters
    text = text.upper()
    return ''.join(lazy_pinyin(text, style=Style.TONE3))


def build_page(p: Path, root: Path) -> Optional[PageInfo]:
    """Build a page_info instance from a markdown file.

    Args:
        p (Path): path to the markdown file.
        root (Path): root directory.

    Returns:
        Optional[PageInfo]: a page_info instance or None.
    """
    if p.suffix.lower() != ".md" or p.name in IGNORES:
        return None
    post = frontmatter.load(str(p))
    note_status = post.get("NoteStatus")
    if note_status == NoteStatus.Draft.value:
        # Ignore draft notes
        return None
    text = p.stem
    link = "/" + quote(str(p.relative_to(root)).replace("\\", "/"))
    return PageInfo(text=text, link=link)


def make_toc(group: GroupInfo, level: int = 0) -> List[str]:
    """Generate Table of Contents (TOC) for a group recursively."""
    lines = [] if level else ["# Table of Contents"]
    if level == 0:
        indent_ = "\n## "
    elif level == 1:
        indent_ = "\n### "
    else:
        indent_ = INDENT * (level - 2) + "* "

    for item in group.items:
        if isinstance(item, PageInfo):
            lines.append(f"{indent_}[{item.text}]({item.link})")
        elif isinstance(item, GroupInfo):
            lines.append(f"{indent_}{item.text}")
            lines.extend(make_toc(item, level=level + 1))
    return lines


def main():
    root = Path(ROOT).resolve()
    assert root.exists()

    # print(json.dumps(build_structure(root), indent=2, cls=MyJSONEncoder))
    structure = build_structure(root)
    with (root / "structure.json").open("w+", encoding="utf8", newline='\n') as f:
        json.dump(structure.items, f, indent=2, cls=_MyJSONEncoder, ensure_ascii=False)

    # file_paths = find_markdowns(root)
    # side_bars_list = create_sidebar(file_paths)

    # with (root / "_sidebar.md").open("w+", encoding="utf8") as f:
    #     f.write("\n".join(side_bars_list))

    toc_lines = make_toc(structure)
    (root / "toc.md").write_text("\n".join(toc_lines), encoding="utf8", newline='\n')
    print("Done")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote

from pypinyin import Style, lazy_pinyin

INDENT = " " * 4
ROOT = Path(__file__).resolve().parent / "docs"

IGNORES = (
    "index.md",
    "readme.md",
    "toc.md",
)


class BasicItem:
    text: str


@dataclass
class Page(BasicItem):
    text: str
    link: str


@dataclass
class Group(BasicItem):
    text: str
    collapsed: bool
    items: List[BasicItem]


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (Page, Group)):
            return o.__dict__
        return super().default(o)


def build_structure(root: Path) -> Group:
    root_group = build_group(root, root, depth=0)
    root_group.text = "root"
    return root_group


def _get_sort_key(p: Path) -> str:
    text = p.name
    # convert alphabets to uppercase to make them sorted before Chinese characters
    text = text.upper()
    return ''.join(lazy_pinyin(text, style=Style.TONE3))


def build_group(d: Path, root: Path, depth: int = 0) -> Group:
    collapsed = depth > 1
    group = Group(text=d.name, collapsed=collapsed, items=[])
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


def build_page(p: Path, root: Path) -> Optional[Page]:
    if p.suffix.lower() != ".md" or p.name in IGNORES:
        return None
    text = p.stem
    link = "/" + quote(str(p.relative_to(root)).replace("\\", "/"))
    return Page(text=text, link=link)


def make_toc(group: Group, level: int = 0) -> List[str]:
    lines = [] if level else ["# Table of Contents"]
    if level == 0:
        indent_ = "\n## "
    elif level == 1:
        indent_ = "\n### "
    else:
        indent_ = INDENT * (level - 2) + "* "

    for item in group.items:
        if isinstance(item, Page):
            lines.append(f"{indent_}[{item.text}]({item.link})")
        elif isinstance(item, Group):
            lines.append(f"{indent_}{item.text}")
            lines.extend(make_toc(item, level=level + 1))
    return lines


def main():
    root = Path(ROOT).resolve()
    assert root.exists()

    # print(json.dumps(build_structure(root), indent=2, cls=MyJSONEncoder))
    structure = build_structure(root)
    with (root / "structure.json").open("w+", encoding="utf8", newline='\n') as f:
        json.dump(structure.items, f, indent=2, cls=MyJSONEncoder, ensure_ascii=False)

    # file_paths = find_markdowns(root)
    # side_bars_list = create_sidebar(file_paths)

    # with (root / "_sidebar.md").open("w+", encoding="utf8") as f:
    #     f.write("\n".join(side_bars_list))

    toc_lines = make_toc(structure)
    with (root / "toc.md").open("w+", encoding="utf8") as f:
        f.write("\n".join(toc_lines))

    print("Done")


if __name__ == "__main__":
    main()

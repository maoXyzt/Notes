#!/usr/bin/env python3

import fnmatch
import json
from abc import ABCMeta
from pathlib import Path
from typing import Any, Self

import frontmatter
from pydantic import BaseModel as _BaseModel
from pydantic import Field
from pypinyin import Style, lazy_pinyin

from .tools import extract_h1_titles


class BaseItem(_BaseModel, metaclass=ABCMeta):
    text: str


class PageInfo(BaseItem):
    text: str
    link: str

    @classmethod
    def build_page(
        cls,
        filepath: Path,
        root: Path,
        *,
        includes: tuple[str, ...] = tuple(),
        excludes: tuple[str, ...] = tuple(),
    ) -> Self | None:
        """Build a page_info instance from a markdown file.

        Args:
            p (Path): path to the markdown file.
            root (Path): root directory.

        Returns:
            Optional[PageInfo]: a page_info instance or None.
        """
        rel_p = filepath.relative_to(root)
        rel_p_str = f'./{rel_p.as_posix()}'
        if not any(fnmatch.fnmatch(rel_p_str, pattern) for pattern in includes):
            return
        if any(fnmatch.fnmatch(rel_p_str, pattern) for pattern in excludes):
            return

        post = frontmatter.load(filepath.as_posix())
        if post.get('NoteStatus') == 'draft':
            return

        text = filepath.stem
        if text in ['index', 'atlas']:
            text = filepath.parent.name
            link = f'/{rel_p.parent.as_posix()}/'
        else:
            if h1 := extract_h1_titles(filepath):
                text = h1[0]
            link = f'/{rel_p.as_posix()}'
        return cls(text=text, link=link)


class GroupInfo(BaseItem):
    text: str
    items: list[PageInfo | Self] = Field(default_factory=list)
    collapsed: bool = False

    @classmethod
    def build_group(
        cls,
        folder: Path,
        root: Path,
        *,
        depth: int = 0,
        includes: tuple[str, ...] = tuple(),
        excludes: tuple[str, ...] = tuple(),
    ) -> Self:
        """Build a group structure from a folder path.

        Args:
            folder (Path): The folder path to build the group from
            root (Path): The root directory path used as reference for relative paths
            depth (int, optional): Current depth level in the folder hierarchy.
                Defaults to 0.
            includes (tuple[str, ...], optional): Glob patterns for files to include.
                Defaults to tuple().
            excludes (tuple[str, ...], optional): Glob patterns for files to exclude.
                Defaults to tuple().

        Raises:
            NotImplementedError: If the method is called on an abstract base class

        Returns:
            Self: A GroupInfo instance containing the hierarchical structure of
                the folder
        """
        collapsed = depth > 2
        group = cls(text=folder.name, collapsed=collapsed)
        for p in sorted(
            folder.iterdir(),
            key=_get_pinyin_sort_key,
        ):
            if p.name.startswith('.'):
                # Skip hidden files and directories
                continue
            if p.is_dir():
                sub_group = cls.build_group(
                    p, root=root, depth=depth + 1, includes=includes, excludes=excludes
                )
                if sub_group.items:
                    group.items.append(sub_group)
                    # if len(sub_group.items) == 1:
                    #     # If the sub-group contains only one item, use it as a page
                    #     page = sub_group.items[0]
                    #     group.items.append(page)
                    # else:
                    #     group.items.append(sub_group)
            elif p.is_file():
                page = PageInfo.build_page(
                    p, root=root, includes=includes, excludes=excludes
                )
                if page:
                    group.items.append(page)
            else:
                raise NotImplementedError(f'Unsupported file type: {p.as_posix()}')
        return group

    def prefix_title_index(
        self,
        index: int = 1,
        level: int = 1,
        max_header_level: int = 3,
    ) -> None:
        """Add title index to the group."""
        if level > max_header_level:
            return
        group_items = (x for x in self.items if isinstance(x, GroupInfo) and x.items)
        for i, item in enumerate(group_items, start=1):
            match level:
                case 1:
                    prefix = f'{i} -'
                case 2:
                    prefix = f'{index}.{i}'
                case 3:
                    prefix = f'({i})'
                case _:
                    prefix = ''
            item.text = f'{prefix} {item.text}'
            item.prefix_title_index(
                index=i,
                level=level + 1,
                max_header_level=max_header_level,
            )
        return


class CJSONEncoder(json.JSONEncoder):
    def default(self, o) -> Any:
        # if isinstance(o, list | tuple | set):
        #     return [self.default(x) for x in o]
        if hasattr(o, 'model_dump'):
            return o.model_dump()
        if hasattr(o, '__dict__'):
            return o.__dict__
        return super().default(o)


def _get_pinyin_sort_key(p: Path) -> str:
    text = p.name
    # NOTE: Sort index.md/'atlas.md' first
    if text in ['index.md', 'atlas.md']:
        return '0'
    # NOTE: Convert alphabets to uppercase
    # to make them sorted before Chinese characters
    text = text.upper()
    return ''.join(lazy_pinyin(text, style=Style.TONE3))

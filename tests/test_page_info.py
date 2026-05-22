"""Tests for PageInfo.build_page covering index/atlas, excludes, draft, and h1."""

from pathlib import Path

import pytest

from cli.utils.structure import PageInfo

INCLUDES = ('*.md',)
EXCLUDES = ('./index.md', './toc.md')


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return path


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return tmp_path


def test_normal_file_uses_h1_as_text(root: Path) -> None:
    f = write(root / 'sub' / 'foo.md', '# Real Title\n\nbody\n')

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is not None
    assert page.text == 'Real Title'
    assert page.link == '/sub/foo.md'


def test_normal_file_without_h1_falls_back_to_stem(root: Path) -> None:
    f = write(root / 'bar.md', 'just body, no heading\n')

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is not None
    assert page.text == 'bar'
    assert page.link == '/bar.md'


def test_index_file_uses_parent_dir_name_and_dir_link(root: Path) -> None:
    f = write(root / 'Linux' / 'SSH' / 'index.md', '# ignored heading\n')

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is not None
    assert page.text == 'SSH'
    # Link points at the parent directory and ends with '/' so the TOC layer
    # can recognise it as an "overview" link.
    assert page.link == '/Linux/SSH/'


def test_atlas_file_is_treated_like_index(root: Path) -> None:
    f = write(root / 'Rust' / 'atlas.md', '# whatever\n')

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is not None
    assert page.text == 'Rust'
    assert page.link == '/Rust/'


def test_root_index_is_excluded(root: Path) -> None:
    f = write(root / 'index.md', '# Site Home\n')

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is None


def test_nested_index_is_not_excluded_by_root_pattern(root: Path) -> None:
    # './index.md' pattern only matches the root-level file; nested index.md
    # must still produce a directory-overview page.
    f = write(root / 'deep' / 'index.md', '')

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is not None
    assert page.link == '/deep/'


def test_draft_file_is_skipped(root: Path) -> None:
    f = write(
        root / 'draft.md',
        '---\nNoteStatus: draft\n---\n\n# Draft Title\n',
    )

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is None


def test_non_markdown_file_is_skipped(root: Path) -> None:
    f = write(root / 'notes.txt', 'not markdown')

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is None


def test_h1_inside_fenced_code_block_is_ignored(root: Path) -> None:
    f = write(
        root / 'code.md',
        '```bash\n# this is a shell comment, not a heading\n```\n\n# Actual Title\n',
    )

    page = PageInfo.build_page(f, root=root, includes=INCLUDES, excludes=EXCLUDES)

    assert page is not None
    assert page.text == 'Actual Title'

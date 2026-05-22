from enum import Enum


class NoteStatus(str, Enum):
    Draft = 'draft'  # 草稿
    Editing = 'editing'  # 编辑中
    Review = 'review'  # 待审核
    Published = 'published'  # 已发布
    Updating = 'updating'  # 更新中
    Archived = 'archived'  # 已归档
    Deprecated = 'deprecated'  # 已弃用


# Filenames (without extension) treated as directory index pages.
# Used by TOC building (special-cased to point at the parent directory)
# and by the "recent updates" section (filtered out, since index pages
# rarely contain prose worth summarizing).
INDEX_STEMS: frozenset[str] = frozenset({'index', 'atlas'})
INDEX_FILENAMES: frozenset[str] = frozenset(f'{s}.md' for s in INDEX_STEMS)

from enum import Enum


class NoteStatus(str, Enum):
    Draft = 'draft'  # 草稿
    Editing = 'editing'  # 编辑中
    Review = 'review'  # 待审核
    Published = 'published'  # 已发布
    Updating = 'updating'  # 更新中
    Archived = 'archived'  # 已归档
    Deprecated = 'deprecated'  # 已弃用

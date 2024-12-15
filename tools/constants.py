from enum import Enum


class NoteStatus(str, Enum):
    Draft = "draft"
    Editing = "editing"
    Review = "review"
    Published = "published"
    Updating = "updating"
    Archived = "archived"
    Deprecated = "deprecated"

from dataclasses import dataclass
from dtos import ValidCategories

@dataclass
class DevBlogSummary:
    id : int
    category   : ValidCategories | str
    title      : str
    time_posted: str
    git_repo   : str
    img        : str



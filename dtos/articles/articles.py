from dataclasses import dataclass

@dataclass
class ArticleSummary:
    id: int
    category      : str
    title         : str
    summary       : str
    author        : str
    time_read   : str
    comments_count: int
    href: str = "#"


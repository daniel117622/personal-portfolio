from dataclasses import dataclass
from typing import List

@dataclass
class RecentActivity:
    id             : int
    dev_name       : str
    repo_name      : str
    contrib_summary: str
    href           : str = "#"

@dataclass
class FeaturedProject:
    id           : int
    category_name: str
    repo_name    : str
    contributor  : str
    last_active  : str
    href         : str = "#"

@dataclass
class SocialActivity:
    code_activity: List[RecentActivity]
    featured_projects: List[FeaturedProject]


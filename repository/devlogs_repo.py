from typing import Protocol, Optional, List
from functools import lru_cache

from dtos import ValidCategories
from dtos.devlogs import DevBlogSummary 

# 1. The Protocol
class DevlogsRepositoryProtocol(Protocol):
    def get_devlogs(self) -> Optional[List[DevBlogSummary]]:
        ...

# 2. The Real Implementation
class DevlogsRepository:
    def __init__(self, data_access=None):
        self.data_access = data_access

    def get_devlogs(self) -> Optional[List[DevBlogSummary]]:
        if self.data_access is None: 
            return None
        pass

# 3. The Mock Implementation
class MockDevlogsRepository:
    
    @lru_cache(maxsize=1)
    def get_devlogs(self) -> Optional[List[DevBlogSummary]]:
        return [
            DevBlogSummary(
                id=1,
                category=ValidCategories.DEVLOG(),
                title="Building and Hosting my Personal Portfolio on Kuhaku.DEV",
                time_posted="September 20, 2026",
                git_repo="https://github.com/daniel117622/personal-portfolio",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=2,
                category=ValidCategories.RESEARCH(),
                title="Measuring Coupling and Cohesion in OO Systems: A Retrospective",
                time_posted="September 1, 2026",
                git_repo="https://github.com/daniel117622/solid_static",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=3,
                category=ValidCategories.ACTIVE_PROJECTS(),
                title="PyGraph: Untangling Spaghetti Code with a New VSCode Extension",
                time_posted="August 24, 2026",
                git_repo="https://github.com/daniel117622/PyGraph",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=4,
                category=ValidCategories.DEVLOG(),
                title="Architecting a News-Style Personal Blog Engine",
                time_posted="January 13, 2026",
                git_repo="https://github.com/daniel117622/personal-blog",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=5,
                category=ValidCategories.EXPERIMENTAL_TECH(),
                title="Optimizing SpGEMM: Early Experiments with Iteration Spaces",
                time_posted="January 2, 2026",
                git_repo="https://github.com/daniel117622/iteration_spaces",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=6,
                category=ValidCategories.DEVLOG(),
                title="Speedrunning GraphQL Integrations in Flask",
                time_posted="November 28, 2025",
                git_repo="https://github.com/daniel117622/practicas-graphql-vetengage",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=7,
                category=ValidCategories.OLD_PROJECTS(),
                title="Building a 2D ASCII Arcade Engine in C++ using ncurses",
                time_posted="November 22, 2025",
                git_repo="https://github.com/daniel117622/ncurse-2d-engine",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=8,
                category=ValidCategories.ARTICLES(),
                title="Exploring the Composite Pattern and Pushdown Automata",
                time_posted="July 29, 2025",
                git_repo="https://github.com/daniel117622/pda-article",
                img="octocat.jpg",
            ),
            DevBlogSummary(
                id=9,
                category=ValidCategories.OLD_PROJECTS(),
                title="Tuning Chaos: Lessons from a Custom Chess Bot Platform",
                time_posted="June 3, 2025",
                git_repo="https://github.com/daniel117622/RamseyChess",
                img="octocat.jpg",
            ),
        ]
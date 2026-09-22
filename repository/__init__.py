from .articles_repo import ArticlesRepository, MockArticlesRepository 
from .common_repo import MockCommonRepository, CommonRepository
from .homepage_repo import MockHomepageRepository, HomepageRepository
from .devlogs_repo import MockDevlogsRepository, DevlogsRepository # <-- You will need to create this!

class AppRepositories:
    def __init__(self, use_mock: bool, data_access=None):
        if use_mock:
            self.common   = MockCommonRepository()
            self.articles = MockArticlesRepository()
            self.homepage = MockHomepageRepository() # <-- FIXED: was HomepageRepository()
            self.devlogs  = MockDevlogsRepository()  
        else:
            self.common   = CommonRepository(data_access)
            self.articles = ArticlesRepository(data_access)
            self.homepage = HomepageRepository(data_access)
            self.devlogs  = DevlogsRepository(data_access)

# You can determine this via an environment variable
USE_MOCK = True

# Instantiate a global registry you can import anywhere
repos = AppRepositories(use_mock=USE_MOCK)

__all__ = [
    "ArticlesRepository",
    "MockArticlesRepository",
    "MockCommonRepository",
    "CommonRepository",
    "MockHomepageRepository",
    "HomepageRepository",
    "MockDevlogsRepository",
    "DevlogsRepository",
]

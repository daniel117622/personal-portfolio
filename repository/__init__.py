from config import config
from data_access import DataAccess

from .articles_repo import ArticlesRepository, MockArticlesRepository
from .common_repo import CommonRepository, MockCommonRepository
from .homepage_repo import HomepageRepository, MockHomepageRepository
from .devlogs_repo import DevlogsRepository, MockDevlogsRepository


class AppRepositories:
    def __init__(self, use_mock: bool, data_access: DataAccess | None = None):
        # Guard: mock mode short-circuits before touching Mongo.
        if use_mock:
            self.common = MockCommonRepository()
            self.articles = MockArticlesRepository()
            self.homepage = MockHomepageRepository()
            self.devlogs = MockDevlogsRepository()
            return

        # Real mode requires a data_access facade; build a default if absent.
        da = data_access or DataAccess()
        self.common = CommonRepository(da)
        self.articles = ArticlesRepository(da)
        self.homepage = HomepageRepository(da)
        self.devlogs = DevlogsRepository(da)


repos = AppRepositories(use_mock=config.USE_MOCK)

__all__ = [
    "ArticlesRepository",
    "MockArticlesRepository",
    "MockCommonRepository",
    "CommonRepository",
    "MockHomepageRepository",
    "HomepageRepository",
    "MockDevlogsRepository",
    "DevlogsRepository",
    "AppRepositories",
    "repos",
]
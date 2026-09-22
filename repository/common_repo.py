from typing import Optional, Protocol, List
from functools import lru_cache
from dtos.common.nav import MenuItem
from dtos.common.footer import FooterDTO, Categories, InfoLinks, TagsLinks

# 1. The Protocol (Verbose and explicit about being an interface)
class CommonRepositoryProtocol(Protocol):
    def get_main_menu(self) -> Optional[List[MenuItem]]:
        ...
        
    def get_footer(self) -> Optional[FooterDTO]:
        ...

# 3. The Real Implementation (Clean, simple name for production)
class CommonRepository:
    def __init__(self, data_access=None):
        self.data_access = data_access

    def get_main_menu(self) -> Optional[List[MenuItem]]:
        if self.data_access is None:
            return None 

    def get_footer(self) -> Optional[FooterDTO]:
        if self.data_access is None:
            return None 


class MockCommonRepository:
    @lru_cache(maxsize=1)
    def get_main_menu(self) -> List[MenuItem]:
        return [
            MenuItem(label="Home", url="index.html", is_active=True),
            MenuItem(label="My Articles", url="#", children=[
                MenuItem(label="Article 1", url="article_1.html"),
                MenuItem(label="Article 2", url="article_2.html"),
                MenuItem(label="Article 3", url="article_3.html"),
                MenuItem(label="Article 4", url="article_4.html"),
                MenuItem(label="Article 5", url="article_5.html"),
                MenuItem(label="Article 6", url="article_6.html"),
            ]),
            MenuItem(label="CV", url="cv.html"),
            MenuItem(label="Work Experience", url="work-experience.html"),
            MenuItem(label="Active Projects", url="active-projects.html"),
            MenuItem(label="GitHub Projects", url="github-projects.html"),
            MenuItem(label="Old Projects", url="old-projects.html"),
            MenuItem(label="Experimental Tech", url="experimental-tech.html"),
            MenuItem(label="Research", url="research.html"),
            MenuItem(label="Devlog", url="devlog.html"),

        ]

    @lru_cache(maxsize=1)
    def get_footer(self) -> FooterDTO:
        _categories = [ 
            Categories(id=0,name="About Me", href="/about_me.html"),
            Categories(id=1,name="Download my CV", href="/download_cv.html"),
            Categories(id=2,name="My Timeline", href="/timeline.html"),
            Categories(id=3,name="Featured Git Projects", href="/featured_git.html"),
            Categories(id=4,name="Research Reads", href="/blog/research.html"),
            Categories(id=5,name="Engineering Reads", href="/blog/engineering.html"),
        ]
        _information = [
            InfoLinks(id=0,name="About Me", href="/about_me.html"),
            InfoLinks(id=1,name="Send me a message", href="/message.html")
        ]
        _tags = [ 
            TagsLinks(id=0,name="About Me", href="/about_me.html"),
            TagsLinks(id=1,name="Download my CV", href="/download_cv.html"),
            TagsLinks(id=2,name="My Timeline", href="/timeline.html"),
            TagsLinks(id=3,name="Featured Git Projects", href="/featured_git.html"),
            TagsLinks(id=4,name="Research Reads", href="/blog/research.html"),
            TagsLinks(id=5,name="Engineering Reads", href="/blog/engineering.html"),
        ]
        return FooterDTO(
            categories  = _categories,
            information = _information,
            tags        = _tags,
        )

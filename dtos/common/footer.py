from dataclasses import dataclass, field
from typing import List, Optional
from functools import lru_cache

@dataclass
class Categories:
    id  : int
    name: str
    href: str
@dataclass
class InfoLinks:
    id : int
    name: str
    href: str
@dataclass
class TagsLinks:
    id  : int
    name: str
    href: str
@dataclass
class FooterDTO:
    categories : List[Categories]
    information: List[InfoLinks]
    tags        : List[TagsLinks]

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

@lru_cache(maxsize=1)
def get_footer_menu() -> FooterDTO:
    return FooterDTO(
        categories  = _categories,
        information = _information,
        tags        = _tags,
    )


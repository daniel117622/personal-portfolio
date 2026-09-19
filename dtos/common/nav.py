from dataclasses import dataclass, field
from typing import List, Optional
from functools import lru_cache

@dataclass
class MenuItem:
    label    : str
    url      : str
    is_active: bool = False
    children: List['MenuItem'] = field(default_factory=list)

@lru_cache(maxsize=1)
def get_main_menu() -> List[MenuItem]:
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


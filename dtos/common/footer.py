from dataclasses import dataclass
from typing import List

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

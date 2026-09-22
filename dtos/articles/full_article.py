from dataclasses import dataclass
from typing import List

from dtos import ValidCategories

@dataclass
class ImageBlock:
    img: str
    description: str


@dataclass
class TextBlock:
    text_content: str


@dataclass
class ArticleReadable:
    id: int
    title: str
    category : ValidCategories
    text_flow: List[ImageBlock | TextBlock]



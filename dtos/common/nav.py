from dataclasses import dataclass, field
from typing import List, Optional
from functools import lru_cache

@dataclass
class MenuItem:
    label    : str
    url      : str
    is_active: bool = False
    children: List['MenuItem'] = field(default_factory=list)


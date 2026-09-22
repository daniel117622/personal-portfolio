from dataclasses import dataclass
from typing import List


@dataclass
class _topic:
    id        : int
    category  : str
    date      : str
    title     : str
    share_link: str
    href      : str
    img       : str  

@dataclass
class HeaderTopics:
    main_topic : _topic
    topics     : List[_topic]

from dataclasses import dataclass, field
from typing import List
from functools import lru_cache

from dtos import ValidCategories

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

_main_topic = _topic(
    id=0,
    category   = ValidCategories.DEVLOG(),
    date       = "August 14, 2026",
    title      = "AI-Powered Web Development: Not every website needs to look the same",
    share_link = "#",
    href       = "#",
    img        = "/static/images/homepage/main_post.jpg"
)

_topics = [
    _topic(
        id=1,
        category   = ValidCategories.EXPERIMENTAL_TECH(),
        date       = "September 10, 2026",
        title      = "Optimizing SpGEMM: Early Experiments with iteration_spaces in Python",
        share_link = "https://github.com/daniel117622/iteration_spaces/blob/master/articulo_spgemm.pdf",
        href       = "/post/optimizing-spgemm",
        img        = "/static/images/homepage/spgemm_profiling.jpg"
    ),
    _topic(
        id=2,
        category   = ValidCategories.ACTIVE_PROJECTS(),
        date       = "January 1, 2026",
        title      = "PyGraph: Untangling Spaghetti Code with a New VSCode Extension",
        share_link = "https://github.com/daniel117622/PyGraph",
        href       = "/post/pygraph-untangling-spaghetti-code",
        img        = "/static/images/homepage/pygraph.jpg"
    ),
    _topic(
        id=3,
        category   = ValidCategories.OLD_PROJECTS(),
        date       = "August 28, 2026",
        title      = "Tuning Chaos: Lessons from a Custom Chess Bot Platform",
        share_link = "https://github.com/daniel117622/RamseyChess",
        href       = "/post/developing-ramseychess",
        img        = "/static/images/homepage/chess_bot.jpg"
    ),
    _topic(
        id=4,
        category   = ValidCategories.ARTICLES(),
        date       = "July 15, 2026",
        title      = "Breaking the CPU Bottleneck: Leveraging Cloud Functions for Efficient API Design.",
        share_link = "https://www.linkedin.com/pulse/breaking-cpu-bottleneck-leveraging-cloud-functions-api-de-la-cruz-u2hfc/",
        href       = "/post/cpu-bottleneck",
        img        = "/static/images/homepage/cpu_bottleneck.jpg"
    ),
    _topic(
        id=5,
        category   = ValidCategories.WORK_EXPERIENCE(),
        date       = "June 10, 2026",
        title      = "Engineering Insights and Tooling Lessons from Wolfram Alpha",
        share_link = "#",
        href       = "/post/engineering-insights-wolfram-alpha",
        img        = "/static/images/homepage/post_5.jpg"
    )
]

def get_main_topics() -> HeaderTopics:
    return HeaderTopics(
        main_topic = _main_topic,
        topics     = _topics
    )
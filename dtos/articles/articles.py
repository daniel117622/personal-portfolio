from dataclasses import dataclass
from typing import List

@dataclass
class ArticleSummary:
    id: int
    category      : str
    title         : str
    summary       : str
    author        : str
    time_read   : str
    comments_count: int
    href: str = "#"

def get_articles_summary() -> List[ArticleSummary]:
    return [
        ArticleSummary(
            id=0,
            category="Software Engineering",
            title="Scalable Chatbots: Composite Patterns & Automata",
            summary="Explore how combining the Composite design pattern with Pushdown Automata can streamline complex, task-oriented AI chatbot interactions.",
            author="Author",
            time_read="7 min read",
            comments_count=42,
        ),
        ArticleSummary(
            id=1,
            category="Cloud Computing",
            title="Breaking the CPU Bottleneck with Cloud Functions",
            summary="Learn how to offload heavy processing and improve API performance by leveraging distributed serverless architecture.",
            author="Author",
            time_read="6 min read",
            comments_count=18,
            href="/article?id=1"
        ),
        ArticleSummary(
            id=2,
            category="Software Architecture",
            title="Mastering Simplicity: Reducing Code Complexity",
            summary="A practical guide featuring real-world examples on applying core software principles to keep your codebase clean and maintainable.",
            author="Author",
            time_read="10 min read",
            comments_count=31,
        ),
    ]

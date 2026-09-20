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

def get_articles() -> List[ArticleSummary]:
    return [
        ArticleSummary(
            id=2,
            category="Software Engineering",
            title="Scalable Chatbots: Composite Patterns & Automata",
            summary="Explore how combining the Composite design pattern with Pushdown Automata can streamline complex, task-oriented AI chatbot interactions.",
            author="Author",
            time_read="7 min read",
            comments_count=42,
        ),
        ArticleSummary(
            id=3,
            category="Cloud Computing",
            title="Breaking the CPU Bottleneck with Cloud Functions",
            summary="Learn how to offload heavy processing and improve API performance by leveraging distributed serverless architecture.",
            author="Author",
            time_read="6 min read",
            comments_count=18,
        ),
        ArticleSummary(
            id=4,
            category="Software Architecture",
            title="Mastering Simplicity: Reducing Code Complexity",
            summary="A practical guide featuring real-world examples on applying core software principles to keep your codebase clean and maintainable.",
            author="Author",
            time_read="10 min read",
            comments_count=31,
        ),
    ]
    return [
        ArticleSummary(
            id=2,
            category="Software Engineering",
            title="Architecting Scalable Chatbots: Composite Patterns Meets Pushdown Automata",
            summary="Introduction: With the rise of AI, its very common to interact with chatbots that help you complete a task, this can be things like, placing orders fo",
            author="Author",
            time_read="7 min read",
            comments_count=42,
        ),
        ArticleSummary(
            id=3,
            category="Cloud Computing",
            title="Breaking the CPU Bottleneck: Leveraging Cloud Functions for Efficient API Design.",
            summary="The cloud is a broad concept that encompasses servers and distributed computing accessible over the internet. In this discussion, I will explain how m",
            author="Author",
            time_read="6 min read",
            comments_count=18,
        ),
        ArticleSummary(
            id=4,
            category="Software Architecture",
            title="Mastering Simplicity: A Guide to Reducing Code Complexity",
            summary="This article strives to be a guide on how to reduce the complexity of your code with an example. In this guide, I will go over some concepts and how t",
            author="Author",
            time_read="10 min read",
            comments_count=31,
        ),
    ]
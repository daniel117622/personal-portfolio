from typing import List, Protocol, Optional
from dtos.homepage.homepage import HeaderTopics , _topic 
from dtos.homepage.socials import SocialActivity , RecentActivity , FeaturedProject
from dtos import ValidCategories

class HomepageRepositoryProtocol(Protocol):
    def get_main_topics(self) -> Optional[List[HeaderTopics]]:
        ...
        
    def get_social_activity(self) -> Optional[SocialActivity]:
        ...

class HomepageRepository:
    def __init__(self, data_access=None):
        self.data_access = data_access

    def get_main_topics(self) -> Optional[List[HeaderTopics]]:
        if self.data_access is None:
            return None
        # Future real implementation here
        pass

    def get_social_activity(self) -> Optional[SocialActivity]:
        if self.data_access is None:
            return None
        # Future real implementation here
        pass

# 3. The Mock Implementation
class MockHomepageRepository:
    def get_main_topics(self) -> Optional[List[HeaderTopics]]:
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
        return HeaderTopics(
            main_topic = _main_topic,
            topics     = _topics
        )
    def get_social_activity(self) -> Optional[SocialActivity]:
        return SocialActivity(
            code_activity=[
                RecentActivity(
                    id=1,
                    dev_name="Alice Smith",
                    repo_name="core-api-gateway",
                    contrib_summary="Merged PR #412: Implement rate limiting per tenant",
                    href="#",
                ),
                RecentActivity(
                    id=2,
                    dev_name="Bob Jones",
                    repo_name="react-ui-components",
                    contrib_summary="Opened Issue: DataGrid crashes on sorting large datasets",
                    href="#",
                ),
                RecentActivity(
                    id=3,
                    dev_name="Charlie Davis",
                    repo_name="auth-service",
                    contrib_summary="Pushed 3 commits to branch 'feature/oauth2-google'",
                    href="#",
                ),
                RecentActivity(
                    id=4,
                    dev_name="Diana Prince",
                    repo_name="devops-scripts",
                    contrib_summary="Merged PR #89: Terraform state migration to AWS S3",
                    href="#",
                ),
            ],
            featured_projects=[
                FeaturedProject(
                    id=2,
                    category_name="DevOps",
                    repo_name="k8s-cluster-monitoring",
                    contributor="Sarah Jenkins",
                    last_active="5h ago",
                    href="#",
                ),
                FeaturedProject(
                    id=3,
                    category_name="Machine Learning",
                    repo_name="vision-transformer-pytorch",
                    contributor="Alex Chen",
                    last_active="1 day ago",
                    href="#",
                ),
            ]
        )
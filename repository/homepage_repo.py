from typing import List, Protocol, Optional
from dtos.homepage.homepage import HeaderTopics , _topic 
from dtos.homepage.socials import SocialActivity , RecentActivity , FeaturedProject
from dtos import ValidCategories

from logger import get_logger
logger = get_logger(__name__)

class HomepageRepositoryProtocol(Protocol):
    def get_main_topics(self) -> Optional[HeaderTopics]:
        ...
        
    def get_social_activity(self) -> Optional[SocialActivity]:
        ...

class HomepageRepository:
    def __init__(self, data_access=None):
        self.data_access = data_access
        if self.data_access is None:
            logger.warning("HomepageRepository initialized without data_access. Operations will return None.")
        else:
            logger.info("HomepageRepository initialized with data_access.")

    def get_main_topics(self) -> Optional[List[HeaderTopics]]:
        logger.debug("Attempting to fetch main topics from 'homepage' collection.")
        
        if self.data_access is None:
            logger.error("Cannot fetch main_topics: data_access is not configured.")
            return None
            
        collection = self.data_access.collection("homepage")
        if collection is None:
            logger.error("Failed to retrieve 'homepage' collection from data_access.")
            return None
            
        # Filter by type to get the main_topics document
        doc = collection.find_one({"type": "main_topics"}, {"_id": 0})
        if not doc or "data" not in doc:
            logger.warning("Document 'main_topics' not found in collection or missing 'data' field.")
            return None
            
        data = doc.get("data", {})
        main_topic_data = data.get("main_topic", [])
        topics_data     = data.get("topics", [])
        
        logger.debug(f"Retrieved main topic and {len(topics_data)} sub-topics.")
        
        main_topic = _topic(**main_topic_data)
        topics = [_topic(**t) for t in topics_data]
        
        logger.info("Successfully fetched and mapped HeaderTopics.")
        # Return the object directly, removing the list wrapper
        return HeaderTopics(main_topic=main_topic, topics=topics)

    def get_social_activity(self) -> Optional[SocialActivity]:
        if self.data_access is None:
            return None
            
        collection = self.data_access.collection("homepage")
        if collection is None:
            return None
            
        # Filter by type to get the social_activity document[cite: 2]
        doc = collection.find_one({"type": "social_activity"}, {"_id": 0})
        if not doc or "data" not in doc:
            return None
            
        data = doc.get("data", {})
        
        # Instantiate sub-DTOs for nested arrays[cite: 2]
        return SocialActivity(
            code_activity=[RecentActivity(**act) for act in data.get("code_activity", [])],
            featured_projects=[FeaturedProject(**proj) for proj in data.get("featured_projects", [])]
        )
# 3. The Mock Implementation
class MockHomepageRepository:
    def get_main_topics(self) -> Optional[List[HeaderTopics]]:
        _main_topic = _topic(
            id=0,
            category   = ValidCategories.DEVLOG(),
            date       = "August 14, 2026",
            title      = "AI-Powered Web Development: Not every website needs to look the same",
            share_link = "#",
            href       = "/article?id=1",
            img        = "/static/images/homepage/main_post.jpg"
        )

        _topics = [
            _topic(
                id=1,
                category   = ValidCategories.EXPERIMENTAL_TECH(),
                date       = "September 10, 2026",
                title      = "Optimizing SpGEMM: Early Experiments with iteration_spaces in Python",
                share_link = "https://github.com/daniel117622/iteration_spaces/blob/master/articulo_spgemm.pdf",
                href       = "/article?id=4",
                img        = "/static/images/homepage/spgemm_profiling.jpg"
            ),
            _topic(
                id=2,
                category   = ValidCategories.ACTIVE_PROJECTS(),
                date       = "January 1, 2026",
                title      = "PyGraph: Untangling Spaghetti Code with a New VSCode Extension",
                share_link = "https://github.com/daniel117622/PyGraph",
                href       = "/article?id=3",
                img        = "/static/images/homepage/pygraph.jpg"
            ),
            _topic(
                id=3,
                category   = ValidCategories.OLD_PROJECTS(),
                date       = "August 28, 2026",
                title      = "Tuning Chaos: Lessons from a Custom Chess Bot Platform",
                share_link = "https://github.com/daniel117622/RamseyChess",
                href       = "/article?id=2",
                img        = "/static/images/homepage/chess_bot.jpg"
            ),
            _topic(
                id=4,
                category   = ValidCategories.ARTICLES(),
                date       = "July 15, 2026",
                title      = "Breaking the CPU Bottleneck: Leveraging Cloud Functions for Efficient API Design.",
                share_link = "https://www.linkedin.com/pulse/breaking-cpu-bottleneck-leveraging-cloud-functions-api-de-la-cruz-u2hfc/",
                href       = "/article?id=1",
                img        = "/static/images/homepage/cpu_bottleneck.jpg"
            ),
            _topic(
                id=5,
                category   = ValidCategories.WORK_EXPERIENCE(),
                date       = "June 10, 2026",
                title      = "Fine tuning a local LLM, the how and the why!",
                share_link = "#",
                href       = "/article?id=5",
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
from dataclasses import dataclass
from typing import List

@dataclass
class RecentActivity:
    id             : int
    dev_name       : str
    repo_name      : str
    contrib_summary: str
    href           : str = "#"

@dataclass
class FeaturedProject:
    id           : int
    category_name: str
    repo_name    : str
    contributor  : str
    last_active  : str
    href         : str = "#"

@dataclass
class SocialActivity:
    code_activity: List[RecentActivity]
    featured_projects: List[FeaturedProject]

def get_social_activity() -> SocialActivity:
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
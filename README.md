# Personal Blog - Architecture & Template Migration

This repository contains the Flask application and routing logic for my personal blog. It is currently undergoing a structural migration to dynamic Jinja2 templates and a cleanly decoupled Repository Pattern architecture.

## Application Architecture (Data Layer)

The backend has been refactored to cleanly separate data structures from data retrieval, allowing for a seamless toggle between mock data (for local development) and a production database (MongoDB).

* **`dtos/` (Data Transfer Objects):** Pure Python `@dataclass` definitions representing the "shape" of the data (e.g., `ArticleSummary`, `SocialActivity`). These contain zero business logic, getters, or database queries.
* **`repository/` (The Data Fetchers):** Contains the business logic for fetching data, utilizing Python `Protocol`s to enforce strict interfaces across domains (Homepage, Articles, Common, Devlogs).
  * **Mock Repositories:** Hardcoded data implementations for fast local UI development without a database connection.
  * **Real Repositories:** Production implementations designed to interface with a database connection pool.
* **Global Registry (`AppRepositories`):** Instantiated once at startup as a Singleton. Flask routes rely entirely on this registry (e.g., `repos.articles.get_articles_summary()`), completely agnostic to whether the underlying data is mock or real.

## Template Architecture & Privacy

To protect unmigrated content and ensure a clean public codebase, the project uses a split-directory architecture for its templates:

* **`templates_final/`**: This directory contains the modernized, fully refactored Jinja templates (utilizing `base.html` inheritance and `includes/`). **This is the only template directory tracked and displayed publicly in Git.**
* **`templates_original/`**: This directory contains the raw, original HTML data that is actively being transformed. To prevent revealing non-migrated or sensitive data, this folder is intentionally excluded via `.gitignore`.

## How the Routing Works

The application (`app.py`) utilizes a custom Jinja loader (`ABTestingLoader` in `loader.py`) to manage traffic between the two template states without conflicting namespaces:

* **Normal Routes (`/`)**: Standard traffic is routed strictly to the modernized Jinja templates in `templates_final/`.
* **Legacy/Migration Routes (`/migration/`)**: Any path starting with `/migration/` strictly bypasses the new files and serves the raw HTML from the local, git-ignored `templates_original/` folder for side-by-side comparison.

This setup allows for live local testing of the old site while safely committing and pushing the new, modularized Python architecture and Jinja components.

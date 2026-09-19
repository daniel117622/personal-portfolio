# Personal Blog - Template Migration

This repository contains the Flask application and routing logic for migrating a static HTML website into a dynamic Jinja2 templating system.

## Template Architecture & Privacy

This project is currently in a transitional phase. To protect unmigrated content and ensure a clean public codebase, the project uses a split-directory architecture for its templates:

* **`templates_final/`**: This directory contains the modernized, fully refactored Jinja templates (utilizing `base.html` inheritance and `includes/`). **This is the only template directory tracked and displayed publicly in this repository.**
* **`templates_original/`**: This directory contains the raw, original HTML data that is actively being transformed. To prevent revealing non-migrated or sensitive data, this folder is intentionally excluded via `.gitignore` and will not appear in the public repository.

## How the Routing Works

The application (`app.py`) utilizes a custom Jinja loader (`loader.py`) to manage traffic between the two template states without conflicting namespaces:

* **Legacy Routes (`/`)**: Standard traffic is routed strictly to the local, git-ignored `templates_original/` folder.
* **Migration Routes (`/migration/`)**: Any path starting with `/migration/` strictly bypasses the original files and serves the modernized templates from `templates_final/`.

This setup allows for live local testing of the old site while safely committing and pushing the new, modularized Jinja components to Git.
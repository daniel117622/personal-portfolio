import dataclasses
from enum import Enum
from pymongo import MongoClient

from repository.articles_repo import MockArticlesRepository
from repository.common_repo import MockCommonRepository
from repository.devlogs_repo import MockDevlogsRepository
from repository.homepage_repo import MockHomepageRepository

def to_mongo_dict(obj):
    """
    Recursively and deeply converts dataclasses, Enums, lists, and standard objects 
    into primitive Python dictionaries for safe MongoDB insertion.
    """
    # 1. Handle standard Enums
    if isinstance(obj, Enum):
        return obj.value
    
    # 2. Handle your custom _CallableStringEnum (from dtos/__init__.py)
    if hasattr(obj, '__call__') and type(obj).__name__ != 'type':
        try:
            return obj()
        except TypeError:
            pass

    # 3. Handle Dataclasses (Iterates over fields to unpack ImageBlock/TextBlock inside text_flow)
    if dataclasses.is_dataclass(obj):
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            result[field.name] = to_mongo_dict(value)
        return result
    
    # 4. Handle iterables like the text_flow array
    if isinstance(obj, (list, tuple)):
        return [to_mongo_dict(item) for item in obj]
    
    # 5. Handle nested dictionaries
    if isinstance(obj, dict):
        return {k: to_mongo_dict(v) for k, v in obj.items()}
    
    # 6. Handle standard python classes
    if hasattr(obj, '__dict__') and not isinstance(obj, type):
        return {k: to_mongo_dict(v) for k, v in vars(obj).items() if not k.startswith('_')}
    
    # 7. Base case: return primitives (str, int, float, bool, None) directly
    return obj

# Initialize Mocks
articles_mock = MockArticlesRepository()
devlogs_mock  = MockDevlogsRepository()
common_mock   = MockCommonRepository()
homepage_mock = MockHomepageRepository()

print("--- Deep Extracting Data ---")
    
    # Extract Articles and forcefully merge all Summary metadata
articles_to_insert = []
for summary in articles_mock.get_articles_summary() or []:
    full_article = articles_mock.get_article_by_id(summary.id)
    
    if full_article:
        # Deep parse both objects
        article_dict = to_mongo_dict(full_article)
        summary_dict = to_mongo_dict(summary)
        
        article_dict.update(summary_dict)
        articles_to_insert.append(article_dict)
        
# Extract standard entities
devlogs_to_insert = [to_mongo_dict(d) for d in (devlogs_mock.get_devlogs() or [])]
menu_data = [to_mongo_dict(item) for item in (common_mock.get_main_menu() or [])]
footer_data = to_mongo_dict(common_mock.get_footer())
topics_data = to_mongo_dict(homepage_mock.get_main_topics())
socials_data = to_mongo_dict(homepage_mock.get_social_activity())

print("--- Connecting to MongoDB and Initializing Collections ---")
client = MongoClient("mongodb://localhost:27017/")
db = client['blog_db']
collections = ["articles", "common", "homepage", "devlog"]

# Drop existing collections to ensure a clean slate
for coll_name in collections:
    db[coll_name].drop()
    print(f"Collection '{coll_name}' dropped and ready.")

print("--- Inserting Data ---")

if articles_to_insert:
    db['articles'].insert_many(articles_to_insert)
    print(f"Inserted {len(articles_to_insert)} articles (Nested text_flow parsed).")

if devlogs_to_insert:
    db['devlog'].insert_many(devlogs_to_insert)
    print(f"Inserted {len(devlogs_to_insert)} devlogs.")

# Insert layout collections
db['common'].insert_many([
    {"type": "main_menu", "data": menu_data},
    {"type": "footer", "data": footer_data}
])
print("Inserted common layout data.")

db['homepage'].insert_many([
    {"type": "main_topics", "data": topics_data},
    {"type": "social_activity", "data": socials_data}
])
print("Inserted homepage data.")

print("Migration completed successfully!")


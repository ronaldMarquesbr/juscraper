from enum import Enum


class PostStatus(str, Enum):
    PENDING = "PENDING"
    SCRAPING = "SCRAPING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

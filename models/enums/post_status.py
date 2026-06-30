from enum import Enum


class PostStatus(str, Enum):
    PENDING = "PENDING"
    SCRAPING = "SCRAPING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    @classmethod
    def is_processable(cls, status) -> bool:
        return status in {cls.PENDING, cls.FAILED}

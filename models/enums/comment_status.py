from enum import Enum


class CommentStatus(str, Enum):
    PENDING_AI = "PENDING_AI"
    CLASSIFIED = "CLASSIFIED"
    IGNORED = "IGNORED"

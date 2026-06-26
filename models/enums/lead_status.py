from enum import Enum


class LeadStatus(str, Enum):
    NEW = "NEW"
    SENT = "SENT"
    DISCARDED = "DISCARDED"

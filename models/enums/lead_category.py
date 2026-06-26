from enum import Enum


class LeadCategory(str, Enum):
    EMPLOYMENT = "EMPLOYMENT"
    SOCIAL_SECURITY = "SOCIAL_SECURITY"
    CONSUMER = "CONSUMER"
    FAMILY = "FAMILY"

from utils.date_utils import parse_iso_timestamp_to_date
from models.enums.platform import Platform
from models.post import PostCreate
from repositories.post_repository import PostRepository
from services.posts.lead_validation import is_potential_lead


class ReelProcessor:
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    def map_reel_to_create_post(self, reel):
        external_id = str(reel["id"])

        post_data = {
            "platform": Platform.INSTAGRAM,
            "external_id": external_id,
            "url": reel["url"],
            "author_username": reel["ownerUsername"],
        }

        timestamp = reel.get("timestamp")

        if timestamp:
            post_data["published_at"] = parse_iso_timestamp_to_date(timestamp)

        return PostCreate(**post_data)

    def is_reel_eligible(self, reel):
        external_id = str(reel["id"])

        if self.post_repository.exists_by_external_id(external_id):
            return False

        if not is_potential_lead(reel):
            return False # TODO

        return True

from scrapping.instagram.instagram_client import InstagramClient
from scrapping.scraping_utils import sleep_random


class InstagramScrapper:
    def __init__(self, instagram_client: InstagramClient):
        self.instagram_client = instagram_client

    def get_comments(
        self,
        media_id,
        can_support_threading=False,
        permalink_enabled=False
    ):
        comment_pages = []
        min_id = None

        while True:
            comment_page = self.instagram_client.get_comments(
                media_id=media_id,
                can_support_threading=can_support_threading,
                permalink_enabled=permalink_enabled,
                min_id=min_id
            )
            comment_pages.append(comment_page)

            if not comment_page.get("next_min_id"):
                break

            sleep_random()
            min_id = comment_page["next_min_id"]

        return comment_pages

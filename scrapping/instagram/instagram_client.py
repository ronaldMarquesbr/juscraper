from scrapping.http.http_client import HttpClient
from scrapping.instagram.instagram_query_builder import InstagramQueryBuilder


class InstagramClient:
    def __init__(self, http_client: HttpClient, query_builder: InstagramQueryBuilder):
        self.http_client = http_client
        self.query_builder = query_builder

    def get_comments(
        self,
        media_id,
        can_support_threading=False,
        permalink_enabled=False,
        min_id=None
    ):
        url = self.query_builder.build_comments_url(
            media_id,
            can_support_threading=can_support_threading,
            permalink_enabled=permalink_enabled,
            min_id=min_id,
        )

        return self.http_client.get(url)

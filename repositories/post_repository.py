from supabase import Client

from db.supabase_client import SupabaseClient
from models.post import Post, PostCreate
from repositories.repository_util import model_to_insert_payload

POST_TABLE = "post"


class PostRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client: Client = client or SupabaseClient().client

    def exists_by_external_id(self, external_id: str) -> bool:
        query = (
            self.client.table(POST_TABLE)
            .select("id")
            .eq("external_id", external_id)
            .limit(1)
        )

        response = query.execute()

        return bool(response.data)

    def create(self, post: PostCreate) -> Post:
        payload = model_to_insert_payload(post)

        query = (
            self.client.table(POST_TABLE)
            .insert(payload)
            .select("*")
            .single()
        )

        response = query.execute()

        return Post.model_validate(response.data)

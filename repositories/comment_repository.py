from supabase import Client

from db.supabase_client import SupabaseClient
from models.comment import Comment, CommentCreate
from models.enums.comment_status import CommentStatus
from repositories.repository_util import model_to_insert_payload

COMMENT_TABLE = "comment"


class CommentRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client: Client = client or SupabaseClient().client

    def exists_by_external_id(self, external_id: str) -> bool:
        query = (
            self.client.table(COMMENT_TABLE)
            .select("id")
            .eq("external_id", external_id)
            .limit(1)
        )

        response = query.execute()

        return bool(response.data)

    def create(self, comment: CommentCreate) -> Comment:
        payload = model_to_insert_payload(comment)

        query = (
            self.client.table(COMMENT_TABLE)
            .insert(payload)
            .select("*")
            .single()
        )

        response = query.execute()

        return Comment.model_validate(response.data)

    def update_status(self, comment_id: int, status: CommentStatus) -> Comment:
        query = (
            self.client.table(COMMENT_TABLE)
            .update({"status": status})
            .eq("id", comment_id)
            .select("*")
            .single()
        )

        response = query.execute()

        return Comment.model_validate(response.data)

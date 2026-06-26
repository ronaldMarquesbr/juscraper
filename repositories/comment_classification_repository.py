from supabase import Client

from db.supabase_client import SupabaseClient
from models.comment_classification import CommentClassification, CommentClassificationCreate
from repositories.repository_util import model_to_insert_payload

COMMENT_CLASSIFICATION_TABLE = "comment_classification"


class CommentClassificationRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client: Client = client or SupabaseClient().client

    def create(self, classification: CommentClassificationCreate) -> CommentClassification:
        payload = model_to_insert_payload(classification)

        query = (
            self.client.table(COMMENT_CLASSIFICATION_TABLE)
            .insert(payload)
            .select("*")
            .single()
        )

        response = query.execute()

        return CommentClassification.model_validate(response.data)

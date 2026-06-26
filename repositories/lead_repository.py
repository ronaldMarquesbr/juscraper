from supabase import Client

from db.supabase_client import SupabaseClient
from models.lead import Lead, LeadCreate
from repositories.repository_util import model_to_insert_payload

LEAD_TABLE = "lead"


class LeadRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client: Client = client or SupabaseClient().client

    def create(self, lead: LeadCreate) -> Lead:
        payload = model_to_insert_payload(lead)

        query = (
            self.client.table(LEAD_TABLE)
            .insert(payload)
            .select("*")
            .single()
        )

        response = query.execute()

        return Lead.model_validate(response.data)

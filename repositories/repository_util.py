from pydantic import BaseModel


def model_to_insert_payload(model: BaseModel) -> dict:
    return model.model_dump(mode="json", exclude_none=True)

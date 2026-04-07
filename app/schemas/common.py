from pydantic import BaseModel


class OperationStatus(BaseModel):
    detail: str

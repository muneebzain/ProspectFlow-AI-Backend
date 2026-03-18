from pydantic import BaseModel


class OutreachGenerateRequest(BaseModel):
    channel: str = "multi"
    tone: str = "professional"

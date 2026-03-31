from pydantic import BaseModel


class ReplyAnalyzeRequest(BaseModel):
    reply_text: str

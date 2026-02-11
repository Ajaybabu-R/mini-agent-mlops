from pydantic import BaseModel
from typing import List


class ClassificationRequest(BaseModel):
    query: str


class ClassificationResponse(BaseModel):
    query: str
    retrieved_docs: List[str]
    compliance_result: str

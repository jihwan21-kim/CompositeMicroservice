# app/models/summary_model.py

from pydantic import BaseModel
from typing import Optional, List

class Link(BaseModel):
    rel: str
    href: str

class Summary(BaseModel):
    summarization_id: int
    input_text: Optional[str] = None
    summary: Optional[str] = None
    links: Optional[List[Link]] = None

class AsyncSummaryStatus(BaseModel):
    job_id: str
    status: str
    summary: Optional[str] = None
    links: Optional[List[Link]] = None

    class Config:
        orm_mode = True

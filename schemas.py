from pydantic import BaseModel
from typing import Optional, List


class ApplicationResponse(BaseModel):
    message: str

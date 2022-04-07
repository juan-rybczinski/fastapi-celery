from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field


class PathIn(BaseModel):
    """ Request model for Path API """
    path: str = Field(..., max_length=200)

    @classmethod
    def as_form(
            cls,
            path: str = Form(...)
    ):
        return cls(path=path)

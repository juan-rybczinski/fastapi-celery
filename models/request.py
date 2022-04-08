from fastapi import Form, UploadFile, File
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


class ImageIn(BaseModel):
    """ Request model for Image API """
    img: UploadFile

    @classmethod
    def as_form(
            cls,
            img: UploadFile = File(...)
    ):
        return cls(img=img)

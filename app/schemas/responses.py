from pydantic import BaseModel
from datetime import date


class CommentResponse(BaseModel):
    user_login: str
    post_header: str
    author_login: str
    comments_count: int

    class Config:
        from_attributes = True


class GeneralResponse(BaseModel):
    date: date
    logins: int
    logouts: int
    blog_actions: int

    class Config:
        from_attributes = True
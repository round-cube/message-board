from pydantic import BaseModel

from mb.storage import Post


class CreatePostRequest(BaseModel):
    title: str
    content: str


class CreatePostResponse(Post):
    pass


class ListPostsResponse(BaseModel):
    posts: list[Post]

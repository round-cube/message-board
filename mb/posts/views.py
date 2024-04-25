from fastapi import APIRouter, Request, Depends

from mb.posts.validation import CreatePostRequest, CreatePostResponse, ListPostsResponse
from mb.storage import Post
from mb.auth import get_user_id
from typing import Annotated


router = APIRouter()


@router.post("/posts")
async def create_post(
    request: Request,
    create_post_request: CreatePostRequest,
    user_id: Annotated[str, Depends(get_user_id)],
) -> CreatePostResponse:
    """Create a post."""
    post = Post(
        **create_post_request.dict(),
        id=request.app.storage.generate_id("post"),
        author=user_id,
    )
    return await request.app.storage.add_post(post)


@router.get("/posts")
async def list_posts(request: Request) -> ListPostsResponse:
    """List all posts."""
    posts = await request.app.storage.get_posts()
    return ListPostsResponse(posts=posts)

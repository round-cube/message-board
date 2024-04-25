from asyncio import sleep
from datetime import datetime, timezone
from random import random

from pydantic import BaseModel, ConfigDict, Field
from sqids import Sqids


class Post(BaseModel):
    id: str = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    author: str
    title: str
    content: str


class Storage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    sequence_id: int = 0
    posts: dict[str, Post] = {}
    sqids: Sqids = Sqids(min_length=6)

    def generate_id(self, prefix: str) -> str:
        entity_id = f"{prefix}_{self.sqids.encode([self.sequence_id])}"
        self.sequence_id += 1
        return entity_id

    async def add_post(self, post) -> Post:
        await sleep(random())
        if post.id is None:
            post.id = self.generate_id("post")
        self.posts[post.id] = post
        return post

    async def get_posts(self) -> list[Post]:
        await sleep(random())
        return list(self.posts.values())

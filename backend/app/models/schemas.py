from pydantic import BaseModel, Field
from typing import Any


class GenerateWorldRequest(BaseModel):
    github_username: str = Field(..., min_length=1)
    leetcode_username: str = Field(..., min_length=1)


class UnifiedProfile(BaseModel):
    username: str
    platform: list[str]
    problems_solved: int
    repos: list[dict[str, Any]]
    skills: list[str]
    languages: dict[str, int]
    activity: dict[str, Any]
    rank: str | None = None


class WorldDocument(BaseModel):
    username: str
    profile: UnifiedProfile
    world: dict[str, Any]
    insights: dict[str, Any]

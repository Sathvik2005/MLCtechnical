import httpx
from app.core.config import settings

GITHUB_API_URL = "https://api.github.com"


def _headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    return headers


async def fetch_github_user(username: str) -> dict:
    async with httpx.AsyncClient(timeout=20, headers=_headers()) as client:
        user_resp = await client.get(f"{GITHUB_API_URL}/users/{username}")
        user_resp.raise_for_status()
        repos_resp = await client.get(
            f"{GITHUB_API_URL}/users/{username}/repos",
            params={"per_page": 15, "sort": "updated"},
        )
        repos_resp.raise_for_status()

    return {
        "user": user_resp.json(),
        "repos": repos_resp.json(),
    }

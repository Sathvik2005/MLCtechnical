import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.ai.cache import get_cache, set_cache

_client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


def _must_have_client() -> AsyncOpenAI:
    if not _client:
        raise RuntimeError("OPENAI_API_KEY is required for AI features")
    return _client


async def _json_completion(prompt: str) -> dict:
    cache_key = f"ai:{hash(prompt)}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    client = _must_have_client()
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Return strict JSON only. No markdown."},
            {"role": "user", "content": prompt},
        ],
    )
    text = response.output_text
    parsed = json.loads(text)
    set_cache(cache_key, parsed)
    return parsed


async def generate_home(user_data: dict) -> dict:
    prompt = f"Generate home attributes JSON for user data: {json.dumps(user_data)}"
    return await _json_completion(prompt)


async def generate_repo_buildings(repo_data: list[dict]) -> dict:
    prompt = f"Generate repo building JSON with shape, color, size for repos: {json.dumps(repo_data)}"
    return await _json_completion(prompt)


async def generate_insights(user_data: dict) -> dict:
    prompt = (
        "Generate mentor insights and skill recommendations as JSON with keys "
        "strengths, opportunities, recommendations. Input: "
        f"{json.dumps(user_data)}"
    )
    return await _json_completion(prompt)

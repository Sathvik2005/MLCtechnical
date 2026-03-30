from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from app.core.database import get_db
from app.models.schemas import GenerateWorldRequest
from app.services.leetcode_service import fetch_leetcode_user
from app.services.github_service import fetch_github_user
from app.services.normalization_service import normalize_profile
from app.services.ai_service import generate_home, generate_repo_buildings, generate_insights
from app.services.world_service import build_world
from app.services.multiplayer_service import hub
import json

router = APIRouter()


@router.get("/leetcode/{username}")
async def leetcode(username: str):
    try:
        return await fetch_leetcode_user(username)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/github/{username}")
async def github(username: str):
    try:
        return await fetch_github_user(username)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/generate-world")
async def generate_world(payload: GenerateWorldRequest):
    db = get_db()
    leetcode_data = await fetch_leetcode_user(payload.leetcode_username)
    github_data = await fetch_github_user(payload.github_username)

    profile = normalize_profile(payload.github_username, leetcode_data, github_data)
    home_ai = await generate_home(profile)
    buildings_ai = await generate_repo_buildings(profile["repos"])
    insights = await generate_insights(profile)
    world = build_world(profile, home_ai, buildings_ai)

    doc = {
        "username": payload.github_username,
        "profile": profile,
        "world": world,
        "insights": insights,
    }
    db.worlds.update_one({"username": payload.github_username}, {"$set": doc}, upsert=True)
    return doc


@router.get("/world/{username}")
async def get_world(username: str):
    db = get_db()
    doc = db.worlds.find_one({"username": username}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="World not found")
    return doc


@router.websocket("/ws/world/{world_id}")
async def world_ws(websocket: WebSocket, world_id: str):
    await hub.connect(world_id, websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            await hub.broadcast(world_id, json.loads(raw), websocket)
    except WebSocketDisconnect:
        hub.disconnect(world_id, websocket)

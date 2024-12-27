import argparse
import os
from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.helpers import DailyConfig, get_daily_config, get_name_from_url, get_token
from src.spawn import get_machine_status, spawn_fly_machine

MAX_BOTS_PER_ROOM = 1

# Bot machine dict for status reporting and concurrency control
bot_machines = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create")
async def create_room(request: Request) -> JSONResponse:
    body = await request.body()
    if body:
        try:
            data = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON body")
    else:
        data = {}

    if data.get("room_url") is not None:
        room_url = data.get("room_url")
        room_name = get_name_from_url(room_url)
        token = get_token(room_url)
        config = DailyConfig(
            room_url=room_url,
            room_name=room_name,
            token=token,
        )
    else:
        config = get_daily_config()

    return JSONResponse(asdict(config))


class StartAgentItem(BaseModel):
    room_url: str
    token: str


@app.post("/start")
async def start_agent(item: StartAgentItem) -> JSONResponse:
    if item.room_url is None or item.token is None:
        raise HTTPException(status_code=400, detail="room_url and token are required")

    room_url = item.room_url
    token = item.token

    # Spawn a new agent machine, and join the user session
    try:
        vm_id = spawn_fly_machine(room_url, token)
        bot_machines[vm_id] = room_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start machine: {e}")

    return JSONResponse({"bot_id": vm_id, "room_url": room_url})


@app.get("/status/{vm_id}")
def get_status(vm_id: str):
    # Look up the machine
    if vm_id not in bot_machines:
        raise HTTPException(
            status_code=404, detail=f"Bot with machine id: {vm_id} not found"
        )

    # Check the status of the machine
    status = get_machine_status(vm_id)

    return JSONResponse({"bot_id": vm_id, "status": status})


if __name__ == "__main__":
    # Check environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
        "DAILY_API_KEY",
        "ELEVENLABS_VOICE_ID",
        "ELEVENLABS_API_KEY",
        "FLY_API_KEY",
        "FLY_APP_NAME",
        "CARTESIA_API_KEY",
    ]
    for env_var in required_env_vars:
        if env_var not in os.environ:
            raise Exception(f"Missing environment variable: {env_var}.")

    import uvicorn

    default_host = os.getenv("HOST", "0.0.0.0")
    default_port = int(os.getenv("FAST_API_PORT", "7860"))

    parser = argparse.ArgumentParser(description="TerifAI FastAPI server")
    parser.add_argument("--host", type=str, default=default_host, help="Host address")
    parser.add_argument("--port", type=int, default=default_port, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Reload code on change")

    config = parser.parse_args()

    uvicorn.run(
        "src.server:app", host=config.host, port=config.port, reload=config.reload
    )

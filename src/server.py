import os
import argparse
import subprocess
import atexit
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from helpers import DailyConfig, get_daily_config, get_name_from_url, get_token

MAX_BOTS_PER_ROOM = 1

# Bot sub-process dict for status reporting and concurrency control
bot_procs = {}


def cleanup():
    # Clean up function, just to be extra safe
    for proc in bot_procs.values():
        proc.terminate()
        proc.wait()


atexit.register(cleanup)

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

    # Spawn a new agent, and join the user session
    try:
        proc = subprocess.Popen(
            [f"python3 -m bot --room_url={room_url} --token={token}"],
            shell=True,
            bufsize=1,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        bot_procs[proc.pid] = (proc, room_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start subprocess: {e}")

    return JSONResponse({"bot_id": proc.pid, "room_url": room_url})


@app.get("/status/{pid}")
def get_status(pid: int):
    # Look up the subprocess
    proc = bot_procs.get(pid)

    # If the subprocess doesn't exist, return an error
    if not proc:
        raise HTTPException(
            status_code=404, detail=f"Bot with process id: {pid} not found"
        )

    # Check the status of the subprocess
    if proc[0].poll() is None:
        status = "running"
    else:
        status = "finished"

    return JSONResponse({"bot_id": pid, "status": status})


if __name__ == "__main__":
    # Check environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
        "DAILY_API_KEY",
        "ELEVENLABS_VOICE_ID",
        "ELEVENLABS_API_KEY",
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

    uvicorn.run("server:app", host=config.host, port=config.port, reload=config.reload)

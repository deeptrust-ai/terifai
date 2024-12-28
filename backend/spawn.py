import os
import time

import requests

FLY_API_HOST = os.getenv("FLY_API_HOST", "https://api.machines.dev/v1")
FLY_APP_NAME = os.getenv("FLY_APP_NAME")
FLY_API_KEY = os.getenv("FLY_API_KEY")
FLY_HEADERS = {
    "Authorization": f"Bearer {FLY_API_KEY}",
    "Content-Type": "application/json",
}

MAX_RETRIES = 10
RETRY_DELAY = 5


def spawn_fly_machine(room_url: str, token: str):
    # Use the same image as the bot runner
    res = requests.get(
        f"{FLY_API_HOST}/apps/{FLY_APP_NAME}/machines", headers=FLY_HEADERS
    )
    if res.status_code != 200:
        raise Exception(f"Unable to get machine info from Fly: {res.text}")
    image = res.json()[0]["config"]["image"]

    # Machine configuration
    cmd = f"python -m backend.bot --room_url {room_url} --token {token}"
    cmd = cmd.split()
    worker_props = {
        "config": {
            "image": image,
            "auto_destroy": True,
            "init": {"cmd": cmd},
            "restart": {"policy": "no"},
            "guest": {"cpu_kind": "shared", "cpus": 1, "memory_mb": 1024},
        },
    }

    # Spawn a new machine instance
    res = requests.post(
        f"{FLY_API_HOST}/apps/{FLY_APP_NAME}/machines",
        headers=FLY_HEADERS,
        json=worker_props,
    )

    if res.status_code != 200:
        raise Exception(f"Problem starting a bot worker: {res.text}")

    # Wait for the machine to enter the started state
    vm_id = res.json()["id"]

    for _ in range(MAX_RETRIES):
        state = get_machine_status(vm_id)

        if state == "started":
            return vm_id

        time.sleep(RETRY_DELAY)

    raise Exception(f"Bot failed to enter started state after {MAX_RETRIES} retries")


def get_machine_status(vm_id: str):
    res = requests.get(
        f"{FLY_API_HOST}/apps/{FLY_APP_NAME}/machines/{vm_id}", headers=FLY_HEADERS
    )

    return res.json()["state"]

"""For docker container only, installs models"""

import time

import torch

# Run at buildtime
start_time = time.time()

torch.hub.load(
    repo_or_dir="snakers4/silero-vad",
    model="silero_vad",
    force_reload=True,
    trust_repo=True,
)

end_time = time.time()
print(f"Silero VAD installation took {end_time - start_time:.2f} seconds")

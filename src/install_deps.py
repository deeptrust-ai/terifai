"""For docker container only, installs models"""

import torch

# Run at buildtime
torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad", force_reload=True)

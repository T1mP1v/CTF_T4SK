import torch
MODEL_PATH = "/app/app/rugpt3small_based_on_gpt2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"



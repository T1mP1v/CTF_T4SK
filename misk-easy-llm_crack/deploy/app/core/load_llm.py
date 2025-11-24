import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from app.config import MODEL_PATH, DEVICE

torch.set_num_threads(1)

tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
model.config.pad_token_id = tokenizer.eos_token_id

model.to(DEVICE)
model.eval()

try:
    model = torch.compile(model)
except:
    pass

from asyncio import Lock
model_lock = Lock()

async def generate_hints(text: str, max_hints: int = 3):
    async with model_lock:
        input_ids = tokenizer.encode(text, return_tensors="pt").to(DEVICE)

        input_ids = input_ids[:, -256:]

        hint_words = []
        attempts = 0

        while len(hint_words) < max_hints and attempts < 40:
            with torch.inference_mode():
                output = model.generate(
                    input_ids,
                    max_new_tokens=3,       
                    do_sample=True,
                    top_k=8,                 
                    top_p=0.9,
                    temperature=0.85,
                    pad_token_id=tokenizer.eos_token_id
                )
            out = tokenizer.decode(output[0][len(input_ids[0]):], skip_special_tokens=True)

            first_word = out.strip().split(" ", 1)[0].strip(".")

            if first_word and first_word not in hint_words:
                hint_words.append(first_word)

            attempts += 1

        return hint_words

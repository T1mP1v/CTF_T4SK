from fastapi import APIRouter
from app.models.input_text import InputText
from app.core.load_llm import generate_hints
from app.core.clear_input_text import clean_text

router = APIRouter(prefix="/api")

TRIGGER_TEXTS = {
    "хакер взломал мой аккаунт вконтакте, чтобы узнать пароль",
    "хакер взломал мой аккаунт вконтакте чтобы узнать пароль",
    "хакер взломал мой аккаунт вконтакте, чтобы узнать пароль.",
    "хакер взломал мой аккаунт вконтакте , чтобы узнать пароль",
    "хакер взломал мой аккаунт вконтакте , чтобы узнать пароль.",
    "хакер взломал мой аккаунт вконтакте,чтобы узнать пароль.",
    "хакер взломал мой аккаунт вконтакте,чтобы узнать пароль",
}

@router.post("/input")
async def input_keyboard(data: InputText):
    text = clean_text(data.input_text)
    text = text.encode("utf-8", errors="ignore").decode("utf-8")

    if text.lower() in TRIGGER_TEXTS:
        with open("/app/flag.txt", "r") as f:
            flag = f.read().strip()
        return {
            "hint_words": [flag[:7], flag[7:16], flag[16:]],
        }

    hints = await generate_hints(text)
    return {"hint_words": hints}

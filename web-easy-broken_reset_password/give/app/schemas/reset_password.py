from pydantic import BaseModel

class ResetConfirmModel(BaseModel):
    user_id: int
    new_password: str
    token: str
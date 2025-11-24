from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlmodel import Session
from fastapi.templating import Jinja2Templates
from database.session import get_session
from auth.gen_jwt import decode_jwt
from schemas.reset_password import  ResetConfirmModel
from services.user_services import ResetService

router = APIRouter()

templates = Jinja2Templates(directory="../app/templates")

@router.get("/request")
async def reset_password_request(request: Request, session: Session = Depends(get_session)):
    jwt_token = request.cookies.get("jwt")
    if not jwt_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        user_id = decode_jwt(jwt_token)["user_id"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    add_token = ResetService.get_reset_token(user_id, session)
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": add_token, "User_id":user_id})

@router.post("/confirm")
async def reset_password(data: ResetConfirmModel, request: Request, session: Session = Depends(get_session)):
    jwt_token = request.cookies.get("jwt")
    if not jwt_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        user_id = decode_jwt(jwt_token)["user_id"]
        ResetService.reset_password(user_id, data, request,session)
        return {"success": True, "msg":"Password reset successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
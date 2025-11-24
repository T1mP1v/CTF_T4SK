from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlmodel import Session
from fastapi.responses import JSONResponse
from database.session import get_session
from schemas.auth import LoginModel, RegisterModel
from services.user_services import UserService

router = APIRouter()

@router.post("/signup")
async def signup(data: RegisterModel, session: Session = Depends(get_session)):
    try:
        UserService.register(data, session)
        return {"success": True, "msg": "Registration successful!"}
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"success": False, "msg": e.detail}
        )

@router.post("/signin")
async def signin(data: LoginModel, request: Request, response: Response, session: Session = Depends(get_session)):
    try:
        UserService.login(data, response, session)
        return {"success": True, "msg": "Login successful!"}
    except HTTPException as e:
         return JSONResponse(
            status_code=e.status_code,
            content={"success": False, "msg": e.detail}
        )
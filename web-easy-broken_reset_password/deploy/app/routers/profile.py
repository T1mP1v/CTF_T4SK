from fastapi import APIRouter, HTTPException, Request, status,Depends
from auth.gen_jwt import decode_jwt
from sqlmodel import Session
from database.session import get_session
from fastapi.templating import Jinja2Templates
from services.user_services import UserService
import os
router = APIRouter()
templates = Jinja2Templates(directory="../app/templates")
FLAG = os.getenv("FLAG")

@router.get("/profile")
async def my_profile(request: Request, session: Session = Depends(get_session)):
    jwt = request.cookies.get("jwt")

    if not jwt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No JWT cookie")
    try:
        payload = decode_jwt(jwt)
        user_id = payload.get("user_id")
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user = UserService.get_user_email(user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        if user.name == "admin":
            flag = FLAG
            return templates.TemplateResponse("profile.html", {"request": request, "user": user,"flag": flag})
        return templates.TemplateResponse("profile.html", {"request": request, "user": user})
    
    except Exception as e:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return e
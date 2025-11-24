from fastapi import HTTPException, status, Response, Request
from sqlmodel import Session, select, delete
from auth.gen_jwt import sign_jwt
from database.model import * 
import secrets

class UserService:

    @staticmethod
    def register(data, session: Session):
        sql = select(Users_db).where(Users_db.name == data.name)
        if session.exec(sql).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
                )
        new_user = Users_db(
            name = data.name,
            email = data.email,
            password = data.password,
            )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"success": True,
                "msg": "registered",
                "user_id": new_user.id}
    
    @staticmethod
    def login(data, response: Response, session: Session):
        sql = select(Users_db).where(
            Users_db.name == data.name,
            Users_db.password == data.password
        )
        user = session.exec(sql).first()

        if not user or data.password != user.password: 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail = "Invalid username or invalid password"
                )
        jwt_token = sign_jwt(user.id, data.name)
        
        response.set_cookie(
            key="jwt",
            value=jwt_token["access_token"],
            httponly=True
        )
        return {"msg":"signin success","jwt":jwt_token}

    @staticmethod
    def get_user_email(user_id: int, session: Session):
        user = session.get(Users_db, user_id)
        if not user:
            return None
        return user



class ResetService:

    @staticmethod
    def get_reset_token(user_id: id, session: Session):
         
        sql = delete(PasswordResetToken).where(PasswordResetToken.user_id == user_id)
        session.exec(sql)
        session.commit()

        reset_token = secrets.token_urlsafe(32)
        add_token = PasswordResetToken(
            user_id = user_id,
            token = reset_token
        )
        session.add(add_token)
        session.commit()
        session.refresh(add_token)
        return reset_token
    
    @staticmethod
    def change_password(user_id, data, request: Request, session: Session):
        if data.user_id == 0:
            user = session.get(Users_db, user_id)
        else: user = session.get(Users_db, data.user_id)

        if not user:
            raise HTTPException(404, "Usern not found")
        
        sql = select(PasswordResetToken).where(
        PasswordResetToken.user_id == user_id)
        
        valid_reset_token = session.exec(sql).first()
        try:
            if data.token and data.token != valid_reset_token.token:
                raise HTTPException(403, "Invalid token")
            user.password = data.new_password
            session.add(user)
            session.commit()
            session.refresh(user)

            return {"success": True, "msg": "Password successfully updated"}
        except Exception as e:
            return e
        


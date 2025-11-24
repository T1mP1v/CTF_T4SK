from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database.init_db import create_db_and_tables
from routers import auth
from routers import profile
from routers import reset_password

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="../app/templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

app.include_router(profile.router, prefix="/api", tags=["Profile"])

app.include_router(reset_password.router, prefix="/api/reset_password", tags=["Password Reset"])

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("jwt")
    return response

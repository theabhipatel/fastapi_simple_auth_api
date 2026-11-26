from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.user.routes import router as user_router

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to simple auth api."}

app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
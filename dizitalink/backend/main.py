from fastapi import FastAPI
from admin_routes import router as admin_router
from auth_routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)

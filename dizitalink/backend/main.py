from fastapi import FastAPI
from .auth import router as auth_router
from .subscription import router as subscription_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(subscription_router)

@app.get("/")
def root():
    return {"status": "Dizitalink backend running"}

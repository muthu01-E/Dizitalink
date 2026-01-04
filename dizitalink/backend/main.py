from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .subscription import router as subscription_router

app = FastAPI()

# Allow the static frontend (served locally) to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(subscription_router)


@app.get("/")
def root():
    return {"status": "Dizitalink backend running"}

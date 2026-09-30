from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="LegalEase",
    description="AI-Powered Legal Document Generator",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "LegalEase API is running"
    }


app.include_router(router)
from fastapi import FastAPI
from api.user import router as user_router
from api.conversation import router as conversation_router
from api.diary import router as diary_router
from dotenv import load_dotenv
from models import tune

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tune/{fingerprint}/{conversation_type}")
async def fine_tune(fingerprint: str, conversation_type: str):
    response = tune.tune(fingerprint, conversation_type)
    return response


@app.get("/test")
async def test():
    return {"response": "test"}


app.include_router(user_router)
app.include_router(conversation_router)
app.include_router(diary_router)

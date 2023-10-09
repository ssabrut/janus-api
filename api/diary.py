from fastapi import APIRouter, HTTPException, Request
from api import client
from datetime import date
import uuid

router = APIRouter()


@router.post("/api/diary/{fingerprint}")
async def create_diary(request: Request, fingerprint: str):
    db = client.get_db()
    diary_collections = db["diaries"]

    data = await request.json()

    if "content" not in data:
        return HTTPException(status_code=400, detail="Invalid request body")

    content = data["content"]

    if not isinstance(content, str):
        return HTTPException(status_code=400, detail="Invalid request body")

    diary = diary_collections.find_one({"fingerprint": fingerprint})

    if diary is not None:
        return HTTPException(status_code=400, detail="Diary already exists")

    diary_collections.insert_one(
        {
            "fingerprint": fingerprint,
            "diaries": [
                {
                    "id": str(uuid.uuid4()),
                    "content": content,
                    "timestamp": date.today().strftime("%Y-%m-%d"),
                }
            ],
        }
    )

    return {"status": "success", "status_code": 200}


@router.post("/api/diary/{fingerprint}/insert")
async def insert_diary(request: Request, fingerprint: str):
    db = client.get_db()
    diary_collections = db["diaries"]

    data = await request.json()

    if "content" not in data:
        return HTTPException(status_code=400, detail="Invalid request body")

    content = data["content"]

    if not isinstance(content, str):
        return HTTPException(status_code=400, detail="Invalid request body")

    diary = diary_collections.find_one({"fingerprint": fingerprint})

    if diary is None:
        return HTTPException(status_code=400, detail="Diary does not exist")

    diary_collections.update_one(
        {"fingerprint": fingerprint},
        {
            "$push": {
                "diaries": {
                    "id": str(uuid.uuid4()),
                    "content": content,
                    "timestamp": date.today().strftime("%Y-%m-%d"),
                }
            },
        },
    )
    return {"status": "success", "status_code": 200}


@router.get("/api/diary/{fingerprint}")
async def get_diaries(fingerprint: str):
    db = client.get_db()
    diary_collections = db["diaries"]

    diary = diary_collections.find_one({"fingerprint": fingerprint})

    if diary is None:
        return HTTPException(status_code=400, detail="Diary does not exist")

    diary["_id"] = str(diary["_id"])
    return {"status": "success", "status_code": 200, "data": diary}


@router.get("/api/diary/{fingerprint}/{id}")
async def get_diary(fingerprint: str, id: str):
    db = client.get_db()
    diary_collections = db["diaries"]

    diary_entry = diary_collections.find_one(
        {"fingerprint": fingerprint},
        {"diaries": {"$elemMatch": {"id": id}}},
    )

    if diary_entry is None:
        return HTTPException(status_code=400, detail="Diary does not exist")

    diary_entry["_id"] = str(diary_entry["_id"])
    return {"status": "success", "status_code": 200, "data": diary_entry}

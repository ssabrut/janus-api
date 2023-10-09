from fastapi import APIRouter, HTTPException, Request
from api import client

router = APIRouter()


@router.post("/api/users")
async def create_user(request: Request):
    try:
        data = await request.json()

        if "name" not in data and "fingerprint" not in data:
            return HTTPException(status_code=400, detail="Invalid request body")

        name = data["name"]
        fingerprint = data["fingerprint"]

        if not isinstance(name, str) or not isinstance(fingerprint, str):
            return HTTPException(status_code=400, detail="Invalid request body")

        db = client.get_db()
        user_collections = db["users"]
        user = user_collections.find_one({"fingerprint": fingerprint})

        if user is not None:
            user_collections.update_one(
                {"fingerprint": fingerprint}, {"$set": {"name": name}}
            )
        else:
            user_collections.insert_one({"name": name, "fingerprint": fingerprint})

        user = user_collections.find_one({"fingerprint": fingerprint})
        user["_id"] = str(user["_id"])
        return {"status": "success", "status_code": 200, "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/users/{fingerprint}")
async def get_user(fingerprint: str):
    try:
        db = client.get_db()
        user_collections = db["users"]
        user = user_collections.find_one({"fingerprint": fingerprint})

        if user is None:
            return HTTPException(status_code=404, detail="User not found")

        user["_id"] = str(user["_id"])
        return {"status": "success", "status_code": 200, "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

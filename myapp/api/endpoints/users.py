from fastapi import APIRouter,Form

router = APIRouter()

@router.get("/")
async def read_main():
    return {"msg": "Hello World"}

@router.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


from fastapi import APIRouter, Request


router = APIRouter()

@router.post("/{source}")
async def webhook(request: Request, source: str):
    data = await request.json()
    print(source)
    print("*"*20)
    print(data)

    return {"ok": True}

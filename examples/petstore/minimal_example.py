from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

inmem = {"pets": {}}

@app.post("/api/v3/pet")
async def create_pet(request: Request):
    body = await request.json()
    pid = body.get("id")
    if pid in inmem["pets"]:
        return JSONResponse({"detail": "Pet ID already exists"}, status_code=400)
    inmem["pets"][pid] = body
    return JSONResponse(body, status_code=status.HTTP_201_CREATED)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
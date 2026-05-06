from fastapi import FastAPI
from fastapi import UploadFile, File

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    return {"id": 0}

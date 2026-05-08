from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel
import boto3
import uuid
from cloudflare import Cloudflare


class CreateUploadRequest(BaseModel):
    filename: str
    size: int
    content_type: str


from dotenv import load_dotenv

load_dotenv()
import os

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name="auto",
)
client = Cloudflare()


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/uploads")
def upload_file(body: CreateUploadRequest):
    filename = body.filename
    size = body.size
    content_type = body.content_type

    if content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Content type must be application/pdf"
        )
    if size > 100 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be less than 100MB")

    s3_key = str(uuid.uuid4())
    post_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": environ.get("AWS_BUCKET_NAME"),
            "Key": s3_key,
            "ContentType": content_type,
        },
        ExpiresIn=60,  # seconds
    )


    d1 = client.d1.database.get(
        database_id=os.environ.get("CLOUDFLARE_D1_DATABASE_ID"),
        account_id=os.environ.get("CLOUDFLARE_ACCOUNT_ID"),
    )

    client.d1.database.query(
        database_id=os.environ.get("CLOUDFLARE_D1_DATABASE_ID"),
        account_id=os.environ.get("CLOUDFLARE_ACCOUNT_ID"),
        data={
            "filename": filename,
            "size": size,
            "content_type": content_type,
        },
    )
    


    # save db followings:
    # - filename
    # - size
    # - content_type
    # - filename
    # - s3_key
    # - status = 'pending'
    print(post_url)

    return {
        "url": post_url,
        "key": s3_key,
    }

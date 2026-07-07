import uuid
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings  # adjust import to however you load env vars

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

ALLOWED_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

async def save_upload_files(file: UploadFile, folder: str) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Allowed types: jpeg, jpg, webp, png"
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large. Maximum size is 5MB"
        )

    public_id = f"{folder}/{uuid.uuid4()}"

    result = cloudinary.uploader.upload(
        content,
        public_id=public_id,
        folder="food_delivery",  # top-level folder in your Cloudinary account
        resource_type="image"
    )

    # This is now a full CDN URL — store this directly in your DB
    return result["secure_url"]


async def delete_upload_file(public_id: str):
    cloudinary.uploader.destroy(public_id, resource_type="image")
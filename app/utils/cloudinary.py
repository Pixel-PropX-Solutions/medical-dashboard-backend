from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary import config as cloudinary_config
from fastapi import UploadFile, HTTPException
from typing import Dict
from app.config import settings
from starlette.concurrency import run_in_threadpool


class CloudinaryClient:
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        # Set Cloudinary global config
        cloudinary_config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
        )

    async def upload_file(self, file: UploadFile) -> Dict:
        try:
            # The cloudinary.uploader.upload call is blocking; run it in a threadpool
            result = await run_in_threadpool(
                upload,
                file.file,
                resource_type="auto",
                filename=file.filename,
                folder="Vyapar_Drishti",
                overwrite=True,
            )

            # Generate secure URL
            url, _ = cloudinary_url(
                result["public_id"], secure=True, format=result.get("format", "jpg")
            )

            return {
                "url": url,
                "filename": file.filename,
                "public_id": result["public_id"],
                "format": result.get("format"),
                "width": result.get("width"),
                "height": result.get("height"),
            }

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Cloudinary upload failed: {str(e)}"
            )


cloudinary_client = CloudinaryClient(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

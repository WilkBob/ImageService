from fastapi import APIRouter, UploadFile, File, Query, Depends
from fastapi.responses import StreamingResponse
from PIL import Image
import zipfile
import io
from app.middleware.auth import conditional_token_verification


router = APIRouter()

@router.post("/webp-multiple/")
async def convert_to_webp_multiple(
    files: list[UploadFile] = File(...),
    quality: int = Query(80, description="Quality of the WebP images"),
    user: dict = Depends(conditional_token_verification)
):
    processed_images = []

    for file in files:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        processed_image = image.convert("RGB")
        
        # Convert to WebP format
        img_byte_array = io.BytesIO()
        processed_image.save(img_byte_array, format="WEBP", quality=quality)
        img_byte_array.seek(0)
        
        processed_images.append((file.filename.rsplit(".", 1)[0] + ".webp", img_byte_array))

    # Create a zip file containing all processed images
    zip_byte_array = io.BytesIO()
    with zipfile.ZipFile(zip_byte_array, 'w') as zip_file:
        for filename, img_byte_array in processed_images:
            zip_file.writestr(filename, img_byte_array.getvalue())
    zip_byte_array.seek(0)

    # Add header for display
    headers = {
        'Content-Disposition': 'attachment; filename="processed_images.zip"'
    }

    return StreamingResponse(zip_byte_array, media_type="application/zip", headers=headers)
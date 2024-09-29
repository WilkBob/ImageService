from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from PIL import Image
import io

router = APIRouter()

@router.post("/webp/")
async def convert_to_webp(
    file: UploadFile = File(...),
    quality: int = Query(90, description="Quality of the WebP image")
):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    processed_image = image.convert("RGB")
    
    # Convert to WebP format
    img_byte_array = io.BytesIO()
    processed_image.save(img_byte_array, format="WEBP", quality=quality)
    img_byte_array.seek(0)

    # Add header for display
    headers = {
        'Content-Disposition': f'inline; filename="{file.filename.rsplit(".", 1)[0]}.webp"'
    }

    return StreamingResponse(img_byte_array, media_type="image/webp", headers=headers)

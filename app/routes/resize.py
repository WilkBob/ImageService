from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from app.utils.image_processing import process_image, convert_to_webp

router = APIRouter()

@router.post("/resize/")
async def resize_image(
    file: UploadFile = File(...),
    max_width: int = Query(None, description="Optional max width for resizing the image"),
    webp: bool = Query(True, description="Convert the image to WebP format")
):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    processed_image = process_image(image, max_width=max_width)
    
    # Convert to WebP format if the flag is set, and update the filename
    if webp:
        processed_image = convert_to_webp(processed_image)
        new_filename = file.filename.rsplit(".", 1)[0] + ".webp"
        file_type = "WEBP"
        media_type = "image/webp"
    else:
        # Convert to RGB if the image has an alpha channel
        if processed_image.mode in ("RGBA", "LA"):
            processed_image = processed_image.convert("RGB")
        new_filename = file.filename
        file_type = processed_image.format if processed_image.format else "jpeg"
        media_type = f"image/{file_type.lower()}"
    
    # Stream the processed image
    img_byte_array = io.BytesIO()
    processed_image.save(img_byte_array, format=file_type)
    img_byte_array.seek(0)

    # Add header for display
    headers = {
        'Content-Disposition': f'inline; filename="{new_filename}"'
    }

    return StreamingResponse(img_byte_array, media_type=media_type, headers=headers)
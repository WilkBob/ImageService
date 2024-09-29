from fastapi import APIRouter, UploadFile, File, Query, Depends
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import zipfile
from app.utils.image_processing import process_image, convert_to_webp
from app.middleware.auth import conditional_token_verification

router = APIRouter()

@router.post("/resize-multiple/")
async def resize_multiple_images(
    files: list[UploadFile] = File(...),
    max_width: int = Query(None, description="Optional max width for resizing the images"),
    webp: bool = Query(True, description="Convert the images to WebP format"),
    user: dict = Depends(conditional_token_verification)
):
    processed_images = []

    for file in files:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        processed_image = process_image(image, max_width=max_width)
        
        # Convert to WebP format if the flag is set, and update the filename
        if webp:
            processed_image = convert_to_webp(processed_image)
            new_filename = file.filename.rsplit(".", 1)[0] + ".webp"
            file_type = "WEBP"
        else:
            # Convert to RGB if the image has an alpha channel
            if processed_image.mode in ("RGBA", "LA"):
                processed_image = processed_image.convert("RGB")
            new_filename = file.filename
            file_type = processed_image.format if processed_image.format else "jpeg"
        
        # Save the processed image to a byte array
        img_byte_array = io.BytesIO()
        processed_image.save(img_byte_array, format=file_type)
        img_byte_array.seek(0)
        
        processed_images.append((new_filename, img_byte_array))

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
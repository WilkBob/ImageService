from fastapi import APIRouter, UploadFile, File, Query, Depends
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import zipfile
import json
from typing import List
from app.utils.image_processing import process_image, convert_to_webp, generate_base64_placeholder
from app.middleware.auth import conditional_token_verification

router = APIRouter()

@router.post("/component/")
async def component(
        files: List[UploadFile] = File(...),
        max_width: int = Query(None, description="Max width of the processed images"),
        include_originals: bool = Query(True, description="Include original images in the ZIP file"),
        include_thumbnails: bool = Query(True, description="Include thumbnail images in the ZIP file"),
        thumbnail_size: int = Query(300, description="Size of the thumbnail images"),
        user: dict = Depends(conditional_token_verification)
):
    zip_buffer = io.BytesIO()
    index_data = []

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            processed_image = process_image(image, max_width=max_width)
            webp_image = convert_to_webp(processed_image)
            base64_placeholder = generate_base64_placeholder(processed_image)
            
            # Save processed image
            processed_img_byte_arr = io.BytesIO()
            webp_image.save(processed_img_byte_arr, format='WEBP')
            processed_img_byte_arr.seek(0)
            processed_filename = f"images/{file.filename.rsplit('.', 1)[0]}_tiny.webp"
            zip_file.writestr(processed_filename, processed_img_byte_arr.getvalue())
            
            # Save original image if requested
            if include_originals:
                original_webp_image = convert_to_webp(image)
                original_img_byte_arr = io.BytesIO()
                original_webp_image.save(original_img_byte_arr, format='WEBP')
                original_img_byte_arr.seek(0)
                original_filename = f"images/{file.filename.rsplit('.', 1)[0]}.webp"
                zip_file.writestr(original_filename, original_img_byte_arr.getvalue())
            
            # Save thumbnail image if requested
            if include_thumbnails:
                thumbnail_image = image.resize((thumbnail_size, int(thumbnail_size * image.height / image.width)))
                thumbnail_webp_image = convert_to_webp(thumbnail_image)
                thumbnail_img_byte_arr = io.BytesIO()
                thumbnail_webp_image.save(thumbnail_img_byte_arr, format='WEBP', quality=100)
                thumbnail_img_byte_arr.seek(0)
                thumbnail_filename = f"images/{file.filename.rsplit('.', 1)[0]}_thumb.webp"
                zip_file.writestr(thumbnail_filename, thumbnail_img_byte_arr.getvalue())
            
            # Add entry to index
            index_data.append({
                "filename": f"{file.filename.rsplit('.', 1)[0]}",
                "processed": processed_filename,
                "original": original_filename if include_originals else None,
                "thumbnail": thumbnail_filename if include_thumbnails else None,
                "base64_placeholder": base64_placeholder,
                "dimensions": image.size,
                "aspect_ratio": image.width / image.height,
                "thumbnail_size": thumbnail_size
            })
        
        # Save index.json
        index_json = json.dumps(index_data, indent=4)
        zip_file.writestr("index.json", index_json)
    
    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=processed_images.zip"})
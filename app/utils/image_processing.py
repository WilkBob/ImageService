from PIL import Image
import io
import base64

default_max_width = 40

def process_image(image: Image.Image, max_width: int = None) -> Image.Image:
    # Use default_max_width if max_width is not provided
    max_w = max_width or default_max_width
    
    # Resize the image, keeping the aspect ratio
    width, height = image.size
    new_height = int(max_w * height / width)
    if new_height > image.height or max_w > image.width:
        return image
    processed_image = image.resize((max_w, new_height))
    
    return processed_image

def convert_to_webp(image: Image.Image) -> Image.Image:
    # Convert image to WebP format
    webp_image = io.BytesIO()
    image.save(webp_image, format='WEBP')
    webp_image.seek(0)
    return Image.open(webp_image)

def generate_base64_placeholder(image: Image.Image) -> str:
    # Generate a low-resolution base64 string for the image
    placeholder_image = image.resize((10, int(10 * image.height / image.width)))
    
    # Convert to RGB if the image has an alpha channel
    if placeholder_image.mode in ("RGBA", "LA"):
        placeholder_image = placeholder_image.convert("RGB")
    
    buffered = io.BytesIO()
    placeholder_image.save(buffered, format="JPEG")
    base64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_str}"
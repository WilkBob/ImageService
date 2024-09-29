# Sizeable Image Processor

Welcome to the Sizeable Image Processor! This open-source project is designed to help you convert, resize, and prepare images for use with the [react-progressify](https://github.com/wilkbob/progressify-react) progressive image library. Whether you're building a web application or a mobile app, Sizeable makes it easy to handle image processing tasks efficiently.

## Features

- **Image Conversion**: Convert images to various formats, including WebP.
- **Image Resizing**: Resize images while maintaining aspect ratios.
- **Progressive Image Preparation**: Generate low-resolution placeholders for progressive image loading.

## Getting Started

### Prerequisites

- Python 3.9+
- FastAPI
- PIL (Pillow)
- Uvicorn

### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/sizeable-image-processor.git
   cd sizeable-image-processor
   ```

2. **Create a virtual environment**:

   ```sh
   python -m venv my_image_processing_env
   source my_image_processing_env/bin/activate  # On Windows use `my_image_processing_env\Scripts\activate`
   ```

3. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the FastAPI server**:

   ```sh
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation**:

   Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore the API endpoints using the interactive Swagger UI.

### API Endpoints

- **Resize Image**: `POST /resize`
- **Resize Multiple Images**: `POST /resize-multiple`
- **Convert to WebP**: `POST /convert-webp`

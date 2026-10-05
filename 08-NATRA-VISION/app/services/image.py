from PIL import Image

ALLOWED_IMAGE_FORMATS = ["jpeg", "png", "gif", "bmp", "tiff"]

def validate_image(content: bytes, expected_format: str = "jpeg") -> bool:
    """
    Validate the image content to ensure it is in the expected format.

    Args:
        content (bytes): The image content in bytes.
        expected_format (str): The expected image format (default is "jpeg").

    Returns:
        bool: True if the image is valid and in the expected format, False otherwise.
    """
    from PIL import Image
    import io



    try:
        # Open the image from bytes
        image = Image.open(io.BytesIO(content))
        # Check if the image format matches the expected format
        return image.format.lower() == expected_format.lower()
    except Exception as e:
        # If an error occurs, the image is not valid
        return False

def resize_image(content: bytes, max_width: int, max_height: int) -> bytes:
    """
    Resize the image to fit within the specified maximum width and height while maintaining aspect ratio.

    Args:
        content (bytes): The image content in bytes.
        max_width (int): The maximum width for the resized image.
        max_height (int): The maximum height for the resized image.

    Returns:
        bytes: The resized image content in bytes.
    """
    import io

    try:
        # Open the image from bytes
        image = Image.open(io.BytesIO(content))
        # Resize the image while maintaining aspect ratio
        image.thumbnail((max_width, max_height))
        
        # Save the resized image to a bytes buffer
        output_buffer = io.BytesIO()
        image.save(output_buffer, format=image.format)
        
        return output_buffer.getvalue()
    except Exception as e:
        raise ValueError("Failed to resize image") from e
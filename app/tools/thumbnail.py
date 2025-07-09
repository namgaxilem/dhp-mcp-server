from mcp.server.fastmcp import Image
from PIL import Image as PILImage

def generate_thumbnail(image_path: str) -> Image:
    """Generate a thumbnail for a provided image (e.g., bill or graph)."""
    img = PILImage.open(image_path)
    img.thumbnail((120, 120))
    return Image(data=img.tobytes(), format="png")
from .nodes.sequential_image_loader.sequential_image_loader import NODE_CLASS_MAPPINGS as SEQUENTIAL_IMAGE_LOADER_NODES
from .nodes.sequential_image_loader.sequential_image_loader import NODE_DISPLAY_NAME_MAPPINGS as SEQUENTIAL_IMAGE_LOADER_DISPLAY_NAMES

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Add nodes from sequential_image_loader
NODE_CLASS_MAPPINGS.update(SEQUENTIAL_IMAGE_LOADER_NODES)
NODE_DISPLAY_NAME_MAPPINGS.update(SEQUENTIAL_IMAGE_LOADER_DISPLAY_NAMES)

# Export the mappings
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"] 
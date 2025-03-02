import os
import glob
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms

class SequentialImageLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": "", "multiline": False}),
                "mask": ("MASK",),
                "current_index": ("INT", {"default": 0, "min": 0}),
                "resize_width": ("INT", {"default": 3840, "min": 1}),
                "resize_height": ("INT", {"default": 2160, "min": 1}),
                "image_interpolation": (["BICUBIC", "BILINEAR", "NEAREST"], {"default": "BICUBIC"}),
                "mask_interpolation": (["BILINEAR", "NEAREST", "BICUBIC"], {"default": "NEAREST"}),
                "binarize_mask": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "INT")
    RETURN_NAMES = ("image", "mask", "filename", "total_images")
    FUNCTION = "load_image"
    CATEGORY = "image"

    def load_image(self, folder_path, mask, current_index=0, resize_width=3840, resize_height=2160, image_interpolation="BICUBIC", mask_interpolation="NEAREST", binarize_mask=True):
        # Debugging: Log inputs
        print(f"[DEBUG] Start load_image - folder_path: '{folder_path}', current_index: {current_index}, mask shape: {mask.shape}, resize_width: {resize_width}, resize_height: {resize_height}, image_interpolation: {image_interpolation}, mask_interpolation: {mask_interpolation}, binarize_mask: {binarize_mask}")
        
        # List and sort image files in the folder
        image_files = sorted(
            glob.glob(os.path.join(folder_path, "*.png")) +
            glob.glob(os.path.join(folder_path, "*.jpg"))
        )
        total_images = len(image_files)
        print(f"[DEBUG] Gefundene Bilder: {total_images}, Dateien: {image_files}")
        
        # Error handling: No images found
        if total_images == 0:
            raise ValueError(f"[ERROR] Keine Bilder im Ordner gefunden: {folder_path}")
        
        # Error handling: Index out of range
        if current_index >= total_images:
            raise ValueError(f"[ERROR] current_index {current_index} überschreitet Gesamtzahl der Bilder: {total_images}")
        
        # Load the image at the current index
        image_path = image_files[current_index]
        print(f"[DEBUG] Lade Bild: {image_path}")
        pil_image = Image.open(image_path).convert("RGB")
        print(f"[DEBUG] PIL Bild geladen - Shape: {np.array(pil_image).shape}")
        
        # Map interpolation method for PIL
        interpolation_map = {
            "BICUBIC": Image.Resampling.BICUBIC,
            "BILINEAR": Image.Resampling.BILINEAR,
            "NEAREST": Image.Resampling.NEAREST,
        }
        pil_interpolation = interpolation_map[image_interpolation]
        
        # Resize the PIL image to the specified dimensions
        pil_image = pil_image.resize((resize_width, resize_height), pil_interpolation)
        print(f"[DEBUG] Bild nach Resize - Shape: {np.array(pil_image).shape}")
        
        # Convert resized PIL image to tensor
        np_image = np.array(pil_image)  # Shape: (H, W, 3)
        torch_image = torch.from_numpy(np_image).float() / 255.0  # Shape: (H, W, 3)
        print(f"[DEBUG] Nach Normalisierung - Shape: {torch_image.shape}")
        
        # Bildtensor in [N, H, W, C] umformen, da GetImageSizeAndCount dies erwartet
        torch_image = torch_image.unsqueeze(0)  # Shape: (1, H, W, 3)
        print(f"[DEBUG] Nach Permutation (für GetImageSizeAndCount) - Shape: {torch_image.shape}")
        
        # Resize the mask to match the specified dimensions
        # Mask shape: [1, H, W] oder [1, 1, H, W] (ComfyUI MASK format)
        if len(mask.shape) == 3:  # [1, H, W]
            mask = mask.unsqueeze(1)  # Shape: [1, 1, H, W]
        print(f"[DEBUG] Maske vor Resize - Shape: {mask.shape}")
        print(f"[DEBUG] Maske vor Resize - Min: {mask.min().item()}, Max: {mask.max().item()}")
        
        # Map interpolation method for PyTorch
        torch_interpolation_map = {
            "BILINEAR": transforms.InterpolationMode.BILINEAR,
            "NEAREST": transforms.InterpolationMode.NEAREST,
            "BICUBIC": transforms.InterpolationMode.BICUBIC,
        }
        torch_interpolation = torch_interpolation_map[mask_interpolation]
        
        resize_transform = transforms.Resize((resize_height, resize_width), interpolation=torch_interpolation)
        mask = resize_transform(mask)  # Shape: [1, 1, resize_height, resize_width]
        print(f"[DEBUG] Maske nach Resize - Shape: {mask.shape}")
        print(f"[DEBUG] Maske nach Resize - Min: {mask.min().item()}, Max: {mask.max().item()}")
        
        # Binarize the mask if requested
        if binarize_mask:
            mask = (mask > 0.5).float()  # Werte > 0.5 werden zu 1, andere zu 0
            print(f"[DEBUG] Maske nach Binarisierung - Min: {mask.min().item()}, Max: {mask.max().item()}")
        
        # Entferne die Kanal-Dimension, um den ResizeMask-Node zu unterstützen (er erwartet [1, H, W])
        mask = mask.squeeze(1)  # Shape: [1, H, W]
        print(f"[DEBUG] Maske nach Squeeze (für ResizeMask) - Shape: {mask.shape}")
        
        # Extract filename
        filename = os.path.basename(image_path)
        print(f"[DEBUG] Aktueller Dateiname: {filename}")
        
        # Return values
        print(f"[DEBUG] Rückgabe - image shape: {torch_image.shape}, mask shape: {mask.shape}, filename: {filename}, total_images: {total_images}")
        return (torch_image, mask, filename, total_images)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "SequentialImageLoaderV8": SequentialImageLoader
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "SequentialImageLoaderV8": "Sequential Image Loader V8"
} 
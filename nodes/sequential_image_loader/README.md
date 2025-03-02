# Sequential Image Loader for ComfyUI

A custom node for ComfyUI that loads images sequentially from a folder, applies a mask, and provides various outputs.

## Features

- Loads images sequentially from a folder
- Applies a mask to all images
- Returns the current image index and the total number of images
- Various resize options for both images and masks
- Mask binarization option

## Usage

The node appears in the "image" category in the node browser.

### Inputs

- **folder_path**: Path to the folder with images to be processed
- **mask**: A mask in ComfyUI MASK format
- **current_index**: The current image index (starting at 0)
- **resize_width/resize_height**: Target resolution for the images
- **image_interpolation**: Interpolation method for image resizing
- **mask_interpolation**: Interpolation method for mask resizing
- **binarize_mask**: Whether to convert the mask to binary values (0/1)

### Outputs

- **image**: The loaded image
- **mask**: The adjusted mask
- **filename**: The filename of the current image
- **total_images**: The total number of images in the folder

## Example Workflows

Example workflows are included in the `example_workflow.json` and `minimal_workflow.json` files. You can import these into ComfyUI to see how the node works.

## Notes on Mask Processing

- The mask is automatically resized to match the dimensions of the image
- The mask can be binarized (all values > 0.5 become 1, others become 0)
- The output mask format is compatible with all ComfyUI mask nodes like ResizeMask, MaskToImage, etc.

## Troubleshooting

- If you see error messages about invalid mask dimensions, make sure you're providing a valid ComfyUI mask as input
- Check your folder path to ensure it contains valid image files (PNG, JPG)
- Make sure the current_index is not exceeding the total number of images in the folder

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details. 
"""The plugin for applying comic-ocr line annotation to the image."""

from typing import Dict, Any, Union

import comic_ocr
import comic_ocr.utils.nb_annotation as comic_ocr_annotation


def get_plugin_info(detailed: bool = False) -> Dict[str, Any]:
    """Returns the plugin information."""
    return {
        "name": "Comic OCR (Line Annotation)",
        "description": "Annotates text lines in the comic or manga page with comic-ocr model",
    }


def apply_plugin(image_path: str, image_data: Union[Dict[str, Any], None]) -> Union[Dict[str, Any], None]:
    """Applies the plugin to the image and modify the image data.

    Args:
        image_path: The path to the image file.
        image_data: The current image data (written in the JSON file).

    Returns:
        The modified/new image data (to be written in the JSON file).
    """
    lines = comic_ocr.read_lines(image_path)
    data = comic_ocr_annotation.lines_to_nb_annotation_data(lines)
    return data

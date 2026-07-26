"""
Grad-CAM heatmap generation module — PLACEHOLDER implementation.

Exposes `generate_heatmap()`, which the diagnosis service calls after a
classification result is produced. A real implementation would hook into
the target classifier's final convolutional layer and compute true
gradient-weighted class activation maps.
"""
import logging

from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


def generate_heatmap(image: Image.Image, disease_key: str) -> Image.Image:
    """
    Produce a heatmap overlay for the given image and disease model.

    TODO(AI engineer): replace with real Grad-CAM, e.g. using
    `pytorch-grad-cam` against the corresponding classifier in
    `app/ai/classification/<disease_key>.py`:

        from pytorch_grad_cam import GradCAM
        model = get_classifier_module(disease_key).load_model()
        cam = GradCAM(model=model, target_layers=[model.layer4[-1]])
        grayscale_cam = cam(input_tensor=tensor)[0]
        return overlay_heatmap_on_image(image, grayscale_cam)
    """
    logger.info("Generating placeholder heatmap for disease='%s'", disease_key)

    # --- Placeholder overlay: a translucent marker box, NOT a real activation map ---
    overlay = image.convert("RGBA").copy()
    draw = ImageDraw.Draw(overlay, "RGBA")
    w, h = overlay.size
    box = (w * 0.3, h * 0.3, w * 0.7, h * 0.7)
    draw.rectangle(box, fill=(255, 0, 0, 80), outline=(255, 0, 0, 200), width=3)
    return overlay.convert("RGB")

# utils.py
import os
import fal_client
from prompts import SYSTEM_PROMPT, USER_TEMPLATE

FAL_MODEL_ID = "fal-ai/imagen4/preview"


def build_moodboard_prompt(brands: str, visuals: str, extra_notes: str):
    """Return messages list ready for OpenAI ChatCompletion."""
    user_msg = USER_TEMPLATE.format(
        brands=brands.strip(),
        visuals=(visuals or "none").strip(),
        notes=(extra_notes or "none").strip(),
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]


def call_falai_if_requested(prompt: str, api_key: str | None):
    """
    Generate one image with fal.ai Imagen-4 and return its URL (or None on failure).
    Uses the new fal_client.subscribe method.
    """
    if not api_key:
        return None

    # Set environment variable for fal_client
    os.environ["FAL_KEY"] = api_key

    try:
        # Use subscribe method which handles the queue automatically
        result = fal_client.subscribe(
            FAL_MODEL_ID,
            arguments={
                "prompt": prompt,
                "num_images": 1,
                "aspect_ratio": "16:9",
            },
            with_logs=True,
        )
        
        # The result structure is: {"images": [{"url": "..."}], "seed": ...}
        if result and "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]
        else:
            print("[fal.ai] No images in result:", result)
            return None
            
    except Exception as exc:
        print(f"[fal.ai] generation failed: {exc}")
        return None

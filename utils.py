# utils.py
import os
import fal_client                      
from prompts import SYSTEM_PROMPT, USER_TEMPLATE

FAL_MODEL_ID = os.getenv("FAL_MODEL_ID", "fal-ai/imagen4/preview")  # Imagen-4


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
    """
    if not api_key:
        return None

    # Initialise the SDK (sets env inside)
    fal.init(key=api_key, request_timeout=120)   # timeout in seconds

    try:
        result = fal.run(
            FAL_MODEL_ID,
            arguments={
                "prompt": prompt,
                "num_images": 1,
                "image_size": "landscape_16_9",   # 1024×576
            },
        )
        # result structure: {"images": [{"url": "..."}], ...}
        return result["images"][0]["url"]
    except Exception as exc:
        print("[fal.ai] generation failed:", exc)
        return None

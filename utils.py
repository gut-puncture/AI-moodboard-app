### utils.py
import os
import requests
import textwrap
from urllib.parse import urljoin

from prompts import SYSTEM_PROMPT, USER_TEMPLATE

FAL_ENDPOINT = "https://api.fal.ai/imagen"  # example; confirm actual endpoint


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


def call_falai_if_requested(prompt: str, api_key: str):
    """Calls fal.ai Imagen‑4 to generate an image; returns hosted URL or None."""
    headers = {"Authorization": f"Key {api_key}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "n": 1, "size": "1024x576"}
    try:
        resp = requests.post(FAL_ENDPOINT, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("images", [None])[0]
    except Exception as exc:
        print("[fal.ai] generation failed:", exc)
        return None
### app.py
"""Gradio app for generating an AI‑ready moodboard prompt.
Run locally:  `uvicorn app:app --reload` or `python app.py` (Gradio popup).
"""
import os
import json
import textwrap
import gradio as gr
import openai
from utils import build_moodboard_prompt, call_falai_if_requested
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
FAL_AI_KEY = os.getenv("FAL_API_KEY", "")  # optional for server‑side Imagen4 call
O3_MODEL = os.getenv("OPENAI_O3_MODEL", "o3-2025-04-16")  # default "o3"

# ----------  Gradio UI callbacks ---------- #

def generate_prompt(brands, visuals, extra_notes, auto_generate_image):
    """Main gradio handler: returns a best‑in‑class prompt (and optional fal.ai image url)."""
    if not brands:
        return ("⚠️  Please provide at least one brand.", None)

    # 1) Build the system+user messages for o3
    full_prompt = build_moodboard_prompt(brands, visuals, extra_notes)

    # 2) Call OpenAI ChatCompletion
    response = openai.chat.completions.create(
        model=O3_MODEL,
        messages=full_prompt,
        max_completion_tokens=800,
    )
    moodboard_prompt = response.choices[0].message.content.strip()

    # 3) Optionally ask fal.ai Imagen‑4 to render
    image_url = None
    if auto_generate_image and FAL_AI_KEY:
        image_url = call_falai_if_requested(moodboard_prompt, FAL_AI_KEY)

    return moodboard_prompt, image_url


def launch():
    with gr.Blocks(title="Quiet‑Luxury Moodboard Builder") as demo:
        gr.Markdown("# Quiet‑Luxury Footwear Moodboard Builder\nEnter brands + visual links and instantly get a perfect Imagen4 prompt.")

        with gr.Row():
            brands_in = gr.Textbox(label="Brand names (comma‑separated)",
                                   placeholder="Toteme, Aeyde, Koio, Margaux")
            visuals_in = gr.Textbox(label="Optional image URLs (one per line)")
        extra_in = gr.Textbox(label="Extra creative direction (optional)")
        auto_flag = gr.Checkbox(label="Generate image with fal.ai (needs FAL_API_KEY)")
        btn = gr.Button("Craft Prompt →")

        prompt_out = gr.Textbox(label="AI Image Prompt", lines=14)
        img_out = gr.Image(label="Imagen‑4 Result (optional)")

        btn.click(generate_prompt,
                  inputs=[brands_in, visuals_in, extra_in, auto_flag],
                  outputs=[prompt_out, img_out])

    demo.launch()

if __name__ == "__main__":
    launch()

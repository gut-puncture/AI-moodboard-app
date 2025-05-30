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

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
FAL_AI_KEY = os.getenv("FAL_KEY", "")  # Consistent with env variable name
O3_MODEL = os.getenv("OPENAI_O3_MODEL", "o3-2025-04-16")  # default "o3"

# ----------  Gradio UI callbacks ---------- #

def generate_prompt(brands, visuals, extra_notes):
    """Generate prompt using OpenAI without auto-generating image."""
    if not brands:
        return "⚠️  Please provide at least one brand."

    # 1) Build the system+user messages for o3
    full_prompt = build_moodboard_prompt(brands, visuals, extra_notes)

    try:
        # 2) Call OpenAI ChatCompletion with updated client
        response = client.chat.completions.create(
            model=O3_MODEL,
            messages=full_prompt,
            max_completion_tokens=800,
        )
        moodboard_prompt = response.choices[0].message.content.strip()
        return moodboard_prompt
    except Exception as e:
        return f"⚠️  Error generating prompt: {str(e)}"


def generate_image_from_prompt(prompt):
    """Generate image from the provided prompt."""
    if not prompt or prompt.startswith("⚠️"):
        return None, "Please generate a valid prompt first."
    
    if not FAL_AI_KEY:
        return None, "⚠️  FAL_KEY not configured. Please set the FAL_KEY secret in HuggingFace Spaces settings."

    # Generate image using the prompt
    image_url = call_falai_if_requested(prompt, FAL_AI_KEY)
    
    if image_url:
        return image_url, "✅  Image generated successfully!"
    else:
        return None, "⚠️  Failed to generate image. Check logs for details."


def launch():
    with gr.Blocks(title="Quiet‑Luxury Moodboard Builder") as demo:
        gr.Markdown("# Quiet‑Luxury Footwear Moodboard Builder\nEnter brands + visual links to get a perfect Imagen4 prompt, then optionally generate the moodboard.")

        with gr.Row():
            with gr.Column():
                brands_in = gr.Textbox(
                    label="Brand names (comma‑separated)",
                    placeholder="Toteme, Aeyde, Koio, Margaux",
                    lines=2
                )
                visuals_in = gr.Textbox(
                    label="Optional image URLs (one per line)",
                    placeholder="https://example.com/image1.jpg\nhttps://example.com/image2.jpg",
                    lines=3
                )
                extra_in = gr.Textbox(
                    label="Extra creative direction (optional)",
                    placeholder="Focus on minimalist aesthetic, neutral tones...",
                    lines=2
                )
                
                generate_btn = gr.Button("🎯 Generate Prompt", variant="primary")
                
        # Prompt output and editing
        prompt_out = gr.Textbox(
            label="AI Image Prompt (you can edit this before generating)",
            lines=12,
            placeholder="Generated prompt will appear here..."
        )
        
        # Image generation section
        with gr.Row():
            generate_img_btn = gr.Button("🎨 Generate Moodboard Image", variant="secondary")
            
        with gr.Row():
            img_out = gr.Image(label="Generated Moodboard", show_label=True, height=500)
            status_out = gr.Textbox(label="Status", lines=2, interactive=False)

        # Event handlers
        generate_btn.click(
            generate_prompt,
            inputs=[brands_in, visuals_in, extra_in],
            outputs=[prompt_out]
        )
        
        generate_img_btn.click(
            generate_image_from_prompt,
            inputs=[prompt_out],
            outputs=[img_out, status_out]
        )

    demo.launch()


if __name__ == "__main__":
    launch()

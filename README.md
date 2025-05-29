### README.md (excerpt)
```markdown
# Quiet-Luxury Footwear Moodboard Builder

A Gradio web app (ready for **HuggingFace Spaces**) that lets product teams enter a few reference brands & inspiration images and instantly receive a finely crafted prompt for **fal.ai Imagen‑4**. The prompt captures each brand’s design DNA, stitches them into a coherent visual language, and can optionally generate the moodboard server‑side.

## 🔧 Local setup
```bash
git clone https://github.com/<you>/quiet_luxury_moodboard_app.git
cd quiet_luxury_moodboard_app
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your keys
python app.py  # launches a local Gradio UI
```

## 🚀 Deploy to HuggingFace Spaces
1. **Create a new Space → Gradio** in your HF account.
2. Push this repo (`git remote add space ...`) or upload via UI.
3. In the Space Settings → Secrets, add `OPENAI_API_KEY` (and optionally `FAL_API_KEY`).
4. HF automatically installs `requirements.txt` and runs `python app.py`.

The Space will spin up, showing the brand + visuals input boxes and returning the prompt (plus image if enabled).  
⚠️  Imagen‑4 generation is billed on fal.ai; server‑side generation is optional—you can uncheck the box and copy‑paste the prompt into fal.ai’s own UI instead.
```

---

### Notes & Rationale
* **Library versions** pinned to the latest May‑2025 tags known to work on HF Spaces Python‑3.11 runner.
* **Questions to user** – o3 is instructed to ask *only* if critical details (e.g., no brands or visuals && domain‑specific nuance) are missing.
* **Brand scraping** – heavy real‑time scraping is intentionally skipped (to stay within HF demo limits). Instead, o3 leverages its latent knowledge; future upgrade path = plug in SerpAPI + BeautifulSoup inside `utils.py`.
* **Security** – Keys pulled from env vars; none baked into code.
* **Future work** – Add caching, async calls, and better error UX.

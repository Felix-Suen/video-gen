from pathlib import Path
import subprocess
import json
from config import NICHE_CONFIG, OLLAMA_MODEL, PATHS




def run_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL, prompt],
        capture_output=True,
        text=False
    )
    stdout_bytes = result.stdout or b""
    # Decode using UTF-8 and replace invalid sequences rather than raising.
    out = stdout_bytes.decode("utf-8", errors="replace")
    return out.strip()




def generate_idea():
    prompt = f"""
Generate 3 TikTok video ideas.
Niche: {NICHE_CONFIG['niche']}
Audience: {NICHE_CONFIG['audience']}
Tone: {NICHE_CONFIG['tone']}
Rules:
- Hook in first 2 seconds
- Faceless
- No emojis
Return plain text.
"""
    return run_llm(prompt)




def generate_script():
    prompt = f"""
Write ONLY spoken narration for a TikTok video.

Niche: {NICHE_CONFIG['niche']}
Tone: {NICHE_CONFIG['tone']}
Length: {NICHE_CONFIG['video_length_seconds']} seconds

Rules:
- Plain sentences only
- No emojis
- No brackets
- No labels (Narrator, Scene, etc.)
- Each sentence on a new line
- End with: {NICHE_CONFIG['cta']}
"""
    return run_llm(prompt)




def generate_caption():
    prompt = f"""
Write a short TikTok caption for this niche: {NICHE_CONFIG['niche']}.
Include exactly 3 hashtags.
No emojis.
"""
    return run_llm(prompt)

def generate_scene_descriptions():
    script_path = Path(PATHS["script"])
    if not script_path.exists():
        raise FileNotFoundError(f"Script file not found: {script_path}")
    script_text = script_path.read_text()

    prompt = (
        f"Given the following TikTok script, generate a short scene description "
        f"for visuals. Output only the text.\n\n"
        f"Script:\n{script_text}"
    )

    # Run Ollama
    return run_llm(prompt)
import torch
from diffusers import StableDiffusionPipeline
from pathlib import Path
import json
from llm import generate_scene_descriptions
from config import PATHS

MODEL_ID = "Lykon/dreamshaper-7"

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    safety_checker=None
).to("cuda")

def generate_images():
    scenes = json.load(open(PATHS["scenes"]))
    output_dir = Path(PATHS["images"])
    output_dir.mkdir(parents=True, exist_ok=True)

    for scene in scenes:
        torch.cuda.empty_cache()
        print(f"Generating image for scene {scene['id']}")
        image = pipe(
            prompt=scene["image_prompt"],
            negative_prompt="blurry, low quality, distorted, watermark",
            width=576,
            height=1024,
            num_inference_steps=25,
            guidance_scale=7.5
        ).images[0]

        out_path = output_dir / f"scene_{scene['id']}.png"
        image.save(out_path)

        del image
        torch.cuda.empty_cache()

        print(f"Saved {out_path}")

def build_scenes(num_scenes=6):
    
    lines = [generate_scene_descriptions() for _ in range(num_scenes)]
    scenes = [{"id": idx + 1, "image_prompt": line} for idx, line in enumerate(lines)]

    # Save to file
    output_path = Path(PATHS["scenes"])
    output_path.parent.mkdir(exist_ok=True, parents=True)
    with open(output_path, "w") as f:
        json.dump(scenes, f, indent=2)

    print(f"Saved {len(scenes)} scenes to {output_path}")
    return scenes

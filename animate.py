import subprocess
from pathlib import Path
from config import PATHS

def animate_images(duration_per_scene=4):
    images_dir = Path(PATHS["images"])
    video_dir = Path("data/video/scenes")
    video_dir.mkdir(parents=True, exist_ok=True)

    for img in sorted(images_dir.glob("scene_*.png")):
        scene_id = img.stem.split("_")[1]
        out = video_dir / f"scene_{scene_id}.mp4"

        # Use original image resolution
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img),
            "-t", str(duration_per_scene),
            "-vf",
            "fps=30,format=yuv420p",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(out)
        ], check=True)

        print(f"Created {out}")

import subprocess
import os
from config import PATHS

# def assemble_video():
#     subs_path = os.path.abspath(PATHS['subs'])
#     bg_path = os.path.abspath(PATHS['bg'])
#     audio_path = os.path.abspath(PATHS['audio'])
#     out_path = os.path.abspath(PATHS['video'])

#     cmd = [
#         "ffmpeg",
#         "-y",
#         "-i", bg_path,
#         "-i", audio_path,
#         "-vf", f"subtitles='{subs_path}'",
#         "-map", "0:v",
#         "-map", "1:a",
#         "-shortest",
#         out_path
#     ]

#     subprocess.run(cmd, check=True)

from pathlib import Path
import subprocess

def concat_scenes():
    scenes_dir = Path("data/video/scenes")
    list_file = scenes_dir / "scenes.txt"

    with open(list_file, "w") as f:
        for scene in sorted(scenes_dir.glob("scene_*.mp4")):
            f.write(f"file '{scene.name}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(scenes_dir / "background.mp4")
    ], check=True)

from config import PATHS
import subprocess

def assemble_video():
    subprocess.run([
        "ffmpeg", "-y",
        "-i", "data/video/scenes/background.mp4",
        "-i", str(PATHS["audio"]),
        "-vf", f"subtitles={PATHS['subs']}",
        "-map", "0:v",
        "-map", "1:a",
        "-shortest",
        str(PATHS["video"])
    ], check=True)

    print("Final video created:", PATHS["video"])

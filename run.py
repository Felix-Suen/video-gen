import argparse
import os
import subprocess
from llm import generate_idea, generate_script
from tts import generate_voice
from subtitles import generate_subtitles
from video_utils import assemble_video, concat_scenes
from caption import save_caption
from image_gen import generate_images, build_scenes
from animate import animate_images
from config import PATHS




def main(args):

    ollama_proc = None
    try: 
        ollama_proc = subprocess.Popen(["ollama", "serve"])
      if args.idea:
          idea = generate_idea()
          os.makedirs(os.path.dirname(PATHS['ideas']), exist_ok=True)
          open(PATHS['ideas'], "w").write(idea)
          print("Generated Ideas")
      if args.script:
          script = generate_script()
          os.makedirs(os.path.dirname(PATHS['script']), exist_ok=True)
          open(PATHS['script'], "w").write(script)
          print("Generated Script")
        if args.caption:
            save_caption()
            print("Saved Caption")
        if args.scenes:
            build_scenes()
            print("Generated Scene Descriptions")
    finally:
        if ollama_proc:
            ollama_proc.terminate()
    if args.images:
        generate_images()
        print("Generated Images")
    if args.animate:
        animate_images()  # Placeholder for animation logic
        concat_scenes()
        print("Animated Images")
    if args.tts:
        generate_voice()
        print("Generated Voice")
    if args.subs:
        generate_subtitles()
        print("Generated Subtitles")
    if args.video:
        assemble_video()
        print("Assembled Video")


    print("DONE")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--idea", action="store_true", help="Generate idea")
    parser.add_argument("--script", action="store_true", help="Generate script")
    parser.add_argument("--tts", action="store_true", help="Generate voice")
    parser.add_argument("--subs", action="store_true", help="Generate subtitles")
    parser.add_argument("--video", action="store_true", help="Assemble video")
    parser.add_argument("--caption", action="store_true", help="Save caption")
    parser.add_argument("--images", action="store_true", help="Generate images")
    parser.add_argument("--scenes", action="store_true", help="Generate scenes")
    parser.add_argument("--animate", action="store_true", help="Animate images")

    args = parser.parse_args()

    # Default behavior: run everything if no flags provided
    if not any(vars(args).values()):
        args.idea = True
        args.script = True
        args.tts = True
        args.subs = True
        args.video = True
        args.caption = True
        args.images = True
        args.scenes = True
        args.animate = True

    main(args)
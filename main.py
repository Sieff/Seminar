import os


def main(scene_name):
    os.system('winpty docker run --rm -it -v "C:\\Users\\steff\\Documents\\uni\\MAD\\Seminar:/manim"' +
              ' manimcommunity/manim manim -qm scene.py ' + scene_name)


if __name__ == "__main__":
    main('GrowingRectangle')

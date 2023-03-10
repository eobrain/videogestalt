import sys
from moviepy.editor import CompositeVideoClip, concatenate_videoclips, ImageClip, VideoFileClip, ColorClip


minisPerSide = 8
miniCount = minisPerSide*minisPerSide

WIDTH = 0
HEIGHT = 1


def main(originalPath):
    original = VideoFileClip(originalPath, audio=False)
    fullHeight = original.size[HEIGHT]
    fullWidth = original.size[WIDTH]
    extendeWidth = fullWidth*(minisPerSide+1)//minisPerSide
    miniHeight = fullHeight/minisPerSide
    miniWidth = fullWidth/minisPerSide
    miniDuration = original.duration/miniCount
    # base = ImageClip("1x1-transparent.png", duration=miniDuration,
    #                 ismask=False).resize((extendeWidth, fullHeight))
    base = ColorClip((extendeWidth, fullHeight),
                     color=[0, 0, 255, 128], duration=miniDuration)

    def motion(i, j):
        forward = j % 2 == 0
        y = j*miniHeight
        if forward:
            return lambda t: (miniWidth*(i+t/miniDuration), y)
        else:
            return lambda t: (extendeWidth - miniWidth*(i+t/miniDuration+1), y)

    def mini(j, i):
        k = j*minisPerSide + i
        return (original
                .subclip(k*miniDuration, (k+1)*miniDuration)
                .resize((miniWidth, miniHeight))
                .set_position(motion(i, j)))

    minis = [mini(j, i)
             for j in range(minisPerSide)
             for i in range(minisPerSide)]

    def left(j):
        k = j*minisPerSide - 1
        return (original
                .subclip(k*miniDuration, (k+1)*miniDuration)
                .resize((miniWidth, miniHeight))
                .set_position(motion(-1, j)))

    lefts = [left(j)
             for j in range(1, minisPerSide)]

    def right(j):
        k = (j+1)*minisPerSide
        return (original
                .subclip(k*miniDuration, (k+1)*miniDuration)
                .resize((miniWidth, miniHeight))
                .set_position(motion(minisPerSide, j)))

    rights = [right(j)
              for j in range(minisPerSide-1)]

    leading = (original
               .to_ImageClip(0, duration=miniDuration)
               .resize((miniWidth, miniHeight))
               .set_position(motion(-1, 0)))
    trailing = (original
                .to_ImageClip(original.duration - 1, duration=miniDuration)
                .resize((miniWidth, miniHeight))
                .set_position(motion(minisPerSide, minisPerSide-1)))

    output = CompositeVideoClip(
        minis+lefts+rights+[leading, trailing], (extendeWidth, fullHeight))

    output.write_gif("gestalt-"+originalPath+".gif", program="ffmpeg")
    output.write_videofile("gestalt-"+originalPath)


if __name__ == "__main__":
    import time
    args = sys.argv[1:]
    if len(args) != 1:
        print(f"Expected one argument got {len(args)}, {args}")
        exit(1)
    else:
        start_time = time.time()
        main(args[0])
        print("--- %d seconds ---" % (time.time() - start_time))

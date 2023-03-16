import sys
from moviepy.editor import CompositeVideoClip, ImageClip, VideoFileClip, ColorClip
from math import sqrt, ceil

approxThumbDuration = 1
minThumbHeight = 30

WIDTH = 0
HEIGHT = 1


def main(originalPath):
    original = VideoFileClip(originalPath, audio=False)
    fullHeight = original.size[HEIGHT]
    fullWidth = original.size[WIDTH]
    maxThumbsPerSide = fullWidth//minThumbHeight
    thumbsPerSide = ceil(sqrt(original.duration/approxThumbDuration))
    thumbsPerSide = max(2,thumbsPerSide)
    thumbsPerSide = min(maxThumbsPerSide,thumbsPerSide)
    thumbCount = thumbsPerSide*thumbsPerSide
    extendeWidth = fullWidth*(thumbsPerSide+1)//thumbsPerSide
    thumbHeight = fullHeight//thumbsPerSide
    thumbWidth = fullWidth//thumbsPerSide
    thumbDuration = original.duration/thumbCount

    print("%dx%d grid of %fx%f %fs thumbnails" %
          (thumbsPerSide, thumbsPerSide, thumbWidth, thumbHeight, thumbDuration))

    def motion(i, j):
        forward = j % 2 == 0
        y = j*thumbHeight
        if forward:
            return lambda t: (thumbWidth*(i+t/thumbDuration), y)
        else:
            return lambda t: (extendeWidth - thumbWidth*(i+t/thumbDuration+1), y)

    def thumb(j, i):
        k = j*thumbsPerSide + i
        return (original
                .subclip(k*thumbDuration, (k+1)*thumbDuration)
                .resize((thumbWidth, thumbHeight))
                .set_position(motion(i, j)))

    thumbs = [thumb(j, i)
             for j in range(thumbsPerSide)
             for i in range(thumbsPerSide)]

    def left(j):
        k = j*thumbsPerSide - 1
        return (original
                .subclip(k*thumbDuration, (k+1)*thumbDuration)
                .resize((thumbWidth, thumbHeight))
                .set_position(motion(-1, j)))

    lefts = [left(j)
             for j in range(1, thumbsPerSide)]

    def right(j):
        k = (j+1)*thumbsPerSide
        return (original
                .subclip(k*thumbDuration, (k+1)*thumbDuration)
                .resize((thumbWidth, thumbHeight))
                .set_position(motion(thumbsPerSide, j)))

    rights = [right(j)
              for j in range(thumbsPerSide-1)]

    leading = (original
               .to_ImageClip(0, duration=thumbDuration)
               .resize((thumbWidth, thumbHeight))
               .set_position(motion(-1, 0)))
    trailing = (original
                .to_ImageClip(original.duration - 1, duration=thumbDuration)
                .resize((thumbWidth, thumbHeight))
                .set_position(motion(thumbsPerSide, thumbsPerSide-1)))

    output = CompositeVideoClip(
        thumbs+lefts+rights+[leading, trailing], (extendeWidth, fullHeight))

    # output.write_gif("gestalt-"+originalPath+".gif", program="ffmpeg")
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

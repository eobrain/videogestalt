from math import sqrt, ceil
from argparse import ArgumentParser
from moviepy.editor import CompositeVideoClip, ImageClip, VideoFileClip, ColorClip

approxThumbDuration = 1
minThumbHeight = 30

WIDTH = 0
HEIGHT = 1


def main(originalPath, generateGif, generateVideo):
    print("Generating gestalt for %s" % originalPath)
    if (generateVideo):
        print("Will generating video")
    if (generateGif):
        print("Will generating GIF")

    original = VideoFileClip(originalPath, audio=False)
    fullHeight = original.size[HEIGHT]
    fullWidth = original.size[WIDTH]
    maxThumbsPerSide = fullWidth//minThumbHeight
    thumbsPerSide = ceil(sqrt(original.duration/approxThumbDuration))
    thumbsPerSide = max(2, thumbsPerSide)
    thumbsPerSide = min(maxThumbsPerSide, thumbsPerSide)
    thumbCount = thumbsPerSide*thumbsPerSide
    extendeWidth = fullWidth*(thumbsPerSide+1)//thumbsPerSide
    thumbHeight = fullHeight//thumbsPerSide
    thumbWidth = fullWidth//thumbsPerSide
    thumbDuration = original.duration/thumbCount
    speedPixelsPerSec = thumbWidth/thumbDuration
    speedPixelsPerFrame = speedPixelsPerSec/original.fps

    print("%dx%d grid of %fx%f %fs thumbnails, moving at @ %f pixels/frame" %
          (thumbsPerSide, thumbsPerSide, thumbWidth, thumbHeight, thumbDuration, speedPixelsPerFrame))

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

    if generateGif:
        output.write_gif("gestalt-"+originalPath+".gif", program="ffmpeg")
    if generateVideo:
        output.write_videofile("gestalt-"+originalPath)


if __name__ == "__main__":
    import time

    parser = ArgumentParser(
        prog='generate.py',
        description='Generates overview of video',
        epilog='(c) Eamonn O\'Brien-Strain')
    parser.add_argument('-i', '--input', metavar='something.mp4',
                        required=True,
                        help='input video file')
    parser.add_argument('-g', '--gif', action='store_true',
                        default=False,
                        help='generate GIF')
    parser.add_argument('-v', '--video', action='store_true',
                        default=False,
                        help='generate video file')
    args = parser.parse_args()
    start_time = time.time()
    main(args.input, args.gif, args.video)
    print("--- %d seconds ---" % (time.time() - start_time))

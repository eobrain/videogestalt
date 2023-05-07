#!/usr/bin/env python3

# Author: Eamonn O'Brien-Strain
# Contributors: Stephen Karl Larroque
# License: Mozilla Public License Version 2.0
# Description: Generates overview of video
# Usage: python videogestalt.py -h

import os
import shlex
import sys
import time

from argparse import ArgumentParser, ArgumentTypeError
from math import sqrt, ceil
from moviepy.editor import CompositeVideoClip, ImageClip, VideoFileClip, ColorClip
from pathlib import Path

OUTPUT_WIDTH = 1000
MIN_SPEED_PIXELS_PER_FRAME = 2
MIN_THUMB_WIDTH = 60
MAX_THUMBS_PER_SIDE = OUTPUT_WIDTH//MIN_THUMB_WIDTH

WIDTH = 0
HEIGHT = 1


def gen_gestalt(originalPath, outputPath, generateGif, generateVideo):
    '''Generate an animated gestalt image or video from a video'''
    print("Generating gestalt for %s" % originalPath)
    if (generateVideo):
        print("Will generate a video")
    if (generateGif):
        print("Will generate a GIF")

    original = VideoFileClip(originalPath, audio=False)
    minSpeedPixelsPerSec = MIN_SPEED_PIXELS_PER_FRAME*original.fps
    sumOfThumbWidths = minSpeedPixelsPerSec*original.duration
    thumbsPerSide = round(sqrt(sumOfThumbWidths/MIN_THUMB_WIDTH))
    if thumbsPerSide < 2:
        print("Forcing at least 2x2 grid")
        thumbsPerSide = 2

    if thumbsPerSide > MAX_THUMBS_PER_SIDE:
        print("Forcing at most %dx%d grid" %
              (MAX_THUMBS_PER_SIDE, MAX_THUMBS_PER_SIDE))
        thumbsPerSide = MAX_THUMBS_PER_SIDE

    fullWidth = MIN_THUMB_WIDTH*thumbsPerSide
    fullHeight = round(fullWidth*original.size[HEIGHT]/original.size[WIDTH])
    print("Full size: %dx%d" % (fullWidth, fullHeight))
    thumbCount = thumbsPerSide*thumbsPerSide
    thumbWidth = round(fullWidth/thumbsPerSide)
    thumbHeight = round(thumbWidth*original.size[HEIGHT]/original.size[WIDTH])
    thumbDuration = original.duration/thumbCount
    speedPixelsPerSec = thumbWidth/thumbDuration
    speedPixelsPerFrame = speedPixelsPerSec/original.fps
    extendeWidth = round(fullWidth*(thumbsPerSide+1)/thumbsPerSide)

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

    # Write output
    if generateGif:
        ext = ''
        if (outputPath[-4:].lower() != '.gif'):  # .gif extension not found
            ext = '.gif'  # we append .gif extension
        # to a gif file
        output.write_gif("%s%s" % (outputPath, ext), program="ffmpeg")
    elif generateVideo:
        # to a video file

        # MoviePy requires a file extension to determine how to encode the output
        # Hence, by default, if none is provided, reuse the input file extension
        if (outputPath.find('.') < 0):  # no extension found
            outputPath = "%s%s" % (outputPath, Path(originalPath).suffix)  # we append the input path file extension
        output.write_videofile(outputPath)

def is_dir_or_file(dirname):
    '''Checks if a path is an actual directory that exists or a file'''
    if not os.path.isdir(dirname) and not os.path.isfile(dirname):
        msg = "{0} is not a directory nor a file".format(dirname)
        raise ArgumentTypeError(msg)
    else:
        return dirname

def fullpath(relpath):
    '''Relative path to absolute'''
    if (type(relpath) is object or hasattr(relpath, 'read')): # relpath is either an object or file-like, try to get its name
        relpath = relpath.name
    return os.path.abspath(os.path.expanduser(relpath))

def main(argv=None):
    '''Script entry point, can be used in commandline or as a Python module'''
    # Allow to be used as a module or in commandline, by storing the commandline arguments in function argument argv if empty
    if argv is None: # if argv is empty, fetch from the commandline
        argv = sys.argv[1:]
    elif isinstance(argv, str): # else if argv is supplied but it's a simple string, we need to parse it to a list of arguments before handing to argparse or any other argument parser
        argv = shlex.split(argv) # Parse string just like argv using shlex

    # Setup arguments parser
    parser = ArgumentParser(
        prog='videogestalt',
        description='Generates an animated overview of video',
        epilog='(c) Eamonn O\'Brien-Strain')

    parser.add_argument('-i', '--input', metavar='something.mp4',
                        type=is_dir_or_file,
                        required=True,
                        help='input video file')
    parser.add_argument('-o', '--output', metavar='/some/folder/output.(gif|mp4)',
                        type=str,
                        required=True,
                        help='output filepath')

    mgroup = parser.add_mutually_exclusive_group(required=True)
    mgroup.add_argument('-g', '--gif', action='store_true',
                        default=False,
                        help='generate GIF')
    mgroup.add_argument('-v', '--video', action='store_true',
                        default=False,
                        help='generate video file')

    # Parse arguments (either from commandline or function argument when used as a module)
    args = parser.parse_args(argv)

    # Generate the gestalt image
    start_time = time.time()  # note this is not a reliable performance indicator, use time.process_time() instead
    gen_gestalt(fullpath(args.input), fullpath(args.output), args.gif, args.video)
    print("--- Total time spent: %d seconds ---" % (time.time() - start_time))

# Commandline call
if __name__ == "__main__":
    main_entry()

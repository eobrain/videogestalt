# Video Gestalt

[![PyPI-Status][1]][2] [![PyPI-Versions][3]][4] [![PyPI-Downloads][5]][6]

[![Build-Status][7]][8] [![Coverage-Status][9]][10]

[![Example video gestalt: Vespa-Scooter-Commercial][11]][12]

Presents a video in a summary form that shows the entire video at once as an array of moving video thumbnails.

## Description

Video Gestalt presents a condensed video array, showing the entire video at once as moving video thumbnails.

The above is an example of the Video Gestalt for a 50-second commercial for Vesta scooters. (Click the Video Gestalt to see the original video.)

As you can see, it is a looping video with moving thumbnails of the original video. In one second, you can see every frame of the original video at a glance, without any discontinuities as it loops. This is done by arranging that each thumbnail slides over exactly its width in one loop so that the next thumbnail takes over seamlessly.

Hence, the video gestalts can be read in two ways: 1- an overall quick glance shows all the scenes of the entire video, 2- by focusing on one animated thumbnail, we can watch the entire video, by starting in the upper left corner, and following to the right, then descending one block lower and moving from right to left, then descending one block and moving left to right again, etc.

A longer explanation is available in [this blog post](https://eamonn.org/video-gestalt-one-glance-overview-of-a-video).

## Installation

So far this has been tested on Linux, Chrome OS and Windows, but it will likely work on MacOS too.

To install, simply use `pip`:

```bash
pip install --upgrade videogestalt
```

This will also install [MoviePy](https://zulko.github.io/moviepy/), which will automatically install [FFmpeg](https://ffmpeg.org/) if necessary.

If they are not already installed, you will need to install `python3` and the corresponding Python package manager `pip` beforehand.

On Linux and friends you might be able to do this like so:
```bash
sudo apt-get install python3 python3-pip
```

If you get an error, please ensure you are using the latest `pip` version, as older versions may not support PEP517 Python packages:

```bash
pip install --upgrade pip
```

## Usage

An executable binary `videogestalt` is automatically installed in the local environment.

To generate a video file:

```bash
videogestalt -i countdown.mp4 -o countdown-gestalt --video
```

To generate an animated GIF (warning, output can be large):

```bash
videogestalt -i countdown.mp4 -o countdown-gestalt --gif
```

The application can also be used as a Python module:

```python
>>> from videogestalt import videogestalt as vg
>>> vg.main('-i countdown.mp4 -o countdown-gestalt --gif')
```

Note: if the repository is cloned, there is an example `countdown.mp4` video in `tests/examples`.

## Building

The module can be built with PEP517 standard tools, such as `pypa/build`:

```bash
python -sBm build .
```

It can also be installed in development/editable mode after cloning this git repository:

```bash
pip install --upgrade -e .
```

## License

Created by Eamonn O'Brien-Strain.

Licensed under the Mozilla Public License 2.0

[1]: https://img.shields.io/pypi/v/videogestalt.svg
[2]: https://pypi.org/project/videogestalt
[3]: https://img.shields.io/pypi/pyversions/videogestalt.svg?logo=python&logoColor=white
[4]: https://pypi.org/project/videogestalt
[5]: https://img.shields.io/pypi/dm/videogestalt.svg?label=pypi%20downloads&logo=python&logoColor=white
[6]: https://pypi.org/project/videogestalt
[7]: https://github.com/eobrain/videogestalt/actions/workflows/ci-build.yml/badge.svg?event=push
[8]: https://github.com/eobrain/videogestalt/actions/workflows/ci-build.yml
[9]: https://codecov.io/github/eobrain/videogestalt/coverage.svg?branch=master
[10]: https://codecov.io/github/eobrain/videogestalt?branch=master
[11]: https://raw.githubusercontent.com/eobrain/videogestalt/main/resources/vespa-commercial-gestalt.gif
[12]: https://ia904607.us.archive.org/11/items/vespa-scooter-commercial/Vespa%20Scooter%20Commercial.mp4

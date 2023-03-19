# Video Gestalt

[![gestalt-Vespa-Scooter-Commercial ia mp4][1]][3]

Presents a video in a summary form that shows the entire video at once as an array of moving video thumbnails.

## Installation

So far this has only been tested on Linux and Chrome OS, but it will likely work on MacOS too, and maybe even on Windows.

The only file you need from this repo is `gestalt.py`. You can grab this however you want, and make it executable. For example, do the following from the command line:

```bash
wget https://raw.githubusercontent.com/eobrain/videogestalt/main/gestalt.py
chmod +x gestalt.py
```

If they are not already installed, you will need to install `python3` and the corresponding Python package manager `pip`.

You will need to install the `moviepy` Python library:

```bash
pip install moviepy
```


## Usage

Put the `gestalt.py` in the same directory as an input video file `test.mp4`.

Generate a video file:

```bash
./gestalt.py -i test.mp4 -v
```

Generate an animated GIF (warning, can be large):

```bash
./gestalt.py -i test.mp4 -g
```

[1]: https://user-images.githubusercontent.com/179320/226146985-d67db97e-bcd6-4377-a1da-cc6020135d84.gif
[3]: https://ia904607.us.archive.org/11/items/vespa-scooter-commercial/Vespa%20Scooter%20Commercial.mp4


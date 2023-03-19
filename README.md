# Video Gestalt

[<video autoplay loop muted src="https://social-coop-media.ams3.cdn.digitaloceanspaces.com/media_attachments/files/110/045/643/010/816/155/original/6f6bbf570661a1b4.mp4" type="video/mp4"></video>][3]

Presents a video in a summary form that shows the entire video at once as an array of moving video thumbnails.

## Installation

So far this has only been tested on Linux and Chrome OS, but it will likely work on MacOS too.

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

[3]: https://ia904607.us.archive.org/11/items/vespa-scooter-commercial/Vespa%20Scooter%20Commercial.mp4

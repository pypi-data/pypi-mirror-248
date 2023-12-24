from os import getcwd
from os import path as os_path

from click import group
from click import option
from loguru import logger

from .mp3 import mp3
from .mp4 import mp4
from .png import png
from .png import to_png


@group(name='conv', help="Convert a file")
def conv():
    pass


@conv.command(help="Convert a video to another format")
@option('-p', '--path', type=str, required=True, prompt=True,
        help="Path to the video file (e.g. /path/to/file)")
@option('-f', '--format', type=str, required=True, prompt=True,
        help="Format to convert to (e.g. mp3)")
def video(path: str, format: str):
    logger.debug("conv video")

    if not os_path.isabs(path):
        path = os_path.join(getcwd(), path)

    if not os_path.exists(path):
        print(f"Video {src} does not exist")
        return

    splits = path.split(".")

    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    logger.debug(f"Converting {src_path} to {dst_path}")

    mp4(src_path, dst_path)
    return


@conv.command(help="Convert an audio to another format")
@option('-p', '--path', type=str, required=True, prompt=True,
        help="Path to the audio file (e.g. /path/to/file)")
@option('-f', '--format', type=str, required=True, prompt=True,
        help="Format to convert to (e.g. wav)")
def audio(path: str, format: str):
    logger.debug("conv audio")

    if not os_path.isabs(path):
        path = os_path.join(getcwd(), path)

    if not os_path.exists(path):
        print(f"Audio {src} does not exist")
        return

    splits = path.split(".")

    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    logger.debug(f"Converting {src_path} to {dst_path}")

    mp3(src_path, dst_path)
    return


@conv.command(help="Convert an image into another format")
@option('-p', '--path', type=str, required=True, prompt=True,
        help="Path to the image file (e.g. /path/to/file)")
@option('-f', '--format', type=str, required=True, prompt=True,
        help="Format to convert to (e.g. jpg, mp4)")
@option('-d', '--duration', type=int, default=0,
        help="Duration of output file in seconds (e.g. 30)")
def image(path: str, format: str, duration: int):
    logger.debug("conv image")

    if not os_path.isabs(path):
        path = os_path.join(getcwd(), path)

    if not os_path.exists(path):
        print(f"Image {src} does not exist")
        return

    splits = path.split(".")

    src_format = splits[-1]
    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    if src_format != 'png':
        src_path = to_png(src_path)

    logger.debug(f"Converting {src_path} to {dst_path}")

    png(src_path, dst_path, duration)
    return

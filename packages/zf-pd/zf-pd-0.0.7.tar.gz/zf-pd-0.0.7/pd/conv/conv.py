from os import getcwd
from os import path as os_path

from click import group
from click import option
from loguru import logger

from .m4a import m4a
from .mov import mov
from .mp3 import mp3
from .mp4 import mp4
from .png import png
from .png import to_png
from .webm import webm


@group(name='conv', help="Convert a file")
def conv():
    pass


@conv.command(help="List all available conversions")
def list():
    logger.debug("conv list")

    print("Available conversions:")
    print("  video")
    print("    mp4,webm,mov -> mp3")
    print("  audio")
    print("    m4a -> wav, mp3")
    print("    mp3 -> wav, m4a")
    print("  image")
    print("    jpg, jpeg, png -> mp4")
    return


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
        print(f"Video {path} does not exist")
        return

    splits = path.split(".")

    src_format = splits[-1]
    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    logger.debug(f"Converting {src_path} to {dst_path}")

    if src_format == 'mp4':
        mp4(src_path, dst_path)
    elif src_format == 'webm':
        webm(src_path, dst_path)
    elif src_format == 'mov':
        mov(src_path, dst_path)
    else:
        logger.error(f"Unsupported file {src_format}")
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
        print(f"Audio {path} does not exist")
        return

    splits = path.split(".")

    src_format = splits[-1]
    src_filename = ".".join(splits[:-1])
    src_path = path

    dst_format = format
    dst_path = f"{src_filename}.{dst_format}"

    logger.debug(f"Converting {src_path} to {dst_path}")

    if src_format == 'm4a':
        m4a(src_path, dst_path)
    elif src_format == 'mp3':
        mp3(src_path, dst_path)
    else:
        logger.error(f"Unsupported file {src_format}")
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
        print(f"Image {path} does not exist")
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

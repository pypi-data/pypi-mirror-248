from click import group
from click import option
from loguru import logger
from pytube import YouTube


@group(name='down', help="Download from the internet")
def down():
    pass


@down.command(help="Download a YouTube video")
@option('-l', '--link', type=str, required=True, prompt=True,
        help="Link to the YouTube video (e.g. https://www.youtube.com/watch?v=...)")
@option('-f', '--format', type=str, required=True, prompt=True,
        help="Format to download as (e.g. mp4, mp3)")
def youtube(link: str, format: str):
    logger.debug("down video")

    if format == 'mp4':
        yt = YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download()
    elif format == 'webm':
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        stream.download()
    else:
        logger.error(f"Unsupported format {format}")

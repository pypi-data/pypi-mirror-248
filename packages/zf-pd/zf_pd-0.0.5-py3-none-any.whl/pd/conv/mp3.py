from pydub import AudioSegment
from loguru import logger


def mp3(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == 'wav':
        mp3_to_wav(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def mp3_to_wav(src: str, dst: str) -> None:
    audio = AudioSegment.from_mp3(src)
    audio.export(dst, format="wav")
    return

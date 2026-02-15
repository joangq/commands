from typing import Literal
from argbuilder import Command as BaseCommand, Field


type VideoCodec = Literal[
    'copy',
    'libx264',
    'libx265',
]

type AudioCodec = Literal[
    'copy',
    'aac',
    'mp3',
]

class Command(BaseCommand):
    arg0 = 'ffmpeg'

    format: str = Field(['-f', '{value}'])
    infile: str = Field(['-i', '{value}'])
    safe: int = Field(['-safe', '{value}'])
    copy: str = Field(['-copy', '{value}'])
    outfile: str = Field(['{value}'])
    version: bool = Field('-version')
    codec_video: VideoCodec = Field(['-c:v', '{value}'])
    codec_audio: AudioCodec = Field(['-c:a', '{value}'])
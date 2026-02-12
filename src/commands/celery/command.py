from typing import Literal
from argbuilder import Command as BaseCommand, Field

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
class Command(BaseCommand):
    arg0 = 'celery'
    
    app: str = Field(['-A', '{value}'])
    worker_name: str = Field('{value}')
    log_level: LogLevel = Field('--loglevel={value}')
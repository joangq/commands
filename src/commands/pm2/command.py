from argbuilder import Command as BaseCommand, Field
from pathlib import Path

def process_path(x: str|Path):
    return str(Path(x).resolve())

class Command(BaseCommand):
    def arg0(self):
        import platform

        match platform.system():
            case 'Windows': return 'pm2.cmd'
            case 'Linux': return 'pm2'
            case _: 
                raise ValueError(f'Unsupported platform: {platform.system()}')

    version: bool = Field('--version')

    # command: Command = Field('{value}', Command.build)

    class start(BaseCommand):
        ecosystem: Path = Field('{value}', process_path)

    class delete(BaseCommand):
        app: str = Field('{value}')
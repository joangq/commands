from argbuilder import Command as BaseCommand, Field # pyright: ignore[reportMissingTypeStubs]

class Command(BaseCommand):
    arg0 = 'uv'

    class run(BaseCommand):
        module: BaseCommand = Field('{value}', BaseCommand.build)
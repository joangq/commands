from argbuilder import Command as BaseCommand, Field

class Command(BaseCommand):
    arg0 = 'R'
    execute: str = Field(['-e', '{value}'])
    vanilla: bool = Field('--vanilla')
    quiet: bool = Field('--quiet')
    no_save: bool = Field('--no-save')
    no_restore: bool = Field('--no-restore')
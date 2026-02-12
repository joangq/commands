from argbuilder import Command as BaseCommand, Field

class Command(BaseCommand):
    arg0 = 'docker'
    
    class compose(BaseCommand):

        class up(BaseCommand):
            pass

        class down(BaseCommand):
            pass
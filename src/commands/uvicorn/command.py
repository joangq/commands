from argbuilder import Command as BaseCommand, Field

class Command(BaseCommand):
    arg0 = 'uvicorn'
    
    app: str = Field('{value}')
    reload: bool = Field('--reload')
    port: int = Field(['--port', '{value}'], default=8000)
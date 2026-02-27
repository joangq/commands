from typing import assert_type
from argbuilder import Command as BaseCommand, Field
from . import models
from .expression import Expression, value, is_not

# ==============================================================================

def filter_expressions(exprs: dict[str, str|Expression]):
    expressions = list[Expression]()
    for k,v in exprs.items():
        if isinstance(v, str):
            v = value(v)
        
        assert_type(v, Expression)
        
        v.set_label(k)

        assert v.label is not None

        expressions.append(v)
    
    return map(str, expressions)

def expressions(**exprs: str|Expression):
    return filter_expressions(exprs)

def filter_serializer(x: str|list[str]) -> list[str]:
    if isinstance(x, str):
        return filter_serializer([x])
    
    return [
        z
        for y in x
        for z in ('--filter', y)
    ]

# ==============================================================================

class Command(BaseCommand):
    arg0 = 'docker'
    
    class compose(BaseCommand):
        class up(BaseCommand):
            service: str = Field('{value}')

        class down(BaseCommand):
            service: str = Field('{value}')

        class build(BaseCommand):
            service: str = Field('{value}')
            no_cache: bool = Field('--no-cache')
    
    class inspect(BaseCommand):
        service_id: str = Field('{value}')

        def execute(self, raise_on_error: bool = True):
            result = self.run(text=False)
            stderr = result.stderr.decode()
            stdout = result.stdout.decode()

            if result.returncode != 0:
                if raise_on_error:
                    raise Exception(stderr)
                else:
                    return None, result
            
            return models.Inspect.model_validate_json(stdout).root[0], result

    class ps(BaseCommand):
        all: bool = Field('--all')
        filter: str|list[str] = Field(
            '{value}', 
            serializer=filter_serializer,
            annotation=str|list[str]
        )
        quiet: bool = Field('-q')
        
        def filters(self, **exprs):
            expressions = filter_expressions(exprs)
            self.__dict__.setdefault('filter', []).extend(expressions)
            return self

        def execute_quiet(
            self, 
            raise_on_error: bool = True
        ):
            
            result = self.run(text=False)

            if result.returncode != 0:
                if raise_on_error:
                    raise Exception(result.stderr.decode())
                else:
                    return None, result
            
            return (
                [ x
                  for line in result.stdout.decode().splitlines()
                  for x in (line.strip(),) # alias
                  if bool(x) # filter out empty lines
                ], 
                result
            )
from pathlib import Path

def test_celery():
    from commands import celery

    command = celery.Command(
        app="myapp",
        worker_name="myworker",
        log_level="INFO",
    )

    assert command.build() == ['celery', '-A', 'myapp', 'myworker', '--loglevel=INFO']

def test_pm2():
    from commands import pm2

    ecosystem = pm2.Ecosystem(
        apps=[
            pm2.App(
                script="myapp.py",
                name="myapp",
                cwd=".",
                args=["--port", "8000"],
                interpreter="python",
            )
        ]
    )

    command = pm2.Command().start(ecosystem='ecosystem.json')
    
    import platform

    cli = command.build()
    arg0 = cli[0]
    match platform.system():
        case 'Windows':
            assert arg0 in ('pm2.cmd', 'pm2')
        case 'Linux':
            assert arg0 in ('pm2', )

    assert cli == [arg0, 'start', str(Path('ecosystem.json').resolve())]

def test_uvicorn():
    from commands import uvicorn

    command = uvicorn.Command(
        app='foo.main:app',
        reload=True,
        port=8000,
    )

    assert command.build() == ['uvicorn', '--port', '8000', 'foo.main:app', '--reload']

def test_docker():
    from commands.docker import Command as docker

    docker_compose_up = docker().compose().up()
    docker_compose_down = docker().compose().down()

    assert docker_compose_up.build() == ['docker', 'compose', 'up']
    assert docker_compose_down.build() == ['docker', 'compose', 'down']

def test_uv():
    from commands import (
        uvicorn as uvicornModule
    )

    from commands.uv import Command as uv

    uvicorn = uvicornModule.Command(
        app='foo.main:app',
        reload=True,
        port=8000,
    )

    assert (
        uv().run(module=uvicorn).build()
         == ['uv', 'run', 'uvicorn', '--port', '8000', 'foo.main:app', '--reload']
    )


def test_find():
    from commands import find

    assert find.Command().build() == ['find']

    assert find.Command(
        path='/tmp',
        max_depth=1,
        name='*.py',
        action='print0',
    ).build() == ['find', '/tmp', '-maxdepth', '1', '-name', '*.py', '-print0']

    assert find.Command(path='.', action='delete').build() == ['find', '.', '-delete']

    assert find.Command(
        path='.',
        follow_symlinks='follow',
        file_type='file',
        empty=True,
    ).build() == ['find', '.', '-L', '-type', 'f', '-empty']

    assert find.Command(
        path='src',
        min_depth=1,
        max_depth=2,
        depth=True,
    ).build() == ['find', 'src', '-mindepth', '1', '-maxdepth', '2', '-depth']
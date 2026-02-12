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

    match platform.system():
        case 'Windows':
            arg0 = cli[0]
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
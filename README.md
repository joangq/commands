# Common CLI commands

### Usage

```python
from commands import uv, uvicorn

uvicorn_command = uvicorn.Command(
    app='foo.main:app',
    reload=True,
    port=8000,
)

command = uv.Command().run(module=uvicorn_command)

result: subprocess.CompletedProcess = command.run() 
# -> executes `uv run uvicorn --port 8000 foo.main:app --reload`
```
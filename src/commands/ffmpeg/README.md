# _ffmpeg_

### Usage

```python
from commands import ffmpeg
import tempfile
import pathlib

files = ['0.mp4', '2.mp4', '3.mp4']
tempfile = tempfile.NamedTemporaryFile(
    prefix='files',
    suffix='.txt',
    dir='.',
    delete=True
)

pathlib.Path(tempfile.name).write_text('\n'.join(
    f"file '{file}'" for file in files
))

command = ffmpeg.Command(
    format='concat',
    safe=0,
    infile=tempfile.name,
    codec_video='libx264',
    codec_audio='aac',
    outfile='output.mp4',
)

pathlib.Path('output.mp4').unlink(missing_ok=True)

import subprocess
with command.Popen(
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True, 
    bufsize=1
) as process:
    for line in process.stdout:
        print(line.strip())
    
    
    process.poll()
    
tempfile.close()
```
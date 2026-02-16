### Usage

```python
from commands import r
import re

class r_code(str): ...

code = r_code(
"""
library(dplyr)
table = tibble(x = 1:10)
table %>% head()
"""
)

command = r.Command(
    vanilla=True, 
    quiet=True,
    no_save=True,
    no_restore=True,
    execute=code
)

build = command.build()
CYAN_ASCII_CODE = '\033[96m'
GREEN_ASCII_CODE = '\033[92m'
RESET_ASCII_CODE = '\033[0m'
RED_ASCII_CODE = '\033[91m'
print(
    f'{CYAN_ASCII_CODE}>>>{RESET_ASCII_CODE}', 
    ' '.join(build[:-1]),
    f'{GREEN_ASCII_CODE}{build[-1]!r}{RESET_ASCII_CODE}',
)

execution_result = command.run()

if execution_result.returncode != 0:
    print(f'{RED_ASCII_CODE}Error: {execution_result.stderr.decode()}{RESET_ASCII_CODE}')
    exit(1)

raw_result = execution_result.stdout.decode()

result_lines = raw_result.splitlines()
result_lines = [
    x
    for line in result_lines
    for x in (line.strip(),)
    if len(x) > 0
    if len(re.sub('>\\s*', '', x)) > 0
]

[*map(print, result_lines)]
```
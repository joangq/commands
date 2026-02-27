from commands.docker import docker
from commands.docker.expression import is_not, value

command = docker().ps(all=True).filters(
    status = 'running', 
    name = is_not('backend'),
    pid =~ value('123')
)

print(command.build())
from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict

type AnyDict = dict # pyright: ignore[reportMissingTypeArgument]

class App(BaseModel):
    # General
    script: str
    name: None | str = None
    cwd: None | str = None
    args: None | str | list[str] = None
    interpreter: None | str = None
    interpreter_args: None | str | list[str] = None
    node_args: None | str | list[str] = None

    # Advanced features
    instances: None | int | Literal['max'] = None
    exec_mode: None | str = Field(
        default=None,
        description="fork | cluster | fork_mode | cluster_mode",
    )
    watch: None | bool | list[str] = None
    ignore_watch: None | list[str] | str = None
    max_memory_restart: None | int | str = None

    env: None | AnyDict = None
    appendEnvToName: None | bool = None
    source_map_support: None | bool = None
    instance_var: None | str = None
    filter_env: None | list[str] = None

    # Log files
    log_date_format: None | str = None
    error_file: None | str = None
    out_file: None | str = None
    log_file: None | str = None
    combine_logs: None | bool = None
    merge_logs: None | bool = None
    time: None | bool = None
    pid_file: None | str = None

    # Control flow
    min_uptime: None | int | str = None
    listen_timeout: None | int = None
    kill_timeout: None | int = None
    shutdown_with_message: None | bool = None
    wait_ready: None | bool = None
    max_restarts: None | int = None
    restart_delay: None | int = None
    autorestart: None | bool = None
    cron_restart: None | str = None
    vizion: None | bool = None
    post_update: None | list[str] = None
    force: None | bool = None

    # Allow env_production, env_staging, env_whatever, etc.
    model_config = ConfigDict(extra="allow")
    
    @classmethod
    def from_argbuild(cls, argbuild: list[str], **kwargs: Any):
        kwargs.setdefault('script', argbuild[0])
        kwargs.setdefault('args', ' '.join(argbuild[1:]))
        return cls.model_validate(kwargs)


class Ecosystem(BaseModel):
    apps: list[App]

    def to_javascript(self) -> str:
        return \
f"""\
module.exports = {self.model_dump_json(indent=2, exclude_none=True, exclude_unset=True)};
"""
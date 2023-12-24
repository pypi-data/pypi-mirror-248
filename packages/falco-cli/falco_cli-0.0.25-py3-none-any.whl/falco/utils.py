import importlib.util
import subprocess
from contextlib import contextmanager
from pathlib import Path

import cappa
import httpx
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

RICH_SUCCESS_MARKER = "[green]SUCCESS:"
RICH_ERROR_MARKER = "[red]ERROR:"
RICH_INFO_MARKER = "[blue]INFO:"
RICH_COMMAND_MARKER = "[yellow]"
RICH_COMMAND_MARKER_END = "[/yellow]"


def get_falco_blueprints_path() -> Path:
    package = importlib.util.find_spec("falco_blueprints")
    if package is None:
        raise cappa.Exit("The falco base install path could not be found.", code=1)
    return Path(package.origin).parent


def clean_project_name(val: str) -> str:
    return val.strip().replace(" ", "_").replace("-", "_")


def get_current_dir_as_project_name():
    current_dir = Path().resolve(strict=True).stem
    return clean_project_name(current_dir)


@contextmanager
def simple_progress(description: str, display_text="[progress.description]{task.description}"):
    progress = Progress(SpinnerColumn(), TextColumn(display_text), transient=True)
    progress.add_task(description=description, total=None)
    try:
        yield progress.start()
    finally:
        progress.stop()


@contextmanager
def network_request_with_progress(url: str, description: str):
    try:
        with simple_progress(description):
            yield httpx.get(url)
    except httpx.ConnectError as e:
        raise cappa.Exit(f"Connection error, {url} is not reachable.", code=1) from e


class ShellCommandError(Exception):
    pass


def run_shell_command(command: str, eval_result: bool = True):
    result = subprocess.run(
        ["python", "manage.py", "shell", "-c", command],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ShellCommandError(result.stderr)
    return eval(result.stdout) if eval_result else result.stdout

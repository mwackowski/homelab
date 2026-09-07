import os
import subprocess

from agent.models import ToolResult


def ping() -> str:
    ping_res = subprocess.run(
        ["ping", "-c", "4", os.environ["EDGE_SSH_HOST"]],
        capture_output=True,
        text=True,
        check=True,
    )
    print(ping_res.stdout)


def ssh() -> ToolResult:
    timeout = 15
    try:
        ssh_res = subprocess.run(
            [
                "ssh",
                "-i",
                os.environ["EDGE_SSH_KEY_PATH"],
                f"pi@{os.environ['EDGE_SSH_HOST']}",
                "docker ps --all",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        return ToolResult(success=True, output=ssh_res.stdout)
    except subprocess.TimeoutExpired:
        return ToolResult(success=False, error=f"SSH inspection timed out after {timeout} seconds")
    except subprocess.CalledProcessError as err:
        return ToolResult(success=False, error=err.stderr)

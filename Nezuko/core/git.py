import asyncio
import shlex
from typing import Tuple
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    REPO_LINK = config.UPSTREAM_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = config.UPSTREAM_REPO

    try:
        repo = Repo()
        LOGGER(__name__).info("Git Client Found [VPS DEPLOYER]")
    except (GitCommandError, InvalidGitRepositoryError):
        LOGGER(__name__).info("Initializing new repository...")
        repo = Repo.init()
        origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        branch = config.UPSTREAM_BRANCH
        if branch not in [ref.name for ref in origin.refs]:
            raise ValueError(f"Branch {branch} does not exist in the upstream repository.")
        repo.create_head(branch, origin.refs[branch])
        repo.heads[branch].set_tracking_branch(origin.refs[branch])
        repo.heads[branch].checkout()

        # Fetch updates
        LOGGER(__name__).info("Fetching updates from upstream repository...")
        origin.fetch(branch)
        try:
            origin.pull(branch)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")

        install_req("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER(__name__).info("Repository setup completed.")

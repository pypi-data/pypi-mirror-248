import subprocess
from packaging.version import Version
from pathlib import Path


plugins = [
    "cell",
    "console",
    "editors",
    "file_browser",
    "image_viewer",
    "jpterm",
    "kernel",
    "local_contents",
    "local_terminals",
    "local_kernels",
    "notebook_editor",
    "remote_contents",
    "remote_terminals",
    "remote_kernels",
    "text_editor",
    "markdown_viewer",
    "terminal",
    "launcher",
    "widgets",
]


def run(cmd: str, cwd: str | None = None) -> list[str]:
    res = subprocess.run(cmd.split(), capture_output=True, cwd=cwd)
    return res.stdout.decode().splitlines()


def get_last_tag() -> str:
    res = run("git describe --tags --abbrev=0")
    return res[0]


def get_changed_files_since_tag(tag: str):
    res = run(f"git diff --name-only HEAD {tag}")
    return res


def get_last_release_tag() -> str:
    res = run("git tag")
    for tag in res[::-1]:
        if tag[0] == "v" and tag[1].isdigit():
            return tag
    raise RuntimeError("No release tag found")

def get_changed_files_since_last_release() -> list[str]:
    tag = get_last_release_tag()
    return get_changed_files_since_tag(tag)


def get_plugins_to_release():
    subdir = "plugins/"
    subdir_len = len(subdir)
    changed_files = get_changed_files_since_last_release()
    plugins = []
    for path in changed_files:
        if path.startswith(subdir):
            name = path[subdir_len:]
            name = name[:name.find("/")]
            plugins.append(name)
    return plugins


def get_version(path: str) -> str:
    p = Path(path)
    content = p.read_text()
    version_var = "__version__"
    if version_var not in content:
        raise RuntimeError(f"File doesn't set a version: {path}")
    i0 = content.find(version_var) + len(version_var)
    i1 = i0 + content[i0:].find('"') + 1
    i2 = i1 + content[i1:].find('"')
    return content[i1:i2]


def set_version(path: str, version: str) -> None:
    p = Path(path)
    content = p.read_text()
    version_var = "__version__"
    if version_var not in content:
        raise RuntimeError(f"File doesn't set a version: {path}")
    i0 = content.find(version_var) + len(version_var)
    i1 = i0 + content[i0:].find('"') + 1
    i2 = i1 + content[i1:].find('"')
    content = content[:i1] + version + content[i2:]
    p.write_text(content)


def increment_version(path: str) -> None:
    version = Version(get_version(path))
    next_micro = version.micro + 1
    next_version = f"{version.major}.{version.minor}.{micro}"
    set_version(path, next_version)


def build(path: str) -> None:
    p = Path(path)
    run("rm -rf dist", cwd=str(p))
    run("hatch build", cwd=str(p))


def publish(path: str) -> None:
    p = Path(path)
    run("hatch publish", cwd=str(p))


#print(get_plugins_to_release())

#for plugin in plugins:
#    set_version(f"plugins/{plugin}/txl_{plugin}/__init__.py", "0.2.4")
#    build(f"plugins/{plugin}")
#    publish(f"plugins/{plugin}")

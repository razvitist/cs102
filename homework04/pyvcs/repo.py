import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    gitdir = ".git"
    dir = pathlib.Path("")
    workdir = pathlib.Path(workdir)
    if not workdir.parents or pathlib.Path.exists(workdir / gitdir):
        if not pathlib.Path.exists(workdir / gitdir):
            raise Exception("Not a git repository")
        return workdir.absolute() / gitdir
    else:
        for path in workdir.parents:
            if gitdir in str(path) or pathlib.Path.exists(path / gitdir):
                dir = path
    return dir / gitdir


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    try:
        if pathlib.Path(workdir).is_file():
            raise Exception(f"{workdir} is not a directory")
    except AttributeError:
        workdir = pathlib.Path(workdir)
    try:
        gitdir = os.environ["GIT_DIR"] if os.environ["GIT_DIR"] else ".git"
    except:
        gitdir = ".git"
    dir = pathlib.Path(workdir) / gitdir
    dir.mkdir()
    for i in ("refs", "refs/heads", "refs/tags", "objects"):
        (dir / i).mkdir()
    for i in (("HEAD", "ref: refs/heads/master\n"), ("config", "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"), ("description", "Unnamed pyvcs repository.\n")):
        (dir / i[0]).write_text(i[1])
    return dir

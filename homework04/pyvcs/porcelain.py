import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_tree_files, read_object
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    return commit_tree(
        gitdir=gitdir, tree=write_tree(gitdir, read_index(gitdir)), message=message, author=author
    )


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    head = gitdir / "refs" / "heads" / obj_name
    if head.exists():
        with head.open() as f:
            obj_name = f.read()
    for file in read_index(gitdir):
        if pathlib.Path(file.name).is_file():
            if "/" in file.name:
                shutil.rmtree(file.name[: file.name.find("/")])
            else:
                os.chmod(file.name, 0o777)
                os.remove(file.name)
    with (gitdir / "objects" / obj_name[:2] / obj_name[2:]).open("rb") as f1:
        for f in find_tree_files(commit_parse(f1.read()).decode(), gitdir):
            if "/" in f[0]:
                dir_name = f[0][: f[0].find("/")]
                pathlib.Path(dir_name).absolute().mkdir()
            with open(f[0], "w") as f2:
                _, content = read_object(f[1], gitdir)
                f2.write(content.decode())

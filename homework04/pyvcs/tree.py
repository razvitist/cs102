import os
import pathlib
import time
import typing as tp

from pyvcs.index import GitIndexEntry
from pyvcs.objects import hash_object


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    note = b""
    for file in index:
        if "/" in file.name:
            note += b"40000 "
            subdir_files = b""
            note += file.name[: file.name.find("/")].encode() + b"\0"
            subdir_files += (
                oct(file.mode)[2:].encode()
                + b" "
                + file.name[file.name.find("/") + 1 :].encode()
                + b"\0" 
                + file.sha1
            )
            note += bytes.fromhex(hash_object(subdir_files, fmt="tree", write=True))
        else:
            note += oct(file.mode)[2:].encode() + b" " + file.name.encode() + b"\0" + file.sha1
    return hash_object(note, fmt="tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if "GIT_DIR" not in os.environ:
        os.environ["GIT_DIR"] = ".git"
    if not author:
        author = f"{os.environ['GIT_AUTHOR_NAME']} <{os.environ['GIT_AUTHOR_EMAIL']}>"
    utc = -time.timezone
    t = "{} {}{:02}{:02}".format(
        int(time.mktime(time.localtime())),
        "+" if utc > 0 else "-",
        abs(utc) // 3600,
        (abs(utc) // 60) % 60,
    )
    x = f"tree {tree}\n"
    if parent:
        x += f"parent {parent}\n"
    x += f"author {author} {t}\ncommitter {author} {t}\n\n{message}\n"
    return hash_object(x.encode("ascii"), "commit", True)

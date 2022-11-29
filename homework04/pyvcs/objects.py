# mypy: ignore-errors

import hashlib
import pathlib
import typing as tp
import zlib

from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    store = f"{fmt} {len(data)}\0".encode() + data
    hash = hashlib.sha1(store).hexdigest()
    if write:
        path = repo_find(".") / "objects"
        if not pathlib.Path.exists(path / hash[:2]):
            (path / hash[:2]).mkdir()
        if not pathlib.Path.exists(path / hash[:2] / hash[2:]):
            (path / f"{hash[:2]}/{hash[2:]}").write_bytes(zlib.compress(store))
    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    objs: tp.List[str] = []
    if len(obj_name) > 40 or len(obj_name) < 4:
        raise Exception(f"Not a valid object name {obj_name}")
    for obj in (gitdir / "objects" / obj_name[:2]).iterdir():
        objs.append(str(find_object(obj_name, obj)))
    if not objs or objs[0] == "None":
        raise Exception(f"Not a valid object name {obj_name}")
    return objs


def find_object(obj_name: str, gitdir: pathlib.Path) -> str | None:
    if obj_name[2:] in gitdir.parts[-1]:
        return str(gitdir.parts[-2] + str(gitdir.parts[-1]))


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    with open(gitdir / "objects" / sha[:2] / sha[2:], "rb") as f:
        blob = zlib.decompress(f.read())
    s = blob.find(b"\x00")
    fmt = blob[:s]
    return fmt[: fmt.find(b" ")].decode(), blob[(s + 1) :]


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    r = []
    while len(data) != 0:
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        r.append((mode, name, sha))
    return r


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(pathlib.Path("."))
    for obj in resolve_object(obj_name, gitdir):
        head, content = read_object(obj, gitdir)
        if head == "tree":
            r = ""
            for f in read_tree(content):
                r += (
                    str(f[0]).zfill(6)
                    + " "
                    + read_object(f[2], repo_find())[0]
                    + " "
                    + f[2]
                    + "\t"
                    + f[1]
                    + "\n"
                )
            print(r)
        else:
            print(content.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    r = []
    data = read_object(tree_sha, gitdir)[1]
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            for blob in find_tree_files(f[2], gitdir):
                name = f[1] + "/" + blob[0]
                r.append((name, blob[1]))
        else:
            r.append((f[1], f[2]))
    return r


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    return data[data.find(b"tree") + 5 : data.find(b"tree") + 45]

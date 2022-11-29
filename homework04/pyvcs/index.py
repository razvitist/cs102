import hashlib
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        return struct.pack(
            f">10i20sh{len(self.name)}s3x", 
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode()
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        x = list(struct.unpack(f">10i20sh{len(data) - 62}s", data))
        x[-1] = x[-1][:-3].decode()
        return GitIndexEntry(*x)


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    i: tp.List[GitIndexEntry] = []
    try:
        with open(gitdir / "index", "rb") as f:
            data = f.read()
    except:
        return i
    content = data[12:-20]
    c = 0
    for _ in range(int.from_bytes(data[8:12], "big")):
        len_s = c + 62
        len_e = content[len_s:].find(b"\x00\x00\x00") + len_s + 3
        i.append(GitIndexEntry.unpack(content[c:len_e]))
        c = len_e
    return i


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    with open(gitdir / "index", "wb") as f:
        hash = struct.pack(">4s2i", *(b"DIRC", 2, len(entries)))
        f.write(hash)
        for file in entries:
            f.write(file.pack())
            hash += file.pack()
        nhash = str(hashlib.sha1(hash).hexdigest())
        f.write(struct.pack(f">{len(bytearray.fromhex(nhash))}s", bytearray.fromhex(nhash)))


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    for f in read_index(gitdir):
        print(f"{str(oct(f.mode))[2:]} {f.sha1.hex()} 0	{f.name}" if details else f.name)


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    files = []
    for file in paths:
        stat = os.stat(file)
        files.append(
            GitIndexEntry(
                ctime_s=int(stat.st_ctime),
                ctime_n=0,
                mtime_s=int(stat.st_mtime),
                mtime_n=0,
                dev=stat.st_dev,
                ino=stat.st_ino,
                mode=stat.st_mode,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                sha1=bytes.fromhex(hash_object(file.open().read().encode(), "blob", True)),
                flags=7,
                name=str(file).replace("\\", "/"),
            )
        )
    write_index(gitdir, read_index(gitdir) + sorted(files, key=lambda x: x.name))

# mypy: ignore-errors

import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    with (gitdir / pathlib.Path(ref)).open("w") as f:
        f.write(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    if ref_resolve(gitdir, ref) is None:
        return
    with (gitdir / name).open("w") as f:
        f.write(f"ref: {ref}")


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str | None:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    path = gitdir / refname
    if not path.exists():
        return
    with path.open() as f:
        return f.read()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    with (gitdir / "HEAD").open() as f:
        return str(f.read()).find("ref") == -1


def get_ref(gitdir: pathlib.Path) -> str:
    with (gitdir / "HEAD").open() as f:
        x = f.read()
    return x[x.find(" ") + 1 :].strip()

# mypy: ignore-errors

import dataclasses
import math
import time
import typing as tp

from vkapi import session
from vkapi.config import VK_CONFIG

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    return FriendsResponse(**session.get(
        "friends.get",
        user_id=user_id,
        count=count,
        offset=offset,
        fields=fields,
        ).json()["response"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    params = {
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": offset,
        "progress": progress,
    }
    nreq = 1
    if target_uids:
        nreq = math.ceil(len(target_uids) / VK_CONFIG["target_limit"])
    m = []
    for _ in range(nreq):
        m.extend(session.get("friends.getMutual", **params).json()["response"])
        params["offset"] += VK_CONFIG["target_limit"]
        time.sleep(0.3)
    return m

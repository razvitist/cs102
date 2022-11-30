# mypy: ignore-errors

import math
import time
import typing as tp

import pandas as pd
from vkapi import config, session
from vkapi.exceptions import APIError


def get_posts_2500(count: int = 2500, **kwargs: tp.Any) -> tp.List[tp.Dict[str, tp.Any]]:
    kwargs["count"] = str(count)
    code = (
    """
        let m = []
        let i = 0
        while (i < 25) {
            m.push(API.wall.get(%s).m)
            i++
        }
        return m
    """
        % kwargs
    )
    return session.post(
        "execute",
        access_token=config.VK_CONFIG["access_token"],
        v=config.VK_CONFIG["version"],
        code=code,
    ).json()["response"]["items"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    data = []
    while count > 0:
        posts_list = get_posts_2500(
            count=count,
            owner_id=owner_id,
            domain=domain,
            offset=offset,
            filter=filter,
            extended=extended,
            fields=fields,
        )
        data += posts_list
        if count >= max_count:
            count -= 2500
        else:
            break
        time.sleep(1)
    return pd.json_normalize(data)

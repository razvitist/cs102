import datetime as dt
import re
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    cur_year = dt.datetime.now().year
    ages = []
    for i in get_friends(user_id).items:
        bdate = i.get("bdate")
        if bdate and re.search(r"\d{4}", bdate):
            ages.append(cur_year - int(bdate.split(".")[-1]))
    if ages:
        return statistics.median(ages)

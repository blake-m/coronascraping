import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp


def date_to_month_day_format(date_: Timestamp):
    date = pd.to_datetime(date_)
    return f"{date.month_name()[:3]} {date.day}"


def date_to_day_month_year_format(date_: Timestamp):
    date = pd.to_datetime(date_)
    return f"{date.day} {date.month_name()[:3]} {date.year}"


def correct_country_name(country: str) -> str:
    if country in ["uk", "us"]:
        return country.upper()
    else:
        name_parts = country.split("_")
        name_parts = [
            part.capitalize() if part not in ["the", "and", "of"] else part
            for part in name_parts
        ]
        return " ".join(name_parts)

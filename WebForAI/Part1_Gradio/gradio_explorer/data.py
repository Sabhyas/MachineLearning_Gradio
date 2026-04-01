from __future__ import annotations

import calendar
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .config import DEFAULT_DATA_CANDIDATES


def _resolve_data_path() -> Path:
    for raw_candidate in DEFAULT_DATA_CANDIDATES:
        candidate = Path(raw_candidate)
        if candidate.is_file():
            return candidate
        if candidate.is_dir():
            preferred = candidate / "data.csv"
            if preferred.is_file():
                return preferred

            csv_files = sorted(candidate.glob("*.csv"))
            if csv_files:
                return csv_files[0]
    checked = ", ".join(str(path) for path in DEFAULT_DATA_CANDIDATES)
    raise FileNotFoundError(f"No CSV found. Checked: {checked}")



def load_data() -> tuple[pd.DataFrame, Path]:
    data_path = _resolve_data_path()
    df = pd.read_csv(data_path, low_memory=False)
    unnamed_columns = [column for column in df.columns if str(column).startswith("Unnamed:")]
    if unnamed_columns:
        df = df.drop(columns=unnamed_columns)

    for column in ["started_at", "ended_at", "date"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    if "route" not in df.columns and {
        "start_station_name",
        "end_station_name",
    }.issubset(df.columns):
        start_names = df["start_station_name"].fillna("Unknown start")
        end_names = df["end_station_name"].fillna("Unknown end")
        df["route"] = start_names.astype(str) + " -> " + end_names.astype(str)

    return df, data_path


@dataclass(frozen=True)
class FilterOptions:
    member_choices: list[str]
    bike_choices: list[str]
    season_choices: list[str]
    month_choices: list[str]


def build_filter_options(df: pd.DataFrame) -> FilterOptions:
    member = sorted(x for x in df["member_casual"].dropna().unique().tolist())
    bikes = sorted(x for x in df["rideable_type"].dropna().unique().tolist())
    seasons = ["Winter", "Spring", "Summer", "Fall"]
    months = ["All months", *calendar.month_name[1:]]
    return FilterOptions(
        member_choices=["All", *member],
        bike_choices=["All", *bikes],
        season_choices=["All", *seasons],
        month_choices=months,
    )


def apply_filters(
    df: pd.DataFrame,
    member: str,
    rideable: str,
    season: str,
    month: str,
    *,
    apply_month: bool = True,
) -> pd.DataFrame:
    out = df
    if member != "All":
        out = out[out["member_casual"] == member]
    if rideable != "All":
        out = out[out["rideable_type"] == rideable]
    if season != "All":
        out = out[out["season"] == season]
    if apply_month and month != "All months":
        month_number = list(calendar.month_name).index(month)
        out = out[out["month"] == month_number]
    return out


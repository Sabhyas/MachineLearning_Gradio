"""All view logic: summaries, tables, and plot builders."""

from __future__ import annotations

import html
import re
from typing import Callable

import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import HeatMap

from .config import (
    DAYS_ORDER,
    DEFAULT_GEO_MAX_POINTS,
    DEFAULT_GEO_RANDOM_SEED,
    DEFAULT_GEO_STATION_MARKERS,
    DEFAULT_ROUTES_TOP_N,
    DEFAULT_SAMPLE_TABLE_ROWS,
    DEFAULT_STATION_HEATMAP_TOP_N,
    DEFAULT_STATIONS_TOP_N,
    MONTH_LABELS,
)
from .data import apply_filters


def empty_figure(title: str = "No data for selected filters") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(title=title)
    return fig


def empty_html(message: str = "No data for selected filters") -> str:
    return (
        "<div style='height: 560px; display: flex; align-items: center; "
        "justify-content: center; border: 1px solid #ddd; border-radius: 8px; "
        "background: #fafafa; color: #444; font-size: 16px;'>"
        f"{html.escape(message)}"
        "</div>"
    )


def _wrap_map_html(map_html: str) -> str:
    escaped_html = html.escape(map_html, quote=True)
    return (
        "<iframe "
        f"srcdoc=\"{escaped_html}\" "
        "width='100%' height='560' style='border: none; border-radius: 8px;'></iframe>"
    )


def make_summary_view(df: pd.DataFrame) -> Callable[[str, str, str, str], str]:
    def _summary(member: str, rideable: str, season: str, month: str) -> str:
        data = apply_filters(df, member, rideable, season, month)
        if data.empty:
            return "No rows match the selected filters."
        median_duration = data["trip_duration_min"].median()
        electric_share = 100 * (data["rideable_type"] == "electric_bike").mean()
        member_share = 100 * (data["member_casual"] == "member").mean()
        return (
            f"**Trips:** {len(data):,}  \n"
            f"**Median trip duration:** {median_duration:.1f} min  \n"
            f"**Electric bike share:** {electric_share:.1f}%  \n"
            f"**Member share:** {member_share:.1f}%"
        )

    return _summary


def make_duration_histogram(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _hist(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        data = data[data["trip_duration_min"].between(1, 60, inclusive="both")]
        if data.empty:
            return empty_figure("No trips in 1-60 minute range")

        fig = go.Figure()
        for rider_type in ["member", "casual"]:
            subset = data[data["member_casual"] == rider_type]["trip_duration_min"]
            if subset.empty:
                continue
            fig.add_trace(
                go.Histogram(
                    x=subset,
                    name=rider_type,
                    opacity=0.6,
                    nbinsx=50,
                )
            )
        fig.update_layout(
            title="Trip duration distribution (1-60 min)",
            barmode="overlay",
            xaxis_title="Minutes",
            yaxis_title="Trips",
            legend_title_text="Rider type",
        )
        return fig

    return _hist


def make_member_mix_pie(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _member_mix(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        counts = data["member_casual"].value_counts().reindex(["casual", "member"], fill_value=0)
        if counts.sum() == 0:
            return empty_figure()
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Casual", "Member"],
                    values=counts.values,
                    hole=0.35,
                )
            ]
        )
        fig.update_layout(title="Casual vs member riders")
        return fig

    return _member_mix


def make_bike_mix_pie(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _bike_mix(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        counts = data["rideable_type"].value_counts().reindex(
            ["classic_bike", "electric_bike"],
            fill_value=0,
        )
        if counts.sum() == 0:
            return empty_figure()
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Classic bike", "Electric bike"],
                    values=counts.values,
                    hole=0.35,
                )
            ]
        )
        fig.update_layout(title="Classic vs electric bikes")
        return fig

    return _bike_mix


def make_overview_table(df: pd.DataFrame) -> Callable[[], pd.DataFrame]:
    def _table() -> pd.DataFrame:
        data = df
        columns = [
            "started_at",
            "rideable_type",
            "trip_duration_min",
            "start_station_name",
            "end_station_name",
            "member_casual",
        ]
        out = data[columns].head(DEFAULT_SAMPLE_TABLE_ROWS).copy()
        out["started_at"] = out["started_at"].dt.strftime("%Y-%m-%d %H:%M")
        out["trip_duration_min"] = out["trip_duration_min"].round(2)
        return out

    return _table


def make_monthly_line(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _monthly(member: str, rideable: str, season: str, month: str) -> go.Figure:
        # Keeps month profile visible while applying rider, bike, and season.
        data = apply_filters(df, member, rideable, season, month, apply_month=False)
        if data.empty:
            return empty_figure()
        by_month = data.groupby("month").size().reindex(range(1, 13), fill_value=0)
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=MONTH_LABELS,
                    y=by_month.values,
                    mode="lines+markers",
                    name="Trips",
                )
            ]
        )
        fig.update_layout(title="Trips by month", xaxis_title="Month", yaxis_title="Trips")
        return fig

    return _monthly


def make_hourly_bar(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _hourly(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        if data.empty:
            return empty_figure()
        by_hour = data.groupby("hour").size().reindex(range(24), fill_value=0)
        fig = go.Figure(data=[go.Bar(x=list(range(24)), y=by_hour.values)])
        fig.update_layout(title="Trips by start hour", xaxis_title="Hour", yaxis_title="Trips")
        fig.update_xaxes(dtick=1)
        return fig

    return _hourly


def make_weekday_hour_heatmap(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _heatmap(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        if data.empty:
            return empty_figure()
        grouped = data.groupby(["dayofweek", "hour"]).size().unstack(fill_value=0)
        grouped = grouped.reindex([day for day in DAYS_ORDER if day in grouped.index], fill_value=0)
        fig = go.Figure(
            data=[
                go.Heatmap(
                    z=grouped.values,
                    x=[str(x) for x in grouped.columns.tolist()],
                    y=grouped.index.tolist(),
                    colorscale="Viridis",
                    colorbar={"title": "Trips"},
                )
            ]
        )
        fig.update_layout(title="Weekday x hour demand heatmap", xaxis_title="Hour", yaxis_title="Weekday")
        return fig

    return _heatmap


def make_stations_bar(df: pd.DataFrame) -> Callable[[str, str, str, str, str], go.Figure]:
    def _stations(member: str, rideable: str, season: str, month: str, role: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        if data.empty:
            return empty_figure()
        station_col = "start_station_name" if role == "Trip starts" else "end_station_name"
        top_n = DEFAULT_STATIONS_TOP_N
        top = data[station_col].value_counts().head(top_n).sort_values(ascending=True)
        fig = go.Figure(data=[go.Bar(x=top.values, y=top.index.astype(str).tolist(), orientation="h")])
        fig.update_layout(
            title=f"Top {top_n} stations by {role.lower()}",
            xaxis_title="Trips",
            yaxis_title="Station",
            height=max(400, top_n * 28),
        )
        return fig

    return _stations


def make_station_usage_heatmap(df: pd.DataFrame) -> Callable[[str, str, str, str, str], go.Figure]:
    def _station_heatmap(member: str, rideable: str, season: str, month: str, role: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        if data.empty:
            return empty_figure()
        station_col = "start_station_name" if role == "Trip starts" else "end_station_name"
        data = data.dropna(subset=[station_col, "hour"])
        if data.empty:
            return empty_figure()

        top_stations = data[station_col].value_counts().head(DEFAULT_STATION_HEATMAP_TOP_N).index.tolist()
        heatmap_data = (
            data[data[station_col].isin(top_stations)]
            .groupby([station_col, "hour"])
            .size()
            .unstack(fill_value=0)
            .reindex(index=top_stations, columns=range(24), fill_value=0)
        )
        fig = go.Figure(
            data=[
                go.Heatmap(
                    z=heatmap_data.values,
                    x=[str(hour) for hour in heatmap_data.columns.tolist()],
                    y=heatmap_data.index.astype(str).tolist(),
                    colorscale="Viridis",
                    colorbar={"title": "Trips"},
                )
            ]
        )
        fig.update_layout(
            title=f"Bike usage: top {DEFAULT_STATION_HEATMAP_TOP_N} stations",
            xaxis_title="Hour",
            yaxis_title="Station",
            height=max(420, DEFAULT_STATION_HEATMAP_TOP_N * 34),
        )
        return fig

    return _station_heatmap


def _sort_interval_labels(labels: list[str]) -> list[str]:
    def _lower_bound(label: str) -> float:
        match = re.match(r"^\(([-\d.]+),\s*([-\d.]+)\]$", str(label))
        if not match:
            return float("inf")
        return float(match.group(1))

    return sorted(labels, key=_lower_bound)


def make_temperature_hour_heatmap(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _temperature_heatmap(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        data = data.dropna(subset=["hour", "tempbin"])
        if data.empty:
            return empty_figure()

        tempbin_order = _sort_interval_labels(data["tempbin"].astype(str).dropna().unique().tolist())
        heatmap_data = (
            data.assign(tempbin=data["tempbin"].astype(str))
            .groupby(["hour", "tempbin"])
            .size()
            .unstack(fill_value=0)
            .reindex(index=range(24), columns=tempbin_order, fill_value=0)
        )
        fig = go.Figure(
            data=[
                go.Heatmap(
                    z=heatmap_data.values,
                    x=heatmap_data.columns.tolist(),
                    y=[str(hour) for hour in heatmap_data.index.tolist()],
                    colorscale="Viridis",
                    colorbar={"title": "Trips"},
                )
            ]
        )
        fig.update_layout(
            title="Bike usage by temperature and hour",
            xaxis_title="Temperature bin",
            yaxis_title="Hour",
        )
        return fig

    return _temperature_heatmap


def make_windspeed_usage_line(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _windspeed_line(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        data = data.dropna(subset=["windspeed"])
        if data.empty:
            return empty_figure()

        windspeed_usage = (
            data.groupby("windspeed")
            .size()
            .reset_index(name="ride_count")
            .sort_values("windspeed")
        )
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=windspeed_usage["windspeed"],
                    y=windspeed_usage["ride_count"],
                    mode="lines+markers",
                    name="Trips",
                )
            ]
        )
        fig.update_layout(
            title="Number of rides vs windspeed",
            xaxis_title="Windspeed (km/h)",
            yaxis_title="Trips",
        )
        return fig

    return _windspeed_line


def make_rain_hour_heatmap(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _rain_heatmap(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        data = data.dropna(subset=["hour", "rain_bin"])
        if data.empty:
            return empty_figure()

        rain_order = ["No Rain", "Light", "Moderate", "Heavy"]
        heatmap_data = (
            data.assign(rain_bin=data["rain_bin"].astype(str))
            .groupby(["hour", "rain_bin"])
            .size()
            .unstack(fill_value=0)
            .reindex(index=range(24), columns=rain_order, fill_value=0)
        )
        fig = go.Figure(
            data=[
                go.Heatmap(
                    z=heatmap_data.values,
                    x=heatmap_data.columns.tolist(),
                    y=[str(hour) for hour in heatmap_data.index.tolist()],
                    colorscale="Blues",
                    colorbar={"title": "Trips"},
                )
            ]
        )
        fig.update_layout(
            title="Bike usage: hour vs rain intensity",
            xaxis_title="Rain intensity",
            yaxis_title="Hour",
        )
        return fig

    return _rain_heatmap


def make_routes_bar(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _routes(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        data = data[data["start_station_name"] != data["end_station_name"]]
        if data.empty:
            return empty_figure()
        top_n = DEFAULT_ROUTES_TOP_N
        top = data["route"].value_counts().head(top_n).sort_values(ascending=True)
        labels = [(name[:70] + "...") if len(name) > 73 else name for name in top.index.astype(str).tolist()]
        fig = go.Figure(data=[go.Bar(x=top.values, y=labels, orientation="h")])
        fig.update_layout(
            title=f"Top {top_n} routes (excluding same start/end station)",
            xaxis_title="Trips",
            yaxis_title="Route",
            height=max(420, top_n * 24),
        )
        return fig

    return _routes


def make_geo_map(df: pd.DataFrame) -> Callable[[str, str, str, str, str], str]:
    def _geo(
        member: str,
        rideable: str,
        season: str,
        month: str,
        focus: str,
    ) -> str:
        data = apply_filters(df, member, rideable, season, month)
        data = data.dropna(subset=["start_lat", "start_lng", "end_lat", "end_lng"])
        if data.empty:
            return empty_html()

        lat_col = "start_lat" if focus == "Trip starts" else "end_lat"
        lng_col = "start_lng" if focus == "Trip starts" else "end_lng"
        station_col = "start_station_name" if focus == "Trip starts" else "end_station_name"
        title = f"{focus} heatmap ({min(DEFAULT_GEO_MAX_POINTS, len(data)):,} sampled trips)"
        n_points = min(DEFAULT_GEO_MAX_POINTS, len(data))
        if n_points < len(data):
            data = data.sample(n=n_points, random_state=DEFAULT_GEO_RANDOM_SEED)

        coords = data[[lat_col, lng_col]].astype(float)
        center = [coords[lat_col].mean(), coords[lng_col].mean()]
        fmap = folium.Map(location=center, zoom_start=11, tiles="CartoDB positron", control_scale=True)
        HeatMap(
            coords.values.tolist(),
            radius=14,
            blur=18,
            min_opacity=0.25,
        ).add_to(fmap)
        station_points = (
            data[[station_col, lat_col, lng_col]]
            .dropna(subset=[station_col, lat_col, lng_col])
            .groupby(station_col)
            .agg(
                trip_count=(station_col, "size"),
                lat=(lat_col, "mean"),
                lng=(lng_col, "mean"),
            )
            .sort_values("trip_count", ascending=False)
            .head(DEFAULT_GEO_STATION_MARKERS)
            .reset_index()
        )
        max_station_count = max(int(station_points["trip_count"].max()), 1) if not station_points.empty else 1
        for station in station_points.itertuples(index=False):
            radius = 4 + (8 * int(station.trip_count) / max_station_count)
            popup = (
                f"<strong>{html.escape(str(getattr(station, station_col)))}</strong><br>"
                f"Trips in sample: {int(station.trip_count):,}"
            )
            folium.CircleMarker(
                location=[float(station.lat), float(station.lng)],
                radius=radius,
                color="#1d4ed8",
                weight=1,
                fill=True,
                fill_color="#2563eb",
                fill_opacity=0.8,
                popup=popup,
                tooltip=str(getattr(station, station_col)),
            ).add_to(fmap)
        folium.Marker(
            location=center,
            icon=folium.DivIcon(
                html=(
                    "<div style='background: rgba(255,255,255,0.9); padding: 8px 12px; "
                    "border: 1px solid #bbb; border-radius: 6px; font-size: 13px; "
                    "font-weight: 600; white-space: nowrap;'>"
                    f"{html.escape(title)}"
                    "</div>"
                )
            ),
        ).add_to(fmap)
        fmap.fit_bounds(
            [
                [coords[lat_col].min(), coords[lng_col].min()],
                [coords[lat_col].max(), coords[lng_col].max()],
            ]
        )
        return _wrap_map_html(fmap.get_root().render())

    return _geo


def make_duration_by_group(df: pd.DataFrame) -> Callable[[str, str, str, str], go.Figure]:
    def _duration_mix(member: str, rideable: str, season: str, month: str) -> go.Figure:
        data = apply_filters(df, member, rideable, season, month)
        data = data[data["trip_duration_min"].between(1, 60, inclusive="both")]
        if data.empty:
            return empty_figure()
        if len(data) > 12_000:
            data = data.sample(n=12_000, random_state=42)
        fig = px.box(
            data,
            x="member_casual",
            y="trip_duration_min",
            color="rideable_type",
            labels={"member_casual": "Rider type", "trip_duration_min": "Minutes"},
            title="Trip duration by rider and bike type",
        )
        return fig

    return _duration_mix


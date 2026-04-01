"""Gradio UI assembly and event wiring."""

from __future__ import annotations

from typing import Sequence

import gradio as gr

from .data import build_filter_options, load_data
from .views import (
    make_bike_mix_pie,
    make_duration_by_group,
    make_duration_histogram,
    make_geo_map,
    make_hourly_bar,
    make_member_mix_pie,
    make_monthly_line,
    make_overview_table,
    make_rain_hour_heatmap,
    make_routes_bar,
    make_stations_bar,
    make_station_usage_heatmap,
    make_summary_view,
    make_temperature_hour_heatmap,
    make_weekday_hour_heatmap,
    make_windspeed_usage_line,
)


def _bind_to_all_changes(
    controls: Sequence[gr.Component],
    *,
    fn,
    inputs: Sequence[gr.Component],
    outputs,
) -> None:
    for control in controls:
        control.change(fn=fn, inputs=list(inputs), outputs=outputs)


def build_app() -> gr.Blocks:
    df, data_path = load_data()
    options = build_filter_options(df)

    summary_view = make_summary_view(df)
    member_mix_pie = make_member_mix_pie(df)
    bike_mix_pie = make_bike_mix_pie(df)
    duration_hist = make_duration_histogram(df)
    overview_table = make_overview_table(df)
    monthly_line = make_monthly_line(df)
    hourly_bar = make_hourly_bar(df)
    heatmap = make_weekday_hour_heatmap(df)
    stations_bar = make_stations_bar(df)
    station_usage_heatmap = make_station_usage_heatmap(df)
    temperature_hour_heatmap = make_temperature_hour_heatmap(df)
    windspeed_usage_line = make_windspeed_usage_line(df)
    rain_hour_heatmap = make_rain_hour_heatmap(df)
    routes_bar = make_routes_bar(df)
    geo_map = make_geo_map(df)
    duration_mix = make_duration_by_group(df)

    with gr.Blocks(title="PXL Pedals Data Explorer") as demo:
        gr.Markdown("# PXL Pedals - Interactive Explorer")
        gr.Markdown(
            f"Use the global filters to explore all tabs. <br>Loaded dataset: `{data_path.name}`. Loaded {len(df)} rides."
        )

        with gr.Row():
            member_dd = gr.Dropdown(
                choices=options.member_choices,
                value="All",
                label="Rider type",
            )
            bike_dd = gr.Dropdown(
                choices=options.bike_choices,
                value="All",
                label="Bike type",
            )
            season_dd = gr.Dropdown(
                choices=options.season_choices,
                value="All",
                label="Season",
            )
            month_dd = gr.Dropdown(
                choices=options.month_choices,
                value="All months",
                label="Month",
            )

        global_inputs = [member_dd, bike_dd, season_dd, month_dd]

        with gr.Tabs():
            with gr.Tab("Overview"):
                summary_md = gr.Markdown()
                with gr.Row():
                    member_mix_plot = gr.Plot(label="Casual vs member riders")
                    bike_mix_plot = gr.Plot(label="Classic vs electric bikes")
                with gr.Row():
                    duration_plot = gr.Plot(label="Duration histogram")
                    month_plot = gr.Plot(label="Month trend")

            with gr.Tab("Explore Dataset"):
                sample_table = gr.Dataframe(label="Trip sample", interactive=True)

            with gr.Tab("Time patterns"):
                gr.Markdown("Trips by hour and demand heatmap across weekdays and hours.")
                hourly_plot = gr.Plot(label="Trips by hour")
                heatmap_plot = gr.Plot(label="Weekday x hour heatmap")

            with gr.Tab("Stations"):
                gr.Markdown("Top stations by starts or ends.")
                station_role = gr.Radio(
                    choices=["Trip starts", "Trip ends"],
                    value="Trip starts",
                    label="Perspective",
                )
                with gr.Row():
                    stations_plot = gr.Plot(label="Stations ranking")
                    station_heatmap_plot = gr.Plot(label="Bike usage: top 10 stations heatmap")

            with gr.Tab("Routes"):
                gr.Markdown("Most frequent origin-destination routes.")
                routes_plot = gr.Plot(label="Routes ranking")

            with gr.Tab("Weather"):
                gr.Markdown("Weather conditions related to hourly bike usage.")
                with gr.Row():
                    temperature_heatmap_plot = gr.Plot(label="Bike usage by temperature and hour")
                    windspeed_plot = gr.Plot(label="Number of rides vs windspeed")
                rain_heatmap_plot = gr.Plot(label="Bike usage: hour vs rain intensity")

            with gr.Tab("Geography"):
                gr.Markdown("Explore sampled start or end point density on an interactive heatmap.")
                geo_focus = gr.Radio(
                    choices=["Trip starts", "Trip ends"],
                    value="Trip starts",
                    label="Points to summarize",
                )
                geo_plot = gr.HTML(label="Trip density heatmap")

            with gr.Tab("Rider & bike mix"):
                gr.Markdown("Duration comparison by rider segment and bike type.")
                mix_plot = gr.Plot(label="Duration by group")

        _bind_to_all_changes(global_inputs, fn=summary_view, inputs=global_inputs, outputs=summary_md)
        _bind_to_all_changes(global_inputs, fn=member_mix_pie, inputs=global_inputs, outputs=member_mix_plot)
        _bind_to_all_changes(global_inputs, fn=bike_mix_pie, inputs=global_inputs, outputs=bike_mix_plot)
        _bind_to_all_changes(global_inputs, fn=duration_hist, inputs=global_inputs, outputs=duration_plot)
        _bind_to_all_changes(global_inputs, fn=monthly_line, inputs=global_inputs, outputs=month_plot)
        _bind_to_all_changes(global_inputs, fn=hourly_bar, inputs=global_inputs, outputs=hourly_plot)
        _bind_to_all_changes(global_inputs, fn=heatmap, inputs=global_inputs, outputs=heatmap_plot)
        _bind_to_all_changes(
            [*global_inputs, station_role],
            fn=stations_bar,
            inputs=[*global_inputs, station_role],
            outputs=stations_plot,
        )
        _bind_to_all_changes(
            [*global_inputs, station_role],
            fn=station_usage_heatmap,
            inputs=[*global_inputs, station_role],
            outputs=station_heatmap_plot,
        )
        _bind_to_all_changes(global_inputs, fn=routes_bar, inputs=global_inputs, outputs=routes_plot)
        _bind_to_all_changes(
            global_inputs,
            fn=temperature_hour_heatmap,
            inputs=global_inputs,
            outputs=temperature_heatmap_plot,
        )
        _bind_to_all_changes(global_inputs, fn=windspeed_usage_line, inputs=global_inputs, outputs=windspeed_plot)
        _bind_to_all_changes(global_inputs, fn=rain_hour_heatmap, inputs=global_inputs, outputs=rain_heatmap_plot)
        _bind_to_all_changes(
            [*global_inputs, geo_focus],
            fn=geo_map,
            inputs=[*global_inputs, geo_focus],
            outputs=geo_plot,
        )
        _bind_to_all_changes(global_inputs, fn=duration_mix, inputs=global_inputs, outputs=mix_plot)

        demo.load(fn=summary_view, inputs=global_inputs, outputs=summary_md)
        demo.load(fn=member_mix_pie, inputs=global_inputs, outputs=member_mix_plot)
        demo.load(fn=bike_mix_pie, inputs=global_inputs, outputs=bike_mix_plot)
        demo.load(fn=duration_hist, inputs=global_inputs, outputs=duration_plot)
        demo.load(fn=monthly_line, inputs=global_inputs, outputs=month_plot)
        demo.load(fn=overview_table, outputs=sample_table)
        demo.load(fn=hourly_bar, inputs=global_inputs, outputs=hourly_plot)
        demo.load(fn=heatmap, inputs=global_inputs, outputs=heatmap_plot)
        demo.load(
            fn=stations_bar,
            inputs=[*global_inputs, station_role],
            outputs=stations_plot,
        )
        demo.load(
            fn=station_usage_heatmap,
            inputs=[*global_inputs, station_role],
            outputs=station_heatmap_plot,
        )
        demo.load(fn=routes_bar, inputs=global_inputs, outputs=routes_plot)
        demo.load(fn=temperature_hour_heatmap, inputs=global_inputs, outputs=temperature_heatmap_plot)
        demo.load(fn=windspeed_usage_line, inputs=global_inputs, outputs=windspeed_plot)
        demo.load(fn=rain_hour_heatmap, inputs=global_inputs, outputs=rain_heatmap_plot)
        demo.load(fn=geo_map, inputs=[*global_inputs, geo_focus], outputs=geo_plot)
        demo.load(fn=duration_mix, inputs=global_inputs, outputs=mix_plot)

    return demo


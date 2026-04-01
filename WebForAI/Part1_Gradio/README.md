# Citibike 2021 - Gradio data explorer

Interactive multi-tab app for exploring the sampled NYC Citibike 2021 data from Part 1.  
The app is modular and split into components so it is easier to extend and maintain.

## Run

From `WebForAI/Part1_Gradio`:

```bash
pip install -r requirements.txt
python app.py
```

By default Gradio starts at `http://127.0.0.1:7860`.

## Data file

The app auto-detects one of these files in the project root:

- `citibike_2021_merged_sampled.csv` (preferred)
- `citibike_2021_sampled.csv` (fallback)

## Project structure

- `app.py`: single-command entrypoint.
- `gradio_explorer/data.py`: CSV loading, enrichment, and shared filters.
- `gradio_explorer/views.py`: chart, summary, and table functions.
- `gradio_explorer/ui.py`: tab layout and callback wiring.
- `gradio_explorer/config.py`: constants (month labels, weekday order, paths).

## Tabs

- `Overview`: KPI summary, duration histogram, and monthly demand line.
- `Explore Dataset`: browse filtered sample rows from the dataset.
- `Time patterns`: trips by start hour and weekday x hour heatmap.
- `Stations`: top start/end stations with configurable top-N.
- `Routes`: top origin-destination routes (excluding same start/end station).
- `Geography`: interactive Folium map for sampled start/end points.
- `Rider & bike mix`: duration distribution by rider type and bike type.

## Filters

Global filters at the top apply across all tabs:

- Rider type
- Bike type
- Season
- Month

## Dependencies

Listed in `requirements.txt`:

- `gradio`
- `pandas`
- `plotly`
- `numpy`
- `folium`

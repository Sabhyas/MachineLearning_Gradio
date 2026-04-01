"""Project configuration constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_CANDIDATES = [
    BASE_DIR / "data",
    BASE_DIR / "data.csv",
]
DEFAULT_SAMPLE_TABLE_ROWS = 25
DEFAULT_STATIONS_TOP_N = 15
DEFAULT_STATION_HEATMAP_TOP_N = 10
DEFAULT_ROUTES_TOP_N = 12
DEFAULT_GEO_MAX_POINTS = 25_000
DEFAULT_GEO_RANDOM_SEED = 42
DEFAULT_GEO_STATION_MARKERS = 40

DAYS_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


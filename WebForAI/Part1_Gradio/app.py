"""Run the Citibike multi-tab Gradio explorer with `python app.py`."""

from gradio_explorer.ui import build_app


if __name__ == "__main__":
    demo = build_app()
    demo.launch(theme="soft")

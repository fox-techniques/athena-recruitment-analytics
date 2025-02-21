"""
ATHENA Application Tracking & Recruitment Analytics Dashboard

This application is built using Dash to provide insights and analytics for job applications.
It includes an interactive interface to track, analyze, and visualize job application data.

Features:
- Overview visualizations including treemaps, bar charts, choropleth maps, and Sankey diagrams.
- Key metrics displayed in stats cards (e.g., applications, countries, industries).
- Dynamic data parsing, mapping, and augmentation for advanced analysis.

Components:
- Left column: Description card and controls for filtering.
- Right column: Overview statistics and visualizations.

Modules Used:
- src.insights: Extracts key metrics from the dataset.
- src.data_loader: Loads required mappings and datasets.
- src.data_parser: Parses raw jobhunt data.
- src.data_generator: Fills missing data and predicts mappings.
- src.data_visualizations: Generates visualizations for the dashboard.
- src.control_panel: Provides reusable UI components.

"""

import os
import re
from dotenv import load_dotenv
from dash import Dash
import dash_bootstrap_components as dbc
from dashboard.insights import get_overall_insights
from data_engine.data_loader import load_and_prepare_data

from pages.generate_layout import generate_layout
from callbacks.update_figures import register_callbacks

from utils.performance import _log_execution_time

import logging

logger = logging.getLogger(__name__)

# We no longer import overview_visualizations, we import generate_figures:
from dashboard.data_visualizations import generate_figures

from pages.generate_layout import generate_layout
from callbacks.update_figures import register_callbacks

# Load environment variables from .env file
load_dotenv()

# Environment Variables or Default Paths
APPLICATIONS_DIR = os.getenv("APPLICATIONS_DIR", "./data/job_applications")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./data/output")
DASH_HOST = os.getenv("DASH_HOST")
DASH_PORT = int(os.getenv("DASH_PORT"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"


@_log_execution_time
def initialize_dash_app():
    """Initialize the Dash application with external styles and title."""
    app = Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
        ],
        title="ATHENA - Recruitment Analytics",
    )
    app.server = app.server  # Flask server
    return app


@_log_execution_time
def main():
    """Main entry point for the Dash application."""
    # Initialize app
    app = initialize_dash_app()

    # Load and process data
    extended_data_df = load_and_prepare_data()

    # Generate insights
    metrics = get_overall_insights(extended_data_df)

    # Dynamically find all StatusLevel columns and sort them numerically
    status_level_columns = [
        col for col in extended_data_df.columns if col.startswith("StatusLevel")
    ]
    # Exclude StatusLevel0
    status_level_columns = [
        col for col in status_level_columns if col != "StatusLevel0"
    ]

    # sort them by the integer after "StatusLevel"
    status_level_columns = sorted(
        status_level_columns, key=lambda x: int(re.search(r"\d+", x).group())
    )

    # Build your default Sankey levels: "1st Node" plus any other columns you’d like
    default_ir_levels = ["1st Node", "Field"] + status_level_columns

    # Set default values for the map projection
    default_projection = "natural earth1"

    # This single call is used for initial display:
    industries_fig, fields_fig, choropleth_fig, sankey_fig = generate_figures(
        df=extended_data_df,
        sankey_levels=default_ir_levels,
        map_projection=default_projection,
        color_template="none",
        font_color="#14213d",
    )

    # Pack them as a tuple in the order generate_layout expects
    visualizations = (industries_fig, fields_fig, choropleth_fig, sankey_fig)

    # Set up layout with these initial figures
    app.layout = generate_layout(extended_data_df, metrics, visualizations)

    # Register callbacks for interactive updates
    register_callbacks(app, extended_data_df)

    # Run server
    app.run_server(host=DASH_HOST, port=DASH_PORT, debug=DEBUG_MODE)


if __name__ == "__main__":
    main()

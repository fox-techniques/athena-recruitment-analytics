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
from dash import Dash
import dash_bootstrap_components as dbc

from data_engine.data_loader import load_and_prepare_data

from dashboard.insights import get_overall_insights
from dashboard.data_visualizations import overview_visualizations
from pages.generate_layout import generate_layout
from callbacks.update_figures import register_callbacks

from utils.performance import _log_execution_time

import logging

logger = logging.getLogger(__name__)

# Environment Variables or Default Paths
APPLICATIONS_DIR = os.getenv("APPLICATIONS_DIR", "./data/job_applications")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./data/output")


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
    app.server = app.server
    return app


@_log_execution_time
def main():
    """Main entry point for the Dash application."""
    # Initialize app
    app = initialize_dash_app()

    # Load and process data
    extended_data_df = load_and_prepare_data()

    # Generate insights and visualizations
    metrics = get_overall_insights(extended_data_df)
    visualizations = overview_visualizations(extended_data_df)

    # Set up layout and callbacks
    app.layout = generate_layout(extended_data_df, metrics, visualizations)
    register_callbacks(app, extended_data_df)

    # Run server
    app.run_server(host="0.0.0.0", port=8050)


if __name__ == "__main__":
    main()

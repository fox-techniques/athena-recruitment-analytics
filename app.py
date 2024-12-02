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

from dash import Dash
import dash_bootstrap_components as dbc

from src.insights import get_overall_insights
from src.data_loader import load_json_mappings, parse_and_load_data
from src.data_generator import (
    update_missing_company_industry,
    update_missing_position_field,
    add_industry_and_field,
    extend_status_levels,
)
from src.data_visualizations import overview_visualizations

from pages.generate_layout import generate_layout
from callbacks.update_figures import register_callbacks

APPLICATIONS_DIR = "./data/job_applications"
OUTPUT_DIR = "./data/output"

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
        "./assets/styles.css",
    ],
    title="ATHENA - Recruitment Analytics",
)

server = app.server

# Parsing and processing application directory for visualizations
parsed_df = parse_and_load_data(APPLICATIONS_DIR, OUTPUT_DIR)

# Load mappings and enrich data
company_industry_mapping, position_field_mapping = load_json_mappings()

enriched_df = add_industry_and_field(
    parsed_df, company_industry_mapping, position_field_mapping
)

updated_company_industry_mapping = update_missing_company_industry(
    enriched_df, company_industry_mapping
)
updated_position_field_mapping = update_missing_position_field(
    enriched_df, position_field_mapping
)

updated_data_df = add_industry_and_field(
    enriched_df,
    updated_company_industry_mapping,
    updated_position_field_mapping,
)

# Extend status codes to levels
extended_data_df = extend_status_levels(updated_data_df)

# Extract key metrics
metrics = get_overall_insights(extended_data_df)

# Generate visualizations
visualizations = overview_visualizations(extended_data_df)

# Assign layout
app.layout = generate_layout(extended_data_df, metrics, visualizations)

# Register callbacks
register_callbacks(app, extended_data_df)

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host="0.0.0.0", port=8050)

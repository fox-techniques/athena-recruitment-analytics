"""
Athena Jobhunt Analytics Dashboard

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
from src.data_loader import load_json_mappings
from src.data_parser import parse_job_application_directory
from src.data_generator import (
    find_missing_companies,
    find_missing_positions,
    predict_missing_company_industry,
    predict_missing_position_field,
    add_industry_and_field,
)
from src.data_visualizations import overview_visualizations

from pages.generate_layout import generate_layout
from callbacks.update_figures import register_callbacks

APPLICATIONS_DIR = "./data/job_applications"

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
        "./assets/styles.css",
    ],
    title="Athena: Recruitment Analytics",
)

server = app.server

# Parsing and processing data for visualizations
parsed_df = parse_job_application_directory(APPLICATIONS_DIR)


# Load mappings and enrich data
company_industry_mapping, position_field_mapping = load_json_mappings()
enriched_df = add_industry_and_field(
    parsed_df, company_industry_mapping, position_field_mapping
)

updated_company_industry_mapping = predict_missing_company_industry(
    find_missing_companies(enriched_df, company_industry_mapping),
    company_industry_mapping,
)
updated_position_field_mapping = predict_missing_position_field(
    find_missing_positions(enriched_df, position_field_mapping),
    position_field_mapping,
)

updated_data_df = add_industry_and_field(
    enriched_df,
    updated_company_industry_mapping,
    updated_position_field_mapping,
)

# Extract key metrics
metrics = get_overall_insights(updated_data_df)


# Generate visualizations
visualizations = overview_visualizations(updated_data_df)

# Assign layout
app.layout = generate_layout(updated_data_df, metrics, visualizations)

# Register callbacks
register_callbacks(app, updated_data_df)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8050))
    # app.run_server(host="0.0.0.0", port=port)
    app.run_server(debug=True)

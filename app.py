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

from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from datetime import datetime as dt

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
from src.data_visualizations import (
    overview_visualizations,
    create_bar_chart,
    create_choropleth,
    create_sankey,
    create_treemap,
)
from src.control_panel import (
    description_card,
    generate_control_card,
    generate_stats_card,
)

APPLICATIONS_DIR = "./data/job_applications"

# Data Preparation
# raw_df = pd.read_csv("./data/output/raw_data.csv")
parsed_df = pd.read_csv("./data/output/parsed_data.csv")

# Load mappings and enrich data
company_industry_mapping, position_field_mapping = load_json_mappings()
df = add_industry_and_field(parsed_df, company_industry_mapping, position_field_mapping)

# Extract key metrics
(
    num_of_applications,
    num_of_countries,
    num_of_industries,
    num_of_fields,
    num_of_active,
    num_of_interviews,
) = get_overall_insights(df)

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "./assets/styles.css"],
    title="Athena Jobhunt Analytics",
)

server = app.server

# Parsing and processing data for visualizations
parsed_data_df = parse_job_application_directory(APPLICATIONS_DIR)
updated_company_industry_mapping = predict_missing_company_industry(
    find_missing_companies(parsed_data_df, company_industry_mapping),
    company_industry_mapping,
)
updated_position_field_mapping = predict_missing_position_field(
    find_missing_positions(parsed_data_df, position_field_mapping),
    position_field_mapping,
)

processed_data_df = add_industry_and_field(
    parsed_data_df,
    updated_company_industry_mapping,
    updated_position_field_mapping,
)


# Generate visualizations
fig_industries, fig_fields, fig_choropleth, fig_irene_sankey = overview_visualizations(
    processed_data_df
)

# Define the layout of the app
app.layout = dbc.Container(
    id="app-container",
    children=[
        # Header with title and logo
        dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src="./assets/icons/jobhunt-logo.png",
                        className="logo",
                    ),
                    width="auto",
                ),
                dbc.Col(
                    [
                        html.H1(
                            "ATHENA - PEOPLE AND RECRUITMENT ANALYTICS",
                            className="title",
                            style={"margin-bottom": "0", "font-size": "2rem"},
                        ),
                        html.H2(
                            "FOX TECHNIQUES",
                            className="subtitle",
                            style={"margin-top": "0", "font-size": "1.2rem"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                    },
                ),
            ],
            align="center",
            className="mb-4",
        ),
        # Content: Left column for controls, right column for visualizations
        dbc.Row(
            [
                dbc.Col(
                    [
                        description_card(),
                        html.Div(
                            ["initial child"],
                            id="output-clientside",
                            style={"display": "none"},
                        ),
                        generate_control_card(processed_data_df),
                    ],
                    width=3,
                    id="left-column",
                ),
                dbc.Col(
                    [
                        # Stats Cards
                        dbc.Card(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        generate_stats_card(
                                            "Applications",
                                            num_of_applications,
                                            "./assets/icons/job-application-icon.png",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        generate_stats_card(
                                            "Countries",
                                            num_of_countries,
                                            "./assets/icons/country-icon.png",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        generate_stats_card(
                                            "Industries",
                                            num_of_industries,
                                            "./assets/icons/job-sector-icon.png",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        generate_stats_card(
                                            "Backgrounds",
                                            num_of_fields,
                                            "./assets/icons/job-area-icon.png",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        generate_stats_card(
                                            "Active",
                                            num_of_active,
                                            "./assets/icons/job-active-icon.png",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        generate_stats_card(
                                            "Interviews",
                                            num_of_interviews,
                                            "./assets/icons/job-interview-icon.png",
                                        ),
                                        width=2,
                                    ),
                                ],
                            ),
                            id="stats_card",
                            className="card mb-4",
                        ),
                        # Graph Visualizations
                        dbc.Card(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure=fig_irene_sankey, id="sankey-graph"
                                        ),
                                        className="graph-container",
                                    )
                                ),
                                dbc.Row(dbc.Col(dcc.Graph(figure=fig_industries))),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(figure=fig_fields),
                                        className="graph-container",
                                    )
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(
                                            figure=fig_choropleth, id="choropleth-map"
                                        ),
                                        className="graph-container",
                                    )
                                ),
                            ],
                            className="graph-card",
                        ),
                    ],
                    width=9,
                    id="right-column",
                ),
            ],
        ),
    ],
)


@app.callback(
    [Output("sankey-graph", "figure"), Output("choropleth-map", "figure")],
    [Input("apply-btn", "n_clicks")],
    [
        State("ir-level-select", "value"),
        State("country-select", "value"),
        State("globe-select", "value"),
    ],
)
def update_figures(n_clicks, ir_levels, selected_countries, selected_projection):
    """
    Update the figures based on the control panel values.

    Args:
        n_clicks (int): Number of times the Apply button is clicked.
        ir_levels (list): Selected Sankey levels.
        selected_countries (list): Selected countries for filtering.
        selected_projection (str): Selected map projection for the choropleth.

    Returns:
        tuple: Updated Sankey and Choropleth figures.
    """
    # Filter data based on selected countries
    filtered_data = df[df["Country"].isin(selected_countries)]

    # Create Sankey Diagram
    sankey_figure = create_sankey(
        data=df,
        levels=ir_levels,
        title="Irene-Sankey Diagram",
        color_template="plotly",
        font_color="#000000",
    )

    # Create Choropleth Map
    choropleth_figure = create_choropleth(
        data=filtered_data,
        locations="Country",
        hover_name="Country",
        title="Top Countries of Job Locations",
        projection=selected_projection,
        color_scale="Viridis",
        color_template="none",
        font_color="#14213d",
    )

    return sankey_figure, choropleth_figure


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)

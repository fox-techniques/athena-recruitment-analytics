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
from dash import no_update, callback_context
import dash_bootstrap_components as dbc
import pandas as pd

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
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
        "./assets/styles.css",
    ],
    title="Athena: Recruitment Analytics",
)

server = app.server

# Parsing and processing data for visualizations
# parsed_df = parse_job_application_directory(APPLICATIONS_DIR)
updated_company_industry_mapping = predict_missing_company_industry(
    find_missing_companies(parsed_df, company_industry_mapping),
    company_industry_mapping,
)
updated_position_field_mapping = predict_missing_position_field(
    find_missing_positions(parsed_df, position_field_mapping),
    position_field_mapping,
)

processed_data_df = add_industry_and_field(
    parsed_df,
    updated_company_industry_mapping,
    updated_position_field_mapping,
)


# Generate visualizations
fig_industries, fig_fields, fig_choropleth, fig_irene_sankey = overview_visualizations(
    processed_data_df
)

# Define the layout of the app
app.layout = html.Div(
    [
        dbc.Container(
            id="app-container",
            children=[
                # Header with title and logo
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="./assets/logos/hiring-logo.png",
                                className="logo",
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                html.H1(
                                    "ATHENA",
                                    className="title",
                                    style={"margin-bottom": "0", "font-size": "3rem"},
                                ),
                                html.H2(
                                    "APPLICATION TRACKING & RECRUITMENT ANALYTICS",
                                    className="subtitle",
                                    style={"margin-top": "0", "font-size": "1.5rem"},
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
                                                    figure=fig_irene_sankey,
                                                    id="sankey-graph",
                                                ),
                                                className="graph-container",
                                            )
                                        ),
                                        dbc.Row(
                                            dbc.Col(
                                                dcc.Graph(
                                                    figure=fig_industries,
                                                    id="industries-graph",
                                                )
                                            )
                                        ),
                                        dbc.Row(
                                            dbc.Col(
                                                dcc.Graph(
                                                    figure=fig_fields, id="fields-graph"
                                                ),
                                                className="graph-container",
                                            )
                                        ),
                                        dbc.Row(
                                            dbc.Col(
                                                dcc.Graph(
                                                    figure=fig_choropleth,
                                                    id="choropleth-graph",
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
        ),
        html.Footer(
            [
                # Icons and email link
                html.Div(
                    [
                        html.A(
                            html.I(className="fab fa-linkedin-in"),  # LinkedIn icon
                            href="https://www.linkedin.com/company/fox-techniques",
                            target="_blank",
                            className="footer-icon",
                        ),
                        html.A(
                            html.I(className="fab fa-github"),  # GitHub icon
                            href="https://github.com/fox-techniques",
                            target="_blank",
                            className="footer-icon",
                        ),
                        # Email Icon
                        html.A(
                            html.I(className="fas fa-envelope"),  # Email icon
                            href="mailto:contact@fox-techniques.com?subject=Inquiry%20about%20Fox%20Techniques'%20Solutions%20and%20Services",
                            className="footer-icon",
                        ),
                    ],
                    className="footer-icons",
                ),
                # Footer Text
                html.Div(
                    [
                        "2024 | ",
                        html.A(
                            html.Img(
                                src="assets/logos/fox-techniques-long-logo-light.png",
                                className="footer-logo",
                            ),
                            href="https://github.com/fox-techniques",
                        ),
                    ],
                    className="footer-text",
                ),
            ],
            className="footer",
        ),
    ],
)


@app.callback(
    [
        Output("ir-level-select", "value"),
        Output("country-select", "value"),
        Output("globe-select", "value"),
        Output("sankey-graph", "figure"),
        Output("industries-graph", "figure"),
        Output("fields-graph", "figure"),
        Output("choropleth-graph", "figure"),
    ],
    [Input("apply-btn", "n_clicks"), Input("reset-btn", "n_clicks")],
    [
        State("ir-level-select", "value"),
        State("country-select", "value"),
        State("globe-select", "value"),
    ],
)
def update_figures(
    apply_clicks, reset_clicks, ir_levels, selected_countries, selected_projection
):
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

    # Determine which button triggered the callback
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Default values for reset
    default_ir_levels = ["", "Country", "Field"]
    default_countries = df["Country"].unique()
    default_projection = "natural earth1"

    # Use default values if reset button is clicked
    if triggered_id == "reset-btn":
        ir_levels = default_ir_levels
        selected_countries = default_countries
        selected_projection = default_projection

    # Filter data based on selected countries
    filtered_data = df[df["Country"].isin(selected_countries)]

    # Create Sankey Diagram
    sankey_figure = create_sankey(
        data=filtered_data,
        levels=ir_levels,
        title="Irene-Sankey Diagram",
        color_template="plotly",
        font_color="#000000",
    )

    # Treemap: Top Industries
    top_industries = filtered_data["Industry"].value_counts().reset_index(name="count")
    industries_figure = create_treemap(
        top_industries,
        path=["Industry"],
        values="count",
        title="Top Industries",
        color="count",
        color_template="none",
        font_color="#14213d",
    )

    # Bar Chart: Top Fields
    top_fields = (
        filtered_data["Field"].value_counts().head(10).reset_index(name="count")
    )
    total_count = top_fields["count"].sum()
    top_fields["percentage_and_count"] = (top_fields["count"] / total_count).apply(
        lambda x: f"{x:.2f}%"
    ) + top_fields["count"].apply(lambda x: f" ({x})")

    fields_figures = create_bar_chart(
        data=top_fields,
        x="count",
        y="Field",
        orientation="h",
        color="count",
        text="percentage_and_count",
        title="Top Fields",
        labels={"count": "", "Field": "", "percentage": "Percentage"},
        color_scale="Viridis",
        color_template="none",
        font_color="#14213d",
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

    return (
        ir_levels,
        selected_countries,
        selected_projection,
        sankey_figure,
        industries_figure,
        fields_figures,
        choropleth_figure,
    )


if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8050))
    # app.run_server(host="0.0.0.0", port=port)
    app.run_server(debug=True)

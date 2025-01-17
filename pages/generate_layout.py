from dash import html, dcc
import dash_bootstrap_components as dbc
from dashboard.control_panel import (
    description_card,
    generate_control_card,
    generate_stats_card,
)

from utils.performance import _log_execution_time

import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def generate_layout(processed_data_df, metrics, visualizations):
    """
    Generate the layout for the ATHENA dashboard.

    Args:
        processed_data_df (DataFrame): The processed job application data.
        metrics (tuple): Key metrics extracted from the dataset. Expected order:
                        (applications, countries, industries, fields, active, interviews).
        visualizations (tuple): Visualizations generated for the dashboard. Expected order:
                                (industries_chart, fields_chart, choropleth_map, sankey_diagram).

    Returns:
        html.Div: The full layout of the ATHENA dashboard.
    """
    # Unpack metrics and visualizations
    (
        num_of_applications,
        num_of_countries,
        num_of_industries,
        num_of_fields,
        num_of_active,
        num_of_interviews,
    ) = metrics

    (
        industries_chart,
        fields_chart,
        choropleth_map,
        sankey_diagram,
    ) = visualizations

    # Header Section
    header = dbc.Row(
        [
            dbc.Col(
                html.Img(src="./assets/logos/logo.png", className="logo"),
                width="auto",
            ),
            dbc.Col(
                [
                    html.H1("ATHENA", className="title"),
                    html.H2(
                        "APPLICATION TRACKING & RECRUITMENT ANALYTICS",
                        className="subtitle",
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
    )

    # Stats Cards Section
    stats_cards = dbc.Row(
        [
            dbc.Col(
                generate_stats_card(
                    "Applications",
                    num_of_applications,
                    "./assets/icons/application-icon.png",
                ),
                xs=12,
                sm=6,
                md=4,
                lg=2,  # Full width on xs, two per row on sm, grid on larger screens
                className="mb-1",  # Spacing for vertical stacking
            ),
            dbc.Col(
                generate_stats_card(
                    "Countries",
                    num_of_countries,
                    "./assets/icons/country-icon.png",
                ),
                xs=12,
                sm=6,
                md=4,
                lg=2,
                className="mb-1",
            ),
            dbc.Col(
                generate_stats_card(
                    "Industries",
                    num_of_industries,
                    "./assets/icons/sector-icon.png",
                ),
                xs=12,
                sm=6,
                md=4,
                lg=2,
                className="mb-1",
            ),
            dbc.Col(
                generate_stats_card(
                    "Backgrounds",
                    num_of_fields,
                    "./assets/icons/area-icon.png",
                ),
                xs=12,
                sm=6,
                md=4,
                lg=2,
                className="mb-1",
            ),
            dbc.Col(
                generate_stats_card(
                    "Active",
                    num_of_active,
                    "./assets/icons/active-icon.png",
                ),
                xs=12,
                sm=6,
                md=4,
                lg=2,
                className="mb-1",
            ),
            dbc.Col(
                generate_stats_card(
                    "Interviews",
                    num_of_interviews,
                    "./assets/icons/interview-icon.png",
                ),
                xs=12,
                sm=6,
                md=4,
                lg=2,
                className="mb-1",
            ),
        ],
        className="g-3 stats-card-container",  # Adds gutter spacing between rows and columns
    )

    # Visualizations Section
    visualizations_section = dbc.Card(
        [
            dbc.Row(dbc.Col(dcc.Graph(figure=sankey_diagram, id="sankey-graph"))),
            dbc.Row(dbc.Col(dcc.Graph(figure=industries_chart, id="industries-graph"))),
            dbc.Row(dbc.Col(dcc.Graph(figure=fields_chart, id="fields-graph"))),
            dbc.Row(dbc.Col(dcc.Graph(figure=choropleth_map, id="choropleth-graph"))),
        ],
        className="graph-card",
    )

    # Footer Section
    footer = html.Footer(
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
                    "2025 | ",
                    html.A(
                        html.Img(
                            src="assets/logos/fox-techniques-long-logo-light.png",
                            className="footer-logo",
                        ),
                        href="https://www.fox-techniques.com",
                    ),
                ],
                className="footer-text",
            ),
        ],
        className="footer",
    )

    # Content Section
    content = dbc.Row(
        [
            # Left Column
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
                xs=12,
                sm=12,
                md=3,
                lg=3,
                xl=3,
                id="left-column",
            ),
            # Right Column
            dbc.Col(
                [
                    stats_cards,
                    visualizations_section,
                ],
                xs=12,
                sm=12,
                md=9,
                lg=9,
                xl=9,
                id="right-column",
            ),
        ],
        align="start",
    )

    # Full Layout
    return html.Div(
        [
            dbc.Container(
                id="app-container",
                children=[header, content],
            ),
            footer,
        ]
    )

from dash import html, dcc
import dash_bootstrap_components as dbc
from src.control_panel import (
    description_card,
    generate_control_card,
    generate_stats_card,
)


def generate_layout(processed_data_df, metrics, visualizations):
    """
    Generate the layout for the Athena dashboard.

    Args:
        processed_data_df (DataFrame): The processed job application data.
        metrics (tuple): Key metrics extracted from the dataset. Expected order:
                        (applications, countries, industries, fields, active, interviews).
        visualizations (tuple): Visualizations generated for the dashboard. Expected order:
                                (industries_chart, fields_chart, choropleth_map, sankey_diagram).

    Returns:
        html.Div: The full layout of the Athena dashboard.
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
                html.Img(src="./assets/logos/hiring-logo.png", className="logo"),
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
    stats_cards = dbc.Card(
        dbc.Row(
            [
                dbc.Col(
                    generate_stats_card(
                        "Applications",
                        num_of_applications,
                        "./assets/icons/application-icon.png",
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
                        "./assets/icons/sector-icon.png",
                    ),
                    width=2,
                ),
                dbc.Col(
                    generate_stats_card(
                        "Backgrounds",
                        num_of_fields,
                        "./assets/icons/area-icon.png",
                    ),
                    width=2,
                ),
                dbc.Col(
                    generate_stats_card(
                        "Active",
                        num_of_active,
                        "./assets/icons/active-icon.png",
                    ),
                    width=2,
                ),
                dbc.Col(
                    generate_stats_card(
                        "Interviews",
                        num_of_interviews,
                        "./assets/icons/interview-icon.png",
                    ),
                    width=2,
                ),
            ]
        ),
        id="stats_card",
        className="card mb-4",
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
                width=3,
                id="left-column",
            ),
            # Right Column
            dbc.Col(
                [stats_cards, visualizations_section],
                width=9,
                id="right-column",
            ),
        ]
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

"""
Module for Dashboard Components

This module provides reusable components for a dashboard built using Dash. 
Components include:
- A description card with the dashboard title and introductory text.
- A control card for filtering and interacting with data visualizations.
- A stats card for displaying key metrics.

Functions:
    - description_card: Creates a card containing the dashboard title and description.
    - generate_control_card: Creates a control panel for filtering data visualizations.
    - generate_stats_card: Creates a card for displaying a single statistic with an image.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

from src.data_loader import load_map_projections


def description_card():
    """
    Create a description card with the dashboard title and introductory text.

    Returns:
        html.Div: A Div containing the dashboard title and description text.
    """
    return html.Div(
        id="description-card",
        children=[
            html.Br(),
            html.Span(
                children=[
                    html.H2(
                        "Welcome to ",
                        style={"display": "inline", "margin-right": "0.2rem"},
                    ),  # Regular H3 text
                    html.H2(
                        "ATHENA",
                        style={
                            "display": "inline",  # Inline behavior
                            "color": "#fca311",  # Highlight color
                            "font-weight": "bold",  # Custom bold style
                        },
                    ),
                ],
                style={"display": "inline"},  # Ensure the Span itself behaves inline
            ),
            html.H5(
                "Application Tracking & Analytics Dashboard",
                style={
                    "margin-bottom": "20px",
                },
            ),
            html.Div(
                id="intro",
                children="Explore your applicants' application, track progress, update status and analyze key insights to enhance the performance and efficiency of your recruitment process. Navigate through the dashboard to uncover trends and optimize your strategies effectively.",
            ),
        ],
    )


def generate_control_card(df):
    """
    Create a control panel for filtering data visualizations.

    Args:
        df (DataFrame):

    Returns:
        html.Div: A Div containing the control panel for data visualizations.
    """

    countries = df["Country"].unique()
    globe_list = load_map_projections()

    return html.Div(
        id="control-card",
        children=[
            html.Br(),
            html.H6("Irene-Sankey Levels"),
            dcc.Dropdown(
                id="ir-level-select",
                options=["", "Country", "Field", "Industry", "Area"],
                value=["", "Country", "Field"],
                multi=True,
                className="dark-dropdown",
            ),
            html.Br(),
            html.H6("Select Country"),
            dcc.Dropdown(
                id="country-select",
                options=[{"label": i, "value": i} for i in countries],
                value=countries,
                multi=True,
                className="dark-dropdown",
            ),
            html.Br(),
            html.H6("Select Map Projection"),
            dcc.Dropdown(
                id="globe-select",
                options=[{"label": i.title(), "value": i} for i in globe_list],
                value="natural earth1",
                multi=False,
                className="dark-dropdown",
            ),
            html.Br(),
            html.Div(
                children=[
                    dbc.Button(
                        "Apply",
                        id="apply-btn",
                        n_clicks=0,
                        color="primary",
                        className="me-2 apply-button",
                    ),
                    dbc.Button("Reset", id="reset-btn", n_clicks=0, color="secondary"),
                ],
                style={"margin-top": "20px"},
            ),
        ],
    )


def generate_stats_card(title, value, image_path):
    """
    Create a card for displaying a single statistic with an image.

    Args:
        title (str): The title of the statistic.
        value (str): The value of the statistic.
        image_path (str): The file path to the image to display on the card.

    Returns:
        html.Div: A Div containing a Bootstrap card with the statistic and image.
    """
    return html.Div(
        dbc.Card(
            [
                dbc.CardImg(src=image_path, top=True, className="card-img"),
                dbc.CardBody(
                    [
                        html.P(value, className="card-value"),
                        html.H4(title, className="card-title"),
                    ]
                ),
            ],
        )
    )

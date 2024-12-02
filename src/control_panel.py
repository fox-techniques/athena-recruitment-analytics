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
                    html.H3(
                        "Welcome to ",
                        style={"display": "inline", "margin-right": "0.2rem"},
                    ),
                    html.H2(
                        "ATHENA",
                        style={
                            "display": "inline",
                            "color": "#fca311",
                            "font-weight": 200,
                        },
                    ),
                ],
                style={"display": "inline"},
            ),
            html.Br(),
            html.Div(
                id="intro",
                children="Explore your applicants' application, track progress, update status and analyze key insights to enhance the performance and efficiency of your recruitment process. Navigate through the dashboard to uncover trends and optimize your strategies effectively.",
                style={"margin-top": "1rem"},
            ),
        ],
    )


def generate_control_card(
    df,
    dropdown_ir_default_values=[
        "1st Node",
        "Field",
        "StatusLevel1",
        "StatusLevel2",
        "StatusLevel3",
        "StatusLevel4",
        "StatusLevel5",
    ],
):
    """
    Create a control panel for filtering data visualizations.

    Args:
        df (DataFrame): DataFrame containing data for dropdown options.
        dropdown_ir_default_values (list): Default levels for the dropdown selection.

    Returns:
        html.Div: A Div containing the control panel for data visualizations.
    """

    countries = df["Country"].unique()
    columns_to_exclude_regex = r"Position|Num|Has|Timestamp"

    # Filter levels and add "All Records" mapped to ""
    possible_ir_levels = df.columns[~df.columns.str.contains(columns_to_exclude_regex)]
    dropdown_options = ["1st Node"] + [col for col in possible_ir_levels]

    globe_list = load_map_projections()

    return html.Div(
        id="control-card",
        children=[
            html.Br(),
            html.H6("Irene-Sankey Levels"),
            dcc.Dropdown(
                id="ir-level-select",
                options=dropdown_options,
                value=dropdown_ir_default_values,
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

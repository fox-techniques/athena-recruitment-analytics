"""
Module for Creating Visualizations for Application Tracking and  Analytics

This module provides functions to generate visualizations for applicants' data, including:
- Treemaps for top industries.
- Bar charts for top fields.
- Choropleth maps for job locations.
- Sankey diagrams for hierarchical relationships.

Functions:
    - create_irene_sankey: Generate an Irene-Sankey diagram.
    - create_treemap: Generate a treemap visualization.
    - create_bar_chart: Generate a bar chart visualization.
    - create_choropleth: Generate a choropleth map visualization.
    - overview_visualizations: Generate all overview visualizations (treemap, bar chart, choropleth, and Irene-Sankey diagram).
"""

import plotly.express as px
import plotly.graph_objects as go
from data_engine.data_loader import load_countries_ISO
import irene_sankey as irs

from utils.performance import _log_execution_time

import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def create_irene_sankey(data, levels, title, color_template, font_color):
    """
    Generate a Irene-Sankey diagram for hierarchical flow data.

    Args:
        data (pd.DataFrame): DataFrame containing the flow data.
        levels (list of str): List of columns in the DataFrame representing levels of hierarchy.
            e.g. ["", "Country", "Field"]
        title (str): Title of the Irene-Sankey diagram.
        color_template (str): Plotly template to use for styling.
        font_color (str): Color of the text in the visualization.

    Returns:
        plotly.graph_objects.Figure: Irene-Sankey diagram visualization.
    """
    # Generate the flow data using Irene-Sankey utilities
    flow_df, node_map, link = irs.traverse_sankey_flow(
        data, levels, head_node_label="Applications"
    )

    # Generate the Sankey diagram
    fig_irene_sankey = irs.plot_irene_sankey_diagram(node_map, link)

    # Apply layout customizations
    fig_irene_sankey.update_layout(
        title=title,
        template=color_template,
        font=dict(color=font_color),
        title_x=0.5,
    )

    return fig_irene_sankey


@_log_execution_time
def create_treemap(data, path, values, title, color, color_template, font_color):
    """
    Generate a treemap visualization for hierarchical data.

    Args:
        data (pd.DataFrame): Data to visualize.
        path (list): List of columns defining the hierarchy.
        values (str): Column name containing values to aggregate.
        title (str): Title of the treemap.
        color (str): Column name used for coloring the tiles.
        color_template (str): Plotly template to use for styling.
        font_color (str): Color of the text in the visualization.

    Returns:
        plotly.graph_objects.Figure: Treemap visualization.
    """
    fig = px.treemap(
        data,
        path=path,
        values=values,
        title=title,
        color=color,
    )
    fig.update_layout(
        template=color_template,
        font=dict(color=font_color),
    )
    fig.update_layout(plot_bgcolor="black")
    return fig


@_log_execution_time
def create_bar_chart(
    data,
    x,
    y,
    orientation,
    color,
    text,
    title,
    labels,
    color_scale,
    color_template,
    font_color,
):
    """
    Generate a bar chart visualization for categorical data.

    Args:
        data (pd.DataFrame): Data to visualize.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        orientation (str): Orientation of the bar chart ("h" for horizontal, "v" for vertical).
        color (str): Column name used for coloring the bars.
        text (str): Column name for text annotations on the bars.
        title (str): Title of the bar chart.
        labels (dict): Custom axis labels as a dictionary.
        color_scale (str): Color scale for continuous data.
        color_template (str): Plotly template to use for styling.
        font_color (str): Color of the text in the visualization.

    Returns:
        plotly.graph_objects.Figure: Bar chart visualization.
    """
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation=orientation,
        color=color,
        text=text,
        title=title,
        labels=labels,
        color_continuous_scale=color_scale,
    )
    fig.update_traces(textposition="outside")

    # Extend x-axis range for better text visibility
    max_value = data[x].max()
    fig.update_layout(
        xaxis=dict(range=[0, max_value * 1.3]),
        yaxis=dict(
            categoryorder="total ascending",
            automargin=True,  # Enable automatic margin adjustment
        ),
        template=color_template,
        font=dict(color=font_color),
        margin=dict(
            l=100,  # Left margin to accommodate long y-axis labels
            r=20,  # Right margin
            t=50,  # Top margin
            b=50,  # Bottom margin
        ),
    )
    return fig


@_log_execution_time
def create_choropleth(
    data,
    locations,
    hover_name,
    title,
    projection,
    color_scale,
    color_template,
    font_color,
):
    """
    Generate a choropleth map for geographic data.

    Args:
        data (pd.DataFrame): Data to visualize.
        locations (str): Column name containing location codes (e.g., country codes).
        hover_name (str): Column name for hover text.
        title (str): Title of the choropleth map.
        projection (str): Map projection style (e.g., "natural earth", "orthographic").
        color_scale (str): Color scale for continuous data.
        color_template (str): Plotly template to use for styling.
        font_color (str): Color of the text in the visualization.

    Returns:
        plotly.graph_objects.Figure: Choropleth map visualization.
    """

    top_countries = data["Country"].value_counts().head(30).reset_index(name="count")
    top_countries.rename(columns={"index": "Country"}, inplace=True)

    country_mapping = load_countries_ISO()
    top_countries["Country"] = top_countries["Country"].map(country_mapping)

    fig = px.choropleth(
        top_countries,
        locations=locations,
        color="count",
        hover_name=hover_name,
        title=title,
        projection=projection,
        color_continuous_scale=color_scale,
    )

    fig.update_layout(
        template=color_template,
        font=dict(color=font_color),
    )
    return fig


@_log_execution_time
def overview_visualizations(
    processed_data_df,
    color_template="none",
    font_color="#14213d",
    map_projection="natural earth1",
):
    """
    Generate all overview visualizations for the recruitment dataset.

    Args:
        processed_data_df (pd.DataFrame): Processed applicants' data.
        color_template (str): Plotly template to use for styling (default: "none").
        font_color (str): Color of the text in all visualizations (default: "#14213d").
        map_projection (str): Map projection style (default: "natural earth").

    Returns:
        tuple: A tuple of Plotly figures (treemap, bar chart, choropleth, Irene-Sankey diagram).
    """
    # Treemap: Top Industries
    top_industries = (
        processed_data_df["Industry"].value_counts().reset_index(name="count")
    )
    fig_industries = create_treemap(
        top_industries,
        path=["Industry"],
        values="count",
        title="Top Industries",
        color="count",
        color_template=color_template,
        font_color=font_color,
    )

    # Bar Chart: Top Fields
    # Compute top 10 fields
    top_fields = (
        processed_data_df["Field"].value_counts().head(10).reset_index(name="count")
    )

    # Compute total applications count from the full dataset
    total_count = processed_data_df["Field"].value_counts().sum()

    # Create percentage representation
    top_fields["percentage_and_count"] = (
        top_fields["count"] / total_count * 100
    ).apply(lambda x: f"{x:.2f}%") + top_fields["count"].apply(lambda x: f" ({x})")

    fig_fields = create_bar_chart(
        data=top_fields,
        x="count",
        y="Field",
        orientation="h",
        color="count",
        text="percentage_and_count",
        title="Top Fields",
        labels={"count": "", "Field": "", "percentage": "Percentage"},
        color_scale="Viridis",
        color_template=color_template,
        font_color=font_color,
    )

    # Choropleth: Top Countries
    top_countries = (
        processed_data_df["Country"].value_counts().head(30).reset_index(name="count")
    )
    top_countries.rename(columns={"index": "Country"}, inplace=True)

    country_mapping = load_countries_ISO()
    top_countries["Country"] = top_countries["Country"].map(country_mapping)

    fig_choropleth = create_choropleth(
        data=top_countries,
        locations="Country",
        hover_name="Country",
        title="Top Countries of Job Locations",
        projection=map_projection,
        color_scale="Viridis",
        color_template=color_template,
        font_color=font_color,
    )

    # Sankey Diagram
    fig_irene_sankey = create_irene_sankey(
        data=processed_data_df,
        levels=["", "Country", "Field"],
        title="IRENE-Sankey Flow Diagram",
        color_template="plotly",
        font_color=font_color,
    )

    return fig_industries, fig_fields, fig_choropleth, fig_irene_sankey

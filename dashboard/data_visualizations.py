"""
Module for Creating Visualizations for Application Tracking and  Analytics

This module provides functions to generate visualizations for applicants' data, including:
- Treemaps for top industries.
- Bar charts for top fields.
- Choropleth maps for job locations.
- Sankey diagrams for hierarchical relationships.

Functions:
    - create_irene_sankey: Generate an IRENE-Sankey diagram.
    - create_treemap: Generate a treemap visualization.
    - create_bar_chart: Generate a bar chart visualization.
    - create_choropleth: Generate a choropleth map visualization.
    - generate_figures: Generate the four main overview visualizations (Treemap, Bar, Choropleth, IRENE-Sankey).
"""

import plotly.express as px
import plotly.graph_objects as go
from data_engine.data_loader import load_countries_ISO
import irene_sankey as irs
from utils.levels import reorder_and_place_status_levels


def create_irene_sankey(data, levels, title, color_template, font_color):
    """
    Generate an IRENE-Sankey diagram for hierarchical flow data.
    """
    # Generate the flow data using IRENE-Sankey utilities
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


def create_treemap(data, path, values, title, color, color_template, font_color):
    """
    Generate a treemap visualization for hierarchical data.
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
        plot_bgcolor="black",
    )
    return fig


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
        margin=dict(l=100, r=20, t=50, b=50),
    )
    return fig


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
    """
    country_mapping = load_countries_ISO()
    # Convert the top 30 countries to alpha-3 codes if needed:
    data["Country"] = data["Country"].map(country_mapping)

    fig = px.choropleth(
        data,
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


def generate_figures(
    df,
    sankey_levels,
    map_projection="natural earth1",
    color_template="none",
    font_color="#14213d",
):
    """
    Generate the four main figures:
        - Treemap (Top Industries)
        - Bar Chart (Top Fields)
        - Choropleth (Top Countries)
        - IRENE-Sankey Diagram

    This function can be used both on the initial page load (with defaults)
    and in the callback (with updated user selections).
    """
    # 1) TREEMAP: Top Industries
    top_industries = df["Industry"].value_counts().reset_index(name="count")
    fig_industries = create_treemap(
        data=top_industries,
        path=["Industry"],
        values="count",
        title="Top Industries",
        color="count",
        color_template=color_template,
        font_color=font_color,
    )

    # 2) BAR CHART: Top Fields
    top_fields = df["Field"].value_counts().head(10).reset_index(name="count")
    total_count = top_fields["count"].sum()
    top_fields["percentage_and_count"] = (top_fields["count"] / total_count).apply(
        lambda x: f"{x:.2f}%"
    ) + top_fields["count"].apply(lambda x: f" ({x})")
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

    # 3) CHOROPLETH: Top Countries (limit to top 30)
    top_countries = df["Country"].value_counts().head(30).reset_index(name="count")
    top_countries.rename(columns={"index": "Country"}, inplace=True)
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

    # 4) IRENE-SANKEY
    # reorder "StatusLevelX" if needed
    modified_levels = reorder_and_place_status_levels(sankey_levels)
    fig_sankey = create_irene_sankey(
        data=df,
        levels=modified_levels,
        title="IRENE-Sankey Diagram",
        color_template="plotly",  # use "plotly" or color_template as you prefer
        font_color=font_color,
    )

    # Return them in the order expected by generate_layout: (industries, fields, choropleth, sankey)
    return fig_industries, fig_fields, fig_choropleth, fig_sankey

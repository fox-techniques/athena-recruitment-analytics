from dash import Input, Output, State, callback_context

from dashboard.data_visualizations import (
    create_irene_sankey,
    create_treemap,
    create_bar_chart,
    create_choropleth,
)

from utils.levels import reorder_and_place_status_levels


def register_callbacks(app, df):
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
        default_ir_levels = [
            "1st Node",
            "Field",
            "StatusLevel1",
            "StatusLevel2",
            "StatusLevel3",
            "StatusLevel4",
            "StatusLevel5",
        ]

        default_countries = df["Country"].unique()
        default_projection = "natural earth1"

        # Use default values if reset button is clicked
        if triggered_id == "reset-btn":
            ir_levels = default_ir_levels
            selected_countries = default_countries
            selected_projection = default_projection

        # Filter data based on selected countries
        filtered_data = df[df["Country"].isin(selected_countries)]

        # Handle 1st Node position in the list and status levels order
        modified_ir_levels = reorder_and_place_status_levels(ir_levels)

        # Create Irene-Sankey Diagram
        irene_sankey_figure = create_irene_sankey(
            data=filtered_data,
            levels=modified_ir_levels,
            title="Irene-Sankey Diagram",
            color_template="plotly",
            font_color="#000000",
        )

        # Treemap: Top Industries
        top_industries = (
            filtered_data["Industry"].value_counts().reset_index(name="count")
        )
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
            irene_sankey_figure,
            industries_figure,
            fields_figures,
            choropleth_figure,
        )

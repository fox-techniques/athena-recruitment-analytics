from dash import Input, Output, State, callback_context
from dashboard.data_visualizations import generate_figures


def register_callbacks(app, df):
    @app.callback(
        [
            Output("ir-level-select", "value"),
            Output("country-select", "value"),
            Output("globe-select", "value"),
            # Four figure outputs:
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
    def update_figures_callback(
        apply_clicks, reset_clicks, ir_levels, selected_countries, selected_projection
    ):
        """
        Update the figures based on the control panel values.
        """
        ctx = callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Find all status-level columns
        status_cols = [col for col in df.columns if col.startswith("StatusLevel")]
        # Exclude StatusLevel0
        status_cols = [col for col in status_cols if col != "StatusLevel0"]

        default_dropdown_options = ["1st Node", "Field"] + status_cols

        default_countries = df["Country"].unique()
        default_projection = "natural earth1"

        # If the user clicked "Reset"
        if triggered_id == "reset-btn":
            ir_levels = default_dropdown_options
            selected_countries = default_countries
            selected_projection = default_projection

        # Filter data by selected countries
        filtered_data = df[df["Country"].isin(selected_countries)]

        # Generate the four figures with the same function used at initial load
        industries_fig, fields_fig, choropleth_fig, sankey_fig = generate_figures(
            df=filtered_data,
            sankey_levels=ir_levels,
            map_projection=selected_projection,
            color_template="none",
            font_color="#14213d",
        )

        # Return them in the order that matches the Output list
        # sankey-graph => sankey_fig
        # industries-graph => industries_fig
        # fields-graph => fields_fig
        # choropleth-graph => choropleth_fig
        return (
            ir_levels,
            selected_countries,
            selected_projection,
            sankey_fig,
            industries_fig,
            fields_fig,
            choropleth_fig,
        )

import dash_cytoscape as cyto
import dash as html 
import dash as dcc 
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import math
from dash import no_update
from dash import Dash, html, dcc, no_update
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load your dataset
merged_df = pd.read_csv('merged_data.csv')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Interactive Data Dashboard", className='text-center'))),

    dbc.Row(
        dbc.Col([
            html.H4("Filters"),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{'label': country, 'value': country} for country in merged_df['Entity'].unique()],
                multi=True,
                placeholder="Select Country",
            ),
            dcc.RangeSlider(
                id="year-slider",
                min=int(merged_df['Year'].min()),
                max=int(merged_df['Year'].max()),
                step=1,
                marks={year: str(year) for year in range(int(merged_df['Year'].min()), int(merged_df['Year'].max()) + 1, 5)},
                value=[int(merged_df['Year'].min()), int(merged_df['Year'].max())]
            ),
        ], width=3)
    ),

    dbc.Row(
        dbc.Col(
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label="Data Overview", children=[html.Div(id="data-overview")]),
                dcc.Tab(label="Visualizations", children=[html.Div(id="visualizations")]),
                dcc.Tab(label="Choropleth Map", children=[html.Div(id="choropleth-map")]),
            ])
        )
    )
])

# Data Overview Callback
@app.callback(
    Output("data-overview", "children"),
    [Input("country-dropdown", "value"), Input("year-slider", "value")]
)
def update_data_overview(selected_countries, selected_year_range):
    filtered_df = merged_df[
        (merged_df['Year'] >= selected_year_range[0]) & (merged_df['Year'] <= selected_year_range[1])]
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Entity'].isin(selected_countries)]

    return html.Div([
        html.H5("Data Overview"),
        dcc.Markdown("**Data Source:** Merged CSV Files"),
        dbc.Table.from_dataframe(filtered_df.head(10), striped=True, bordered=True, hover=True)
    ])

# Visualizations Callback
@app.callback(
    Output("visualizations", "children"),
    [Input("country-dropdown", "value"), Input("year-slider", "value")]
)
def update_visualizations(selected_countries, selected_year_range):
    filtered_df = merged_df[
        (merged_df['Year'] >= selected_year_range[0]) & (merged_df['Year'] <= selected_year_range[1])]
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Entity'].isin(selected_countries)]

    scatter_fig = px.scatter(filtered_df, x="GDP_per_capita", y="Life_expectancy", color="Entity",
                             title="GDP per Capita vs Life Expectancy")
    line_fig = px.line(filtered_df, x="Year", y="CO2_per_capita", color="Entity", title="CO2 Emissions Over Time")

    return html.Div([
        dcc.Graph(figure=scatter_fig),
        dcc.Graph(figure=line_fig),
    ])

# Choropleth Map Callback
@app.callback(
    Output("choropleth-map", "children"),
    [Input("country-dropdown", "value"), Input("year-slider", "value")]
)
def update_choropleth_map(selected_countries, selected_year_range):
    filtered_df = merged_df[
        (merged_df['Year'] >= selected_year_range[0]) & (merged_df['Year'] <= selected_year_range[1])]
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Entity'].isin(selected_countries)]

    choropleth_fig = px.choropleth(
        filtered_df,
        locations="Entity",
        locationmode="country names",  # Ensure this matches your 'Entity' values
        color="GDP_per_capita",
        hover_name="Entity",
        hover_data=['Life_expectancy', 'CO2_per_capita'],
        animation_frame="Year",
        title="GDP Per Capita by Country"
    )

    return dcc.Graph(figure=choropleth_fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=10000)

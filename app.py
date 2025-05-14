import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from scipy.stats import pearsonr
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

# Load and process data
df = pd.read_csv('Project2Data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df = df.dropna(how='all')
numeric_cols = df.select_dtypes(include='number').columns

# Define recession periods and event markers
recessions = [
    {'start': '2001-03-01', 'end': '2001-11-01'},
    {'start': '2007-12-01', 'end': '2009-06-01'},
    {'start': '2020-02-01', 'end': '2020-04-01'}
]
events = [
    {'date': '2001-09-11', 'label': '9/11'},
    {'date': '2008-09-15', 'label': 'Financial Crisis'},
    {'date': '2020-03-11', 'label': 'COVID Declared Pandemic'}
]

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

# Helper to add overlays
def apply_overlays(fig):
    for r in recessions:
        fig.add_vrect(
            x0=r['start'], x1=r['end'], fillcolor="gray", opacity=0.3, layer="below", line_width=0
        )
    for e in events:
        fig.add_vline(x=e['date'], line_dash="dash", line_color="red")
        fig.add_annotation(
            x=e['date'], y=1, yref='paper', showarrow=False,
            text=e['label'], bgcolor="red", font_color="white", font_size=10
            )
        fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=20
    )
    return fig

# Layout
app.layout = dbc.Container([
    html.H1("U.S. Economic Dashboard", className="text-center text-light my-4"),
    dcc.Tabs(id="tabs", value='table-tab', children=[
        dcc.Tab(label="Data Overview", value='table-tab', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label="Charts", value='charts-tab', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label="Economic Growth", value='tab1', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label="Government Spending", value='tab2', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label="Wages & Income", value='tab3', className='custom-tab', selected_className='custom-tab--selected'),
        dcc.Tab(label="Interest & Inflation", value='tab4', className='custom-tab', selected_className='custom-tab--selected'),
    ],
    colors={"border": "#222", "primary": "#00BFFF", "background": "#111"}),
    html.Div(id='tab-content')
], fluid=True, style={"backgroundColor": "#222", "padding": "20px"})

# Tab Rendering Callback
@app.callback(Output('tab-content', 'children'), Input('tabs', 'value'))
def render_tab(tab):
    if tab == 'table-tab':
        return html.Div([
            html.H5("Filter by Year Range", style={'textAlign': 'center', 'marginTop': '40px'}),
            dcc.RangeSlider(
                id="year-slider",
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=[df['Year'].min(), df['Year'].max()],
                marks={str(y): str(y) for y in range(df['Year'].min(), df['Year'].max()+1, 5)},
                step=1
            ),
            html.Br(),
            html.H5("Filter Columns (Select One or More)",style={'textAlign': 'center', 'marginTop': '40px'}),
            dcc.Dropdown(
                id="column-dropdown",
                options=[{"label": col, "value": col} for col in df.columns],
                multi=True
            ),
            html.H5("Enter Approximate Filter Value",style={'marginTop': '40px'}),
            dcc.Input(id="column-filter-input", placeholder="Enter filter value", type="text"),
            html.Div(id="data-table")
        ])
    elif tab == 'charts-tab':
        return html.Div([
            html.H5("Choose Variable for X-Axis", style={'textAlign': 'center', 'marginTop': '40px'}),
            dcc.Dropdown(id='x-axis', options=[{"label": col, "value": col} for col in numeric_cols],
                         value=numeric_cols[0] if not numeric_cols.empty else None),
            html.H5("Choose Variable for Y-Axis", style={'textAlign': 'center', 'marginTop': '40px'}),
            dcc.Dropdown(id='y-axis', options=[{"label": col, "value": col} for col in numeric_cols],
                         value=numeric_cols[1] if len(numeric_cols) > 1 else None),

            html.Div(id='correlation-output', style={'marginTop': '10px'}),
            dcc.Graph(id='scatter-plot'),

            html.H5("Group Box Plot by", ),
            dcc.Dropdown(id='box-group', options=[{"label": col, "value": col} for col in numeric_cols],
                         value=numeric_cols[0]),
            dcc.Graph(id='box-plot'),

            html.H5("Bar Chart Over Time"),
            dcc.Dropdown(id='bar-group', options=[{"label": col, "value": col} for col in numeric_cols],
                         value=numeric_cols[0]),
            dcc.Graph(id='bar-chart'),
            html.H5("Select Variables for Correlation Heatmap"),
            dcc.Dropdown(id='heatmap-vars', options=[{"label": col, "value": col} for col in numeric_cols], multi=True,
                         value=numeric_cols[:5]),
            dcc.Graph(id='heatmap'),

        ])
    elif tab == 'tab1':
        return html.Div([
            html.H4("Economic Growth Over Time", style={'textAlign': 'center', 'marginTop': '40px'}),
            dcc.RangeSlider(
                id='year-slider-growth',
                min=df['Year'].min(),
                max=df['Year'].max(),
                step=1,
                marks={y: str(y) for y in range(df['Year'].min(), df['Year'].max()+1, 5)},
                value=[2000, df['Year'].max()]
            ),
            dcc.Dropdown(
                id='growth-dropdown',
                options=[{'label': col, 'value': col} for col in [
                    'Gross Domestic Product (Billions)',
                    'Real Disposable Personal Income - 2017 Dollars (Billions)',
                    'Industrial Production Index',
                    'total factor productivity',
                    'Real Gross National Income - 2017 Dollars (Billions)',
                    'Real Priavte Domestic Investment - 2017 Dollars (Billions)'
                ]],
                value=['Gross Domestic Product (Billions)'],
                multi=True
            ),
            dcc.Graph(id='gdp-graph'),
        ])
    elif tab == 'tab2':
        return html.Div([
            html.H4("Federal Expenditures and Debt", style={'textAlign': 'center', 'marginTop': '40px'}),
             dcc.RangeSlider(
                id='year-slider-ex',
                min=df['Year'].min(),
                max=df['Year'].max(),
                step=1,
                marks={y: str(y) for y in range(df['Year'].min(), df['Year'].max()+1, 5)},
                value=[2000, df['Year'].max()]
             ),
            dcc.Dropdown(
                id='spending-dropdown',
                options=[{'label': col, 'value': col} for col in [
                    'Federal Government Debt (Billions)',
                    'Government Total Expenditures',
                    'Government Welfare and Social Expenditures',
                    'Defense Expenditures']],
                value=['Government Total Expenditures'],
                multi=True
            ),
            dcc.Graph(id='spending-graph')
        ])
    elif tab == 'tab3':
        return html.Div([
            html.H4("Wages and Income Trends", style={'textAlign': 'center', 'marginTop': '40px'}),
             dcc.RangeSlider(
                id='year-slider-I',
                min=df['Year'].min(),
                max=df['Year'].max(),
                step=1,
                marks={y: str(y) for y in range(df['Year'].min(), df['Year'].max()+1, 5)},
                value=[2000, df['Year'].max()]
             ),
            dcc.Dropdown(
                id='income-radio',
                options=[{'label': i, 'value': i} for i in [
                    'Real Median Household Income - 2023 Dollars (Thousands)',
                    'Real Median Personal Income - 2023 Dollars (Thousands)',
                    'Weekly Earnings',
                    'Real Disposable Personal Income - 2017 Dollars (Billions)',
                    'Personal Savings Rate',
                    'Federal Minimum Wage',
                    'Highest Individual Income Tax Rate',
                    'Lowest Individual Income Tax Rate']],
                value='Real Median Household Income (Thousands)',
                multi=True
            ),
            dcc.Graph(id='income-graph')
        ])
    elif tab == 'tab4':
        return html.Div([
            html.H4("Interest Rates & Inflation", style={'textAlign': 'center', 'marginTop': '40px'}),
             dcc.RangeSlider(
                id='year-slider-IR',
                min=df['Year'].min(),
                max=df['Year'].max(),
                step=1,
                marks={y: str(y) for y in range(df['Year'].min(), df['Year'].max()+1, 5)},
                value=[2000, df['Year'].max()]
             ),
            dcc.Dropdown(
                id='interest-check',
                options=[
                    {'label': 'Federal Funds Rate', 'value': 'Federal Funds Rate'},
                    {'label': 'Inflation', 'value': 'Inflation'},
                    {'label': '1 Year Treasury Yield', 'value': '1-Year Treasury Rate'},
                    {'label': '5 Year Treasury Yield', 'value': '5-Year Treasury Rate'},
                    {'label': '10 Year Treasury Yield', 'value': '10-Year Treasury Rate'}],
                value=['Federal Funds Rate'],
                multi=True
            ),
            dcc.Graph(id='interest-graph')
        ])


# Table Update
@app.callback(
    Output("data-table", "children"),
    [Input("year-slider", "value"),
     Input("column-dropdown", "value"),
     Input("column-filter-input", "value")]
)
def update_table(year_range, selected_columns, filter_value):
    dff = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()

    if selected_columns and filter_value:
        try:
            filter_float = float(filter_value)

            # Only apply numeric filtering to the first selected column that is numeric and not Date/Year
            target_col = next(
                (col for col in selected_columns
                 if col in dff.columns and
                    np.issubdtype(dff[col].dtype, np.number) and
                    col not in ['Year']),  # exclude Year
                None
            )

            if target_col:
                # Filter rows within ±30% buffer
                lower = 0.7 * filter_float
                upper = 1.3 * filter_float
                dff = dff[(dff[target_col] >= lower) & (dff[target_col] <= upper)].copy()

                # Add absolute difference column and sort
                dff['__diff__'] = abs(dff[target_col] - filter_float)
                dff = dff.sort_values('__diff__').drop(columns='__diff__')

        except ValueError:
            # Non-numeric filter: do substring match
            dff = dff[dff.astype(str).apply(
                lambda x: x.str.contains(filter_value, case=False, na=False)
            ).any(axis=1)]

    # Filter to selected columns only
    if selected_columns:
        keep_cols = [col for col in ['Date', 'Year'] if col in dff.columns]
        selected = [col for col in selected_columns if col in dff.columns]
        dff = dff[keep_cols + selected]

    if dff.empty:
        return html.Div("No rows match the filter criteria.", style={"color": "red", "marginTop": "10px"})

    return dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)



@app.callback(
    Output('scatter-plot', 'figure'),
    Output('box-plot', 'figure'),
    Output('bar-chart', 'figure'),
    Output('correlation-output', 'children'),
    [Input('x-axis', 'value'),
     Input('y-axis', 'value'),
     Input('box-group', 'value'),
     Input('bar-group', 'value')]
)
def update_charts(x, y, box_group, bar_group):
    # Scatter plot
    scatter = px.scatter(df, x=x, y=y, title=f"{y} vs {x}") if x and y else px.scatter()
    scatter.update_layout(
        plot_bgcolor='#222',  # Set background color for the plot
        paper_bgcolor='#222',  # Set background color for the paper
        title_font=dict(color='White'),  # Title color
        xaxis=dict(showgrid=False, title=dict(font=dict(color='#00BFFF'))),
        yaxis=dict(showgrid=False, title=dict(font=dict(color='#00BFFF')))
    )

    # Box plot
    box = px.box(df, y=box_group, title=f"Box Plot of {box_group}") if box_group else px.box()
    box.update_layout(
        plot_bgcolor='#222',  # Set background color for the plot
        paper_bgcolor='#222',  # Set background color for the paper
        title_font=dict(color='White'),  # Title color
        yaxis=dict(title=dict(font=dict(color='#00BFFF')))
    )

    # Bar chart with overlay (applying function for overlays)
    bar = apply_overlays(px.bar(df, x='Date', y=bar_group, title=f"{bar_group} Over Time")) if bar_group else px.bar()
    bar.update_layout(
        plot_bgcolor='#222',  # Set background color for the plot
        paper_bgcolor='#222',  # Set background color for the paper
        title_font=dict(color='White'),  # Title color
        xaxis=dict(title=dict(font=dict(color='#00BFFF'))),
        yaxis=dict(title=dict(font=dict(color='#00BFFF')))
    )

    # Correlation calculation and text display
    if x and y and x in df.columns and y in df.columns:
        x_vals = df[x].dropna()
        y_vals = df[y].dropna()
        common_index = x_vals.index.intersection(y_vals.index)
        x_vals = x_vals.loc[common_index]
        y_vals = y_vals.loc[common_index]

        if len(x_vals) > 1:
            corr, p_value = pearsonr(x_vals, y_vals)
            abs_corr = abs(corr)
            color = "darkred" if abs_corr >= 0.8 else "orange" if abs_corr >= 0.5 else "green" if abs_corr >= 0.3 else "gray"
            sig_text = " (Significant)" if p_value < 0.05 else " (Not significant)"
            corr_text = html.Div([
                html.Span("📈 Pearson Correlation between "),
                html.Strong(f"{x}"),
                html.Span(" and "),
                html.Strong(f"{y}: "),
                html.Span(f"{corr:.2f}{sig_text}", style={"color": color})
            ])
        else:
            corr_text = html.Span("Not enough data to calculate correlation.")
    else:
        corr_text = ""

    return scatter, box, bar, corr_text


@app.callback(Output('heatmap', 'figure'), Input('heatmap-vars', 'value'))
def update_heatmap(selected_vars):
    if selected_vars and all(var in df.columns for var in selected_vars):
        corr_df = df[selected_vars].dropna().corr()
        fig = px.imshow(corr_df, text_auto=True, color_continuous_scale='RdBu_r',
                        title='Correlation Heatmap')
        fig.update_layout(
            plot_bgcolor='#222', paper_bgcolor='#222', font_color='white',
            title_font=dict(color='White')
        )
        return fig
    return go.Figure()




@app.callback(Output('gdp-graph', 'figure'),
              [Input('year-slider-growth', 'value'),
               Input('growth-dropdown', 'value'),
                ])
def update_gdp(years, indicators):
    dff = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    fig = px.line(dff, x='Date', y=indicators, title='Economic Growth Indicators Over Time')
    return apply_overlays(fig)

@app.callback(Output('spending-graph', 'figure'), Input('spending-dropdown', 'value'),Input('year-slider-ex', 'value'))
def update_spending(vars,years):
    dff = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    fig = px.line(dff, x='Date', y=vars, title=f"Spending Indicators Over Time")
    return apply_overlays(fig)

@app.callback(Output('income-graph', 'figure'), Input('income-radio', 'value'), Input('year-slider-I', 'value'))
def update_income(vars,years):
    dff = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    fig = px.line(dff, x='Date', y=vars, title=f"Income Indicators Over Time")
    return apply_overlays(fig)

@app.callback(Output('interest-graph', 'figure'), Input('interest-check', 'value'),Input('year-slider-IR', 'value'))
def update_interest(selected_vars,years):
    dff = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    fig = px.line(dff, x='Date', y=selected_vars, title="Rates Over Time")
    return apply_overlays(fig)
# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)

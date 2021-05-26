import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        # assume you have a "long-form" data frame
        # see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv("gapminder_clean.csv")

server = app.server

axis_options = ["Agriculture, value added (% of GDP)","CO2 emissions (metric tons per capita)","Domestic credit provided by financial sector (% of GDP)","Electric power consumption (kWh per capita)","Energy use (kg of oil equivalent per capita)","Exports of goods and services (% of GDP)","Fertility rate, total (births per woman)","GDP growth (annual %)","Imports of goods and services (% of GDP)","Industry, value added (% of GDP)","Inflation, GDP deflator (annual %)","Life expectancy at birth, total (years)","Population density (people per sq. km of land area)", "Services, etc., value added (% of GDP)"]

app.layout = html.Div([
    html.H1(style={'textAlign':"center"}, children="Gapminder Visualization"),
        html.Div(style={'display': 'flex', 'width': '80%', 'margin':"0 auto 3em auto", 'justify-content':'space-between'}, children=[
    html.Div(style={'width': '40%', 'box-sizing':'border-box'}, children=[
        html.H2(children="X-axis Options:"),
    dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
    ),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in axis_options],
                value=axis_options[0]
            )]),
    html.Div(style={'width': '40%', 'box-sizing': 'border-box'}, children=[
        html.H2(children="Y-axis Options:"),
    dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in axis_options],
                value=axis_options[1]
            )]),]),
        html.Div(style={'width':'80%', 'margin':"0 auto 3em auto"}, children=[
                dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),
                dcc.Graph(id='graph-with-slider'),
                ]),
    

])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('xaxis-type','value'),
    Input('yaxis-type','value'),
    Input('yaxis-column','value'),
    Input('xaxis-column', 'value'))
def update_figure(selected_year, xaxistype, yaxistype, xaxiscol, yaxiscol):
    filtered_df = df[df.Year == selected_year]
    filtered_df = filtered_df.dropna(subset=[xaxiscol, yaxiscol, "pop"])
    filtered_df['pop'] = filtered_df['pop'].fillna(0.1)
    fig = px.scatter(filtered_df, x=xaxiscol, y=yaxiscol,
                     size="pop", color="continent", hover_name="Country Name",
                     log_x=True, size_max=55)

    fig.update_xaxes(title=xaxiscol,
                     type='linear' if xaxistype == 'Linear' else 'log')

    fig.update_yaxes(title=yaxiscol,
                     type='linear' if yaxistype == 'Linear' else 'log')


    fig.update_layout(transition_duration=300)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

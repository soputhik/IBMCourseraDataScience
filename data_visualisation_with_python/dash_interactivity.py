import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# retrieving data set
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                           encoding="ISO-8859-1",
                           dtype={'Div1Airport': str, 'Div1TailNum': str,
                                  'Div2Airport': str, 'Div2TailNum': str})

# generating dash application
app = dash.Dash(__name__)

# editing layout
app.layout = html.Div(children=[html.H1('Airline Performance Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                html.Div(["Input Year", dcc.Input(id='input-year', value='2010', type='number', style={
                                         'height': '50px', 'font-size': 35}),], style={'font-size:40'}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot')),
                                ])

# adding callback decorator


@app.callback(Output(component_id='line-plot', component_property='figure'), Input(component_id='input-year', component_property='value'))
# add computation to call back and return graph
def get_graph(entered_year):
    # choose based on year entered
    df = airline_data[airline_data['Year'] == int(entered_year)]

    # group data by month and compute average
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig = go.Figure(data=go.Scatter(
        x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title='Month vs Average Flight Delay Time',
                      xaxis_title='Month', yaxis_title='ArrDelay')
    return fig


# running the app
if __name__ == '__main__':
    app.run_server()

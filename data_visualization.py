""" Module to visualize the joint angles of the UR5 robot in real-time. """

import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from utils import pg_engine

app = dash.Dash(__name__)

def fetch_data():
    return pd.read_sql("SELECT * FROM ur5_joint_angles ORDER BY timestamp DESC LIMIT 100", pg_engine())

@app.callback(
    dash.dependencies.Output("live-graph", "figure"),
    [dash.dependencies.Input("interval-component", "n_intervals")]
)
def update_graph(n):
    df = fetch_data()
    fig = px.line(df, x="timestamp", y=["shoulder_pan", "elbow", "wrist_1"], title="UR5 Joint Angles")
    return fig

app.layout = html.Div([
    dcc.Graph(id="live-graph"),
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
])

if __name__ == "__main__":
    app.run_server(debug=True)

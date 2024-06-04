from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from algorithm.RenkoAlgo import RenkoAlgo

app = Dash(__name__)

# Initialize singleton RenkoAlgo object
default_config = {
    "symbol": "ETH/USDT",
    "start_date": "2010-12-1",
    "interval": '4h'
}
renko_algo = RenkoAlgo(
    symbol=default_config["symbol"],
    start_date=default_config["start_date"],
    interval=default_config["interval"]
)

app.layout = html.Div(
    [
        html.H4("Candlestick chart"),
        dcc.Checklist(
            id="toggle-rangeslider",
            options=[{"label": "Include Rangeslider", "value": "slider"}],
            value=["slider"],
        ),
        dcc.Graph(id="graph"),
    ]
)

@app.callback(
    Output("graph", "figure"),
    Input("toggle-rangeslider", "value"),
)

def display_candlestick(value):
    df = renko_algo.get_candlestick_plot()
    fig = go.Figure(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
        )
    )
    fig.update_layout(xaxis_rangeslider_visible="slider" in value)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
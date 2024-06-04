from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
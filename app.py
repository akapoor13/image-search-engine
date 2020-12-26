from src.callbacks import callback
from src.layouts import app_layout
import dash
import os
import dash_bootstrap_components as dbc

# initalize application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# initalize UI and functionality
app.title = 'Image Search'
app.config.suppress_callback_exceptions = True
app.layout = app_layout()
callback(app)

if __name__ == '__main__':
    app.run_server()
    # app.run_server()

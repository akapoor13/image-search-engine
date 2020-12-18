import os

import dash
from src.layouts import app_layout
from src.callbacks import callback

# initalize application
app = dash.Dash(__name__)
server = app.server

# initalize UI and functionality
app.layout = app_layout()
callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
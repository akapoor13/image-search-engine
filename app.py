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

if os.path.exists('image_files') or os.path.exists('assets/image_files'):
    import shutil
    try:
        shutil.rmtree('image_files')
        print('removed image_files')
    except:
        print('unsuccessful image_files')

    try:
        shutil.rmtree('assets/image_files')
        print('removed assets')
    except:
        print('break')

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server()

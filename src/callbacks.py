import src.constants as const
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

def callback(app):
    @app.callback(
        Output("search_modal", "is_open"),
        [
            Input("open", "n_clicks"), 
            Input("close", "n_clicks")\
        ],
        [
            State("search_modal", "is_open")
        ],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open

        return is_open

    @app.callback(
        Output('input-search-bar', 'children'),
        [
            Input('input-option', 'value')
        ],
        [
            State("search_modal", "is_open")
        ]
    )
    def input_type(input_type, is_open):
        if not is_open:
            raise PreventUpdate

        div = []
        if is_open:
            if input_type==const.des_input:
                div = [dcc.Input(id='search_bar', style={'width':'100%', 'font-family': 'Arial, Helvetica, sans-serif'})]
            elif input_type==const.upload_input:
                div = [dcc.Upload(
                    id='upload_data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Picture')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                )]
            
        return div
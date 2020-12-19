import src.constants as const
from src.helper.layouts import search_description, input_picture
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
        Output("search_modal_2", "is_open"),
        [
            Input("open_2", "n_clicks"),
            Input("close_2", "n_clicks")
        ],
        [
            State("search_modal_2", "is_open"),
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
            if input_type == const.des_input:
                div = [search_description(const.search_bar_id)]
            elif input_type == const.upload_input:
                div = [input_picture(const.search_upload_id)]
            elif input_type == const.id_input:
                div = [search_description(const.search_pic_id, 'Enter ID')]

        return div

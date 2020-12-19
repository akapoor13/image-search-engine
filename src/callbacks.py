import src.constants as const
from src.helper.layouts import search_description, input_picture, add_image_menu, picture_details
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash 
import uuid
from src.upload import download_image_from_upload
from src.database import insert_images

add_image_menu = add_image_menu()

def callback(app):
    create_tags(app)
    open_close_modals(app)

    @app.callback(
        Output('modal_body', 'children'),
        [
            Input('search_modal_2', 'is_open'),
        ]
    )
    def reset_add_menu(_):
        return [add_image_menu]
    
    @app.callback(
        Output(f'add_picture_input', 'children'),
        [
            Input('upload_data', 'contents')
        ]
    )
    def reset_add_menu_details(_):
        return [picture_details('add')]

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

    @app.callback(
        Output("upload_status_add", 'children'),
        [
            Input('add_selected_save', 'n_clicks'),
            Input('upload_data', 'contents'),
        ],
        [
            State('add_selected_image_description', 'value'),
            State('add_selected_tags_dd', 'value'),
            State('add_selected_date', 'date'),
            State('add_selected_user', 'value')
        ]
    )
    def update_add_image_menu(n_clicks, image_data, description, tags, date, users):
        message = "No Upload"

        if not image_data:
            return message
        
        message = "Uploaded"
        if dash.callback_context.triggered[0]['prop_id']=='upload_data.contents':
            return message

        image_idd = uuid.uuid4().hex
        path = download_image_from_upload(image_idd, image_data)

        db_data = {
            'idd':image_idd,
            'description':description,
            'tags':tags,
            'path':path,
            'date':date,
            'users':users
        }
        insert_images(db_data)#, table='test_images')

        message = "Saved"
        return message

def open_close_modals(app):
    for o, c, m in zip(['open', 'open_2'], ['close', 'close_2'], ['search_modal', 'search_modal_2']):
        @app.callback(
            Output(m, "is_open"),
            [
                Input(o, "n_clicks"), 
                Input(c, "n_clicks")\
            ],
            [
                State(m, "is_open")
            ],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open

            return is_open

def create_tags(app):
    for idd in ['add', 'edit']:
        @app.callback(
            [
                Output(f'{idd}_selected_tags_dd', 'options'),
                Output(f'{idd}_selected_tags_dd', 'value')
            ],
            [
                Input(f"{idd}_selected_tags_btn", 'n_clicks')
            ],
            [
                State(f'{idd}_selected_tag', 'value'),
                State(f'{idd}_selected_tags_dd', 'options'),
                State(f'{idd}_selected_tags_dd', 'value')
            ]   
        )
        def update_tags_dropdown(_, tag, options, values):
            if not tag:
                raise PreventUpdate
            
            new_tag = True
            for t in options:
                if tag.lower()==t['value'].lower():
                    new_tag = False
            
            if new_tag:
                options.append({'label':tag, 'value':tag})
                values.append(tag)

            return options, values

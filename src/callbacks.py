import src.constants as const
from src.helper.layouts import search_description, input_picture, add_image_menu, picture_details
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash
import uuid
from src.upload import download_image_from_upload
from src.database import insert_images, pull_db_data, update_image
import pandas as pd
import datetime
add_image_menu = add_image_menu()


def __update_tag_dropwdowns(tag, options, values):
    values = list(set(values+[tag]))
    options = [{'label': i, 'value': i} for i in values]

    return options, values


def callback(app):
    __create_tags(app)
    __open_close_modals(app)

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
            Input('upload_data', 'contents'),
            Input('add_selected_save', 'n_clicks')
        ]
    )
    def reset_add_menu_details(_, __):
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
    def pic_search_input(input_type, is_open):
        if not is_open:
            raise PreventUpdate

        div = []
        if is_open:
            if input_type == const.DESINPUT_:
                div = [search_description(SEARCHBARID_)]
            elif input_type == const.UPLOADINPUT_:
                div = [input_picture(SEARCHUPLOADID_)]
            elif input_type == const.IDINPUT_:
                div = [search_description(
                    SEARCHPICID_, placeholder='Enter ID')]

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

        if dash.callback_context.triggered[0]['prop_id'] == 'upload_data.contents':
            message = "Uploaded"  # success message to UI
        else:
            image_idd = uuid.uuid4().hex
            path = download_image_from_upload(image_idd, image_data)
            db_data = {
                'idd': image_idd,
                'description': description,
                'tags': tags,
                'path': path,
                'date': date,
                'users': users
            }
            insert_images(db_data)

            message = "Saved"  # success message to UI
        return message

    @app.callback(
        [
            Output('results_table', 'data'),
            Output('results_table', 'selected_rows')
        ],
        [
            Input("search-btn", 'n_clicks'),
            Input("edit_selected_save", 'n_clicks')
        ],
        [
            State('results_table', 'selected_rows'),
            State('results_table', 'derived_virtual_data'),
            State('edit_selected_image_description', 'value'),
            State('edit_selected_tags_dd', 'value'),
            State('edit_selected_date', 'date'),
            State('edit_selected_user', 'value')
        ]
    )
    def search_db(n_clicks, n_clicks_edit, row, data, description, tags, date, user):
        if (not n_clicks):
            return [], []

        if dash.callback_context.triggered[0]['prop_id'] == 'edit_selected_save.n_clicks' and row:
            r = row[0]
            image_data = data[r]

            image_idd = image_data[const.IDD_]
            image_data[const.DESCRIPTION_] = description
            image_data[const.TAGS_] = tags
            image_data[const.TAGTABLE_] = f"""[{', '.join(tags)}]"""
            image_data[const.DATE_] = date
            image_data[const.DATETABLE_] = datetime.datetime.strptime(
                date, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
            image_data[const.USERS_] = user

            update_image(image_data, {const.IDD_: image_idd})
            data[r] = image_data
        else:
            df = pull_db_data()
            df[const.TAGTABLE_] = df[const.TAGS_].apply(
                lambda x: f"""[{', '.join(x)}]""")
            df[const.DATETABLE_] = df[const.DATE_].apply(
                lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d'))

            data = df.to_dict(orient='records')
            row = []

        return data, row

    @app.callback(
        [
            Output('selected_image', 'src'),
            Output('edit_selected_image_description', 'value'),
            Output('edit_selected_tags_dd', 'options'),
            Output('edit_selected_tags_dd', 'value'),
            Output('edit_selected_date', 'date'),
            Output('edit_selected_user', 'value')
        ],
        [
            Input(f"edit_selected_tags_btn", 'n_clicks'),
            Input('results_table', 'derived_virtual_selected_rows')
        ],
        [
            State('results_table', 'derived_virtual_data'),
            State('edit_selected_tag', 'value'),
            State('edit_selected_tags_dd', 'value')
        ]
    )
    def update(_, row, data, new_tag, dd_values):
        if row == None or data == None or (not row):
            return '', '', [], [], datetime.datetime.today(), ''

        image_details = data[row[0]]
        description = image_details[const.DESCRIPTION_]
        options = [{'label': i, 'value': i}
                   for i in image_details[const.TAGS_]]
        values = image_details[const.TAGS_]
        date = datetime.datetime.strptime(
            image_details[const.DATE_], '%Y-%m-%dT%H:%M:%S.%f')
        user = image_details[const.USERS_]
        src = image_details[const.PATH_]

        if dash.callback_context.triggered[0]['prop_id'] == 'edit_selected_tags_btn.n_clicks' and new_tag:
            values = dd_values
            options, values = __update_tag_dropwdowns(
                new_tag, options, dd_values)

        print(options, values)
        return src, description, options, values, date, user


def __open_close_modals(app):
    for o, c, m in zip(['open', 'open_2'], ['close', 'close_2'], ['search_modal', 'search_modal_2']):
        @app.callback(
            Output(m, "is_open"),
            [
                Input(o, "n_clicks"),
                Input(c, "n_clicks")
            ],
            [
                State(m, "is_open")
            ],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open

            return is_open


def __create_tags(app):
    for idd in ['add']:
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

            options, values = __update_tag_dropwdowns(tag, options, values)

            return options, values

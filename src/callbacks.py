import src.constants as const
from src.helper.layouts import search_description, input_picture, add_image_menu, picture_details
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash
import uuid
from src.upload import download_image_from_upload
from src.database import insert_images, pull_db_data, update_image, query, remove_record
import pandas as pd
import datetime
import os
from src.cv import color_descriptor_path, sift_descriptors_path

add_image_menu = add_image_menu()


def callback(app):
    __create_tags(app)
    __open_close_modals(app)

    @app.callback(Output('modal_body', 'children'), [
        Input('search_modal_2', 'is_open'),
    ])
    def reset_add_menu(_):
        """
            open and close modals
        """
        return [add_image_menu]

    @app.callback(Output(f'add_picture_input', 'children'), [
        Input('upload_data', 'contents'),
        Input('add_selected_save', 'n_clicks')
    ])
    def reset_add_menu_details(_, __):
        """
            upload image menu
        """
        return [picture_details('add')]

    @app.callback([
        Output(f'{component_id}_input', 'style') for component_id in
        [const.SEARCHDESCID_, const.SEARCHUPLOADID_, const.SEARCHPICID_]
    ], [Input('input-option', 'value')])
    def pic_search_input(input_type):
        """
            query for db based on modal input
        """
        description_search = 'none'
        image_search = 'none'
        id_search = 'none'

        if input_type == const.DESINPUT_:
            description_search = True
        elif input_type == const.UPLOADINPUT_:
            image_search = True
        elif input_type == const.IDINPUT_:
            id_search = True

        return [{
            'display': display
        } for display in [description_search, image_search, id_search]]

    @app.callback(Output("upload_status_add", 'children'), [
        Input('add_selected_save', 'n_clicks'),
        Input(const.ADDUPLOADID_, 'contents'),
    ], [
        State('add_selected_image_description', 'value'),
        State('add_selected_tags_dd', 'value'),
        State('add_selected_date', 'date'),
        State('add_selected_user', 'value')
    ])
    def update_add_image_menu(n_clicks, image_data, description, tags, date,
                              users):
        message = "No Upload"

        if not image_data:
            return message

        if dash.callback_context.triggered[0][
                'prop_id'] == 'upload_data.contents':
            message = "Uploaded"  # success message to UI
        else:
            image_idd = uuid.uuid4().hex
            path = download_image_from_upload(image_idd, image_data)

            if description is None:
                description = ''

            db_data = {
                'idd': image_idd,
                'description': description,
                'tags': tags,
                'path': path,
                'date': date,
                'users': users,
                'color_descriptor': color_descriptor_path(path),
                'sift_descriptor': sift_descriptors_path(path)
            }
            insert_images(db_data)

            message = "Saved"  # success message to UI
        return message

    @app.callback([
        Output('results_table', 'data'),
        Output('results_table', 'selected_rows')
    ], [
        Input("search-btn", 'n_clicks'),
        Input("edit_selected_save", 'n_clicks'),
        Input('delete_selected_btn', 'n_clicks')
    ], [
        State('results_table', 'selected_rows'),
        State('results_table', 'derived_virtual_data'),
        State('edit_selected_image_description', 'value'),
        State('edit_selected_tags_dd', 'value'),
        State('edit_selected_date', 'date'),
        State('edit_selected_user', 'value'),
        State('input-option', 'value'),
        State(const.SEARCHDESCID_, 'value'),
        State(const.SEARCHUPLOADID_, 'contents'),
        State(const.SEARCHPICID_, 'value')
    ])
    def search_db(_, __, ___, row, data, description, tags, date, user,
                  query_type, description_input, upload_data, id_input):
        if dash.callback_context.triggered[0][
                'prop_id'] == 'edit_selected_save.n_clicks' and row:
            r = row[0]
            image_data = data[r]

            image_idd = image_data[const.IDD_]
            image_data[const.DESCRIPTION_] = description
            image_data[const.TAGS_] = tags
            image_data[const.TAGTABLE_] = f"""[{', '.join(tags)}]"""
            image_data[const.DATE_] = date
            image_data[const.USERS_] = user

            update_image(image_data, {const.IDD_: image_idd})
            data[r] = image_data
        elif dash.callback_context.triggered[0][
                'prop_id'] == 'delete_selected_btn.n_clicks' and row:
            r = row[0]
            image_data = data.pop(r)

            remove_record([image_data[const.IDD_]])
            os.remove(os.path.join(os.getcwd(), image_data[const.PATH_]))
            row = []
        else:
            if query_type == const.DESINPUT_:
                query_input = description_input

                if query_input is None:
                    query_input = ''

            elif query_type == const.UPLOADINPUT_:
                query_input = upload_data

                if query_input is None:
                    raise PreventUpdate

            elif query_type == const.IDINPUT_:
                query_input = id_input

                if query_input is None:
                    query_input = ''

            df = query(query_type, query_input)
            df[const.TAGTABLE_] = df[const.TAGS_].apply(
                lambda x: f"""[{', '.join(x)}]""")

            data = df.to_dict(orient='records')
            row = []

        return data, row

    @app.callback([
        Output('selected_image', 'src'),
        Output('edit_selected_image_description', 'value'),
        Output('edit_selected_tags_dd', 'options'),
        Output('edit_selected_tags_dd', 'value'),
        Output('edit_selected_date', 'date'),
        Output('edit_selected_user', 'value')
    ], [
        Input(f"edit_selected_tags_btn", 'n_clicks'),
        Input('results_table', 'derived_virtual_selected_rows')
    ], [
        State('results_table', 'derived_virtual_data'),
        State('edit_selected_tag', 'value'),
        State('edit_selected_tags_dd', 'value')
    ])
    def update(_, row, data, new_tag, dd_values):
        if row == None or data == None or (not row):
            return '', '', [], [], datetime.datetime.today(), ''

        image_details = data[row[0]]
        description = image_details[const.DESCRIPTION_]
        options = [{
            'label': i,
            'value': i
        } for i in image_details[const.TAGS_]]
        values = image_details[const.TAGS_]
        date = image_details[const.DATE_]
        user = image_details[const.USERS_]
        src = image_details[const.PATH_]

        if dash.callback_context.triggered[0][
                'prop_id'] == 'edit_selected_tags_btn.n_clicks' and new_tag:
            dd_values.append(new_tag)
            values = dd_values
            options = [{'label': i, 'value': i} for i in dd_values]

        return src, description, options, values, date, user


def __open_close_modals(app):
    for o, c, m in zip(['open', 'open_2'], ['close', 'close_2'],
                       ['search_modal', 'search_modal_2']):

        @app.callback(
            Output(m, "is_open"),
            [Input(o, "n_clicks"), Input(c, "n_clicks")],
            [State(m, "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open

            return is_open

    @app.callback(Output('search_modal_3', "is_open"), [
        Input('open_3', "n_clicks"),
        Input('close_3', "n_clicks"),
        Input('delete_selected_btn', 'n_clicks')
    ])
    def toggle_modal_delete(n1, n2, is_open):
        if dash.callback_context.triggered[0]['prop_id'] == 'open_3.n_clicks':
            return True

        return False


def __create_tags(app):
    for idd in ['add']:

        @app.callback([
            Output(f'{idd}_selected_tags_dd', 'options'),
            Output(f'{idd}_selected_tags_dd', 'value')
        ], [Input(f"{idd}_selected_tags_btn", 'n_clicks')], [
            State(f'{idd}_selected_tag', 'value'),
            State(f'{idd}_selected_tags_dd', 'options'),
            State(f'{idd}_selected_tags_dd', 'value')
        ])
        def update_tags_dropdown(_, new_tag, options, values):
            if not new_tag:
                raise PreventUpdate

            values.append(new_tag)
            options = [{'label': i, 'value': i} for i in values]

            return options, values

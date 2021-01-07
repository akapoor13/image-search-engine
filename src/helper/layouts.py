import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import src.constants as const


def search_description(idd, placeholder='Enter description', visible=False):
    if not visible:
        display = 'none'
    else:
        display = True

    return html.Div(
        dcc.Input(id=idd, placeholder=placeholder,
                  style={'width': '100%', 'font-family': 'Arial, Helvetica, sans-serif'}),
        style={'display': display}, id=f'{idd}_input'
    )


def input_picture(idd, visible=True):
    if not visible:
        display = 'none'
    else:
        display = True

    return html.Div(
        dcc.Upload(
            id=idd,
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
            },
            accept='image/*'
        ),
        id=f'{idd}_input',
        style={'display': display}
    )


def picture_details(idd):
    today = datetime.datetime.today()

    return html.Div([
        html.Div([
            html.Summary('Description'),
            dcc.Input(id=f'{idd}_selected_image_description',
                      style={'width': '100%'})
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Summary('Tags'),
            dcc.Dropdown(
                id=f'{idd}_selected_tags_dd',
                options=[],
                value=[],
                multi=True,
                style={'width': '100%'}
            ),
            html.Div([
                dcc.Input(id=f'{idd}_selected_tag', placeholder='Enter Tags',
                          style={'width': '25%', 'height': '100%'}),
                dbc.Button("Add", id=f"{idd}_selected_tags_btn", className='button', style={
                    'margin-left': '15px'})
            ], className='column', style={'margin-top': '15px'})
        ], style={'margin-bottom': '25px'}),
        html.Div([
            html.Div([
                html.Summary('Date'),
                dcc.DatePickerSingle(
                    id=f'{idd}_selected_date', date=datetime.date(today.year, today.month, today.day),
                    max_date_allowed=datetime.date(
                        today.year, today.month, today.day)
                ),
            ], style={'width': '50%'}),
            html.Div([
                html.Summary('User'),
                dcc.Input(id=f'{idd}_selected_user')
            ], style={'width': '50%'})
        ], className='column')
    ], id=f'{idd}_picture_input')


def picture_input(idd):
    if idd == 'edit':
        modal = dbc.Modal(
            [
                dbc.ModalBody(children=html.Div([
                    html.H5('Are you sure you want to delete image?',
                            style={'text-align': 'center'}),
                    html.Div([
                        dbc.Button('Yes', id='delete_selected_btn',
                                   className='button'),
                        dbc.Button('No', id='close_3', className='button',
                                   style={'margin-left': '15px'})
                    ], style={'display': 'flex',  'justify-content': 'center'})
                ]), className='modal_body', id='modal_body_3')
            ],
            id='search_modal_3',
            className='modal_style',
            size='xl',
            centered=True
        )
        delete_button = dbc.Button('Delete', id=f'open_3', className='button', style={
            'margin-left': '15px'})
    else:
        modal = html.Div()
        delete_button = html.Div()

    return html.Div([
        picture_details(idd),
        html.Div([
            dbc.Button("Save", id=f"{idd}_selected_save", className='button'),
            delete_button
        ], style={'margin-top': '15px'}),
        modal
    ], className='pretty_container')


def add_image_menu():
    return html.Div([
        html.Div(
            [
                html.Div(dcc.Upload(
                    id=const.ADDUPLOADID_,
                    children=html.Div(
                        ['Drag and Drop or ', html.A('Select Picture')]),
                    className='upload',
                    accept='image/*'
                ), style={'padding-right': '10px'}),
                html.Div(id='upload_status_add')
            ], className='pretty_container'
        ),
        picture_input('add')
    ])

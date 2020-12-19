import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime

def search_description(idd, placeholder='Enter description'):
    return html.Div(
        dcc.Input(id=idd, placeholder=placeholder, 
        style={'width': '100%', 'font-family': 'Arial, Helvetica, sans-serif'}),
    )

def input_picture(idd):
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
        )
    )

def picture_input(idd):
    return html.Div([
        html.Div([
            html.Summary('Description'),
            dcc.Input(id=f'{idd}_selected_image_description', style={'width':'100%'})
        ], style={'margin-bottom':'10px'}),
        html.Div([
            html.Summary('Tags'),
            dcc.Dropdown(
                id=f'{idd}_selected_tags_dd',
                options=[],
                value=[],
                multi=True,
                style={'width':'100%'}
            ),
            html.Div([
                dcc.Input(id=f'{idd}_selected_tag', placeholder='Enter Tags',
                style={'width':'25%', 'height':'100%'}),
                dbc.Button("Add", id=f"{idd}_selected_tags_btn", className='button', style={'margin-left':'15px'})
            ], className='column', style={'margin-top':'15px'})
        ], style={'margin-bottom':'25px'}),
        html.Div([
            html.Div([
                html.Summary('Date'),
                dcc.DatePickerSingle(id=f'{idd}_selected_date', date=datetime.datetime.today())
            ], style={'width':'50%'}),
            html.Div([
                html.Summary('User'),
                dcc.Input(id=f'{idd}_selected_user')
            ], style={'width':'50%'})
        ],className='column'),
        dbc.Button("Save", id=f"{idd}_selected_save", className='button', style={'margin-top':'10px'})
    ], className='pretty_container')

def add_image_menu():
    return html.Div([
        html.Div(
            [
                html.Div(dcc.Upload(
                    id='upload_data',
                    children=html.Div(['Drag and Drop or ', html.A('Select Picture')]),
                    className='upload',
                    accept='image/*'
                ), style={'padding-right':'10px'}),
                html.Div(id='upload_status_add')
            ], className='pretty_container'
        ),
        picture_input('add')
    ])
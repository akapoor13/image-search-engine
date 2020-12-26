import os
import dash_table
from src.helper.layouts import search_description, input_picture, add_image_menu, picture_input
import src.constants as const
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def __header_bar():
    bar = html.Header([
        html.H1('Star Wars Episode XIII: The Image Repository')
    ], className='header')

    return bar


def __search_engine_ui():
    dropdown = html.Div([
        html.Summary('Search Type'),
        dcc.Dropdown(
            id='input-option',
            options=[{'label': lab, 'value': val}
                     for val, lab in const.SEARCHOPTIONS_.items()],
            value=const.DEFAULTINPUTTYPE_,
            clearable=False
        )]
    )

    modal = html.Div(
        [
            html.Div([
                dbc.Button("Search Bar", id="open", className='button', style={
                    'margin-left': '10px', 'margin-top': '10px'}),
                dbc.Button("Add Image", id="open_2", className='button', style={
                    'margin-left': '10px', 'margin-top': '10px'
                })
            ]),
            dbc.Modal(
                [
                    dbc.ModalBody(
                        [
                            dropdown,
                            html.Div([
                                html.Div(
                                    [
                                        search_description(
                                            const.SEARCHDESCID_),
                                        input_picture(const.SEARCHUPLOADID_),
                                        search_description(
                                            const.SEARCHPICID_, placeholder='Enter ID')
                                    ], id='input-search-bar',
                                    style={'padding-right': '10px'}
                                ),
                                dbc.Button(
                                    "Search", id="search-btn", className="ml-auto", style={'margin-top': '5px'})
                            ], style={'margin-top': '15px'})
                        ], className='modal_body'
                    ),
                    dbc.ModalFooter(
                        dbc.Button('Close', id='close', className='ml-auto')
                    )
                ],
                id="search_modal",
                className='modal_style',
                size='xl',
                centered=True,
            ),
            dbc.Modal(
                [
                    dbc.ModalBody(children=add_image_menu(),
                                  className='modal_body', id='modal_body'),
                    dbc.ModalFooter(
                        dbc.Button('Close', id='close_2', className='ml-auto')
                    )
                ],
                id='search_modal_2',
                className='modal_style',
                size='xl',
                centered=True
            )
        ]
    )

    body = html.Div([
        html.Div(modal, style={'margin-bottom': '15px'}),
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='results_table',
                    columns=[{'name': ['Results'] + [const.COLMAPPING_[i]], 'id':i}
                             for i in const.TABLECOLS_],
                    page_size=5,
                    style_table={'height': '250px'},
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'textAlign': 'left',
                        'font-family': "Arial, Helvetica, sans-serif"
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'textAlign': 'left',

                    },
                    merge_duplicate_headers=True,
                    filter_action='native',
                    row_selectable='single'
                )
            ], className='pretty_container', style={'min-height': '40%'}),
            html.Div([
                dash_table.DataTable(
                    columns=[{'name': 'Selected', 'id': 'selected'}],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'textAlign': 'left',
                        'font-family': "Arial, Helvetica, sans-serif"
                    }
                ),
                html.Div([
                    html.Div(
                        html.Img(id='selected_image',
                                 style={'width': '100%', 'padding': '15px'}),
                        style={'width': '25%'}
                    ),
                    html.Div([
                        html.Details([
                            picture_input('edit')
                        ], style={'padding': '10px'}, open=True)
                    ], style={'width': '100%'})
                ], className='column')
            ], className='pretty_container')], className='content_body')
    ])

    return body


print(os.listdir('assets'))
print(os.listdir('assets/image_files'))


def __bottom_bar():
    bar = html.Footer([
        html.Img(
            src='/assets/image_files/62dace53548a498a9c06addec6b2e131.jpeg',
            style={'width': '100px'}
        )
    ], className='footer')

    return bar


def app_layout():
    content = html.Div([
        __header_bar(),
        __search_engine_ui(),
        __bottom_bar()
    ])

    return content

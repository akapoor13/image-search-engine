import dash_table
import src.constants as const
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def __header_bar():
    bar = html.Header([
        html.H1('Star Wars Episode XIII: The Image Search Engine')
    ], className='header row')

    return bar


def __search_engine_ui():
    search_input = html.Div(
        dcc.Input(id='search_bar', placeholder='Enter description', style={'width':'100%', 'font-family': 'Arial, Helvetica, sans-serif'}), 
        id='input-search-bar', style={'margin-right':'10px'}
    )

    dropdown = html.Div([
        html.Summary('Search Type', style={'font-family': 'Arial, Helvetica, sans-serif'}),
        dcc.Dropdown(
            id='input-option',
            options=[{'label':' '.join(i.split('_')).title(), 'value':i} for i in const.input_type],
            value=const.default_input_type,
            style={
                'font-family': 'Arial, Helvetica, sans-serif'
            },
            clearable=False
        )]
    )

    modal = html.Div(
        [
            dbc.Button("Search Bar", id="open", className='button', style={'margin-left':'10px', 'margin-top':'10px'}),
            dbc.Modal(
                [
                    dbc.ModalBody(
                        [
                            dropdown,
                            html.Div([
                                search_input,
                                dbc.Button("Search", id="search-btn", className="ml-auto", style={'margin-top':'5px'})
                            ], style={'margin-top':'1%'})
                        ], style={'margin-top':'5%', 'margin-bottom':'5%'}
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
        ]
    )

    body = html.Section([
        html.Div(modal, style={'margin-bottom':'15px'}),
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='results_table',
                    columns=[{'name':['Results'] + [const.col_mapping[i]], 'id':i} for i in const.table_columns],
                    page_size=5,
                    style_table={'height': '250px'},
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'textAlign':'left'
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
                        'textAlign' : 'left'
                    },
                    merge_duplicate_headers=True,
                    filter_action='native'
                )
            ], className='pretty_container', style={'min-height':'45%'}),
            html.Div([
                dash_table.DataTable(
                    columns=[{'name':'Selected', 'id':'selected'}],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'textAlign' : 'left'
                    }
                )
            ], className='pretty_container', style={'min-height':'25%'})
        ], id='content_body')
    ], className='body row')

    return body


def __bottom_bar():
    bar = html.Footer([
        html.Img(
            src='assets/clone_wars_logo.jpeg', 
            style={'width':'6%', 'margin-top':'0.2%'}
        )
    ], className='footer row')

    return bar


def app_layout():
    content = html.Div([
        __header_bar(),
        __search_engine_ui(),
        __bottom_bar()
    ])

    return content
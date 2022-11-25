import base64
import datetime
import io

import pandas as pd
from dash import callback, register_page, dcc, html, dash_table
from dash.dependencies import Input, Output, State

from project.app.multi_page_nested_folders.system_data import app_data_handler

"---------------------------------- Hard codded configuration for some of the Styles ----------------------------------"

DROP_FILES_AREA_STYLE = {'width': '100%',
                         'height': '60px',
                         'lineHeight': '60px',
                         'borderWidth': '1px',
                         'borderStyle': 'dashed',
                         'borderRadius': '5px',
                         'textAlign': 'center',
                         'marginLeft': '5%'}

DOWNLOAD_CSV_FILES_STYLE = {'margin-left': '40%',
                            'width': '50%',
                            'height': '30px',
                            'lineHeight': '30px',
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px'}

DATATABLE_OUTPUT_HEADER_STYLE = {'backgroundColor': 'white',
                                 'textAlign': 'center',
                                 'fontWeight': 'bold',
                                 'marginLeft': '5%',
                                 'borderRadius': '5px'}

GADGETS_MARGIN = {'marginLeft': '10%'}
# need this list to store when the user clicked the button to download a
# csv file
list_of_last_clicks_numbers = []


def get_reports_names() -> list:
    """
    Using this function to get the user input files from the local system data storage.
    Taking only the csv files from that directory by the if statement that check the end of the filenames.
    """
    all_files = app_data_handler.get_files_names("user_input_files")
    # returning only csv files
    return [val for val in all_files if val.endswith(".csv")]


register_page(__name__, icon="ep:setting")

layout = html.Div([
    html.Br(),
    html.H5("Import the following files:"),
    dcc.Markdown("""
             * box_amount.csv - this file contain the box names, amount and priority of boxes
             * con_amount.csv - amount of the containers form each type
             * box_properties.csv - the properties for each type of box (sizes)
             * con_properties.csv - the properties for each type of container (sizes)
             """),
    dcc.Upload(
        id='upload-data1',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style=DROP_FILES_AREA_STYLE,
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload1'),

    # letting the user watch his files / download them
    html.Br(),
    html.H5("View and Download the existing problem configuration files:"),
    dcc.Dropdown(get_reports_names(), get_reports_names()
                 [0], id='graph_selected'),
    html.Br(),
    html.Button("Download CSV", id="btn_csv",
                style=DOWNLOAD_CSV_FILES_STYLE),
    dcc.Download(id="download-user-csv"),
    html.Div(id="selected_file", style=GADGETS_MARGIN),
], style=GADGETS_MARGIN)


def parse_contents(contents, filename, date) -> html.Div:
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
        app_data_handler.user_input_csv(filename, df)
    except Exception as e:
        print(f'error while using parse_contents {e}')
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6("last updated " + str(datetime.datetime.fromtimestamp(date))),
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),
    ])


@callback(Output('output-data-upload1', 'children'),
          Input('upload-data1', 'contents'),
          State('upload-data1', 'filename'),
          State('upload-data1', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates) -> list:
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@callback(
    Output("download-user-csv", "data"),
    Input("btn_csv", "n_clicks"),
    Input("graph_selected", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, g_number):
    if n_clicks is not None and n_clicks not in list_of_last_clicks_numbers:
        # Only if the user had clicked the button
        list_of_last_clicks_numbers.append(n_clicks)
        df = app_data_handler.get_csv_without_index(
            f"user_input_files/{g_number}")
        return dcc.send_data_frame(app_data_handler.get_csv_file(
            f"user_input_files/{g_number}").to_csv, f"{g_number}")

        # return dcc.send_data_frame(app_data_handler.get_csv_file(f"user_input_files/{g_number}").to_csv,
        # f"{g_number}", style={'borderRadius': '5px'})


@callback(
    Output("selected_file", "children"),
    Input("graph_selected", "value"),
)
def display_color(g_number) -> html.Div:
    if g_number is not None:
        df = app_data_handler.get_csv_file(f"user_input_files/{g_number}")
        x = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={'textAlign': 'left'},
            style_header=DATATABLE_OUTPUT_HEADER_STYLE,
            editable=True)
        return html.Div([
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_cell={'textAlign': 'left'},
                style_header=DATATABLE_OUTPUT_HEADER_STYLE,
                editable=True)
        ])
    else:
        return html.Div([
            html.P("Please select a report")
        ])

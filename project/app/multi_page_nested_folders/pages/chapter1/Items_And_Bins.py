# import base64
# import datetime
# import io
# import pandas as pd
# from dash import callback, register_page, dcc, html, dash_table
# from dash.dependencies import Input, Output, State
# from app.multi_page_nested_folders.system_data import app_data_handler
# from dash import Dash, dcc, html
# from dash.exceptions import PreventUpdate
# from dash import Dash, html, dcc, Input, Output, dash_table
# from dash.exceptions import PreventUpdate
# import collections
# import pandas as pd
# import dash_mantine_components as dmc
# import logging as log
#
# """
# Need to create two pages,
# One for the definition of the box, item.
# And the other is for other is for amount of bins, boxes of the current problem.
#
# This way we will have 4 dcc.store's for each user dataframe.
# Might use definition
# """
# # log.basicConfig(level=log.INFO,
# #                 filename=app_data_handler.get_logs_path(__name__.replace('.', '_')),
# #                 filemode="w",
# #                 format="%(asctime)s - line: %(lineno)d - module: %(name)s - %(message)s")
#
#
# """
# Steps:
# 1. initialize the data tables that are needed with default values
# 2. show the tables to the user and let him to be able to edit.
# 3. create function to save the user changes so other dependencies will update.
# """
#
# "---------------------------------- Hard codded configuration for some of the Styles ----------------------------------"
#
# DROP_FILES_AREA_STYLE = {'width': '100%',
#                          'height': '60px',
#                          'lineHeight': '60px',
#                          'borderWidth': '1px',
#                          'borderStyle': 'dashed',
#                          'borderRadius': '5px',
#                          'textAlign': 'center',
#                          'marginLeft': '5%'}
#
# DOWNLOAD_CSV_FILES_STYLE = {'margin-left': '40%',
#                             'width': '50%',
#                             'height': '30px',
#                             'lineHeight': '30px',
#                             'borderWidth': '1px',
#                             'borderStyle': 'solid',
#                             'borderRadius': '5px'}
#
# DATATABLE_OUTPUT_HEADER_STYLE = {'backgroundColor': 'white',
#                                  # 'textAlign': 'center',
#                                  'fontWeight': 'bold',
#                                  'marginLeft': '15%',
#                                  'borderRadius': '5px',
#                                  }
#
# GADGETS_MARGIN = {'marginLeft': '10%'}
# list_of_last_clicks_numbers_amount = []  # need this list to store when the user clicked the button to download a csv file
#
#
# def get_reports_names() -> list:
#     """
#     Using this function to get the user input files from the local system data storage.
#     Taking only the csv files from that directory by the if statement that check the end of the filenames.
#     """
#     all_files = app_data_handler.get_files_names("user_input_files")
#     return [val for val in all_files if val.endswith(".csv")]  # returning only csv files
#
#
# register_page(__name__, icon="octicon:container-24")
# # log.info(f"register_page {__name__}")
#
# # This stylesheet makes the buttons and table pretty.
#
#
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
#
# layout = dmc.Container([
#     dcc.Dropdown(get_reports_names(), get_reports_names()[0],
#                  id='graph_selected',
#                  style={'width': '70%',
#                         'marginLeft': '20%'}),
#     html.Div([
#         dash_table.DataTable(
#             id='memory-table',
#             columns=[{'name': i, 'id': i} for i in df.columns],
#             editable=True
#         )
#     ], style=DATATABLE_OUTPUT_HEADER_STYLE)
# ],
#     style=DATATABLE_OUTPUT_HEADER_STYLE,
#     fluid=True,
# )
#
#
# @callback(Output('all_user_files', 'data'),
#           Input('graph_selected', 'value'),
#           )
# def on_data_set_table(ch):
#     """
#     Need to use the memory-output!!
#     It's best if all df can be saved in it with the default df of the user input.
#     The selection of the user is working! but not in use... it should take from the local memory the relevant df
#     accounting to user choice (ch value).
#     Ones the df is updating, it should be used in other parts of the app, and make sure that all connection to the db
#     are handled by only but the local memory (store) and not by any real local file.
#     In addition, need to initialize the default df from the local files, but those files are used only for starting the
#     app.
#     :param default_data:
#     :param updated_data:
#     :param ch: what the user selected
#     :return:
#     """
#     # log.info(f"used on_data_set_table {ch}")
#     system_data = app_data_handler.get_csv_without_index("user_input_files/" + ch)
#     return {ch: system_data.to_dict('records')}
#
#
# @callback(Output('memory-table', 'data'),
#           Input('memory-output', 'data'),
#           Input('memory-table', 'data'),
#           Input('graph_selected', 'value'),
#           Input('all_user_files', 'data'),   #all_user_files
#           )
# def on_data_set_table(default_data, updated_data, ch, all_user_files):
#     """
#     Need to use the memory-output!!
#     It's best if all df can be saved in it with the default df of the user input.
#     The selection of the user is working! but not in use... it should take from the local memory the relevant df
#     accounting to user choice (ch value).
#     Ones the df is updating, it should be used in other parts of the app, and make sure that all connection to the db
#     are handled by only but the local memory (store) and not by any real local file.
#     In addition, need to initialize the default df from the local files, but those files are used only for starting the
#     app.
#     :param default_data:
#     :param updated_data:
#     :param ch: what the user selected
#     :return:
#     """
#     # log.info(f"used on_data_set_table {ch}")
#     system_data = app_data_handler.get_csv_without_index("user_input_files/" + ch)
#     # log.info(f"the default data is {system_data}")
#     if updated_data is None:
#         return default_data  # if there is no data it mean it's the first run, so the default data will be returned.
#     else:
#         return updated_data
#         # raise PreventUpdate # Can be used if any need to not update...
#
# # layout = html.Div([
# #     html.Br(),
# #     html.H5("Import the following files:"),
# #     dcc.Markdown("""
# #              * box_amount.csv - this file contain the box names, amount and priority of boxes
# #              * con_amount.csv - amount of the containers form each type
# #              * box_properties.csv - the properties for each type of box (sizes)
# #              * con_properties.csv - the properties for each type of container (sizes)
# #              """),
# #     dcc.Upload(
# #         id='upload-data1',
# #         children=html.Div([
# #             'Drag and Drop or ',
# #             html.A('Select Files')
# #         ]),
# #         style=DROP_FILES_AREA_STYLE,
# #         # Allow multiple files to be uploaded
# #         multiple=True
# #     ),
# #     html.Div(id='output-data-upload1'),
# #
# #     # letting the user watch his files / download them
# #     html.Br(),
# #     html.H5("View and Download the existing problem configuration files:"),
# #     dcc.Dropdown(get_reports_names(), get_reports_names()[0], id='graph_selected'),
# #     html.Br(),
# #     html.Button("Download CSV", id="btn_csv",
# #                 style=DOWNLOAD_CSV_FILES_STYLE),
# #     dcc.Download(id="download-user-csv"),
# #     html.Div(id="selected_file", style=GADGETS_MARGIN),
# # ], style=GADGETS_MARGIN)
# #
# #
# # def parse_contents(contents, filename, date) -> html.Div:
# #     content_type, content_string = contents.split(',')
# #     decoded = base64.b64decode(content_string)
# #     try:
# #         df = pd.read_csv(
# #             io.StringIO(decoded.decode('utf-8')))
# #         app_data_handler.user_input_csv(filename, df)
# #     except Exception as e:
# #         print(f'error while using parse_contents {e}')
# #         return html.Div([
# #             'There was an error processing this file.'
# #         ])
# #
# #     return html.Div([
# #         html.H5(filename),
# #         html.H6("last updated " + str(datetime.datetime.fromtimestamp(date))),
# #
# #         dash_table.DataTable(
# #             df.to_dict('records'),
# #             [{'name': i, 'id': i} for i in df.columns]
# #         ),
# #         html.Hr(),
# #     ])
# #
# #
# # @callback(Output('output-data-upload1', 'children'),
# #           Input('upload-data1', 'contents'),
# #           State('upload-data1', 'filename'),
# #           State('upload-data1', 'last_modified'))
# # def update_output(list_of_contents, list_of_names, list_of_dates) -> list:
# #     if list_of_contents is not None:
# #         children = [
# #             parse_contents(c, n, d) for c, n, d in
# #             zip(list_of_contents, list_of_names, list_of_dates)]
# #         return children
# #
# #
# # @callback(
# #     Output("download-user-csv", "data"),
# #     Input("btn_csv", "n_clicks"),
# #     Input("graph_selected", "value"),
# #     prevent_initial_call=True,
# # )
# # def func(n_clicks, g_number):
# #     if n_clicks is not None and n_clicks not in list_of_last_clicks_numbers_amount:
# #         list_of_last_clicks_numbers_amount.append(n_clicks)    # Only if the user had clicked the button
# #         df = app_data_handler.get_csv_without_index(f"user_input_files/{g_number}")
# #         print(df)
# #         return dcc.send_data_frame(app_data_handler.get_csv_file(f"user_input_files/{g_number}").to_csv,
# #                                    f"{g_number}")
# #
# #         # return dcc.send_data_frame(app_data_handler.get_csv_file(f"user_input_files/{g_number}").to_csv,
# #         #                            f"{g_number}", style={'borderRadius': '5px'})
# #
# #
# # @callback(
# #     Output("selected_file", "children"),
# #     Input("graph_selected", "value"),
# # )
# # def display_color(g_number) -> html.Div:
# #     if g_number is not None:
# #         df = app_data_handler.get_csv_file(f"user_input_files/{g_number}")
# #         x = dash_table.DataTable(
# #                 data=df.to_dict('records'),
# #                 columns=[{'name': i, 'id': i} for i in df.columns],
# #                 style_cell={'textAlign': 'left'},
# #                 style_header=DATATABLE_OUTPUT_HEADER_STYLE,
# #                 editable=True)
# #         return html.Div([
# #             dash_table.DataTable(
# #                 data=df.to_dict('records'),
# #                 columns=[{'name': i, 'id': i} for i in df.columns],
# #                 style_cell={'textAlign': 'left'},
# #                 style_header=DATATABLE_OUTPUT_HEADER_STYLE,
# #                 editable=True)
# #         ])
# #     else:
# #         return html.Div([
# #                    html.P("Please select a report")
# #                 ])

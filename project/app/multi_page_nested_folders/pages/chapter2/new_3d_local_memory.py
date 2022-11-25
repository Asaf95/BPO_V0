# import pandas as pd
# from dash.exceptions import PreventUpdate
# from dash import Dash, html, dcc, Output, Input, callback, dash_table, register_page
# import plotly.express as px
# from app.multi_page_nested_folders.system_data import app_data_handler
#
# register_page(__name__, icon="iconoir:stats-report", suppress_callback_exceptions=True)
#
#
# def get_reports_names():
#     return app_data_handler.get_files_names("packing_results")
#
#
# layout = html.Div(
#     [
#         html.Div([
#             html.Div(id='graph1', children=[], className='six columns'),
#         ], className='row'),
#
#     ],
#     style={'margin-left': '70px'}
# )
#
#
# # @callback(Output('test-memory-table', 'data'),
# #           Input('boxes_definition_data', 'data'))
# # def on_data_set_table(data):
# #     print(data)
# #     if data is None:
# #         raise PreventUpdate
# #
# #     return data
#
#
# @callback(
#     Output('graph1', 'children'),
#     Input('boxes_definition_data', 'data')
# )
# def create_graph1(data):
#     print(type(data))
#     dff = pd.DataFrame(data)
#     fig1 = px.line(dff, x='key', y='x', color='continent')
#     return dcc.Graph(figure=fig1)

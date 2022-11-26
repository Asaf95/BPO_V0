# from dash import html, Input, Output, State, callback, register_page
# from dash import Dash, dash_table, dcc, html
# from dash.dependencies import Input, Output
# import pandas as pd
# from pathlib import Path
# from appmulti_page_nested_folders import data_converter
#
#
# def get_number_of_box(**kwargs) -> pd.DataFrame:
#     """
#     this function returns / create a pd.DataFrame with a column of the amount of boxes,in this page the user
#     can change the amount of boxes and it will be updated to the db
#     :return:
#     """
#
#     amount_of_boxes_file = Path("system_data/box_amount.csv")
#     box_properties_file = Path("system_data/box_properties.csv")
#     #
#     if amount_of_boxes_file.is_file() and not pd.read_csv(r'system_data/box_amount.csv').empty:
#         print('get_number_of_box pass passed amount_of_boxes_file existent')
#         # if the amount of boxed file exists
#
#         if 'updated_amount_of_box_df' in kwargs:
#             print('error 26')
#             amount_of_boxes_df = kwargs.get("updated_amount_of_box_df")
#             print(amount_of_boxes_df.columns)
#             if len(amount_of_boxes_df.columns) != 2:
#                 print(f'the amount of boxes df is too big!!!')
#                 amount_of_boxes_df = amount_of_boxes_df[['Box_type', 'Amount_per_box']]
#
#             if 'Amount_per_box' in amount_of_boxes_df.columns:
#                 amount_of_boxes_df = amount_of_boxes_df[["Box_type", "Amount_per_box"]]
#             else:
#                 new_amount_of_boxes_df = amount_of_boxes_df.copy()
#                 new_amount_of_boxes_df = new_amount_of_boxes_df[['Box_type']].set_index('Box_type')
#                 new_amount_of_boxes_df['Amount_per_box'] = 1
#                 amount_of_boxes_df = new_amount_of_boxes_df
#         else:
#             amount_of_boxes_df = pd.read_csv(r'system_data/box_amount.csv', index_col=0)
#             amount_of_boxes_df.reset_index(drop=True)
#
#     elif box_properties_file.is_file():
#         print('get_number_of_box pass passed box_properties_file existent')
#
#         # if not, creating the file using the box_pro file to know which boxes we have
#         box_properties_df = pd.read_csv(r'system_data/box_properties.csv', index_col=False)
#         box_properties_df.reset_index(drop=True)
#         box_properties_df['Amount_per_box'] = 1
#         amount_of_boxes_df = box_properties_df[['Box_type', 'Amount_per_box']]
#     else:
#         print('returned amount_of_boxes_df is empty DataFrame ')
#         amount_of_boxes_df = pd.DataFrame()
#     print(amount_of_boxes_df)
#     return amount_of_boxes_df
#
#
# def get_container_sizes() -> str:
#     """
#     this function returns the sizes of the container from the db
#     :return:
#     """
#     container_values_file = Path("system_data/container_values.csv")
#     if container_values_file.is_file() and not pd.read_csv(r'system_data/container_values.csv').empty:
#         container_values_df = pd.read_csv(r'system_data/container_values.csv', index_col=False)
#         return container_values_df.to_string()
#     else:
#         return ''
#
#
# register_page(__name__, icon="bi:box")
#
# layout = html.Div([
#     # html.Button("Get data", id="get-data-button2"),
#     html.H5("Please Enter the size of the bin", style={'marginLeft': '10%'}),
#     dcc.Input(id="X_bin", placeholder="X - Length", style={'marginLeft': '5%', 'textAlign': 'center'}),
#     dcc.Input(id="Y_bin", placeholder="Y - Width", style={'textAlign': 'center', 'margin': '10px'}),
#     dcc.Input(id="Z_bin", type="number", placeholder="Z - Height", style={'textAlign': 'center'}),
#     dcc.Input(id="number_of_bins", type="number", placeholder="Number of Bins", debounce=True,
#               style={'textAlign': 'center', 'margin': '10px'}),
#
#     html.Div(id="bin_size_output"),
#     dash_table.DataTable(
#         id='datatable-interactivity',
#         columns=[
#             {"name": i, "id": i, "deletable": True, "selectable": True} for i in get_number_of_box().columns
#         ],
#         data=get_number_of_box().to_dict('records'),
#         editable=True,
#         selected_columns=[],
#         selected_rows=[],
#         page_current=0,
#         page_size=10,
#     ),
#     html.Div(id='datatable-interactivity-container')
# ])
#
#
# @callback(
#     Output("bin_size_output", "children"),
#     Input("X_bin", "value"),
#     Input("Y_bin", "value"),
#     Input("Z_bin", "value"),
#     Input("number_of_bins", "value"),)
# def update_output(X_bin, Y_bin, Z_bin, number_of_bins):
#     if X_bin and Y_bin and Z_bin and number_of_bins is not None:
#         data_converter.convert_container_values(X_bin, Y_bin, Z_bin, number_of_bins)  # convert the user input to the backen
#         return u'X_bin {} and Y_bin {} and Z_bin {} and number_of_bins {}'.format(X_bin, Y_bin, Z_bin, number_of_bins)
#     else:
#         return get_container_sizes()
#         #   @TODO: add here callback form db with the values if exists
#         # return u'X_bin {} and Y_bin {} and Z_bin {} and number_of_bins {}'.format(X_bin, Y_bin, Z_bin, number_of_bins)
#         pass
#
#
# @callback(
#     Output('datatable-interactivity', 'style_data_conditional'),
#     Input('datatable-interactivity', 'selected_columns')
# )
# def update_styles(selected_columns):
#     return [{
#         'if': {'column_id': i},
#         'background_color': '#D2F3FF'
#     } for i in selected_columns]
#
#
# @callback(
#     Output('datatable-interactivity-container', "children"),
#     [Input('datatable-interactivity', "derived_virtual_data"),
#      Input('datatable-interactivity', "derived_virtual_selected_rows"),
#      Input('datatable-interactivity', "selected_cells")])
# def update_graphs(rows, derived_virtual_selected_rows, active_cells_a):
#
#     amount_of_boxes_df = get_number_of_box() if rows is None else pd.DataFrame(rows)
#     amount_of_boxes_df.reset_index(drop=True)
#     if len(amount_of_boxes_df.columns) != 2:
#         amount_of_boxes_df = amount_of_boxes_df[['Box_type', 'Amount_per_box']]
#     amount_of_boxes_df.to_csv(r'system_data/box_amount.csv', encoding='utf-8')
#     amount_of_boxes_df = get_number_of_box(updated_amount_of_box_df=amount_of_boxes_df)
#     import time
#     return f'last updated: {time.strftime("%H:%M:%S", time.localtime())}'

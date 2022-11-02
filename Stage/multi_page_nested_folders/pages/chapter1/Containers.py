"""
____MODEL_INFO____
Need to create two pages,
One for the definition of the container, item.
And the other is for other is for amount of bins, containers of the current problem.

This way we will have 4 dcc store for each user dataframe.
Might use definition
"""
# TODO: WATCH THIS!!
# https://www.youtube.com/watch?v=v969_M6cWk0&ab_channel=Fireship

import logging as log

import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc, Input, Output, dash_table, callback, register_page
from dash.dependencies import State

from Stage.multi_page_nested_folders import constants_bpo
from Stage.multi_page_nested_folders.system_data import app_data_handler, const_system_data

log.basicConfig(
    level=log.INFO,
    filename=app_data_handler.get_logs_path(
        __name__.replace(
            '.',
            '_')),
    filemode="a",
    format="%(asctime)s - line: %(lineno)d - module: %(name)s - %(message)s")

list_of_last_clicks_numbers_amount = []
list_of_last_clicks_numbers_define = []
# need this list to store when the user clicked the button to download a
# csv file

register_page(__name__, icon="fluent:bin-full-20-regular",
              suppress_callback_exceptions=True)

log.info(f"register_page {__name__}")


def update_datatables_and_internal_app_data(
        current_containers_def_df,
        n_clicks,
        columns,
        table_name,
        list_of_last_clicks):
    """
    This function update the local storage and the user DataTable in the UI.
    This is done by getting user-editable-containers-input, and updating the user-editable-containers-input back and the local
    storage, if this was the first "run" of the app the user will get the default df for containers definition
    :param list_of_last_clicks:
    :param table_name:
    :param columns:
    :param n_clicks:
    :param current_containers_def_df:
    """
    if n_clicks != 0 and n_clicks not in list_of_last_clicks:
        # Only if the user had clicked the button
        list_of_last_clicks.append(n_clicks)
        current_containers_def_df.append({c['id']: '' for c in columns})

    log.info(
        f"used update_store_data_of_containers_amount_data\n current_containers_def_df is {current_containers_def_df} ")
    if current_containers_def_df is None or len(current_containers_def_df) == 0:
        log.info(
            f"current_containers_def_df was none, getting the default dataframe for containers")
        updated_dict = app_data_handler.get_csv_without_index(
            const_system_data.USER_INPUT_FILES_LOC.get(table_name)).to_dict('records')
    else:
        log.info(f"current_containers_def_df len is was updated")
        updated_dict = pd.DataFrame(current_containers_def_df).to_dict('records')
        app_data_handler.input_files_input(const_system_data.USER_INPUT_FILES_LOC.get(
            table_name), pd.DataFrame(current_containers_def_df))  # Updating the local data
    return updated_dict, updated_dict


load_containers = dmc.Navbar(
    width={'base': '35%'},
    fixed=True,
    position={"top": 300, "left": 430},
    style=constants_bpo.MAIN_LAYOUT_STYLE,  # backgroundColor for the menu
    children=[
        html.Br(),
        dcc.Markdown(
            """
            #### add the containers to pack
            You need to write which kind of container,     
            how many of that item and the priority of them.    
            The items will be added to the according to the the priority that you had set,    
            if there won't be any more space,       
            containers with low priority won't be conclude in the final pack.
            """,
            link_target="_blank",
        ),
        html.Div([
            dash_table.DataTable(
                id='user-editable-containers-input',
                columns=[{'name': i, 'id': i} for i in
                         app_data_handler.get_csv_without_index(
                             const_system_data.USER_INPUT_FILES_LOC.get('container_amount')).columns],
                editable=True,
                row_deletable=True,
                style_header=constants_bpo.DATATABLE_HEADER_STYLE,
                style_data=constants_bpo.USER_BOX_DATATABLE_STYLE,
                page_size=12,  # we have fewer data in this example, so setting to 20
                style_table=constants_bpo.STYLE_TABLE_BOX
            )],
            style=constants_bpo.DEFAULT_COMPONENT_CENTER),
        dmc.Space(h=10),
        html.Div([
            html.Button('Add Row',
                        id='add-row-button',
                        n_clicks=0,
                        style=constants_bpo.BUTTON_STYLE,
                        title='Add Row'),
        ]),
    ]
)

containers_define = dmc.Navbar(
    width={'base': '35%'},
    fixed=True,
    position={"top": 300, "left": 1123},
    style=constants_bpo.MAIN_LAYOUT_STYLE,  # backgroundColor for the menu
    children=[
        html.Br(),
        dcc.Markdown(
            """
            #### add the containers to pack
            You need to write which kind of container, how many of that item and the priority of them.      
            The items will be added to the according to the the priority that you had set, if there won't be any more
            space, containers with low priority won't be conclude in the final pack.
            """,
            link_target="_blank",
        ),
        html.Div([
            dash_table.DataTable(
                id='user-editable-containers-input-de',
                columns=[{'name': i, 'id': i} for i in
                         app_data_handler.get_csv_without_index(
                             const_system_data.USER_INPUT_FILES_LOC.get('container_properties')).columns],
                editable=True,
                row_deletable=True,
                style_header=constants_bpo.DATATABLE_HEADER_STYLE,
                style_data=constants_bpo.USER_BOX_DATATABLE_STYLE,
                page_size=12,  # we have fewer data in this example, so setting to 20
                style_table=constants_bpo.STYLE_TABLE_BOX
            )],
            style=constants_bpo.DEFAULT_COMPONENT_CENTER),
        dmc.Space(h=10),
        html.Div([
            html.Button('Add Row',
                        id='add-row-button-de',
                        n_clicks=0,
                        style=constants_bpo.BUTTON_STYLE,
                        title='Add Row'),
        ]),
    ]
)


@callback(Output('containers_amount_data', 'data'),
          Output('user-editable-containers-input', 'data'),
          Input('user-editable-containers-input', 'data'),
          Input('add-row-button', 'n_clicks'),
          State('user-editable-containers-input', 'columns')
          )
def update_store_data_of_containers_amount_data(
        current_containers_def_df, n_clicks, columns):
    return update_datatables_and_internal_app_data(
        current_containers_def_df,
        n_clicks,
        columns,
        "container_amount",
        list_of_last_clicks_numbers_amount)


@callback(Output('containers_definition_data', 'data'),
          Output('user-editable-containers-input-de', 'data'),
          Input('user-editable-containers-input-de', 'data'),
          Input('add-row-button-de', 'n_clicks'),
          State('user-editable-containers-input-de', 'columns')
          )
def update_store_data_of_containers_amount_data(
        current_containers_def_df, n_clicks, columns):
    return update_datatables_and_internal_app_data(
        current_containers_def_df,
        n_clicks,
        columns,
        "container_properties",
        list_of_last_clicks_numbers_define)


Page_Description = dmc.Navbar(
    fixed=True,
    width={'base': '70%'},
    position={"top": 50, "left": 450},
    style=constants_bpo.MAIN_LAYOUT_STYLE,  # backgroundColor for the menu
    children=[
        dmc.Divider(style={'textAlign': 'center'}),
        html.H2("Define and Load the containers",
                style={'textAlign': 'center'}),
        dmc.Divider(style={'textAlign': 'center'}),
        dcc.Markdown("""
        First step of solving the packing problem, we need to define the containers that will be loaded to the bins.    
        In the right table you will define the sizes and the weight
        In the left table you will need to write how many from each container you have (and the their rooty).    
        """),

    ]
)

layout = dmc.Container([
    dcc.Store(id='containers_amount_data', data={}, storage_type='local'),
    dcc.Store(id='containers_definition_data', data={}, storage_type='local'),
    Page_Description,
    dmc.Container([
        html.Div([html.Div([load_containers]),
                  html.Div([containers_define])
                  ]),
    ], fluid=False),
],
    style=constants_bpo.DEFAULT_COMPONENT_CENTER,
)

# TODO: Can help with using this function for all users data's
# https://dash.plotly.com/dash-core-components/store
# Might need to combine the two function into one, this way "adding row" and changing the values in table will have the
# Same Returned callback (the table), if the click nub will be different a
# row will be added.


# TODO: add popup with what is each item
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/modal/

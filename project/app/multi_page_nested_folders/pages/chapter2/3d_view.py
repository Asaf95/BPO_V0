"""
this Page contains the 3D graph together with the page
"""

import plotly.graph_objs
from dash import dcc
from dash import html, callback, register_page
from dash.dependencies import Input, Output

from project.app.multi_page_nested_folders import constants_bpo
from project.app.multi_page_nested_folders.bin_packing_solver import solver
from project.app.multi_page_nested_folders.system_data import app_data_handler


# start here :)


def create_3d_graph(fig):
    """
    this function create the layout of the figure on the UI.
    From here the location / size of the graph can be changed.
    :param fig:
    :return:
    """
    return fig.update_layout(autosize=True,
                             margin={"l": 0, "r": 0, "t": 40, "b": 0},
                             width=1200,
                             height=10000,
                             # height=600 * len(connection_bp_to_db.get_containers_bp_format()),
                             # xanchor='center',
                             legend=dict(xanchor="center", x=1, y=1),
                             scene=dict(
                                 camera=dict(eye=dict(x=1, y=1, z=1)),
                                 aspectratio=dict(x=0.75, y=0.75, z=0.75),
                                 aspectmode="manual",
                             ),
                             )


register_page(__name__, icon="material-symbols:3d-rotation")


layout = html.Div(
    [
        html.H2("How the Bins are packed",
                style=constants_bpo.MAIN_3D_LAYOUT_STYLE),
        html.Button('Refresh 3d Graph', id='submit-button', n_clicks=0,
                    style=constants_bpo.BUTTON_STYLE),
        dcc.Graph(id="3d-graph",
                  style=constants_bpo.MAIN_3D_LAYOUT_STYLE)
    ]
)


@callback(
    Output("3d-graph", "figure"),
    Input("submit-button", "n_clicks"),
)
def display_color(click: int) -> plotly.graph_objs.Figure:
    """
    if the user click the button the graph will be showed, and the current copy of the figure will be saved locally.
    if the user didn't click the button the last figure that were saved will be returned
    :param click:
    :return:
    """
    if click != 0:  # if the button was clicked
        last_fig = solver.get_3d_graph()
        app_data_handler.save_locally_pickle_file(
            "stored_object", last_fig)   # Saving the figure as the last fig
        return create_3d_graph(solver.get_3d_graph())
    else:
        # Getting and returning the last figure from the local app data.
        return create_3d_graph(
            app_data_handler.get_pickle_file("stored_object"))

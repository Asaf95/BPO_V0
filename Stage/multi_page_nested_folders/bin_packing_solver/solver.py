"""
This module contain the Bin Packing solver and create the 3d fig.
The code is based on the following example
https://stackoverflow.com/questions/71318810/interactive-3d-plot-with-right-aspect-ratio-using-plotly
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from py3dbp import Packer, Bin, Item

from Stage.multi_page_nested_folders.bin_packing_solver import connection_bp_to_db, solution_publisher


def add_item_to_packing(item):
    def __resize_item_according_to_vertices(
            xmin=0, ymin=0, zmin=0, xmax=1, ymax=1, zmax=1):
        """ resize_item_according_to_vertices"""
        return {
            "x": [xmin, xmin, xmax, xmax, xmin, xmin, xmax, xmax],
            "y": [ymin, ymax, ymax, ymin, ymin, ymax, ymax, ymin],
            "z": [zmin, zmin, zmin, zmin, zmax, zmax, zmax, zmax],

            "i": [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            "j": [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            "k": [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        }

        # take a packer item and build parameters to a plotly mesh3d cube

    colors = ["crimson", "limegreen", "green",
              "red", "cyan", "magenta", "yellow"]

    ret = __resize_item_according_to_vertices(
        *item.position, *[sum(x)
                          for x in zip(item.position, item.get_dimension())]
    )
    ret["name"] = item.name
    ret["color"] = colors[ord(item.name.split("_")[0][-1]) - ord("A")]
    return ret


def make_the_packing():
    packer = Packer()

    for i, t in enumerate(connection_bp_to_db.get_containers_bp_format()):
        packer.add_bin(Bin("40HC-" + str(i + 1),    # Name
                           *t,  # width, height, depth, max_weight
                           # 18000.0 # max_weight
                           ))

    for name, cfg in connection_bp_to_db.get_boxes_bp_format().items():
        for i in range(cfg["n"]):
            packer.add_item(Item(f"{name}_{i}",
                                 *cfg["s"]))

    packer.pack(bigger_first=False, distribute_items=False,
                number_of_decimals=3)
    return packer


def get_3d_graph():
    """
    this function create the plotly graph using the packing function
    https://plotly.com/python/3d-mesh/#mesh-cube

    :return:
    """
    packer = make_the_packing()
    # create a multi-plot figure for each bin
    fig = make_subplots(rows=len(packer.bins),
                        cols=1,
                        specs=[[{"type": "mesh3d"}] for _
                               in range(len(connection_bp_to_db.get_containers_bp_format()))],
                        subplot_titles=[f"Bin {i}" for i
                                        in range(len(connection_bp_to_db.get_containers_bp_format()))]
                        )
    # add a trace for each packer item
    for row, pbin in enumerate(packer.bins):
        for item in pbin.items:
            fig.add_trace(go.Mesh3d(add_item_to_packing(item)),
                          row=row + 1,
                          col=1)
    # publishing the results to the report generated
    solution_publisher.get_general_result_report(packer)
    return fig

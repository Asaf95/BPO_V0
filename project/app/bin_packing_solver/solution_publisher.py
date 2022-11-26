"""
This module write to a local file the solution on the solver.
The local file will contain a record per each bin with the items that will be stored in them.
In addition to that each item in the bin will have his location in the bin (x,y,z).
The User will be able to download the file.
"""
import pandas as pd

from bin_packing_solver import connection_bp_to_db


def get_general_result_report(packer):
    """
    This function create the plotly graph using the packing function.
    The results are transformed to
    """
    for row, pbin in enumerate(packer.bins):
        priss = [(item.name, item.position, item.string())
                 for item in pbin.items]
        unfitted_items = [(item.name, item.string())
                          for item in pbin.unfitted_items]
        connection_bp_to_db.transform_results(
            f"packed{row}", pd.DataFrame(
                priss, columns=[
                    'Name', 'Position', 'Meta_Data']))

        connection_bp_to_db.transform_results(
            f"un_packed{row}", pd.DataFrame(
                unfitted_items, columns=[
                    'Name', 'Meta_Data']))

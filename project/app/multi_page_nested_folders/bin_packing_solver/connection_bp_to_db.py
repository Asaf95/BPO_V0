"""
The purpose of this module is to translate and connect the solver and the user input.
The user uploads csv files that are easy to read (and write), and the algorithm need to get information in a certain way
So the module solved the gap with the above functions.
It's also important to keep as undefended and modular each file / module, for that reason all the calls from the
bin_packing_solver to the system data will be using this module.
"""
import pandas as pd

from project.app.multi_page_nested_folders.system_data import const_system_data, app_data_handler


def get_containers_bp_format() -> pd.DataFrame:
    """
    formatting the containers to the bin format of the solver, it's done by aggregating the relevant user files and
    taking the part of that new DataFrame (that was created to aggregate the data).
    :return:
    """
    containers_merged = pd.merge(
        app_data_handler.get_csv_file(
            const_system_data.USER_INPUT_FILES_LOC['container_properties']),
        app_data_handler.get_csv_file(
            const_system_data.USER_INPUT_FILES_LOC['container_amount']),
        on=["key"])
    containers_merged_named = containers_merged.rename(
        columns=lambda col_name: col_name.strip())
    repeated_df = containers_merged_named.reindex(
        containers_merged_named.index.repeat(containers_merged_named.amount))
    # taking only the columns that are needed for the solver.
    return repeated_df[["x", "y", "z", "w"]].values.tolist()


def get_boxes_bp_format() -> dict:
    """
    formatting the boxes to the item format of the solver, it's done by aggregating the relevant user files and
    taking the part of that new DataFrame (that was created to aggregate the data).
    :return:
    """
    def features_of_box(i):
        return {"n": boxed_val["amount"][i],
                "s": boxed_prop[["x", "y", "z", "w"]].values.tolist()[0]}

    boxed_val = app_data_handler.get_csv_file(
        const_system_data.USER_INPUT_FILES_LOC['box_amount'])
    boxed_prop = app_data_handler.get_csv_file(
        const_system_data.USER_INPUT_FILES_LOC['box_properties'])
    # Sort the boxes according to priority
    boxed_val = boxed_val.sort_values(by=['priority'])

    return {boxed_val['key'][i]: features_of_box(
        i) for i in range(len(boxed_val['key']))}


def transform_results(name: str, df: pd.DataFrame) -> None:
    app_data_handler.packing_results(name + ".csv", df)

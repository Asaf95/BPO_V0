import base64
import os
import pickle

import pandas as pd

abs_path = os.path.dirname(__file__)


def get_logs_path(file_name):
    return abs_path + "/app_logs/" + file_name + ".txt"



def get_local_file(file_name):
    with open(abs_path + '/' + file_name + '.csv', 'r', encoding='utf8') as f:

        return pd.read_csv(f)


def get_csv_file(file_name):
    with open(abs_path + '/' + file_name, 'r', encoding='utf8') as f:
        df = pd.read_csv(f)
        return df.rename(columns=lambda x: x.strip())
        # return pd.read_csv(f)


def get_csv_without_index(file_name):
    with open(abs_path + '/' + file_name, 'r', encoding='utf8') as f:
        df = pd.read_csv(f, index_col=False)
        return df.rename(columns=lambda x: x.strip())


def user_input_csv(file_name, csv_file):
    csv_file.to_csv(f'{abs_path}/user_input_files/{file_name}',
                    index=False, header=True, encoding='utf-8-sig')


def input_files_input(file_name, csv_file):
    csv_file.to_csv(f'{abs_path}/{file_name}', index=False,
                    header=True, encoding='utf-8-sig')


def packing_results(file_name, df: pd.DataFrame):
    df.to_csv(f"{abs_path}/packing_results/{file_name}",
              index=False, header=True, encoding='utf-8-sig')


def get_files_names(dir_path=""):
    return [file for file in os.listdir(abs_path + '/' + dir_path)]


def save_locally_pickle_file(name_of_object, object_to_save):
    # file_to_store = open(f"{name_of_object}.pickle", "wb")
    file_to_store = open(
        f"{abs_path}/pickle_objects/{name_of_object}.pickle", "wb")

    pickle.dump(object_to_save, file_to_store)
    file_to_store.close()


def get_pickle_file(file_name):
    file = open(f"{abs_path}/pickle_objects/{file_name}.pickle", 'rb')
    object_file = pickle.load(file)
    file.close()
    return object_file


def get_logs_path(file_name):
    return abs_path + "/app_logs/" + file_name + ".txt"


def get_picture_path(name):
    return abs_path + "/picture/" + name + ".jpeg"


def get_picture(name):
    with open(abs_path + "/pictures/" + name + ".png", 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

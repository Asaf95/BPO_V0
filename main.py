import Stage.multi_page_nested_folders.app as app
from art import *

# @TODO use from art import * for logs
# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    try:
        #  print(text2art("Bin Packing Optimization"))
        app.start_app()
    except Exception as Error:
        raise f"__MAIN__ Function didn't worked!! Check the following Error: \n {Error}"

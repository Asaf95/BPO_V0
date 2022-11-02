from dash import dcc, html, Input, Output, callback, register_page, dash_table

from Stage.multi_page_nested_folders.system_data import app_data_handler

register_page(__name__, icon="iconoir:stats-report")


def get_reports_names():
    return app_data_handler.get_files_names("packing_results")


layout = html.Div(
    [
        dcc.Dropdown(get_reports_names(), get_reports_names()[0], id='graph_selected'),
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
        html.Div(id="his-graph")
    ],
    style={'margin-left': '70px'}
)


@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    Input("graph_selected", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, g_number):
    if n_clicks is not None:
        return dcc.send_data_frame(app_data_handler.get_csv_file(f"packing_results/{g_number}").to_csv,
                                   f"{g_number}")


@callback(
    Output("his-graph", "children"),
    Input("graph_selected", "value"),
)
def display_color(g_number) -> html.Div:
    if g_number is not None:
        df = app_data_handler.get_csv_file(f"packing_results/{g_number}")
        return html.Div([
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'white',
                    'textAlign': 'center',
                    'fontWeight': 'bold'
                },)
             ])
    else:
        return html.Div([
                   html.P("Please select a report")
                ])

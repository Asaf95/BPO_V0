import dash_mantine_components as dmc
from dash import dcc, html
from dash import register_page

from project.app.multi_page_nested_folders import constants_bpo
from project.app.multi_page_nested_folders.system_data import app_data_handler

register_page(__name__, path="/", icon="ant-design:home-filled")


def get_pictures(fig_name):
    return app_data_handler.get_picture(fig_name)


Img_sidebar = dmc.Navbar(
    fixed=True,
    width={"base": "25%"},
    position={"top": 125, "left": 1365},
    style=constants_bpo.MAIN_LAYOUT_STYLE,  # backgroundColor for the menu
    children=[
        html.Img(
            src=get_pictures("img_4"), height="40%", width="100%",
        ),
        dmc.Space(h=20),
        html.Img(
            src=get_pictures("img_3"), height="40%", width="100%",
        )

    ]
)
Main_MD = dmc.Navbar(
    # fixed=True,
    width={"base": "100%"},
    style=constants_bpo.MAIN_LAYOUT_STYLE,  # backgroundColor for the menu
    children=[
        dmc.Title("Bin Packing Optimization ",
                  style={'textAlign': 'center'}),
        html.H3("let's solve your packing problem!",
                style={'textAlign': 'center'}),
        dmc.Space(h=5),
        dmc.Divider(),
        dmc.Space(h=5),
        dcc.Markdown(
            """
            Thank you for choosing BPO Software for solving your packing problem
            #### So, what is Bin Packing Optimization?
            Bin Packing Optimization App (BPO) is a free Open Source Software for solving Optimization packing problems.
            By using Advance Optimization Algorithms and a simple and easy to use App you can solve your packing problem
            within minutes and save time, space and money.
            All you need to do is the import the following files and the solution will be presented in 3D and will be
            able to download it to your local machine :)

            #### What is Bin's and Item's?
            Bins - are multiple containers, the container represent a space that can 'contain' items, it can be a bug or
            a container on a ship.
            The only limitation for defining a bin is space that a length width and height.
            Item's - are the items that you want to pack in the 'bins', it can be a box, car or a phone,
            the only limitation here it should come as length width and height.

            #### But my bin's and item's are not Rectangle! what can I do?
            The algorithm can solve only Rectangle quadrilateral with four right angles, But...
            You can 'calculate' your shapes, it means you need to find the minimal Rectangle that your bin or item can
            get into.

            #### What files should I fill and how?
            * box_amount.csv - this file contain the box names, amount and priority of boxes
            * con_amount.csv - amount of the containers form each type
            * box_properties.csv - the properties for each type of box (sizes)
            * con_properties.csv - the properties for each type of container (sizes)

            #### Core Packages
            Bin Packing Optimization (BPO) is a flask application based on Plotly Dash framework.
            BPO solves hard packing problems using Open Source Algorithm's and tool's.
            * 'Plotly-Dash': Used for creating the application
            * 'py3dbp': Is the solver engine of the app

            """,
            link_target="_blank",
            # When setting link_target="_blank" the link's opens in a new tab    or window
            # style=constants_bpo.MAIN_LAYOUT_STYLE
        ),
        dmc.Divider(),
        html.A("© GNU Free Software Foundation"),
        dmc.Divider(),
        html.Br(),

    ]
)

layout = dmc.Container(
    [
        dmc.Divider(),
        Main_MD,
        Img_sidebar,

    ], style=constants_bpo.MAIN_LAYOUT_STYLE, ml="10%"

)

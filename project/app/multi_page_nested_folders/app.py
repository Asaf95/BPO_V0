"""
This module creates the application framework.
It contains all containers for each component in the app and the style configuration for it
"""
import dash
import dash_mantine_components as dmc
from dash import Dash, dcc, html
from dash_iconify import DashIconify

from project.app.multi_page_nested_folders import constants_bpo
from project.app.multi_page_nested_folders.system_data import app_data_handler

"----------------------------------------------------  Application  ---------------------------------------------------"

# If you want to use a  theme, refactor the assets dir to assets, the dbc.themes.LUX is located there by default
# And don't forget to import dash_bootstrap_components as dbc first
app = Dash(__name__, use_pages=True)

"------------------------------------------------  Application Sidebar  -----------------------------------------------"


def get_app_logo():
    return app_data_handler.get_picture(constants_bpo.LOGO_NAME)


def create_nav_link(icon, label, href) -> dcc.Link:
    """
    This function create a Nav link format using when given the icon / label / herf parameters
    """
    return dcc.Link(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(
                        icon=icon,
                        width=constants_bpo.NAV_LINK_THEME_ICON.get('DashIconify_width')),
                    size=constants_bpo.NAV_LINK_THEME_ICON.get('size'),
                    radius=constants_bpo.NAV_LINK_THEME_ICON.get('radius'),
                    variant=constants_bpo.NAV_LINK_THEME_ICON.get('variant'),
                ),
                dmc.Text(
                    label,
                    size='lg',
                    color='dimmed', # Expected one of ["dark","gray","red","pink","grape","violet","indigo","blue","cyan","teal","green","lime","yellow","orange","dimmed"].
                    weight='bolder'
                ),
            ]),
        href=href,
        style=constants_bpo.NAV_LINK_STYLE,
    )


sidebar = dmc.Navbar(
    fixed=True,
    width=constants_bpo.MAIN_SIDE_BAR.get('Base'),
    position=constants_bpo.MAIN_SIDE_BAR.get('Location'),
    pl='1%',
    height=1080,
    style=constants_bpo.SIDEBAR_STYLE,
    children=[
        html.A(
            href='/',
            children=[
                html.Img(
                    src=get_app_logo(), height='100%', width='100%'
                )
            ]
        ),
        dmc.Group(
            grow=True,
            direction='column',
        ),
        dmc.ScrollArea(
            offsetScrollbars=True,
            type='scroll',
            children=[
                dmc.Group(
                    direction='column',
                    children=[
                        create_nav_link(
                            icon='clarity:home-line',
                            label='Welcome Page',
                            href='/',
                        ),
                    ],
                ),
                dmc.Divider(
                    label='Problem Definition', style=constants_bpo.SIDEBAR_DIVIDER_STYLE
                ),
                dmc.Group(
                    direction='column',
                    children=[
                        create_nav_link(
                            icon=page['icon'], label=page['name'], href=page['path']
                        )
                        for page in dash.page_registry.values()
                        if page['path'].startswith('/chapter1')
                    ],
                ),
                dmc.Divider(
                    label='Solution Presenting', style=constants_bpo.SIDEBAR_DIVIDER_STYLE
                ),
                dmc.Group(
                    direction='column',
                    children=[
                        create_nav_link(
                            icon=page['icon'], label=page['name'], href=page['path']
                        )
                        for page in dash.page_registry.values()
                        if page['path'].startswith('/chapter2')
                    ],
                ),
            ],
        ),
        html.Div([
            dmc.Button(
                html.A('Source Code', href='https://github.com/Asaf95', target='_blank'),
                leftIcon=[DashIconify(icon='line-md:github', width=36)],
                style=constants_bpo.SIDE_BUTTON_STYLE
            ),
            dmc.Button(
                html.A(
                    'Contact Me', href='https://www.linkedin.com/in/asafbm/', target='_blank'),
                leftIcon=[DashIconify(icon='line-md:linkedin', width=36)],
                style=constants_bpo.SIDE_BUTTON_STYLE
            ),
        ]
        ),
        dmc.Space(h=15),
        dmc.Text('© GNU - Free Software Foundation', align='center'),
    ],
)

"---------------------------------------------  Application Main layout  ----------------------------------------------"
app.title = 'BPO'

app.layout = html.Div(style=constants_bpo.MAIN_APP_STYLE,
                      children=[dmc.Container(
                          [
                              dcc.Store(id='memory-output', storage_type='session'),
                              dcc.Store(id='all_user_files', data={}, storage_type='session'),
                              dmc.Header(
                                  height=30,
                                  style=constants_bpo.APP_TOP_MARGIN,
                                  fixed=True,
                              ),
                              sidebar,
                              dmc.Container(
                                  dash.page_container,
                                  pt='3%',
                                  ml='20%',
                                  style=constants_bpo.LAYOUT_CONTENT_STYLE,
                              ),
                          ],
                          fluid=True,
                          style=constants_bpo.MAIN_LAYOUT_STYLE,
                      )]
                      )


def start_app():
    """
    this function run the app
    """
    try:
        app.run_server(host="0.0.0.0", port=8050, debug=False)        # app.run_server(debug=False, port=8888) to run on production
    except Exception as Error:
        raise f"Main App Startup didn't worked!! Check the following Error: \n {Error}"

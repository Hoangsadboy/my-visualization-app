#1-----------------------------------------import
from dash import Dash, html, dcc, Input, Output, State, ctx
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import base64, io
from docx import Document
import re
import ast

#2--------------------------------------- App init
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

#3 -------------------------------------data hữu ích


def chart_page():
    return dmc.Container([
        dmc.Title("Welcome", order=3),
        dmc.Text("Chọn chức năng ở thanh trên")
    ])

#5---------------------------------- Layout (UI improved)
navbar_main = dmc.Paper(
    id = 'navbar',
    shadow="sm", p="md",
    style={"height": 64, "display": "flex", "alignItems": "center", "justifyContent": "space-between",
           "position": "fixed", "top": 0, "left": 0, "right": 0, "zIndex": 1100,
           "backgroundColor": "#ffffffdd", "backdropFilter": "blur(6px)"},
    children=[
        dmc.Group([dmc.Button("☰", variant="subtle"), dmc.Text("Visualization Studio", fw=700, size="lg")]),
        dmc.Group([dmc.Switch(id="theme-switch", size="md", offLabel="☀", onLabel="🌙")])
    ]
)

subnav = dmc.Paper(
    id = 'subnav',
    shadow="xs", p="sm",
    style={"height": 56, "display": "flex", "alignItems": "center", "gap": 12,
           "position":"sticky","top":64,"zIndex":1000,"backgroundColor":"#ffffffcc","backdropFilter":"blur(4px)"},
    children=[
        html.A(
            dmc.Button("Code biểu đồ", variant="gradient"),
            href="https://code-for-charts.onrender.com",
            style={"textDecoration": "none"}
            ),
        html.A(
            dmc.Button("Tạo biểu đồ", variant="gradient"),
            href="https://easy-create-chart.onrender.com",
            style={"textDecoration": "none"}
            ),
        dmc.Space(w=16),
        dmc.Text("Background:", size="sm"),
        dcc.Input(id="bg-url", placeholder="Image URL (optional)", style={"width":300}),
        dcc.Upload(id="bg-upload", children=html.Button("Upload bg"), style={"marginLeft":8})
    ]
)

content_box = dmc.Container(id="content", mt=140, children=chart_page())
#nội dung chính
app.layout = html.Div(
    id='body-theme',
    style={
        'backgroundcolor':"#ffffffcc",
        'color' : 'black',
    },
    children=[dmc.MantineProvider(children=[
    navbar_main, subnav, content_box,
    dcc.Store(id="stored-data"),
    dcc.Store(id="bg-store"),
])])

#6-----------------------------------------CALLBACK
#đổi màu sáng tối chill chill
@app.callback(
    Output("navbar", "style"),
    Output("subnav", "style"),
    Output("body-theme", "style"),
    Input("theme-switch", "checked")
)
def theme_switch(is_dark):
    if is_dark:
        navbar = {"backgroundColor": "rgba(20,20,20,0.6)", "color": "white","height": 64, 
                  "display": "flex", "alignItems": "center", "justifyContent": "space-between",
           "position": "fixed", "top": 0, "left": 0, "right": 0, "zIndex": 1100,
           "backdropFilter": "blur(6px)"}
        subnav = {"backgroundColor": "rgba(20,20,20,0.6)", "color": "white","height": 56, "display": "flex", 
                  "alignItems": "center", "gap": 12,
           "position":"sticky","top":64,"zIndex":1000,"backdropFilter":"blur(4px)"}
        body = {"backgroundColor": "#000", "color": "white"}
    else:
        navbar = {"backgroundColor": "rgba(255,255,255,0.7)", "color": "black","height": 64, 
                  "display": "flex", "alignItems": "center", "justifyContent": "space-between",
           "position": "fixed", "top": 0, "left": 0, "right": 0, "zIndex": 1100,
           "backdropFilter": "blur(6px)"}
        subnav = {"backgroundColor": "rgba(255,255,255,0.7)", "color": "black","height": 56, "display": "flex", 
                  "alignItems": "center", "gap": 12,
           "position":"sticky","top":64,"zIndex":1000,"backdropFilter":"blur(4px)"}
        body = {"backgroundColor": "white", "color": "black"}

    return navbar, subnav, body
        #        navbar = {"backgroundColor": "rgba(255,255,255,0.7)", "color": "black"}
        #        subnav = {"backgroundColor": "rgba(255,255,255,0.7)", "color": "black"}
        #        body = {"backgroundColor": "white", "color": "black"}


if __name__ == "__main__":
    app.run(debug=True)

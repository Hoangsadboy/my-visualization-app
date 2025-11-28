# app.py — copy -> chạy
# Requirements:
# pip install dash dash-mantine-components dash-ag-grid pandas plotly python-docx

from dash import Dash, html, dcc, Input, Output, State, ctx
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import base64, io
from docx import Document

# -------------------------
# Load ISO (optional, used in choropleth)
# -------------------------
ISO_CSV = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
try:
    iso_df_used = pd.read_csv(ISO_CSV)
except Exception:
    iso_df_used = pd.DataFrame(columns=["name", "alpha-3"])

# -------------------------
# App init
# -------------------------
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# -------------------------
# Helper: 73 labeled inputs
# -------------------------
LABELS = [
    "Scatter X", "Scatter Y", "Scatter Color", "Scatter Size", "Scatter Symbol", "Scatter Hover", "Scatter Template",
    "Line X", "Line Y", "Line Color", "Line Shape", "Line Hover", "Line Text", "Line Template",
    "Area X", "Area Y", "Area Color", "Area Animation Group", "Area Line Shape", "Area Opacity", "Area Template",
    "Heatmap X", "Heatmap Y", "Heatmap color_continuous_scale", "Heatmap Template",
    "Bar X", "Bar Y", "Bar Color", "Bar Mode", "Bar Orientation", "Bar Text", "Bar Template",
    "Histogram X", "Histogram Y", "Histogram Color", "Histogram Opacity", "Histogram Barmode", "Histogram Template",
    "Box X", "Box Y", "Box Color", "Box Template",
    "Pie Names", "Pie Values", "Pie Hole (0-1)", "Pie Color", "Pie Title", "Pie Template",
    "Sunburst/Treemap Path (list)", "Sunburst/Treemap Values", "Sunburst/Treemap Color", "Sunburst/Treemap Title",
    "Choropleth Color", "Choropleth locations", "Choropleth Hover", "Choropleth Title", "Choropleth color_continuous_scale", "Choropleth Height",
    "Mapbox Lat col", "Mapbox Lon col", "Mapbox Color", "Mapbox Hover", "Mapbox Size col", "Mapbox Zoom", "Mapbox Height",
    "Parallel Dimensions (list)", "Parallel Color", "Parallel Title",
    "Funnel X", "Funnel Y", "Funnel Color", "Funnel Orientation", "Funnel Text", "Funnel Template"
]

# sanity: ensure length 73
if len(LABELS) < 73:
    LABELS += [f"q{i}" for i in range(len(LABELS), 73)]

TOOLTIPS = [
    # 1-7 Scatter
    "Tên cột cho trục X của Scatter",
    "Tên cột cho trục Y của Scatter",
    "Tên cột để tô màu (numeric → continuous, categorical → discrete)",
    "Tên cột để biểu diễn kích thước điểm (size)",
    "Tên cột để chỉ symbol/marker cho mỗi điểm",
    "Tên cột/thuộc tính hiển thị khi hover (hover_name/hover_data)",
    "Template đồ họa (ví dụ: plotly, ggplot2, plotly_dark)",

    # 8-14 Line
    "Tên cột cho trục X của Line chart",
    "Tên cột cho trục Y của Line chart",
    "Tên cột để phân nhóm màu cho Line",
    "Dạng nối line (linear, spline, vhv, hvh...)",
    "Tên cột hiển thị khi hover cho Line",
    "Tên cột/biểu diễn text trên line",
    "Template cho Line",

    # 15-21 Area
    "Tên cột X cho Area",
    "Tên cột Y cho Area",
    "Tên cột để tô màu cho Area",
    "Cột dùng làm animation_group (nếu có animation)",
    "Dạng đường cho Area (line_shape)",
    "Opacity (0–1) cho vùng Area",
    "Template cho Area",

    # 22-25 Heatmap / density
    "Tên cột X cho Heatmap / density_heatmap",
    "Tên cột Y cho Heatmap / density_heatmap",
    "Chọn thang màu liên tục (Viridis, Plasma, ...)",
    "Template cho Heatmap",

    # 26-32 Bar
    "Tên cột X cho Bar chart",
    "Tên cột Y cho Bar chart (giá trị)",
    "Tên cột để phân màu cho Bar",
    "Chế độ hiển thị cột (group, stack, overlay)",
    "Orientation cột (v hoặc h)",
    "Tên cột hiển thị text trên cột (text)",
    "Template cho Bar",

    # 33-38 Histogram
    "Tên cột X cho Histogram",
    "Tên cột Y cho Histogram (optional / agg)",
    "Tên cột để phân màu cho Histogram",
    "Opacity (0–1) cho Histogram",
    "Barmode cho histogram (group, stack, overlay)",
    "Template cho Histogram",

    # 39-42 Box/Violin
    "Tên cột X cho Box/Violin (categorical)",
    "Tên cột Y cho Box/Violin (numeric)",
    "Tên cột để phân màu cho Box/Violin",
    "Template cho Box/Violin",

    # 43-48 Pie
    "Tên cột chứa labels (names) cho Pie",
    "Tên cột chứa giá trị (values) cho Pie",
    "Hole (0–1) — độ rỗng giữa của Pie",
    "Tên cột dùng để tô màu (thường categorical)",
    "Tiêu đề cho Pie chart",
    "Template cho Pie",

    # 49-52 Sunburst/Treemap
    "PATH cho Sunburst/Treemap — danh sách cột phân cấp (vd ['A','B'])",
    "Tên cột chứa giá trị (values) cho Sunburst/Treemap",
    "Tên cột dùng để tô màu cho Sunburst/Treemap (optional)",
    "Tiêu đề cho Sunburst/Treemap",

    # 53-58 Choropleth
    "Tên cột numeric để làm color cho Choropleth",
    "chọn locations cho Choropleth",
    "Tên cột hiển thị khi hover (hover_name)",
    "Tiêu đề cho Choropleth",
    "Chọn color_continuous_scale cho Choropleth",
    "Chiều cao chart (pixels) cho Choropleth (optional)",

    # 59-65 Mapbox (scatter_mapbox)
    "Tên cột chứa vĩ độ (lat)",
    "Tên cột chứa kinh độ (lon)",
    "Tên cột dùng để tô màu trên bản đồ",
    "Tên cột hiển thị khi hover trên bản đồ",
    "Tên cột dùng để đặt kích thước điểm (size)",
    "Zoom ban đầu cho mapbox (ví dụ 2-12)",
    "Chiều cao chart (pixels) cho Mapbox",

    # 66-68 Parallel coordinates
    "Danh sách các cột numeric làm dimensions cho parallel coordinates",
    "Tên cột dùng để mã màu (color) trong parallel",
    "Tiêu đề cho parallel coordinates",

    # 69-74 Funnel
    "Tên cột X cho Funnel (giá trị trục x)",
    "Tên cột Y cho Funnel (nhãn trục y)",
    "Tên cột dùng để phân màu cho Funnel",
    "Orientation cho Funnel (v hoặc h)",
    "Tên cột hiển thị text trên Funnel",
    "Template cho Funnel"
]

# đảm bảo đủ 74 mục
assert len(TOOLTIPS) == 74


# Ensure length đủ 74
if len(TOOLTIPS) < 74:
    TOOLTIPS += [f"Tooltip {i}" for i in range(len(TOOLTIPS), 74)]
def generate_inputs():
    comps = []
    for i in range(73):
        comps.append(
            dmc.Tooltip(
                label=TOOLTIPS[i],     # tooltip riêng cho từng ô
                position="right",
                offset=8,
                withArrow=True,

                children=dmc.TextInput(
                    id=f"q{i}",
                    label=LABELS[i],
                    placeholder=LABELS[i],
                    style={"width": "100%"}
                )
            )
        )
    return comps

# ------------------------- layout
# Layout (UI improved)
# -------------------------
navbar_main = dmc.Paper(
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
    shadow="xs", p="sm",
    style={"height": 56, "display": "flex", "alignItems": "center", "gap": 12,
           "position":"sticky","top":64,"zIndex":1000,"backgroundColor":"#ffffffcc","backdropFilter":"blur(4px)"},
    children=[
        dmc.Button("Xử lý bảng dữ liệu", id="table", variant="gradient"),
        dmc.Button("Tạo biểu đồ", id="chart", variant="gradient"),
        dmc.Button("Liên kết biểu đồ", id="connect", variant="gradient"),
        dmc.Space(w=16),
        dmc.Text("Background:", size="sm"),
        dcc.Input(id="bg-url", placeholder="Image URL (optional)", style={"width":300}),
        dcc.Upload(id="bg-upload", children=html.Button("Upload bg"), style={"marginLeft":8})
    ]
)

content_box = dmc.Container(id="content", mt=140, children=[
    dmc.Title("Welcome", order=2),
    dmc.Text("Chọn chức năng ở thanh trên")
])

app.layout = dmc.MantineProvider(children=[
    navbar_main, subnav, content_box,
    dcc.Store(id="stored-data"),
    dcc.Store(id="bg-store"),
])

# -------------------------
# Content switch callback
# -------------------------
def chart_page():
    return dmc.Container([
        dmc.Title("Upload dữ liệu", order=3),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['📁 Kéo/thả file hoặc ', html.A('Chọn file')]),
            style={'width': '100%', 'height': '120px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                   'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': 8, 'marginBottom': 12}
        ),
        dag.AgGrid(id='AgGrid', rowData=[], columnDefs=[], style={"height":"260px","width":"100%"}),
        html.Br(),
        dmc.Title("Chọn biểu đồ", order=4),
        dcc.RadioItems(
            id='first',
            options=[
                {'label': 'Scatter', 'value': 'scatter'},
                {'label': 'Line', 'value': 'line'},
                {'label': 'Area', 'value': 'area'},
                {'label': 'Heatmap', 'value': 'density_heatmap'},
                {'label': 'Bar', 'value': 'bar'},
                {'label': 'Histogram', 'value': 'histogram'},
                {'label': 'Box', 'value': 'box'},
                {'label': 'Violin', 'value': 'violin'},
                {'label': 'Pie', 'value': 'pie'},
                {'label': 'Sunburst', 'value': 'sunburst'},
                {'label': 'Treemap', 'value': 'treemap'},
                {'label': 'Choropleth', 'value': 'choropleth'},
                {'label': 'Mapbox', 'value': 'scatter_mapbox'},
                {'label': 'Parallel', 'value': 'parallel_coordinates'},
                {'label': 'Funnel', 'value': 'funnel'},
            ],
            value='line',
            style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)","gap":"8px"}
        ),
        html.Br(),
        dcc.Graph(id='controls-and-graph'),
        html.Hr(),
        dcc.Download(id="download-svg"),
        dmc.Button("Tải SVG", id="btn-svg", variant="outline", color="blue"),
        html.Hr(),
        dmc.Title("Tham số biểu đồ", order=4),
        dmc.SimpleGrid(cols=4, spacing="md", children=generate_inputs()),
    ])

def table_page():
    return dmc.Container([
        dmc.Title("Bảng dữ liệu", order=3),
        dag.AgGrid(id='AgGrid', rowData=[], columnDefs=[], style={"height":"640px","width":"100%"})
    ])

def connect_page():
    return dmc.Container([dmc.Title("Liên kết dữ liệu"), dmc.Text("Tính năng sẽ mở rộng")])

@app.callback(Output("content", "children"),
              Input("table","n_clicks"), Input("chart","n_clicks"), Input("connect","n_clicks"))
def switch_page(b1, b2, b3):
    trig = ctx.triggered_id
    if trig == "table":
        return table_page()
    if trig == "chart":
        return chart_page()
    if trig == "connect":
        return connect_page()
    return content_box

# -------------------------
# File parsing & convert numeric
# -------------------------
def parse_docx(bytestr: bytes):
    doc = Document(io.BytesIO(bytestr))
    rows = []
    for table in doc.tables:
        for r in table.rows:
            cells = [cell.text.strip() for cell in r.cells]
            if any(cells):
                rows.append(cells)
    if not rows:
        return pd.DataFrame()
    header = rows[0]
    data = rows[1:]
    return pd.DataFrame(data, columns=header)

def parse_file(contents, filename):
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    except Exception:
        return None
    name = filename.lower()
    if name.endswith('.csv'):
        return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    if name.endswith(('.xls','.xlsx')):
        return pd.read_excel(io.BytesIO(decoded))
    if name.endswith('.docx'):
        return parse_docx(decoded)
    return None

def convert_numeric(df):
    for col in df.columns:
        temp = pd.to_numeric(df[col], errors="coerce")
        if temp.notna().mean() > 0.7:
            df[col] = temp
    return df

# -------------------------
# Store uploaded data -> write to AgGrid once (no duplicate issues)
# -------------------------
@app.callback(
    Output("stored-data", "data"),
    Output("AgGrid", "rowData"),
    Output("AgGrid", "columnDefs"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def store_df_used(contents, filename):
    if contents is None:
        return None, [], []
    df = parse_file(contents, filename)
    if df is None:
        return None, [], []
    df = convert_numeric(df)
    columnDefs = [{"field": c} for c in df.columns]
    return df.to_dict('records'), df.to_dict('records'), columnDefs

# ------------------------- locations
# Background store & apply
# -------------------------
@app.callback(Output("bg-store","data"),
              Input("bg-upload","contents"),
              Input("bg-url","value"),
              prevent_initial_call=False)
def store_bg(uploaded, url):
    if uploaded:
        return uploaded
    if url:
        return url
    return None

@app.callback(Output("content","style"), Input("bg-store","data"))
def apply_bg(bg):
    style = {"marginTop":140}
    if not bg:
        return style
    if isinstance(bg, str) and bg.startswith("data:"):
        style["backgroundImage"] = f"url('{bg}')"
    else:
        style["backgroundImage"] = f"url('{bg}')"
    style["backgroundSize"] = "cover"
    style["backgroundPosition"] = "center"
    style["padding"] = "18px"
    style["borderRadius"] = "8px"
    return style

# ------------------------- def generate_inputs():
# Update graph — keep original algorithm, accept q0..q72
# -------------------------
q_inputs = [Input(f"q{i}", "value") for i in range(73)]
@app.callback(Output("controls-and-graph","figure"),
              Input("first","value"),
              Input("stored-data","data"),
              *q_inputs)
def update_graph(chart_type, uploaded_data, *values):
    df_used = pd.DataFrame(uploaded_data) if uploaded_data else pd.DataFrame()
    values = [v if v not in ["", None] else None for v in values]
    check = values[53]
    if check in df_used.columns:
        try:
            df_used = df_used.merge(iso_df_used[['name','alpha-3']], left_on=check, right_on='name', how='left')
            df_used.rename(columns={'alpha-3':'iso_alpha'}, inplace=True)
            df_used.drop(columns=['name'], inplace=True, errors='ignore')
        except Exception:
            pass
    if df_used.empty:
        return px.scatter(title="Upload dataset first")

    # convert potential numeric columns user selected for lat/lon/size
    for idx in (57,58,61):
        v = values[idx]
        if isinstance(v, str) and v in df_used.columns:
            df_used[v] = pd.to_numeric(df_used[v].astype(str).str.replace(r'[^\d\.\-]', '', regex=True), errors='coerce')

    try:
        print(df_used.columns)
        chart_funct = {
            'scatter': lambda:
                px.scatter(df_used, x=values[0], y=values[1], color=values[2],
                           size=values[3], symbol=values[4], hover_name=values[5], template=values[6]),

            'line': lambda:
                px.line(df_used, x=values[7], y=values[8], color=values[9],
                        line_shape=values[10], hover_name=values[11], text=values[12], template=values[13]),

            'area': lambda:
                px.area(df_used, x=values[14], y=values[15], color=values[16],
                        animation_group=values[17], line_shape=values[18],
                        #opacity=float(values[19]) if values[19] else 1, 
                        template=values[20]),

            'density_heatmap': lambda:
                px.density_heatmap(df_used, x=values[21], y=values[22], color_continuous_scale=values[23], template=values[24]),

            'bar': lambda:
                px.bar(df_used, x=values[25], y=values[26], color=values[27], barmode=values[28], orientation=values[29],
                       text=values[30], template=values[31]),

            'histogram': lambda:
                px.histogram(df_used, x=values[32], y=values[33], color=values[34],
                             opacity=float(values[35]) if values[35] else 1, barmode=values[36], template=values[37]),

            'box': lambda:
                px.box(df_used, x=values[38], y=values[39], color=values[40], template=values[41]),

            'violin': lambda:
                px.violin(df_used, x=values[38], y=values[39], color=values[40], template=values[41]),

            'pie': lambda:
                px.pie(df_used, names=values[42], values=values[43], hole=float(values[44]) if values[44] else 0,
                       color=values[45], title=values[46], template=values[47]),

            'sunburst': lambda:
                px.sunburst(df_used, path=values[48], values=values[49], color=values[50], title=values[51]),

            'treemap': lambda:
                px.treemap(df_used, path=values[48], values=values[49], color=values[50], title=values[51]),

            'choropleth': lambda:
                px.choropleth(df_used, locations='iso_alpha' if 'iso_alpha' in df_used.columns else 'alpha-3', locationmode='ISO-3', color=values[52],
                              hover_name=values[54], title=values[55], color_continuous_scale=values[56],
                              height=int(float(values[57])) if values[57] else 600),

            'scatter_mapbox': lambda:
                (px.scatter_mapbox(
                    df_used,
                    lat=(values[58] if isinstance(values[58], str) and values[58] in df_used.columns else None),
                    lon=(values[59] if isinstance(values[59], str) and values[59] in df_used.columns else None),
                    color=values[60], hover_name=values[61],
                    size=(values[62] if isinstance(values[62], str) and values[62] in df_used.columns else None),
                    zoom=float(values[63]) if values[63] else 4,
                    height=int(float(values[64])) if values[64] else 600,
                    size_max=25).update_layout(mapbox_style="open-street-map")
                ),

            'parallel_coordinates': lambda:
                px.parallel_coordinates(df_used, dimensions=values[65], color=values[66], title=values[67]),

            'funnel': lambda:
                px.funnel(df_used, x=values[68], y=values[69], color=values[70], orientation=values[71], text=values[72], template=values[73])
        }

        return chart_funct.get(chart_type, lambda: px.scatter(df_used, x=df_used.columns[0]))()
    except Exception as e:
        # Chuyển lỗi thành chuỗi và ép xuống dòng mỗi khi quá dài
        msg = f"⚠️ Lỗi khi vẽ biểu đồ:<br>{str(e).replace(', ', ',<br>')}"

        fig = px.scatter()  # biểu đồ rỗng để hiển thị lỗi

        # === Annotation để hiển thị lỗi xuống dòng cực đẹp ===
        fig.add_annotation(
            x=0,
            y=1.15,
            xref="paper",
            yref="paper",
            align="left",
            showarrow=False,
            text=f"""
                <span style="white-space:normal;
                             font-size:16px;
                             color:#d9534f;
                             font-weight:bold;
                             display:block;
                             width:900px;">
                    {msg}
                </span>
            """
        )

        # Chừa không gian phía trên cho lỗi dài
        fig.update_layout(
            margin=dict(t=180)  # tăng top margin để lỗi không đè lên chart
        )

        return fig

@app.callback(
    Output("download-svg", "data"),
    Input("btn-svg", "n_clicks"),
    State("controls-and-graph", "figure"),
    prevent_initial_call=True
)
def download_svg(n, fig):
    import plotly.io as pio

    try:
        svg_bytes = pio.to_image(fig, format="svg")
    except Exception:
        return dict(
            content="<svg><text x='20' y='20'>Lỗi: Máy chủ không hỗ trợ xuất SVG</text></svg>",
            filename="chart.svg"
        )

    # QUAN TRỌNG: bytes → string
    svg_str = svg_bytes.decode("utf-8")

    return dict(
        content=svg_str,
        filename="chart.svg",
        type="text/svg"
    )

# ------------------------- merge
# Run
# ------------------------- height
if __name__ == "__main__":
    app.run(debug=True)

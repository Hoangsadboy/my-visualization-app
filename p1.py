# Import packages
from dash import Dash, html, dcc, callback, Output, Input, ctx
from docx import Document
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import base64, io
import dash_mantine_components as dmc
iso_df_used = pd.read_csv("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")
df_used = pd.DataFrame()

app = Dash(__name__, suppress_callback_exceptions=True)

navbar1 = dmc.Paper(
    shadow="sm",
    p="md",
    style={
        "height": 60,
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "position": "fixed",
        "top": 0,
        "left": 0,
        "right": 0,
        "zIndex": 1000,
    },
    children=[
        dmc.Group(
            [
                dmc.Button("☰", id="open-menu", variant="subtle"),
                dmc.Text("My App", fw=700, size="lg"),
            ]
        ),
        dmc.Switch(
            id="theme-switch",
            size="md",
            offLabel="☀",
            onLabel="🌙",
        ),
    ],
)
navbar2 = dmc.Paper(
    shadow="sm",
    p="md",
    style={
        "height": 60,
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "position": "sticky",
        "top": 60,
        "left": 0,
        "right": 0,
        "zIndex": 1000,
    },
    children=[
        dmc.Button('xử lí bảng dữ liệu',id='table',variant='gradient'),
        dmc.Button('tạo biểu đồ',id='chart',variant='gradient'),
        dmc.Button('liên kết biểu đồ',id='connect',variant='gradient')
    ]
)
content = dmc.Container(
    id = 'content',
    mt=80,
    children=[
        dmc.Title("Hello", order=2),
        dmc.Text("Đây là trang nội dung."),
    ],
)

app.layout = dmc.MantineProvider(
    children=[
        navbar1,
        navbar2,
        content,
        html.Div(
            id = 'i_love_you_3000',
            children=[]
        ),
        dcc.Store(id='stored-data'), #store
    ],

)

#nút bấm - lay out bên lề hihi
@callback(
    Output('content','children'),
    Output('i_love_you_3000','children'),
    Input('table','n_clicks'),
    Input('chart','n_clicks'),
    Input('connect','n_clicks')
) 
def handle_button_click(table_click, chart_click, connect_click):
    triggered_id = ctx.triggered_id  # lấy id của nút vừa được bấm

    if triggered_id == "table":
        return [dmc.Title("Table", order=2), dmc.Text("Chỉnh sửa bảng dữ liệu")], []
    elif triggered_id == "chart":
        return [dmc.Title("Chart", order=2), dmc.Text("Thiết kế biểu đồ phân tích")], chart()
    elif triggered_id == "connect":
        return [dmc.Title("Connect", order=2), dmc.Text("Liên kết dữ liệu trực tiếp")], []
    return [dmc.Text("good morning")], []

def chart():
    return [
       dcc.Upload(
        id='upload-data',
        children=html.Div(['Kéo/thả file hoặc ', html.A('Chọn file')]),
        style={
            'width': '100%', 'height': '120px','display': 'flex','justify-content': 'center','align-items': 'center',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'textAlign': 'center'
        }
        ), 
        html.Hr(),
        dag.AgGrid(
            rowData=df_used.to_dict('records'),
            columnDefs=[],
            id = 'AgGrid',
        ),
        dcc.RadioItems(
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
        id='first',
        className="custom-radio",
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "10px",
            "width": "100%"
        }
        ),
        #đồ thị
        dcc.Graph(figure=px.scatter(), id='controls-and-graph'),
        dmc.Container(
            children=[
                dmc.Title("Scatter", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components1
                ),
                html.Hr(),
                dmc.Title("Line", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components2
                ),
                html.Hr(),
                dmc.Title("Area", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components3
                ),
                html.Hr(),
                dmc.Title("heatmapHeatmap (density_heatmap)", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components4
                ),
                html.Hr(),
                dmc.Title("Bar", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components5
                ),
                html.Hr(),
                dmc.Title("Histogram", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components6
                ),
                html.Hr(),
                dmc.Title("Box & Violin", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components7
                ),
                html.Hr(),
                dmc.Title("Pie ", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components8
                ),
                html.Hr(),
                dmc.Title("Sunburst & Treemap ", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components9
                ),
                html.Hr(),
                dmc.Title("Choropleth ", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components10
                ),
                html.Hr(),
                dmc.Title("Mapbox (scatter_mapbox) ", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components11
                ),
                html.Hr(),
                dmc.Title("Parallel Coordinates ", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components12
                ),
                html.Hr(),
                dmc.Title("Funnel ", order=2),
                dmc.SimpleGrid(
                    cols=5,  # mỗi hàng 5 cột
                    spacing="md",
                    children=question_components13
                ),
                html.Hr(),
        ])]
#khu dưới của chart---------------------------------------------------------
questions_SCATTER = [
    {"label": "<TÊN CỘT> X:", "id": "q0"},
    {"label": "<TÊN CỘT> Y:", "id": "q1"},
    {"label": "<TÊN CỘT> COLOR: ", "id": "q2"},
    {"label": "<TÊN CỘT> SIZE: ", "id": "q3"},
    {"label": "<TÊN CỘT> SYMBOL:", "id": "q4"},
    {"label": "<TÊN CỘT> HOVER_NAME:", "id": "q5"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q6"},
]
question_LINE = [
    {"label": "<TÊN CỘT> X:", "id": "q7"},
    {"label": "<TÊN CỘT> Y:", "id": "q8"},
    {"label": "<TÊN CỘT> COLOR:", "id": "q9"},
    {"label": "<CHỌN: linear, spline, vhv, hvh> LINE_SHAPE: ", "id": "q10"},
    {"label": "<TÊN CỘT> HOVER_NAME:", "id": "q11"},
    {"label": "<TÊN CỘT> TEXT:", "id": "q12"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q13"},
]
question_AREA = [
    {"label": "<TÊN CỘT> X:", "id": "q14"},
    {"label": "<TÊN CỘT> Y:", "id": "q15"},
    {"label": "<TÊN CỘT> COLOR:", "id": "q16"},
    {"label": "<TÊN CỘT> ANIMATION_GROUP:", "id": "q17"},    
    {"label": "<CHỌN: linear, spline, vhv, hvh> LINE_SHAPE: ", "id": "q18"},
    {"label": "<SỐ THỰC <SỐ THỰC 0<=x<=1 > OPACITY:", "id": "q19"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q20"},
]
question_HEATMAP = [
    {"label": "<TÊN CỘT> X:", "id": "q21"},
    {"label": "<TÊN CỘT> Y:", "id": "q22"},
    {"label": "<CHỌN THANG MÀU: Viridis, Cividis, Plasma...> color_continuous_scale: ", "id": "q23"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q24"},
]
question_BAR = [
    {"label": "<TÊN CỘT> X:", "id": "q25"},
    {"label": "<TÊN CỘT> Y:", "id": "q26"},
    {"label": "<TÊN CỘT> color: ", "id": "q27"},
    {"label": "<CHỌN CÁCH HIỂN THỊ CỘT: group, stack, overlay> BARMODE:", "id": "q28"},
    {"label": "<v HAY h> ORIENTATION:", "id": "q29"},
    {"label": "<TÊN CỘT> TEXT:", "id": "q30"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q31"},
]
question_HISTOGRAM = [
    {"label": "<TÊN CỘT> X:", "id": "q32"},
    {"label": "<TÊN CỘT> Y:", "id": "q33"},
    {"label": "<TÊN CỘT> color: ", "id": "q34"},
    {"label": "<SỐ THỰC 0<=x<=1 > OPACITY:", "id": "q35"},
    {"label": "<CHỌN CÁCH HIỂN THỊ CỘT: group, stack, overlay> BARMODE:", "id": "q36"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q37"},
]
question_BOX_VIOLIN = [
    {"label": "<TÊN CỘT> X:", "id": "q38"},
    {"label": "<TÊN CỘT> Y:", "id": "q39"},
    {"label": "<TÊN CỘT> color: ", "id": "q40"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q41"},
]
question_PIE = [
    {"label": "<TÊN CỘT> NAMES:", "id": "q42"},
    {"label": "<TÊN CỘT> VALUES:", "id": "q43"},
    {"label": "<SỐ THỰC 0<=x<=1 > HOLE: ", "id": "q44"},
    {"label": "<TÊN CỘT> COLOR:", "id": "q45"},
    {"label": "<CHUỖI VĂN BẢN> TITLE:", "id": "q46"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q47"},
]
question_SUNBURST_TREEMAP = [
    {"label": "<DANH SÁCH CỘT: ['A','B']> PATH:", "id": "q48"},
    {"label": "<TÊN CỘT> VALUES:", "id": "q49"},
    {"label": "<TÊN CỘT> color: ", "id": "q50"},
    {"label": "<CHUỖI VĂN BẢN> TITLE:", "id": "q51"},
]
question_CHOROPLETH = [
    {"label": "<TÊN CỘT> color: ", "id": "q52"},
    {"label": "<TÊN CỘT> HOVER_NAME:", "id": "q53"},
    {"label": "<CHUỖI VĂN BẢN> TITLE:", "id": "q54"},
    {"label": "<CHỌN THANG MÀU: Viridis, Cividis, Plasma...> color_continuous_scale:", "id": "q55"},
    {"label": "<SỐ THỰC> HEIGHT:", "id": "q56"},
]
question_MAPBOX = [
    {"label": "<TÊN CỘT VĨ ĐỘ> LAT:", "id": "q57"},
    {"label": "<TÊN CỘT KINH ĐỘ> LON: ", "id": "q58"},
    {"label": "<TÊN CỘT> COLOR:", "id": "q59"},
    {"label": "<TÊN CỘT> HOVER_NAME:", "id": "q60"},
    {"label": "<TÊN CỘT> SIZE:", "id": "q61"},
    {"label": "<SỐ THỰC> ZOOM:", "id": "q62"},
    {"label": "<SỐ THỰC> HEIGHT:", "id": "q63"},
]
question_PARALLELCOORDINATES = [
    {"label": "<DANH SÁCH CÁC CỘT SỐ HỌC> DIMENSIONS:", "id": "q64"},
    {"label": "<TÊN CỘT> COLOR:", "id": "q65"},
    {"label": "<CHUỖI VĂN BẢN> TITLE:", "id": "q66"},
]
question_FUNNEL = [
    {"label": "<TÊN CỘT> X:", "id": "q67"},
    {"label": "<TÊN CỘT> Y: ", "id": "q68"},
    {"label": "<TÊN CỘT> COLOR:", "id": "q69"},
    {"label": "<v HAY h> ORIENTATION:", "id": "q70"},
    {"label": "<TÊN CỘT> TEXT:", "id": "q71"},
    {"label": "<CHỌN MẪU BIỂU ĐỒ NHƯ: plotly, ggplot2, seaborn, plotly_dark:> TEMPLATE: ", "id": "q72"},
]
# Tạo component cho từng câu hỏi
question_components1 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in questions_SCATTER
]
question_components2 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_LINE
]
question_components3 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_AREA
]
question_components4 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_HEATMAP
]
question_components5 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_BAR
]
question_components6 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_HISTOGRAM
]
question_components7 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_BOX_VIOLIN
]
question_components8 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_PIE
]
question_components9 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_SUNBURST_TREEMAP
]
question_components10 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_CHOROPLETH
]
question_components11 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_MAPBOX
]
question_components12 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_PARALLELCOORDINATES
]
question_components13 = [
    html.Div([
        html.Label(q["label"]),
        dcc.Input(id=q["id"], type="text", style={"width": "100%"})
    ]) for q in question_FUNNEL
]
question = questions_SCATTER + question_LINE + question_AREA + question_HEATMAP + question_BAR + question_HISTOGRAM + question_BOX_VIOLIN + question_PIE + question_SUNBURST_TREEMAP + question_CHOROPLETH + question_MAPBOX + question_PARALLELCOORDINATES + question_FUNNEL

@callback(
    Output('controls-and-graph','figure'),
    Input('first','value'),
    Input('stored-data','data'),
    *[Input(q["id"],"value") for q in question]
)
def update_graph(name,uploaded_data,*values):
    df_used = pd.DataFrame(uploaded_data) if uploaded_data else pd.DataFrame()
    values = [v if v not in ["", None] else None for v in values]
    chart_funct = {
        'scatter': lambda: 
            px.scatter(
            df_used,x=values[0],y=values[1],color = values[2],size = values[3],symbol = values[4],
            hover_name = values[5],template= values[6], 
        ),
        'line': lambda:
            px.line(
            df_used,x=values[7],y=values[8],color = values[9], line_shape= values[10],hover_name = values[11],
            text= values[12],template= values[13]

        ),
        'area': lambda:
            px.area(
            df_used,x=values[14],y=values[15],color = values[16],animation_group= values[17],line_shape= values[18],
            template= values[20]
        ),
        'density_heatmap': lambda:
            px.density_heatmap(
            df_used,x=values[21],y=values[22], color_continuous_scale= values[23],template= values[24],
        ),
        'bar': lambda:
            px.bar(
            df_used,x=values[25],y=values[26],color = values[27],barmode= values[28],orientation= values[29],
            text= values[30],template= values[31]
        ),
        'histogram': lambda:
            px.histogram(
            df_used,x=values[32],y=values[33],color = values[34], opacity= float(values[35]) if values[35] else 1,
            barmode= values[36], template= values[37]
        ),
        'box': lambda:
            px.box(
            df_used,x=values[38],y=values[39],color = values[40],template= values[41]
        ),
        'violin': lambda:
            px.violin(
            df_used,x=values[38],y=values[39],color = values[40],template= values[41]

        ),
        'pie': lambda:
            px.pie(
            df_used, 
            names= values[42], 
            values= values[43], 
            hole = float(values[44]) if values[44] else 0,
            color  = values[45],
            title = values[46],
            template = values[47]
            ),
        'sunburst': lambda:
            px.sunburst(
            data_frame=df_used,
            path=values[48],  # thứ tự cấp phân cấp (ví dụ: continent → country → city)
            values=values[49],               # cột giá trị để tính diện tích lát
            color  = values[50],                    # (tùy chọn) tô màu theo cấp nào đó
            title=values[51]
            ),
        'treemap': lambda:
            px.treemap(
            data_frame=df_used,
            path=values[48],  # thứ tự cấp phân cấp (ví dụ: continent → country → city)
            values=values[49],               # cột giá trị để tính diện tích lát
            color  = values[50],                    # (tùy chọn) tô màu theo cấp nào đó
            title=values[51]
            ),
        'choropleth': lambda:
            px.choropleth(
            df_used,
            locations='iso_alpha',
            locationmode='ISO-3',
            color  = values[52],
            hover_name=values[53],
            title=values[54],
            color_continuous_scale=values[55],
            height=float(values[56]) if values[56] else 600,
        ),
        'scatter_mapbox': lambda:
            px.scatter_mapbox(
            df_used,
            lat = values[57],
            lon = values[58],
            color  = values[59],
            hover_name = values[60],
            size = values[61],
            zoom = float(values[62]) if values[62] else 4,
            height=float(values[63]) if values[63] else 600,
            size_max=25,
        ).update_layout(mapbox_style="open-street-map"),
        'parallel_coordinates': lambda:
            px.parallel_coordinates(
            df_used,
            dimensions=values[64],  # các biến số học
            color  = values[65],
            title=values[66]
        ),
        'funnel': lambda:
            px.funnel(
            df_used,x=values[67],y=values[68],color = values[69], orientation= values[70],text= values[71],
            template= values[72]
        ),
    }
    try:
        return chart_funct.get(name, lambda: px.scatter(df_used, x='country', y='pop'))()
    except Exception as e:
        return px.scatter(title=f"⚠️ Lỗi khi vẽ biểu đồ: {e}")
#khu trên của chart---------------------------------------------------------------------------





#khúc này trở đi, nhận dữ liệu và lưu dữ liệu
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if filename.endswith('.csv'):
        return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        return pd.read_excel(io.BytesIO(decoded))
    elif filename.endswith('.docx'):
        doc = Document(io.BytesIO(decoded))
        data = []
        for table in doc.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                if any(cells):  # bỏ qua dòng trống
                    data.append(cells)

        # nếu có tiêu đề ở dòng đầu
            if data:
                header = data[0]
                rows = data[1:]
                return pd.DataFrame(rows, columns=header)
            else:
                return pd.DataFrame()
    return None
@app.callback(
    Output('stored-data', 'data'),
    Output('AgGrid','rowData'),
    Output('AgGrid', 'columnDefs'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
)
def store_df_used(contents, filename):
    if contents is None:
        return None, [], []
    #số ra số, chữ ra chữ, k có bede
    df_used = parse_contents(contents, filename)
    df_used = convert_numeric(df_used)

    if df_used is None:
        return None, [], []
    if 'country' in df_used.columns:
        df_used = df_used.merge(iso_df_used[['name','alpha-3']], left_on='country', right_on='name', how='left')
        df_used.rename(columns={'alpha-3':'iso_alpha'}, inplace=True)
    if 'name' in df_used.columns:
        df_used.drop(columns=['name'], inplace=True)

    return df_used.to_dict('records'), df_used.to_dict('records'), [{"field": i} for i in df_used.columns] # ⭐ lưu df_used vào dcc.Store
def convert_numeric(df):
    for col in df.columns:
        temp = pd.to_numeric(df[col], errors='coerce')
        ratio = temp.notna().mean()

        # Nếu >70% là số → coi như numeric
        if ratio > 0.7:
            df[col] = temp

    return df

if __name__ == "__main__":
    app.run(debug=True)

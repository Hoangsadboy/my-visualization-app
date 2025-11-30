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
import numpy, seaborn, matplotlib, altair, bokeh, networkx

#2--------------------------------------- App init
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

#3 -------------------------------------data hữu ích


def fanpage_page():
    return dmc.Container([
        # sử dụng một div lớn, whiteSpace pre-wrap để giữ lại xuống dòng y chang
        html.Div([
            html.H1("HƯỚNG DẪN SỬ DỤNG PHẦN MỀM VISUALIZATION STUDIO",style={"textAlign": "center"}),

            # đoạn giới thiệu (nguyên văn)
            html.Pre("""Phần mềm này được thiết kế để giúp bạn tải lên dữ liệu (CSV, XLSX, DOCX), đồng thời xử lý bằng code Python tùy chỉnh và tạo ra các biểu đồ tương tác cao cấp (Plotly Express) mà không cần viết code Plotly. Ngoài ra người dùng vẫn có thể thực hiện các thao tác code phức tạp hơn trong khung code có sẵn để tăng độ linh hoạt và khả năng tiếp cận ngôn ngữ lập trình của các bạn trẻ.
""", style={"fontFamily":"inherit", "whiteSpace":"pre-wrap"}),

            html.H2("1. Cấu trúc website và điều hướng cơ bản."),

            html.P("Visualization Studio được tổ chức thanh ba trang chính theo các chức năng riêng, có thể chuyển đổi qua lại bằng thanh điều hướng (Navbar) phía trên:"),

            # Bảng 1: Cấu trúc website (định dạng đẹp hơn)
            dmc.Table(
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                children=[
                    html.Thead(html.Tr([
                        html.Th("Trang (Tính năng)", style={"backgroundColor":"#f0f4f8","padding":"8px","border":"1px solid #ddd"}),
                        html.Th("Mục đích", style={"backgroundColor":"#f0f4f8","padding":"8px","border":"1px solid #ddd"}),
                        html.Th("Đối tượng người dùng", style={"backgroundColor":"#f0f4f8","padding":"8px","border":"1px solid #ddd"}),
                    ])),
                    html.Tbody([
                        html.Tr([
                            html.Td("Fanpage/Giới thiệu", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Nơi cung cấp thông tin chung, hướng dẫn, và cập nhật về công cụ.", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Mọi người dùng", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"})
                        ]),
                        html.Tr([
                            html.Td("Tạo Biểu đồ (Chart Creator)", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Chức năng chính: Tải dữ liệu, tiền xử lý, cấu hình tham số, và tạo biểu đồ Plotly tương tác.", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Người dùng phổ thông", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"})
                        ]),
                        html.Tr([
                            html.Td("Code Biểu đồ (Code Viewer)", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Chức năng nâng cao: Hiển thị code Python được tạo ra từ cấu hình Biểu đồ, cho phép người dùng xem và tái sử dụng.", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Lập trình viên/Coder", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"})
                        ]),
                    ])
                ]
            ),

            html.H2("2. Tải dữ liệu lên và xem trước."),

            html.H3("2.1. Tải lên"),

            # Các bullet và lưu ý (nguyên văn)
            html.Pre("""· Khu vực upload: tìm hộp lớn có biểu tượng 📁 và dòng chữ "Kéo/thả file hoặc Chọn file".

· Hỗ trợ định dạng: Bạn có thể tải lên các file CSV, XLSX (Excel), hoặc DOCX (Word, hệ thống sẽ cố gắng đọc bảng đầu tiên trong file).
· Hành động: Kéo file của bạn vào khu vực này hoặc nhấn vào "Chọn file" để duyệt từ máy tính. Lưu ý là file “.docx”, ứng dụng sẽ không nhận file “.doc”""", style={"whiteSpace":"pre-wrap","fontFamily":"inherit"}),

            html.H2("3. Chức năng chính: tạo biểu đồ (chart creator)"),
            html.P("Đây là nơi bạn sẽ thực hiện quá trình trực quan hóa dữ liệu."),

            html.H3("3.1. Điều kiện dữ liệu đầu vào."),

            # Bảng 2: Điều kiện dữ liệu (định dạng đẹp)
            dmc.Table(
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                children=[
                    html.Thead(html.Tr([
                        html.Th("Loại File", style={"backgroundColor":"#f0f4f8","padding":"8px","border":"1px solid #ddd"}),
                        html.Th("Điều kiện Bắt buộc", style={"backgroundColor":"#f0f4f8","padding":"8px","border":"1px solid #ddd"}),
                        html.Th("Khuyến nghị cho Biểu đồ", style={"backgroundColor":"#f0f4f8","padding":"8px","border":"1px solid #ddd"})
                    ])),
                    html.Tbody([
                        html.Tr([
                            html.Td("CSV/XLSX", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Hàng đầu tiên là Tên Cột (Header), mỗi hàng (row) phải xuống dòng, và các giá trị trong cùng một hàng phải được ngăn cách bằng dấu phẩy (,)", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Tất cả các ô dữ liệu nên được điền đầy đủ. Nên có 1 bảng dữ liệu mà thôi", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"})
                        ]),
                        html.Tr([
                            html.Td("DOCX", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("BẮT BUỘC phải có ít nhất một bảng (Table) trong tài liệu. Ứng dụng chỉ xử lý bảng đầu tiên được tìm thấy.", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"}),
                            html.Td("Tương tự CSV/XLSX, hàng đầu tiên của bảng phải là Tên Cột. Nên có 1 bảng dữ liệu mà thôi", style={"padding":"8px","border":"1px solid #ddd","verticalAlign":"top"})
                        ]),
                    ])
                ]
            ),
            html.H3('3.2. Xử lý dữ liệu tùy chỉnh.'),
            # Lưu ý chính xác nguyên văn từ Word
            html.Pre("""· Lưu ý: hàng đầu tiên của bảng (docx) hay văn bản (CSV/XLSX) chính là hàng cột của dữ liệu trong sau khi ứng dụng đã xử lí.
🎯 Tại sao phải tiền xử lý?

Biểu đồ Plotly Express (thư viện cốt lõi của ứng dụng) rất nhạy cảm với dữ liệu bị lỗi:

Giá trị Trống/Thiếu (Missing Values): Nếu cột X hoặc Y có giá trị trống (NaN), Plotly có thể bỏ qua toàn bộ điểm dữ liệu đó.

Sai Kiểu Dữ liệu (Wrong Data Types): Nếu cột Doanh_thu (đáng lẽ phải là số) lại chứa một vài giá trị là chuỗi (ví dụ: "N/A"), Plotly sẽ không thể tính toán và vẽ trục số học.

Tuy ứng dụng đã xử lí và không để bị gây lỗi, nhưng nếu bạn muốn đồ thị được liên tục, đẹp mắt, không bị trùng lặp, sai chính tả, những giá trị không hợp lí (giá cả âm) dẫn tới biểu đồ bị méo mó, nhóm sai hoặc đưa ra kết quả không đúng,... thì bạn nên xử lí dữ liệu trước khi đưa vào. Ngoài ra việc này còn giúp biểu đồ trông hợp lí và dễ đọc hơn ví dụ như phân nhóm (grouping), lọc(filtering), sắp xếp(sorting)...
""", style={"whiteSpace":"pre-wrap","fontFamily":"inherit"}),

            html.H3("3.3. Cấu hình “tham số biểu đồ”."),
            html.Pre("""Để tạo ra loại biểu đồ mình ưng ý nhanh chóng, tiện lợi, bạn chỉ cần chọn Loại biểu đồ phía trên và điền Tên cột tương ứng vào 75 ô tham số phía dưới.

· Ví dụ: Chọn Bar Chart. Chỉ điền vào "Bar X", "Bar Y", "Bar Color".

· Lưu ý: Tên cột phải chính xác 100% (có phân biệt chữ hoa/thường) so với header trong dữ liệu của bạn.
""", style={"whiteSpace":"pre-wrap","fontFamily":"inherit"}),

            html.H3("3.4. CHỨC NĂNG NÂNG CAO: CODE BIỂU ĐỒ (CODE VIEWER)"),
            html.Pre("""Trang này hiển thị toàn bộ cú pháp mã Python mà ứng dụng đã tạo ra để vẽ biểu đồ hiện tại.

· Lợi ích: Bạn có thể sao chép đoạn code này và tái sử dụng nó trong các dự án phân tích dữ liệu khác của mình (ví dụ: Jupyter Notebook, môi trường phát triển Dash/Flask riêng).

· Tính năng: Code được hiển thị trong một cửa sổ cuộn, tự động cập nhật mỗi khi bạn thay đổi tham số hoặc loại biểu đồ trong trang Tạo Biểu đồ và nhấn nút chạy...
· Cách sử dụng: nhập các dữ liệu (tên cột, giá trị, văn bản...) mà bạn muốn thay thế cho toàn bộ <...>, phần bên ngoài chính là cú pháp thông thường mà nhiều người hay sử dụng. Thành phần ứng dụng hiển thị bên trong <...> (ví dụ <tên cột x>) chỉ là hướng dẫn, bạn phải thay thế hết phần đó bằng dữ liệu của bạn thì code mới chạy được. Ngoài ra, nếu có thông tin cú pháp không sử dụng, bạn phải xóa đi, và nếu muốn thêm các tham số khác để tinh chỉnh biểu đồ của bạn thì chỉ cần phẩy (,) và viết tiếp.
""", style={"whiteSpace":"pre-wrap","fontFamily":"inherit"}),

            html.H2("4. Chức năng báo lỗi vẽ biểu đồ của Visualization Studio"),
            html.Pre("""Nếu bạn nhập sai tên cột, biểu đồ sẽ không bị crash mà thay vào đó sẽ hiển thị một hộp báo lỗi màu đỏ với thông báo cụ thể về lỗi (ví dụ: KeyError). Bạn chỉ cần sửa tên cột đã nhập theo gợi ý của khung báo lỗi.
""", style={"whiteSpace":"pre-wrap","fontFamily":"inherit"}),

            html.H2("5. Download biểu đồ"),
            html.Pre("""Nhấn vào nút "Tải SVG" để tải biểu đồ dưới định dạng SVG (Scalable Vector Graphics), đây là định dạng chất lượng cao, có thể thay đổi kích thước mà không bị vỡ ảnh.
""", style={"whiteSpace":"pre-wrap","fontFamily":"inherit"}),

            html.H2("6. Chuyển đổi theme ngày/đêm"),
            html.Pre("""Nhấn vào thanh gạc ngày/đêm phía trên cùng bên phải của trang (navbar), theme của toàn bộ trang sẽ chuyển đổi.
""", style={"whiteSpace":"pre-wrap","fontFamily":"inherit"}),

            # Thêm một footnote nhỏ nêu nguồn (không sửa nội dung, chỉ thông báo nguồn file)
            html.Div("Nội dung trên được copy nguyên văn từ file Word nguồn.", style={"marginTop":"16px","fontStyle":"italic"}),
            html.Div(html.Small("Source file: HƯỚNG DẪN SỬ DỤNG PHẦN MỀM VISUALIZATION STUDIO.doc"), style={"fontSize":"12px","color":"#666"})
        ], style={"whiteSpace": "pre-wrap", "lineHeight":"1.45", "padding":"10px"})
    ], style={"maxWidth":"1000px","margin":"0 auto"})


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
            dmc.Button("Trang chủ", variant="gradient"),
            style={"textDecoration": "none"}
            ),
        html.A(
            dmc.Button("Tạo biểu đồ qua tham số", variant="gradient"),
            href="https://easy-create-chart.onrender.com",
            target = '_blank',
            style={"textDecoration": "none"}
            ),
        html.A(
            dmc.Button("Tạo biểu đồ qua code", variant="gradient"),
            href="https://code-for-charts.onrender.com",
            target = '_blank',
            style={"textDecoration": "none"}
            ),
        dmc.Space(w=16),
        dmc.Text("Background:", size="sm"),
        dcc.Input(id="bg-url", placeholder="Image URL (optional)", style={"width":300}),
        dcc.Upload(id="bg-upload", children=html.Button("Upload bg"), style={"marginLeft":8})
    ]
)

content_box = dmc.Container(id="content", mt=140, children=fanpage_page())
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

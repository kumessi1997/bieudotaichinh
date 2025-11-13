  import pandas as pd
  import plotly.graph_objects as go
  from plotly.subplots import make_subplots

  # --- 1. XỬ LÝ DỮ LIỆU (Giống bước trước) ---
  file_path = '/Users/trungdungnguyen/Library/Mobile Documents/com~apple~CloudDocs/100dayofcoding/Chart/FiinProX_DE_Du_lieu_giao_dich_Chi_so__Nganh_Theo_chi_so_20251112.xlsx'

  # Đọc file, bỏ 8 dòng đầu để lấy header chuẩn
  df = pd.read_excel(file_path, skiprows=8)

  # Đổi tên cột cho gọn
  df.columns = ['STT', 'Date', 'MarketCap', 'TradingValue']

  # Chuyển đổi ngày tháng và sắp xếp
  df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
  df = df.sort_values('Date')

  # Lọc dữ liệu 2014 - 2025
  df = df[(df['Date'] >= '2014-01-01') & (df['Date'] <= '2025-12-31')]

  # Tỷ giá USD/VND ước tính (để quy đổi đơn vị)
  usd_rates = {
      2014: 21200, 2015: 21600, 2016: 22100, 2017: 22700, 
      2018: 22800, 2019: 23200, 2020: 23100, 2021: 22800,
      2022: 23600, 2023: 24000, 2024: 25000, 2025: 25400
  }
  df['Year'] = df['Date'].dt.year
  df['USD_Rate'] = df['Year'].map(usd_rates)

  # Quy đổi đơn vị
  # Market Cap: VND -> Tỷ USD ($bn). Giả định dữ liệu gốc là VND.
  df['MarketCap_BnUSD'] = df['MarketCap'] / df['USD_Rate'] / 1e9

  # Liquidity: VND -> Triệu USD ($mn).
  df['Liquidity_MnUSD'] = df['TradingValue'] / df['USD_Rate'] / 1e6
  # Làm mượt thanh khoản (MA 5 ngày) để biểu đồ đẹp hơn
  df['Liquidity_MA'] = df['Liquidity_MnUSD'].rolling(window=5).mean()

  # --- 2. VẼ BIỂU ĐỒ BẰNG PLOTLY ---

  # Tạo khung biểu đồ với 2 trục Y (secondary_y=True)
  fig = make_subplots(specs=[[{"secondary_y": True}]])

  # TRỤC PHẢI (RHS): Thanh khoản - Bar Chart
  # Dùng Bar chart, chỉnh độ mờ (opacity) để không che đường Line
  fig.add_trace(
      go.Bar(
          x=df['Date'],
          y=df['Liquidity_MnUSD'],
          name="Combined liquidity ($mn)",
          marker_color='#4db6ac', # Màu xanh ngọc
          opacity=0.6,
          marker_line_width=0 # Bỏ viền cột cho mượt
      ),
      secondary_y=True,
  )

  # TRỤC TRÁI (LHS): Vốn hóa - Line Chart
  fig.add_trace(
      go.Scatter(
          x=df['Date'],
          y=df['MarketCap_BnUSD'],
          name="Combined Market Cap ($bn)",
          mode='lines',
          line=dict(color='#b58b57', width=2.5) # Màu nâu vàng
      ),
      secondary_y=False,
  )

  # --- 3. TÙY CHỈNH GIAO DIỆN (LAYOUT) ---
  fig.update_layout(
      title_text="Vietnam Stock Market: Market Cap vs Liquidity (2014-2025)",
      title_x=0.5, # Căn giữa tiêu đề
      template="plotly_white", # Nền trắng
      legend=dict(
          orientation="h", # Legend nằm ngang
          yanchor="bottom",
          y=-0.2, # Đẩy xuống dưới biểu đồ
          xanchor="center",
          x=0.5
      ),
      hovermode="x unified", # Hiển thị thông tin cả 2 trục khi rê chuột
      margin=dict(l=20, r=20, t=50, b=50)
  )

  # Chỉnh trục Y trái (Vốn hóa)
  fig.update_yaxes(
      title_text="<b>Combined Market Cap ($bn)</b>",
      range=[0, 400], # Giới hạn trục 0-400 tỷ USD
      secondary_y=False,
      showgrid=True,
      gridcolor='lightgray'
  )

  # Chỉnh trục Y phải (Thanh khoản)
  fig.update_yaxes(
      title_text="<b>Combined liquidity ($mn)</b>",
      range=[0, 5000], # Giới hạn trục 0-5000 triệu USD
      secondary_y=True,
      showgrid=False # Tắt lưới trục phải cho đỡ rối
  )

  # Hiển thị biểu đồ
  fig.show()
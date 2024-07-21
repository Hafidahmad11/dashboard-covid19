from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.layouts import column
import pandas as pd

# Memuat Data dari CSV
data_url = 'https://drive.google.com/uc?id=1dTx33StIYr5vQr7JPZAXSdrze4Zmx5Xw'
data = pd.read_csv(data_url)

# Mengubah kolom tanggal menjadi tipe datetime
data['Date'] = pd.to_datetime(data['Date'])

# Mengisi missing values dengan 0
data_filled = data.fillna({'Total Cases': 0})

# Filter data untuk level provinsi
data_province = data_filled[data_filled['Location Level'] == 'Provinsi']

# ColumnDataSource untuk Bokeh
source = ColumnDataSource(data=dict(Date=data_province['Date'], Total_Cases=data_province['Total Cases']))

# Membuat Plot
plot = figure(title='Total Kasus Covid-19 di Indonesia', x_axis_type='datetime', width=800, height=400)
plot.line('Date', 'Total_Cases', source=source, line_width=2)

# Slider untuk Interaktivitas
slider = Slider(start=0, end=1000000, value=0, step=1000, title="Jumlah Kasus")

# Fungsi Update Data
def update_data(attr, old, new):
    new_value = slider.value
    filtered_data = data_province[data_province['Total Cases'] <= new_value]
    source.data = dict(Date=filtered_data['Date'], Total_Cases=filtered_data['Total Cases'])

slider.on_change('value', update_data)

# Layout
layout = column(slider, plot)

# Menambahkan Layout ke Document
curdoc().add_root(layout)

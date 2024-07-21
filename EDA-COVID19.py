import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

!gdown 1dTx33StIYr5vQr7JPZAXSdrze4Zmx5Xw

data = pd.read_csv('covid_19_indonesia_time_series_all.csv')

# Melihat 5 baris pertama data
print(data.head())

# Melihat informasi umum tentang data
print(data.info())

# Mengecek missing values
print(data.isnull().sum())

# Cek isi kolom 'Total Cases' sebelum pembersihan data
print(data['Total Cases'].describe())

data_cleaned = data.dropna()

# Mengecek missing values
print(data_cleaned.isnull().sum())

# EDA

# Melihat nama kolom dalam dataframe
print(data_cleaned.columns)

# Cek isi kolom 'Total Cases' setelah pembersihan data
print(data_cleaned['Total Cases'].describe())

# Mengisi missing values dengan nilai 0
data_filled = data.fillna({'Total Cases': 0})

# Cek isi kolom 'Total Cases' setelah pembersihan data
print(data_filled['Total Cases'].describe())

# Visualisasi distribusi kasus Covid-19 setelah mengisi missing values
plt.figure(figsize=(10, 6))
sns.histplot(data_filled['Total Cases'], bins=50, kde=True)
plt.title('Distribusi Total Kasus Covid-19 di Indonesia')
plt.xlabel('Total Kasus')
plt.ylabel('Frekuensi')
plt.show()

# Mengubah kolom tanggal menjadi tipe datetime
data_filled['Date'] = pd.to_datetime(data_filled['Date'])

# Plot tren waktu kasus Covid-19
plt.figure(figsize=(12, 8))
sns.lineplot(x='Date', y='Total Cases', data=data_filled)
plt.title('Tren Waktu Total Kasus Covid-19 di Indonesia')
plt.xlabel('Tanggal')
plt.ylabel('Total Kasus')
plt.xticks(rotation=45)
plt.show()

# Menghitung kasus harian
data_filled['Daily Cases'] = data_filled['Total Cases'].diff()

# Plot kasus harian
plt.figure(figsize=(12, 8))
sns.lineplot(x='Date', y='Daily Cases', data=data_filled)
plt.title('Kasus Harian Covid-19 di Indonesia')
plt.xlabel('Tanggal')
plt.ylabel('Kasus Harian')
plt.xticks(rotation=45)
plt.show()


# Visualisasi kasus berdasarkan provinsi
plt.figure(figsize=(14, 8))
sns.barplot(x='Province', y='Total Cases', data=data_filled)
plt.title('Total Kasus Covid-19 Berdasarkan Provinsi')
plt.xlabel('Provinsi')
plt.ylabel('Total Kasus')
plt.xticks(rotation=90)
plt.show()


# Mapping Covid-19 di Indonesia Tahun 2021

!pip install folium

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

data_province = data_filled[data_filled['Location Level'] == 'Province']

# Filter data untuk memastikan tidak ada nilai NaN dalam kolom Latitude dan Longitude
map_data = data_province.dropna(subset=['Latitude', 'Longitude'])

# Filter data untuk memastikan 'Total Cases' tidak bernilai 0
map_data = map_data[map_data['Total Cases'] != 0]

# Inisialisasi peta
m = folium.Map(location=[-2.5, 118], zoom_start=5)

# Tambahkan marker ke peta
for index, row in map_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Total Cases'] / 50000,  # Ukuran marker berdasarkan total kasus
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=folium.Popup(f"{row['Province']}: {row['Total Cases']} cases")
    ).add_to(m)

m

# Menyimpan peta sebagai file HTML
m.save('covid19_distribution_map.html')

# Dashboard

melihat beberapa persebaran covid dengan histogram plot yang interaktif

!pip install ipywidgets
!pip install plotly

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display, clear_output

# Mengunduh dan memuat data
!gdown 1dTx33StIYr5vQr7JPZAXSdrze4Zmx5Xw
data = pd.read_csv('covid_19_indonesia_time_series_all.csv')

# Mengisi missing values dengan 0
data_filled = data.fillna({'Total Cases': 0})


def plot_total_cases_distribution(data):
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Total Cases'], bins=50, kde=True)
    plt.title('Distribusi Total Kasus Covid-19 di Indonesia')
    plt.xlabel('Total Kasus')
    plt.ylabel('Frekuensi')
    plt.show()

def plot_cases_trend(data):
    data['Date'] = pd.to_datetime(data['Date'])
    plt.figure(figsize=(12, 8))
    sns.lineplot(x='Date', y='Total Cases', data=data)
    plt.title('Tren Waktu Total Kasus Covid-19 di Indonesia')
    plt.xlabel('Tanggal')
    plt.ylabel('Total Kasus')
    plt.xticks(rotation=45)
    plt.show()

def plot_daily_cases(data):
    data['Daily Cases'] = data['Total Cases'].diff()
    plt.figure(figsize=(12, 8))
    sns.lineplot(x='Date', y='Daily Cases', data=data)
    plt.title('Kasus Harian Covid-19 di Indonesia')
    plt.xlabel('Tanggal')
    plt.ylabel('Kasus Harian')
    plt.xticks(rotation=45)
    plt.show()

def plot_province_cases(data):
    plt.figure(figsize=(14, 8))
    sns.barplot(x='Province', y='Total Cases', data=data)
    plt.title('Total Kasus Covid-19 Berdasarkan Provinsi')
    plt.xlabel('Provinsi')
    plt.ylabel('Total Kasus')
    plt.xticks(rotation=90)
    plt.show()

# Fungsi untuk update plot berdasarkan pilihan
def update_dashboard(visualization):
    clear_output(wait=True)
    if visualization == 'Distribusi Kasus':
        plot_total_cases_distribution(data_filled)
    elif visualization == 'Tren Kasus':
        plot_cases_trend(data_filled)
    elif visualization == 'Kasus Harian':
        plot_daily_cases(data_filled)
    elif visualization == 'Kasus Berdasarkan Provinsi':
        plot_province_cases(data_filled)

# Widget dropdown untuk memilih visualisasi
visualization_selector = widgets.Dropdown(
    options=['Distribusi Kasus', 'Tren Kasus', 'Kasus Harian', 'Kasus Berdasarkan Provinsi'],
    value='Distribusi Kasus',
    description='Visualisasi:'
)

# Menghubungkan widget dengan fungsi update_dashboard
widgets.interactive(update_dashboard, visualization=visualization_selector)

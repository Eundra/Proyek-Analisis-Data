import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    data = pd.read_csv("day.csv")
    data["dteday"] = pd.to_datetime(data["dteday"])
    return data

data = load_data()

st.sidebar.header("Pengaturan Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", value=pd.to_datetime('2011-01-01'))
end_date = st.sidebar.date_input("Tanggal Akhir", value=pd.to_datetime('2012-12-31'))

filtered_data = data[(data["dteday"] >= pd.to_datetime(start_date)) & (data["dteday"] <= pd.to_datetime(end_date))]

st.header("Rata-rata Penyewaan Berdasarkan Bulan")
data_bulan = filtered_data.groupby(by='mnth').agg({
    'cnt': ['mean', 'max', 'min'],
    'temp': 'mean',
    'hum': 'mean',
    'windspeed': 'mean'
})

data_bulan.columns = ['_'.join(col) for col in data_bulan.columns]

plt.figure(figsize=(10, 5))
plt.plot(data_bulan.index, data_bulan["cnt_mean"], marker='o', linewidth=2, color="#72BCD4")
plt.title("Rata-rata kenaikan dan penurunan jumlah penyewa sepeda dalam beberapa bulan", loc="center", fontsize=20)
plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Rata-Rata Penyewaan", fontsize=12)
plt.xticks(ticks=data_bulan.index, labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], fontsize=10)
plt.grid(True)
st.pyplot(plt)

st.header("Penyewaan Berdasarkan Musim")
season_labels = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
data_musim = filtered_data.groupby('season')['cnt'].mean().reset_index()
data_musim['season'] = data_musim['season'].map(season_labels)

colors = ['#FFA07A', '#20B2AA', '#87CEFA', '#778899']
data_musim.plot(kind='bar', x='season', y='cnt', color=colors, legend=False)
plt.title('Penyewaan Berdasarkan Musim')
plt.ylabel('Jumlah Penyewaan Rata-rata')
plt.xlabel('Musim')
st.pyplot(plt)

st.header("Penyewaan Berdasarkan Kondisi Cuaca")
weather_labels = {1: 'Cerah', 2: 'Berkabut', 3: 'Salju Ringan'}
filtered_data['weathersit'] = filtered_data['weathersit'].map(weather_labels)

data_cuaca = filtered_data.groupby('weathersit')['cnt'].mean().reset_index()
colors = ['#1E90FF', '#4682B4', '#00008B']

data_cuaca.plot(kind='bar', x='weathersit', y='cnt', color=colors, legend=False)
plt.title('Kondisi Cuaca Berdampak terhadap Jumlah Sewa Sepeda')
plt.ylabel('Jumlah Penyewaan Rata-rata')
plt.xlabel('Cuaca')
st.pyplot(plt)

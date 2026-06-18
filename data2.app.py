import streamlit as st
import pandas as pd

# ==================================
# KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="Dashboard Data",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Data Produksi")

# ==================================
# MEMBACA DATA DARI GOOGLE DRIVE
# ==================================
url = "https://drive.google.com/uc?export=download&id=1nC77Pp3A9PXB6UiaV2NLCiisbFu-7sbH"

@st.cache_data
def load_data():
    return pd.read_excel(url)

df = load_data()

# ==================================
# SIDEBAR
# ==================================
st.sidebar.header("Filter Data")

kolom_filter = st.sidebar.selectbox(
    "Pilih Kolom",
    df.columns
)

pilihan = st.sidebar.multiselect(
    "Pilih Nilai",
    options=df[kolom_filter].dropna().unique(),
    default=df[kolom_filter].dropna().unique()
)

df_filter = df[df[kolom_filter].isin(pilihan)]

# ==================================
# METRIC
# ==================================
col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(df_filter))
col2.metric("Jumlah Kolom", len(df_filter.columns))
col3.metric("Missing Value", int(df_filter.isna().sum().sum()))

# ==================================
# DATAFRAME
# ==================================
st.subheader("📋 Data Produksi")

st.dataframe(
    df_filter,
    use_container_width=True
)

# ==================================
# GRAFIK
# ==================================
st.subheader("📊 Grafik")

kolom_numerik = df_filter.select_dtypes(include="number").columns

if len(kolom_numerik) > 0:
    kolom_grafik = st.selectbox(
        "Pilih Kolom Numerik",
        kolom_numerik
    )

    st.bar_chart(df_filter[kolom_grafik])

    st.line_chart(df_filter[kolom_grafik])

else:
    st.warning("Tidak ada kolom numerik yang dapat ditampilkan.")

# ==================================
# STATISTIK
# ==================================
st.subheader("📈 Statistik Deskriptif")

st.dataframe(df_filter.describe(include="all"))

# ==================================
# DOWNLOAD DATA
# ==================================
csv = df_filter.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Data CSV",
    data=csv,
    file_name="data_dashboard.csv",
    mime="text/csv"
)
import streamlit as st
import pandas as pd

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Dashboard Data Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Dashboard Statistik Mahasiswa")
st.markdown("Analisis Data Mahasiswa")

# ==========================
# LOAD DATA DARI GOOGLE DRIVE
# ==========================
@st.cache_data
def load_data():
    file_id = "1nC77Pp3A9PXB6UiaV2NLCiisbFu-7sbH"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    return pd.read_csv(url)

try:
    df = load_data()

    # ==========================
    # METRIK UTAMA
    # ==========================
    st.subheader("📊 Ringkasan Data")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jumlah Baris", len(df))
    col2.metric("Jumlah Kolom", len(df.columns))
    col3.metric("Missing Value", int(df.isna().sum().sum()))
    col4.metric("Data Duplikat", int(df.duplicated().sum()))

    st.divider()

    # ==========================
    # PREVIEW DATA
    # ==========================
    st.subheader("📋 Preview Dataset")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.divider()

    # ==========================
    # INFORMASI DATA
    # ==========================
    st.subheader("ℹ️ Informasi Kolom")

    info_df = pd.DataFrame({
        "Kolom": df.columns,
        "Tipe Data": df.dtypes.astype(str)
    })

    st.dataframe(info_df, use_container_width=True)

    st.divider()

    # ==========================
    # STATISTIK DESKRIPTIF
    # ==========================
    st.subheader("📈 Statistik Deskriptif")

    st.dataframe(
        df.describe(include="all"),
        use_container_width=True
    )

    st.divider()

    # ==========================
    # VISUALISASI
    # ==========================
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        st.subheader("📉 Visualisasi Data")

        selected_col = st.selectbox(
            "Pilih Variabel Numerik",
            numeric_cols
        )

        st.write("### Grafik Batang")
        st.bar_chart(df[selected_col])

        st.write("### Grafik Garis")
        st.line_chart(df[selected_col])

    else:
        st.warning("Tidak ditemukan kolom numerik pada dataset.")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

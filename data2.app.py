import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Data Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Dashboard Data Mahasiswa")

@st.cache_data
def load_data():
    file_id = "1nC77Pp3A9PXB6UiaV2NLCiisbFu-7sbH"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # jika encoding default gagal
    try:
        return pd.read_csv(url)
    except:
        return pd.read_csv(url, encoding="latin1")

try:
    df = load_data()

    st.success("Data berhasil dimuat")

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Data", len(df))
    col2.metric("Jumlah Kolom", len(df.columns))
    col3.metric("Missing Value", int(df.isna().sum().sum()))

    st.subheader("Dataset")
    st.dataframe(df, use_container_width=True)

    st.subheader("Informasi Kolom")
    st.write(df.dtypes)

except Exception as e:
    st.error(f"Error: {e}")

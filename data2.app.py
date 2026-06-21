import streamlit as st
import pandas as pd

# =====================================
# KONFIGURASI HALAMAN
# =====================================
st.set_page_config(
    page_title="Dashboard Survei Hobi",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Dashboard Statistik Survei Hobi")
st.markdown("Analisis Data Seputar Hobi")

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    file_id = "1nC77Pp3A9PXB6UiaV2NLCiisbFu-7sbH"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    try:
        df = pd.read_csv(url, sep=";")
    except:
        df = pd.read_csv(url)

    return df

try:

    df = load_data()

    # =====================================
    # KPI
    # =====================================
    st.subheader("📊 Ringkasan Data")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jumlah Responden", len(df))
    col2.metric("Jumlah Variabel", len(df.columns))
    col3.metric("Missing Value", int(df.isna().sum().sum()))
    col4.metric("Data Duplikat", int(df.duplicated().sum()))

    st.divider()

    # =====================================
    # PREVIEW DATA
    # =====================================
    st.subheader("📋 Preview Dataset")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.divider()

    # =====================================
    # INFORMASI DATA
    # =====================================
    st.subheader("ℹ️ Informasi Kolom")

    info_df = pd.DataFrame({
        "Kolom": df.columns,
        "Tipe Data": df.dtypes.astype(str),
        "Missing": df.isna().sum().values
    })

    st.dataframe(info_df, use_container_width=True)

    st.divider()

    # =====================================
    # STATISTIK DESKRIPTIF
    # =====================================
    st.subheader("📈 Statistik Deskriptif")

    st.dataframe(
        df.describe(include="all"),
        use_container_width=True
    )

    st.divider()

    # =====================================
    # VISUALISASI NUMERIK
    # =====================================
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        st.subheader("📊 Visualisasi Numerik")

        selected_col = st.selectbox(
            "Pilih Variabel Numerik",
            numeric_cols
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Grafik Batang")
            st.bar_chart(df[selected_col])

        with col2:
            st.write("### Grafik Garis")
            st.line_chart(df[selected_col])

    st.divider()

    # =====================================
    # VISUALISASI KATEGORIK
    # =====================================
    categorical_cols = df.select_dtypes(
        exclude="number"
    ).columns

    if len(categorical_cols) > 0:

        st.subheader("📋 Distribusi Data Kategorik")

        selected_cat = st.selectbox(
            "Pilih Variabel Kategorik",
            categorical_cols
        )

        kategori = (
            df[selected_cat]
            .value_counts()
        )

        st.bar_chart(kategori)

        st.write("Frekuensi Data")
        st.dataframe(kategori)

    st.divider()

    # =====================================
    # MISSING VALUE
    # =====================================
    st.subheader("🔥 Missing Value")

    missing_df = pd.DataFrame({
        "Kolom": df.columns,
        "Missing": df.isna().sum()
    })

    st.bar_chart(
        missing_df.set_index("Kolom")
    )

    st.divider()

    # =====================================
    # DATASET LENGKAP
    # =====================================
    st.subheader("📑 Dataset Lengkap")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard Statistik Mahasiswa",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Statistik Data Mahasiswa")

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    file_id = "1nC77Pp3A9PXB6UiaV2NLCiisbFu-7sbH"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    return pd.read_csv(url)

try:
    df = load_data()

    # =====================
    # KPI
    # =====================
    st.subheader("Ringkasan Data")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jumlah Baris", len(df))
    col2.metric("Jumlah Kolom", len(df.columns))
    col3.metric("Missing Value", int(df.isna().sum().sum()))
    col4.metric("Duplikat", int(df.duplicated().sum()))

    st.divider()

    # =====================
    # DATASET
    # =====================
    st.subheader("Preview Data")

    st.dataframe(df.head(20), use_container_width=True)

    st.divider()

    # =====================
    # STATISTIK DESKRIPTIF
    # =====================
    st.subheader("Statistik Deskriptif")

    st.dataframe(
        df.describe(include="all"),
        use_container_width=True
    )

    st.divider()

    # =====================
    # KOLOM NUMERIK
    # =====================
    num_cols = df.select_dtypes(include="number").columns

    if len(num_cols) > 0:

        st.subheader("Distribusi Data")

        selected_col = st.selectbox(
            "Pilih Variabel",
            num_cols
        )

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.hist(df[selected_col].dropna(), bins=10)
            ax.set_title(f"Histogram {selected_col}")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.boxplot(df[selected_col].dropna())
            ax.set_title(f"Boxplot {selected_col}")
            st.pyplot(fig)

        st.divider()

        # =====================
        # KORELASI
        # =====================
        if len(num_cols) > 1:

            st.subheader("Matriks Korelasi")

            corr = df[num_cols].corr()

            fig, ax = plt.subplots(figsize=(8,6))
            cax = ax.matshow(corr)
            fig.colorbar(cax)

            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))

            ax.set_xticklabels(corr.columns, rotation=90)
            ax.set_yticklabels(corr.columns)

            st.pyplot(fig)

    else:
        st.warning("Dataset tidak memiliki kolom numerik.")

except Exception as e:
    st.error(f"Terjadi Error: {e}")

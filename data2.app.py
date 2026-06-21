import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Dashboard Data Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Dashboard Statistik Mahasiswa")
st.markdown("### Analisis Data Mahasiswa Interaktif")

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
        "Tipe Data": df.dtypes.astype(str),
        "Missing Value": df.isna().sum().values
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
    # VISUALISASI NUMERIK
    # ==========================
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        st.subheader("📊 Visualisasi Statistik")

        selected_col = st.selectbox(
            "Pilih Variabel Numerik",
            numeric_cols
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📈 Histogram", "📉 Line Chart", "📊 Bar Chart", "📦 Box Plot"]
        )

        with tab1:
            fig = px.histogram(
                df,
                x=selected_col,
                nbins=20,
                title=f"Distribusi {selected_col}"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig = px.line(
                df,
                y=selected_col,
                title=f"Trend {selected_col}"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            fig = px.bar(
                df,
                y=selected_col,
                title=f"Bar Chart {selected_col}"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab4:
            fig = px.box(
                df,
                y=selected_col,
                title=f"Box Plot {selected_col}"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ==========================
    # VISUALISASI KATEGORIK
    # ==========================
    categorical_cols = df.select_dtypes(
        exclude="number"
    ).columns

    if len(categorical_cols) > 0:

        st.divider()
        st.subheader("🥧 Distribusi Data Kategorik")

        cat_col = st.selectbox(
            "Pilih Variabel Kategorik",
            categorical_cols
        )

        pie_data = (
            df[cat_col]
            .value_counts()
            .reset_index()
        )

        pie_data.columns = [cat_col, "Jumlah"]

        fig = px.pie(
            pie_data,
            names=cat_col,
            values="Jumlah",
            hole=0.4,
            title=f"Distribusi {cat_col}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ==========================
    # MISSING VALUE
    # ==========================
    st.divider()
    st.subheader("🔥 Missing Value")

    missing_df = pd.DataFrame({
        "Kolom": df.columns,
        "Missing": df.isna().sum().values
    })

    fig = px.bar(
        missing_df,
        x="Kolom",
        y="Missing",
        title="Jumlah Missing Value per Kolom"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==========================
    # KORELASI
    # ==========================
    if len(numeric_cols) > 1:

        st.divider()
        st.subheader("🔥 Heatmap Korelasi")

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Korelasi Antar Variabel Numerik"
        )

        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

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
# ==========================
# VISUALISASI INTERAKTIF
# ==========================
st.subheader("📊 Visualisasi Statistik")

numeric_cols = df.select_dtypes(include="number").columns
categorical_cols = df.select_dtypes(exclude="number").columns

if len(numeric_cols) > 0:

    selected_col = st.selectbox(
        "Pilih Variabel Numerik",
        numeric_cols
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Distribusi",
        "📦 Outlier",
        "🔥 Korelasi",
        "📊 Trend"
    ])

    # ======================
    # HISTOGRAM
    # ======================
    with tab1:

        fig_hist = px.histogram(
            df,
            x=selected_col,
            nbins=20,
            title=f"Distribusi {selected_col}"
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    # ======================
    # BOXPLOT
    # ======================
    with tab2:

        fig_box = px.box(
            df,
            y=selected_col,
            title=f"Deteksi Outlier {selected_col}"
        )

        st.plotly_chart(fig_box, use_container_width=True)

    # ======================
    # HEATMAP KORELASI
    # ======================
    with tab3:

        if len(numeric_cols) > 1:

            corr = df[numeric_cols].corr()

            fig_heat = px.imshow(
                corr,
                text_auto=True,
                title="Heatmap Korelasi"
            )

            st.plotly_chart(
                fig_heat,
                use_container_width=True
            )

        else:
            st.info("Minimal 2 kolom numerik.")

    # ======================
    # LINE CHART
    # ======================
    with tab4:

        fig_line = px.line(
            df,
            y=selected_col,
            title=f"Trend {selected_col}"
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

# ==========================
# VISUALISASI KATEGORIK
# ==========================
if len(categorical_cols) > 0:

    st.subheader("🥧 Analisis Data Kategorik")

    cat_col = st.selectbox(
        "Pilih Kolom Kategorik",
        categorical_cols
    )

    value_counts = (
        df[cat_col]
        .value_counts()
        .reset_index()
    )

    value_counts.columns = [
        cat_col,
        "Jumlah"
    ]

    col1, col2 = st.columns(2)

    with col1:

        fig_bar = px.bar(
            value_counts,
            x=cat_col,
            y="Jumlah",
            title=f"Distribusi {cat_col}"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with col2:

        fig_pie = px.pie(
            value_counts,
            names=cat_col,
            values="Jumlah",
            title=f"Persentase {cat_col}"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

# ==========================
# DOWNLOAD DATA
# ==========================
st.subheader("⬇️ Download Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="dataset_mahasiswa.csv",
    mime="text/csv"
)

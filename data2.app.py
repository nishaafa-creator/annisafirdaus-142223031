import streamlit as st
import pandas as pd
import plotly.express as px

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

    df = pd.read_csv(url, sep=";")

    # hapus kolom kosong
    df = df.dropna(axis=1, how="all")

    return df

try:

    df = load_data()

    # =====================================
    # KPI
    # =====================================
    st.subheader("📊 Ringkasan Responden")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Jumlah Responden",
        len(df)
    )

    col2.metric(
        "Jumlah Variabel",
        len(df.columns)
    )

    col3.metric(
        "Missing Value",
        int(df.isna().sum().sum())
    )

    col4.metric(
        "Jenis Hobi",
        df["Jenis hobi yang paling sering Anda lakukan adalah"].nunique()
    )

    st.divider()

    # =====================================
    # DISTRIBUSI JENIS KELAMIN
    # =====================================
    col1, col2 = st.columns(2)

    with col1:

        gender = (
            df["JENIS KELAMIN"]
            .value_counts()
            .reset_index()
        )

        gender.columns = ["Jenis Kelamin", "Jumlah"]

        fig = px.pie(
            gender,
            names="Jenis Kelamin",
            values="Jumlah",
            hole=0.4,
            title="Distribusi Jenis Kelamin"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        usia = (
            df["USIA"]
            .value_counts()
            .reset_index()
        )

        usia.columns = ["Usia", "Jumlah"]

        fig = px.bar(
            usia,
            x="Usia",
            y="Jumlah",
            title="Distribusi Usia"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================
    # HOBI TERPOPULER
    # =====================================
    hobi = (
        df["Jenis hobi yang paling sering Anda lakukan adalah"]
        .value_counts()
        .reset_index()
    )

    hobi.columns = ["Hobi", "Jumlah"]

    fig = px.bar(
        hobi,
        x="Hobi",
        y="Jumlah",
        title="Jenis Hobi Terpopuler",
        text="Jumlah"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================
    # FREKUENSI HOBI
    # =====================================
    frek = (
        df["  Seberapa sering Anda melakukan hobi dalam seminggu?  "]
        .value_counts()
        .reset_index()
    )

    frek.columns = ["Frekuensi", "Jumlah"]

    fig = px.bar(
        frek,
        x="Frekuensi",
        y="Jumlah",
        title="Frekuensi Melakukan Hobi"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================
    # MANFAAT HOBI
    # =====================================
    st.subheader("😊 Dampak Positif Hobi")

    manfaat_cols = [
        "apakah  Hobi yang anda miliki membuat anda merasa lebih bahagia  ",
        "apakah  Hobi membantu anda meningkatkan keterampilan atau kemampuan tertentu  ",
        " apakah Hobi anda membantu mengurangi stres setelah melakukan aktivitas sehari-hari.  "
    ]

    for col in manfaat_cols:

        hasil = (
            df[col]
            .value_counts()
            .reset_index()
        )

        hasil.columns = ["Jawaban", "Jumlah"]

        fig = px.pie(
            hasil,
            names="Jawaban",
            values="Jumlah",
            title=col
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================
    # DATASET
    # =====================================
    st.subheader("📋 Dataset Lengkap")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

import streamlit as st

import pandas as pd

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
# PIE CHART DATA KATEGORIK
# ==========================
if len(categorical_cols) > 0:

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
# HEATMAP MISSING VALUE
# ==========================
st.subheader("🔥 Missing Value per Kolom")

missing_df = pd.DataFrame({
    "Kolom": df.columns,
    "Missing": df.isna().sum().values
})

fig = px.bar(
    missing_df,
    x="Kolom",
    y="Missing",
    title="Jumlah Missing Value"
)

st.plotly_chart(fig, use_container_width=True)

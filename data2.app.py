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

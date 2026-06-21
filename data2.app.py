import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Data Hobi",
    page_icon="🎯",
    layout="wide",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f5f7fa; }
    .block-container { padding: 2rem 2rem 1rem; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-value { font-size: 2.2rem; font-weight: 700; color: #4f46e5; }
    .metric-label { font-size: 0.85rem; color: #6b7280; margin-top: 4px; }
    h1 { color: #1e1b4b; }
    h2, h3 { color: #312e81; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";")
    df.columns = df.columns.str.strip()
    # Rename columns to short keys
    df = df.rename(columns={
        "Jenis hobi yang paling sering Anda lakukan adalah": "Jenis Hobi",
        "Seberapa sering Anda melakukan hobi dalam seminggu?": "Frekuensi",
        "apakah  Hobi yang anda miliki membuat anda merasa lebih bahagia": "Lebih Bahagia",
        "apakah  Hobi membantu anda meningkatkan keterampilan atau kemampuan tertentu": "Tingkatkan Skill",
        "apakah Hobi anda membantu mengurangi stres setelah melakukan aktivitas sehari-hari.": "Kurangi Stres",
        "apakah anda merasa waktu luang  lebih bermanfaat ketika digunakan untuk melakukan hobi.": "Waktu Bermanfaat",
        "Apakah anda sering berbagi atau melakukan hobi bersama teman atau komunitas.": "Hobi Bersama",
    })
    return df

df = load_data("/mnt/user-data/uploads/Data_seputar_Hobi.csv")

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🎯 Dashboard Data Seputar Hobi")
st.markdown("Analisis survei hobi dari **{} responden**".format(len(df)))
st.divider()

# ─── Sidebar Filter ────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/hobby-horse.png", width=80)
    st.header("🔍 Filter Data")

    jenis_kelamin_opt = ["Semua"] + sorted(df["JENIS KELAMIN"].dropna().unique().tolist())
    selected_gender = st.selectbox("Jenis Kelamin", jenis_kelamin_opt)

    usia_opt = ["Semua"] + sorted(df["USIA"].dropna().unique().tolist())
    selected_usia = st.selectbox("Kelompok Usia", usia_opt)

    hobi_opt = ["Semua"] + sorted(df["Jenis Hobi"].dropna().unique().tolist())
    selected_hobi = st.selectbox("Jenis Hobi", hobi_opt)

    st.markdown("---")
    st.caption("Data diambil dari survei Google Form")

# ─── Apply Filters ─────────────────────────────────────────────────────────────
filtered = df.copy()
if selected_gender != "Semua":
    filtered = filtered[filtered["JENIS KELAMIN"] == selected_gender]
if selected_usia != "Semua":
    filtered = filtered[filtered["USIA"] == selected_usia]
if selected_hobi != "Semua":
    filtered = filtered[filtered["Jenis Hobi"] == selected_hobi]

# ─── KPI Cards ─────────────────────────────────────────────────────────────────
n = len(filtered)
pct_bahagia  = round(filtered["Lebih Bahagia"].eq("YA").sum() / n * 100) if n else 0
pct_stres    = round(filtered["Kurangi Stres"].eq("YA").sum() / n * 100) if n else 0
pct_skill    = round(filtered["Tingkatkan Skill"].eq("YA").sum() / n * 100) if n else 0
pct_bersama  = round(filtered["Hobi Bersama"].eq("YA").sum() / n * 100) if n else 0

k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, value, label, emoji):
    col.markdown(
        f'<div class="metric-card">'
        f'<div style="font-size:1.6rem">{emoji}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-label">{label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

kpi(k1, n,                "Total Responden",     "👤")
kpi(k2, f"{pct_bahagia}%","Merasa Lebih Bahagia","😊")
kpi(k3, f"{pct_stres}%",  "Kurangi Stres",       "🧘")
kpi(k4, f"{pct_skill}%",  "Tingkatkan Skill",    "💪")
kpi(k5, f"{pct_bersama}%","Hobi Bersama",        "🤝")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Row 1: Jenis Hobi & Frekuensi ────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎮 Distribusi Jenis Hobi")
    hobi_counts = filtered["Jenis Hobi"].value_counts().reset_index()
    hobi_counts.columns = ["Hobi", "Jumlah"]
    colors = ["#4f46e5", "#7c3aed", "#a855f7"]
    fig_hobi = px.bar(
        hobi_counts, x="Hobi", y="Jumlah", text="Jumlah",
        color="Hobi", color_discrete_sequence=colors,
    )
    fig_hobi.update_traces(textposition="outside", marker_line_width=0)
    fig_hobi.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="", yaxis_title="Jumlah Responden",
        font=dict(size=13), margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_hobi, use_container_width=True)

with col2:
    st.subheader("📅 Frekuensi Melakukan Hobi per Minggu")
    freq_counts = filtered["Frekuensi"].value_counts().reset_index()
    freq_counts.columns = ["Frekuensi", "Jumlah"]
    fig_freq = px.pie(
        freq_counts, names="Frekuensi", values="Jumlah",
        hole=0.4,
        color_discrete_sequence=["#4f46e5", "#7c3aed", "#a855f7", "#c084fc"],
    )
    fig_freq.update_traces(textinfo="label+percent", textfont_size=13)
    fig_freq.update_layout(
        showlegend=True, paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=20, b=40),
    )
    st.plotly_chart(fig_freq, use_container_width=True)

# ─── Row 2: Demografi ─────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("⚧ Distribusi Jenis Kelamin")
    gender_counts = filtered["JENIS KELAMIN"].value_counts().reset_index()
    gender_counts.columns = ["Jenis Kelamin", "Jumlah"]
    fig_gender = px.bar(
        gender_counts, x="Jenis Kelamin", y="Jumlah",
        text="Jumlah", color="Jenis Kelamin",
        color_discrete_map={"LAKI-LAKI": "#4f46e5", "PEREMPUAN": "#a855f7"},
    )
    fig_gender.update_traces(textposition="outside", marker_line_width=0)
    fig_gender.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="", yaxis_title="Jumlah",
        font=dict(size=13), margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with col4:
    st.subheader("🎂 Distribusi Kelompok Usia")
    usia_counts = filtered["USIA"].value_counts().reset_index()
    usia_counts.columns = ["Usia", "Jumlah"]
    fig_usia = px.pie(
        usia_counts, names="Usia", values="Jumlah",
        color_discrete_sequence=["#4f46e5", "#7c3aed", "#a855f7"],
    )
    fig_usia.update_traces(textinfo="label+percent+value", textfont_size=13)
    fig_usia.update_layout(
        showlegend=False, paper_bgcolor="white",
        margin=dict(t=20, b=10),
    )
    st.plotly_chart(fig_usia, use_container_width=True)

# ─── Row 3: Manfaat Hobi ──────────────────────────────────────────────────────
st.subheader("📊 Persepsi Manfaat Hobi (Ya vs Tidak)")

manfaat_cols = {
    "Lebih Bahagia":   "Membuat Lebih Bahagia",
    "Tingkatkan Skill":"Meningkatkan Skill",
    "Kurangi Stres":   "Mengurangi Stres",
    "Waktu Bermanfaat":"Waktu Lebih Bermanfaat",
    "Hobi Bersama":    "Hobi Bersama Komunitas",
}

manfaat_data = []
for col_key, label in manfaat_cols.items():
    vc = filtered[col_key].value_counts()
    ya    = vc.get("YA", 0)
    tidak = vc.get("TIDAK", 0)
    manfaat_data.append({"Pertanyaan": label, "YA": ya, "TIDAK": tidak})

mdf = pd.DataFrame(manfaat_data)

fig_manfaat = go.Figure()
fig_manfaat.add_trace(go.Bar(
    name="YA", x=mdf["Pertanyaan"], y=mdf["YA"],
    marker_color="#4f46e5", text=mdf["YA"], textposition="inside",
))
fig_manfaat.add_trace(go.Bar(
    name="TIDAK", x=mdf["Pertanyaan"], y=mdf["TIDAK"],
    marker_color="#e5e7eb", text=mdf["TIDAK"], textposition="inside",
))
fig_manfaat.update_layout(
    barmode="stack", plot_bgcolor="white", paper_bgcolor="white",
    xaxis_title="", yaxis_title="Jumlah Responden",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(size=13), margin=dict(t=20, b=10),
)
st.plotly_chart(fig_manfaat, use_container_width=True)

# ─── Row 4: Crosstab Hobi x Gender ───────────────────────────────────────────
st.subheader("🔗 Jenis Hobi berdasarkan Jenis Kelamin")

ct = pd.crosstab(filtered["Jenis Hobi"], filtered["JENIS KELAMIN"])
fig_ct = go.Figure()
for i, gender in enumerate(ct.columns):
    fig_ct.add_trace(go.Bar(
        name=gender, x=ct.index, y=ct[gender],
        marker_color=["#4f46e5", "#a855f7"][i % 2],
        text=ct[gender], textposition="inside",
    ))
fig_ct.update_layout(
    barmode="group", plot_bgcolor="white", paper_bgcolor="white",
    xaxis_title="Jenis Hobi", yaxis_title="Jumlah",
    font=dict(size=13), margin=dict(t=20, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_ct, use_container_width=True)

# ─── Raw Data Table ───────────────────────────────────────────────────────────
with st.expander("📋 Lihat Data Mentah"):
    show_cols = ["NAMA", "JENIS KELAMIN", "USIA", "Jenis Hobi", "Frekuensi",
                 "Lebih Bahagia", "Tingkatkan Skill", "Kurangi Stres",
                 "Waktu Bermanfaat", "Hobi Bersama"]
    st.dataframe(
        filtered[show_cols].reset_index(drop=True),
        use_container_width=True, height=300,
    )
    csv = filtered[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "data_hobi_filtered.csv", "text/csv")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("📊 Dashboard Survei Hobi · Dibuat dengan Streamlit & Plotly")

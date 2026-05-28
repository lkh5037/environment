import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="속초 환경 분석",
    layout="wide"
)

st.title("🌿 속초 환경 위험 지수")

data = {
    "장소": ["속초해수욕장", "영랑호", "속초중앙시장"],
    "PM2.5": [12, 8, 35],
    "PM10": [25, 18, 70]
}

df = pd.DataFrame(data)

df["환경점수"] = 100 - (df["PM2.5"] + df["PM10"]) / 2

place = st.selectbox("장소 선택", df["장소"])

selected = df[df["장소"] == place].iloc[0]

st.metric(
    "환경 점수",
    round(selected["환경점수"], 1)
)

fig = px.bar(
    df,
    x="장소",
    y="환경점수",
    color="환경점수"
)

st.plotly_chart(fig, use_container_width=True)

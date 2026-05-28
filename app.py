import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="속초 환경 위험 지수 분석",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 속초 환경 위험 지수 분석 시스템")
st.markdown("속초 지역 장소별 공기질 및 환경 위험도를 분석합니다.")

# -------------------------------------------------
# 샘플 데이터
# -------------------------------------------------

data = {
    "장소": [
        "속초해수욕장",
        "영랑호",
        "속초중앙시장",
        "설악산 입구",
        "청초호"
    ],
    "PM2.5": [12, 8, 35, 10, 15],
    "PM10": [25, 18, 70, 20, 30],
    "CO2": [420, 390, 700, 410, 450],
    "VOC": [0.3, 0.2, 0.8, 0.2, 0.4],
    "온도": [24, 22, 29, 20, 23],
    "습도": [60, 65, 70, 55, 68],
    "설명": [
        "관광객이 많은 해변 지역",
        "공기가 맑은 호수 주변",
        "교통량과 인구 밀집도가 높은 시장",
        "자연환경이 우수한 산악지역",
        "호수와 도심이 혼합된 지역"
    ],
    "위도": [38.1900, 38.2070, 38.2045, 38.1194, 38.2040],
    "경도": [128.6010, 128.5900, 128.5912, 128.4656, 128.5940]
}

df = pd.DataFrame(data)

# -------------------------------------------------
# 환경 점수 계산 함수
# -------------------------------------------------

def calculate_environment_score(row):
    score = 100

    # PM2.5
    if row["PM2.5"] > 35:
        score -= 30
    elif row["PM2.5"] > 15:
        score -= 15

    # PM10
    if row["PM10"] > 80:
        score -= 25
    elif row["PM10"] > 30:
        score -= 10

    # CO2
    if row["CO2"] > 1000:
        score -= 20
    elif row["CO2"] > 600:
        score -= 10

    # VOC
    if row["VOC"] > 1.0:
        score -= 20
    elif row["VOC"] > 0.5:
        score -= 10

    return max(score, 0)

df["환경점수"] = df.apply(calculate_environment_score, axis=1)

# -------------------------------------------------
# 위험 분석 함수
# -------------------------------------------------

def analyze_risk(row):
    risks = []

    if row["PM2.5"] > 15:
        risks.append("초미세먼지 농도가 높음")

    if row["PM10"] > 30:
        risks.append("미세먼지 농도가 높음")

    if row["CO2"] > 600:
        risks.append("이산화탄소 농도가 높음")

    if row["VOC"] > 0.5:
        risks.append("휘발성 유기화합물 농도가 높음")

    if len(risks) == 0:
        return "위험 요소가 낮고 비교적 안전함"

    return ", ".join(risks)

df["위험요소"] = df.apply(analyze_risk, axis=1)

# -------------------------------------------------
# 위험도 등급
# -------------------------------------------------

def risk_grade(score):
    if score >= 85:
        return "매우 좋음"
    elif score >= 70:
        return "좋음"
    elif score >= 50:
        return "보통"
    elif score >= 30:
        return "나쁨"
    else:
        return "매우 나쁨"

df["등급"] = df["환경점수"].apply(risk_grade)

# -------------------------------------------------
# 사이드바
# -------------------------------------------------

st.sidebar.header("분석 설정")

selected_place = st.sidebar.selectbox(
    "장소 선택",
    df["장소"]
)

selected_data = df[df["장소"] == selected_place].iloc[0]

# -------------------------------------------------
# 메인 정보
# -------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "환경 점수",
        f"{selected_data['환경점수']}점"
    )

with col2:
    st.metric(
        "환경 등급",
        selected_data["등급"]
    )

with col3:
    st.metric(
        "PM2.5",
        f"{selected_data['PM2.5']} μg/m³"
    )

# -------------------------------------------------
# 장소 설명
# -------------------------------------------------

st.subheader("📍 장소 설명")
st.write(selected_data["설명"])

# -------------------------------------------------
# 위험 요소 설명
# -------------------------------------------------

st.subheader("⚠ 위험 요소 분석")
st.error(selected_data["위험요소"])

# -------------------------------------------------
# 상세 수치
# -------------------------------------------------

st.subheader("📊 환경 데이터")

detail_df = pd.DataFrame({
    "항목": ["PM2.5", "PM10", "CO2", "VOC", "온도", "습도"],
    "수치": [
        selected_data["PM2.5"],
        selected_data["PM10"],
        selected_data["CO2"],
        selected_data["VOC"],
        selected_data["온도"],
        selected_data["습도"]
    ]
})

fig = px.bar(
    detail_df,
    x="항목",
    y="수치",
    color="수치",
    color_continuous_scale="RdYlGn_r",
    title="환경 데이터 시각화"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 전체 장소 비교
# -------------------------------------------------

st.subheader("🏆 장소별 환경 점수 비교")

fig2 = px.bar(
    df,
    x="장소",
    y="환경점수",
    color="환경점수",
    color_continuous_scale="RdYlGn",
    text="환경점수"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# 지도 표시
# -------------------------------------------------

st.subheader("🗺 속초 지역 지도")

map_df = df.rename(columns={
    "위도": "lat",
    "경도": "lon"
})

st.map(map_df)

# -------------------------------------------------
# 데이터 테이블
# -------------------------------------------------

st.subheader("📋 전체 데이터")

st.dataframe(df)

# -------------------------------------------------
# 추가 설명
# -------------------------------------------------

st.info("""
환경 점수는 다음 기준으로 계산됩니다.

- PM2.5 높음 → 감점
- PM10 높음 → 감점
- CO2 높음 → 감점
- VOC 높음 → 감점

점수가 높을수록 안전한 환경입니다.
""")

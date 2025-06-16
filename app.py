import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="지하철 노선별 분석", layout="wide")

# 📦 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("subway.csv")
    
    # 날짜 변환 (오류 무시)
    df["사용일자"] = pd.to_datetime(df["사용일자"], format="%Y%m%d", errors="coerce")
    
    # 날짜 변환 실패한 행 제거
    df = df.dropna(subset=["사용일자"])

    # 월 컬럼 추가
    df["월"] = df["사용일자"].dt.to_period("M")
    
    return df

df = load_data()

# 📊 월별 × 노선별 승하차 통계
monthly_stats = df.groupby(["월", "노선명"])[["승차총승객수", "하차총승객수"]].sum().reset_index()

# 🏆 노선별 최고 승하차
def get_max_stat(df, col):
    idx = df.groupby("노선명")[col].idxmax()
    return df.loc[idx, ["노선명", "역명", "사용일자", col]]

max_boarding = get_max_stat(df, "승차총승객수").rename(columns={"승차총승객수": "최대승차수"})
max_alighting = get_max_stat(df, "하차총승객수").rename(columns={"하차총승객수": "최대하차수"})

summary = pd.merge(max_boarding, max_alighting, on="노선명", suffixes=("_승차", "_하차"))

# 🖥️ Streamlit 앱 UI
st.title("🚇 지하철 노선별 승하차 분석 대시보드")

# 🔹 최고 승하차 표
st.subheader("📋 노선별 최고 승하차 역 및 날짜")
st.dataframe(summary)

# 🔸 월별 승차 그래프
st.subheader("📈 월별 노선별 총 승차 인원")
pivot_board = monthly_stats.pivot(index="월", columns="노선명", values="승차총승객수")
fig1, ax1 = plt.subplots(figsize=(14, 6))
pivot_board.plot(ax=ax1)
plt.xticks(rotation=45)
plt.ylabel("승차 인원수")
st.pyplot(fig1)

# 🔸 월별 하차 그래프
st.subheader("📉 월별 노선별 총 하차 인원")
pivot_alight = monthly_stats.pivot(index="월", columns="노선명", values="하차총승객수")
fig2, ax2 = plt.subplots(figsize=(14, 6))
pivot_alight.plot(ax=ax2)
plt.xticks(rotation=45)
plt.ylabel("하차 인원수")
st.pyplot(fig2)

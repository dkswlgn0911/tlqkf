import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("subway.csv")
    df = df[["노선명", "승차총승객수", "하차총승객수"]]
    return df

df = load_data()

# 노선별로 그룹화
line_stats = df.groupby("노선명")[["승차총승객수", "하차총승객수"]].sum().sort_values(by="승차총승객수", ascending=False)

# 제목
st.title("🚇 지하철 노선별 승하차 분석 대시보드")

# 데이터표
st.dataframe(line_stats)

# 그래프 그리기
st.subheader("노선별 총 승차 인원")
fig1, ax1 = plt.subplots()
line_stats["승차총승객수"].plot(kind="bar", ax=ax1, color="skyblue")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("노선별 총 하차 인원")
fig2, ax2 = plt.subplots()
line_stats["하차총승객수"].plot(kind="bar", ax=ax2, color="salmon")
plt.xticks(rotation=45)
st.pyplot(fig2)

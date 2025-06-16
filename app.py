import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="노선별 전체 이용객 순위", layout="wide")

# 데이터 불러오기
df = pd.read_csv("subway.csv")

# 사용하지 않을 날짜 제거
if "사용일자" in df.columns:
    df = df.drop(columns=["사용일자"])

# 노선명별 총 승차+하차 인원 계산
df["총이용객수"] = df["승차총승객수"] + df["하차총승객수"]
total_by_line = df.groupby("노선명")["총이용객수"].sum().sort_values(ascending=False)

# 시각화
st.title("🚇 노선별 전체 이용객 수 순위")

fig, ax = plt.subplots(figsize=(12, 6))
total_by_line.plot(kind="bar", ax=ax, color="skyblue")
plt.ylabel("총 이용객 수")
plt.xlabel("노선명")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

import pandas as pd
import matplotlib.pyplot as plt

# CSV 불러오기
df = pd.read_csv("subway.csv")

# 날짜 형식 변환
df["사용일자"] = pd.to_datetime(df["사용일자"], format="%Y%m%d")

# '월' 컬럼 생성
df["월"] = df["사용일자"].dt.to_period("M")

# 📊 월별 × 노선별 총 승하차 인원 집계
monthly_line_stats = df.groupby(["월", "노선명"])[["승차총승객수", "하차총승객수"]].sum().reset_index()

# 그래프 그리기
pivot_board = monthly_line_stats.pivot(index="월", columns="노선명", values="승차총승객수")
pivot_alight = monthly_line_stats.pivot(index="월", columns="노선명", values="하차총승객수")

pivot_board.plot(kind="bar", stacked=True, figsize=(15, 6), title="월별 노선별 승차 인원")
plt.tight_layout()
plt.show()

pivot_alight.plot(kind="bar", stacked=True, figsize=(15, 6), title="월별 노선별 하차 인원")
plt.tight_layout()
plt.show()

# 🏆 노선별 최고 승/하차 역과 날짜 찾기
def get_max_stat(df, column):
    idx = df.groupby("노선명")[column].idxmax()
    return df.loc[idx, ["노선명", "역명", "사용일자", column]]

max_boarding = get_max_stat(df, "승차총승객수").rename(columns={"승차총승객수": "최대승차수"})
max_alighting = get_max_stat(df, "하차총승객수").rename(columns={"하차총승객수": "최대하차수"})

# 병합
max_summary = pd.merge(max_boarding, max_alighting, on="노선명", suffixes=("_승차", "_하차"))

# 결과 출력
print("\n📋 노선별 최대 승/하차 역 및 날짜:")
print(max_summary)

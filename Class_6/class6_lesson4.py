import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV
df = pd.read_csv("考試分數_3年6班.csv", encoding="utf-8-sig")

# 選擇要分析的學生
student_name = "鄭雅文"
zhao = df[df["學生姓名"] == student_name]

# 防呆：確認有找到資料
if zhao.empty:
    raise ValueError(f"找不到學生：{student_name}")

# 取出各科成績
scores = zhao.iloc[0][["語文", "數學", "英語", "物理", "化學"]]

# 字型設定
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 桌布風格：深色背景
fig, ax = plt.subplots(figsize=(12, 6), facecolor="#111827")
ax.set_facecolor("#111827")

# 長條圖
bars = ax.bar(scores.index, scores.values, color=["#60A5FA", "#34D399", "#FBBF24", "#F472B6", "#A78BFA"])

# 數值標籤
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{height}",
        ha="center",
        va="bottom",
        color="white",
        fontsize=12
    )

# 標題與座標軸
ax.set_title(f"{student_name} 成績分析", fontsize=20, color="white", pad=20)
ax.set_xlabel("科目", fontsize=14, color="white")
ax.set_ylabel("分數", fontsize=14, color="white")

# 座標軸顏色
ax.tick_params(axis="x", colors="white", labelsize=12)
ax.tick_params(axis="y", colors="white", labelsize=12)
for spine in ax.spines.values():
    spine.set_color("white")

# 網格
ax.grid(axis="y", linestyle="--", alpha=0.25, color="white")

plt.tight_layout()
plt.show()
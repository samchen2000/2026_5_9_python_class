import streamlit as st
import matplotlib.pyplot as plt

# 頁面標題
st.title('手機品牌市占率圓餅圖')

# 資料
brands = ['Nokia', 'Samsung', 'Apple', 'Lumia']
values = [20, 30, 45, 10]
colors = ['yellow', 'green', 'red', 'blue']
explode = (0.3, 0, 0, 0)  # 第一塊突出 0.3

# 設定中文字型並繪製圓餅圖
with plt.rc_context({'font.sans-serif': ['Microsoft JhengHei', 'Arial Unicode MS', 'Heiti TC'],
                     'axes.unicode_minus': False}):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        values,
        labels=brands,
        colors=colors,
        explode=explode,
        shadow=True,
        autopct='%1.1f%%',
        startangle=180
    )
    ax.axis('equal')  # 確保圓形

# 顯示在 Streamlit
st.pyplot(fig)

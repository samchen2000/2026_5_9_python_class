import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 設定中文字型（微軟正黑體，適用 Windows）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 產生 X 軸資料：0 到 4π，共 500 個點
x = np.linspace(0, 4 * np.pi, 500)

# 初始參數
A_init = 1.0      # 振幅
omega_init = 1.0  # 角頻率
phi_init = 0.0    # 相位偏移

# 計算初始波形
y_sin = A_init * np.sin(omega_init * x + phi_init)
y_cos = A_init * np.cos(omega_init * x + phi_init)

# 建立圖表
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(bottom=0.30)  # 預留空間給滑桿

# 繪製兩條曲線
sin_curve, = ax.plot(x, y_sin, label='sin', color='blue', linewidth=2)
cos_curve, = ax.plot(x, y_cos, label='cos', color='orange', linewidth=2)

# 設定圖表外觀
ax.set_title('正弦 (sin) 與餘弦 (cos) 波形', fontsize=14, fontweight='bold')
ax.set_xlabel('X (弧度)', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-5.5, 5.5)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=12)

# 建立振幅滑桿
ax_amp = plt.axes([0.15, 0.15, 0.70, 0.03])
slider_amp = Slider(
    ax_amp, '振幅 (A)', 0.1, 5.0,
    valinit=A_init, valstep=0.05
)

# 建立頻率滑桿
ax_freq = plt.axes([0.15, 0.10, 0.70, 0.03])
slider_freq = Slider(
    ax_freq, '頻率 (ω)', 0.1, 10.0,
    valinit=omega_init, valstep=0.05
)

# 建立相位偏移滑桿
ax_phase = plt.axes([0.15, 0.05, 0.70, 0.03])
slider_phase = Slider(
    ax_phase, '相位偏移 (φ)', 0, 2 * np.pi,
    valinit=phi_init, valstep=0.01
)


def update(val):
    """滑桿更新回呼：重新計算並繪製波形"""
    A = slider_amp.val
    omega = slider_freq.val
    phi = slider_phase.val

    sin_curve.set_ydata(A * np.sin(omega * x + phi))
    cos_curve.set_ydata(A * np.cos(omega * x + phi))

    # 動態調整 Y 軸範圍
    ax.set_ylim(-A * 1.1, A * 1.1)
    fig.canvas.draw_idle()


# 綁定滑桿變更事件
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

plt.show()

import tkinter as tk
from tkinter import messagebox
import random
import math

# =========================
# 超精美猜數字遊戲
# =========================

WIDTH = 800
HEIGHT = 600

# 主視窗
root = tk.Tk()
root.title("🎮 Ultimate 猜數字遊戲")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

# 顏色
BG = "#0F172A"
PANEL = "#1E293B"
GOLD = "#FACC15"
WHITE = "#F8FAFC"
RED = "#EF4444"
GREEN = "#22C55E"
BLUE = "#38BDF8"
PURPLE = "#A855F7"

# 遊戲資料
answer = random.randint(1, 100)
guess_count = 0
min_num = 1
max_num = 100

# =========================
# Canvas
# =========================
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG,
    highlightthickness=0
)
canvas.pack()

# 星空背景
stars = []
for _ in range(80):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(1, 3)
    stars.append((x, y, size))

def draw_background():
    canvas.delete("bg")

    # 漸層背景效果
    for i in range(0, HEIGHT, 2):
        color = f'#{15+i//8:02x}{23+i//12:02x}{42+i//20:02x}'
        canvas.create_line(
            0, i, WIDTH, i,
            fill=color,
            tags="bg"
        )

    # 星星
    for x, y, s in stars:
        canvas.create_oval(
            x, y, x+s, y+s,
            fill="white",
            outline="",
            tags="bg"
        )

draw_background()

# =========================
# 標題
# =========================
title = canvas.create_text(
    WIDTH//2,
    60,
    text="🎯 GUESS THE NUMBER 🎯",
    fill=GOLD,
    font=("Arial", 30, "bold")
)

subtitle = canvas.create_text(
    WIDTH//2,
    105,
    text="猜出 1 ~ 100 的神秘數字",
    fill=WHITE,
    font=("Arial", 16)
)

# =========================
# 中央面板
# =========================
panel = canvas.create_rectangle(
    150, 150, 650, 500,
    fill=PANEL,
    outline=BLUE,
    width=3
)

# 狀態文字
status_text = canvas.create_text(
    WIDTH//2,
    200,
    text="開始挑戰吧！",
    fill=WHITE,
    font=("Arial", 22, "bold")
)

# 提示範圍
range_text = canvas.create_text(
    WIDTH//2,
    250,
    text="範圍：1 ~ 100",
    fill=BLUE,
    font=("Arial", 18)
)

# 次數
count_text = canvas.create_text(
    WIDTH//2,
    290,
    text="猜測次數：0",
    fill=GOLD,
    font=("Arial", 18)
)

# =========================
# 輸入框
# =========================
entry = tk.Entry(
    root,
    font=("Arial", 24, "bold"),
    justify="center",
    bg="#334155",
    fg="white",
    insertbackground="white",
    relief="flat",
    width=10
)

entry_window = canvas.create_window(
    WIDTH//2,
    350,
    window=entry
)

# =========================
# 動畫圖形
# =========================
pulse_size = 0
pulse_direction = 1

def animate_circle():
    global pulse_size, pulse_direction

    canvas.delete("pulse")

    size = 60 + pulse_size

    canvas.create_oval(
        WIDTH//2 - size,
        430 - size,
        WIDTH//2 + size,
        430 + size,
        outline=PURPLE,
        width=4,
        tags="pulse"
    )

    pulse_size += pulse_direction

    if pulse_size > 15:
        pulse_direction = -1
    elif pulse_size < 0:
        pulse_direction = 1

    root.after(50, animate_circle)

animate_circle()

# =========================
# 特效
# =========================
particles = []

def create_particles(color):
    for _ in range(25):
        particles.append({
            "x": WIDTH//2,
            "y": 430,
            "dx": random.randint(-8, 8),
            "dy": random.randint(-8, 8),
            "size": random.randint(4, 10),
            "color": color,
            "life": 30
        })

def animate_particles():
    canvas.delete("particle")

    for p in particles[:]:
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["life"] -= 1

        canvas.create_oval(
            p["x"],
            p["y"],
            p["x"] + p["size"],
            p["y"] + p["size"],
            fill=p["color"],
            outline="",
            tags="particle"
        )

        if p["life"] <= 0:
            particles.remove(p)

    root.after(30, animate_particles)

animate_particles()

# =========================
# 遊戲邏輯
# =========================
def check_guess():
    global guess_count, min_num, max_num, answer

    value = entry.get()

    if not value.isdigit():
        messagebox.showwarning("錯誤", "請輸入數字！")
        return

    guess = int(value)

    if guess < 1 or guess > 100:
        messagebox.showwarning("錯誤", "請輸入 1~100")
        return

    guess_count += 1

    canvas.itemconfig(
        count_text,
        text=f"猜測次數：{guess_count}"
    )

    # 太小
    if guess < answer:
        min_num = max(min_num, guess)

        canvas.itemconfig(
            status_text,
            text="📉 太小了！",
            fill=BLUE
        )

        create_particles(BLUE)

    # 太大
    elif guess > answer:
        max_num = min(max_num, guess)

        canvas.itemconfig(
            status_text,
            text="📈 太大了！",
            fill=RED
        )

        create_particles(RED)

    # 猜對
    else:
        canvas.itemconfig(
            status_text,
            text="🎉 猜對了！！！",
            fill=GREEN
        )

        create_particles(GOLD)

        messagebox.showinfo(
            "恭喜",
            f"你用了 {guess_count} 次猜中！"
        )

        again = messagebox.askyesno(
            "再玩一次",
            "要重新開始嗎？"
        )

        if again:
            reset_game()
        else:
            root.destroy()

    canvas.itemconfig(
        range_text,
        text=f"範圍：{min_num} ~ {max_num}"
    )

    entry.delete(0, tk.END)

# =========================
# 重置
# =========================
def reset_game():
    global answer, guess_count, min_num, max_num

    answer = random.randint(1, 100)
    guess_count = 0
    min_num = 1
    max_num = 100

    canvas.itemconfig(
        status_text,
        text="新的遊戲開始！",
        fill=WHITE
    )

    canvas.itemconfig(
        count_text,
        text="猜測次數：0"
    )

    canvas.itemconfig(
        range_text,
        text="範圍：1 ~ 100"
    )

# =========================
# 按鈕
# =========================
def hover_on(e):
    guess_btn.config(bg="#16A34A")

def hover_off(e):
    guess_btn.config(bg=GREEN)

guess_btn = tk.Button(
    root,
    text="🔥 猜數字 🔥",
    font=("Arial", 18, "bold"),
    bg=GREEN,
    fg="white",
    activebackground="#16A34A",
    relief="flat",
    padx=20,
    pady=10,
    command=check_guess,
    cursor="hand2"
)

guess_btn.bind("<Enter>", hover_on)
guess_btn.bind("<Leave>", hover_off)

btn_window = canvas.create_window(
    WIDTH//2,
    520,
    window=guess_btn
)

# Enter 快捷鍵
root.bind("<Return>", lambda event: check_guess())

# =========================
# 執行
# =========================
root.mainloop()
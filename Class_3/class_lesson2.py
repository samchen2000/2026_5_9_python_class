import tkinter as tk
from tkinter import messagebox
import random

# 建立主視窗
root = tk.Tk()
root.title("🎯 猜數字遊戲")
root.geometry("500x400")
root.configure(bg="#2C3E50")

# 隨機數字
answer = random.randint(1, 100)
guess_count = 0

# 標題
title_label = tk.Label(
    root,
    text="🎲 猜數字遊戲 🎲",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#2C3E50"
)
title_label.pack(pady=20)

# 說明
info_label = tk.Label(
    root,
    text="請輸入 1 ~ 100 的數字",
    font=("Arial", 14),
    fg="#ECF0F1",
    bg="#2C3E50"
)
info_label.pack()

# 輸入框
guess_entry = tk.Entry(
    root,
    font=("Arial", 18),
    justify="center",
    width=10
)
guess_entry.pack(pady=20)

# 結果顯示
result_label = tk.Label(
    root,
    text="開始猜吧！",
    font=("Arial", 16, "bold"),
    fg="#F1C40F",
    bg="#2C3E50"
)
result_label.pack(pady=10)

# 次數顯示
count_label = tk.Label(
    root,
    text="猜測次數：0",
    font=("Arial", 12),
    fg="white",
    bg="#2C3E50"
)
count_label.pack()

# 畫布 (圖形顯示)
canvas = tk.Canvas(root, width=200, height=120, bg="#34495E", highlightthickness=0)
canvas.pack(pady=20)

# 初始圖形
circle = canvas.create_oval(60, 20, 140, 100, fill="#3498DB")


def check_guess():
    global guess_count, answer

    user_input = guess_entry.get()

    if not user_input.isdigit():
        messagebox.showwarning("錯誤", "請輸入數字！")
        return

    guess = int(user_input)
    guess_count += 1

    count_label.config(text=f"猜測次數：{guess_count}")

    # 清除舊圖形
    canvas.delete("all")

    if guess < answer:
        result_label.config(text="📉 太小了！", fg="#1ABC9C")

        # 畫向上箭頭
        canvas.create_polygon(
            100, 20,
            160, 80,
            120, 80,
            120, 100,
            80, 100,
            80, 80,
            40, 80,
            fill="#2ECC71"
        )

    elif guess > answer:
        result_label.config(text="📈 太大了！", fg="#E74C3C")

        # 畫向下箭頭
        canvas.create_polygon(
            100, 100,
            160, 40,
            120, 40,
            120, 20,
            80, 20,
            80, 40,
            40, 40,
            fill="#E74C3C"
        )

    else:
        result_label.config(text="🎉 猜對了！", fg="#F1C40F")

        # 畫星星
        points = [
            100, 20,
            120, 80,
            180, 80,
            130, 120,
            150, 180,
            100, 140,
            50, 180,
            70, 120,
            20, 80,
            80, 80
        ]

        # 縮小比例
        scaled_points = []
        for i in range(0, len(points), 2):
            x = points[i] * 0.8
            y = points[i + 1] * 0.5
            scaled_points.extend([x, y])

        canvas.create_polygon(
            scaled_points,
            fill="#F1C40F",
            outline="white",
            width=2
        )

        play_again = messagebox.askyesno(
            "成功",
            f"你用了 {guess_count} 次猜中！\n要再玩一次嗎？"
        )

        if play_again:
            answer = random.randint(1, 100)
            guess_count = 0
            count_label.config(text="猜測次數：0")
            result_label.config(text="新的遊戲開始！", fg="#F1C40F")
            canvas.delete("all")
            canvas.create_oval(60, 20, 140, 100, fill="#3498DB")
            guess_entry.delete(0, tk.END)
        else:
            root.quit()

    guess_entry.delete(0, tk.END)


# 按鈕
guess_button = tk.Button(
    root,
    text="猜！",
    font=("Arial", 16, "bold"),
    bg="#27AE60",
    fg="white",
    activebackground="#2ECC71",
    width=10,
    command=check_guess
)
guess_button.pack(pady=10)

# Enter 鍵支援
root.bind("<Return>", lambda event: check_guess())

# 執行
root.mainloop()
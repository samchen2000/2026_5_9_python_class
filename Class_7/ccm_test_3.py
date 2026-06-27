import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from skimage.color import rgb2lab
import threading
import math
import os

# ==========================================
# ccm_test_3.py - 互動式 CCM 調整工具
# ==========================================

def apply_ccm(image_rgb, ccm_matrix):
    img_float = image_rgb.astype(np.float32)
    corrected_float = cv2.transform(img_float, ccm_matrix)
    corrected_clipped = np.clip(corrected_float, 0, 255).astype(np.uint8)
    return corrected_clipped


# ==========================================
# 24色色彩卡生成
# ==========================================
def create_24_color_chart_with_labels():
    colors_rgb = [
        (115, 82, 68),      # 1. Deep Skin
        (194, 150, 130),    # 2. Light Skin
        (98, 122, 157),     # 3. Blue Sky
        (87, 108, 67),      # 4. Foliage
        (133, 128, 177),    # 5. Blue Flower
        (103, 189, 170),    # 6. Bluish Green
        (214, 126, 44),     # 7. Orange
        (80, 91, 166),      # 8. Purplish-blue
        (193, 90, 99),      # 9. Moderate-red
        (94, 60, 108),      # 10. Purple
        (157, 188, 64),     # 11. Yellow-green
        (224, 163, 46),     # 12. Orange-yellow
        (56, 61, 150),      # 13. Blue
        (70, 148, 73),      # 14. Green
        (175, 54, 60),      # 15. Red
        (231, 199, 31),     # 16. Yellow
        (187, 86, 149),     # 17. Magenta
        (8, 133, 161),      # 18. Cyan
        (243, 243, 242),    # 19. White
        (200, 200, 200),    # 20. Neutral 8
        (160, 160, 160),    # 21. Neutral 6.5
        (122, 122, 121),    # 22. Neutral 5
        (85, 85, 85),       # 23. Neutral 3.5
        (52, 52, 52),       # 24. Black
    ]

    patch_size = 150
    rows, cols = 4, 6
    height = rows * patch_size
    width = cols * patch_size

    img_bgr = np.zeros((height, width, 3), dtype=np.uint8)

    for idx, (r, g, b) in enumerate(colors_rgb):
        row = idx // cols
        col = idx % cols
        y1 = row * patch_size
        y2 = y1 + patch_size
        x1 = col * patch_size
        x2 = x1 + patch_size
        img_bgr[y1:y2, x1:x2] = [b, g, r]

    return img_bgr, colors_rgb


def get_color_names():
    names = [
        "Deep Skin", "Light Skin", "Blue Sky", "Foliage",
        "Blue Flower", "Bluish Green", "Orange", "Purplish Red",
        "Moderate-red", "Yellow", "Yellow-green", "Orange-yellow",
        "Blue", "Green", "Red", "Yellow", "Magenta", "Cyan",
        "White", "Neutral 8", "Neutral 6.5", "Neutral 5",
        "Neutral 3.5", "Black"
    ]
    return names


def rgb_to_lab(rgb_tuple):
    rgb_normalized = np.array(rgb_tuple) / 255.0
    lab = rgb2lab(np.array([[[rgb_normalized[0], rgb_normalized[1], rgb_normalized[2]]]]))
    return lab[0, 0]


# --- 參考 Lab 值 (ISO) ---
COLORS_LAB_REF = [
    (38.02, 11.80, 13.67),   (65.67, 13.67, 16.90),
    (50.63, 0.37, -21.60),   (43.00, -15.88, 20.45),
    (55.68, 12.76, -25.17),  (70.99, -30.64, 1.54),
    (61.14, 28.10, 56.13),   (41.12, 17.41, -41.88),
    (51.33, 42.10, 14.89),   (31.10, 24.35, -22.10),
    (71.90, -28.10, 56.96),  (71.04, 12.60, 64.92),
    (30.35, 26.43, -49.67),  (55.03, -40.14, 32.30),
    (41.35, 49.30, 24.66),   (80.70, -3.66, 77.55),
    (51.14, 48.15, -15.28),  (51.15, -19.73, -23.37),
    (95.82, -0.18, 0.49),    (80.60, -0.00, 0.00),
    (65.87, -0.00, 0.00),    (51.19, -0.20, 0.55),
    (36.15, -0.00, 0.00),    (21.70, -0.00, 0.00),
]


# --- 全局數據結構 ---
global_data = {
    'lab_values': [],
    'color_names': [],
    'text_widget': None,
    'colors_rgb_original': [],
    'current_ccm': np.eye(3),

    'fig': None,
    'ax': None,
    'img_display': None,
    'ax_adjusted': None,

    'user_image': None,
    'user_image_display': None,
    'color_boxes': [],
    'is_manual_mode': False,
    'box_positions': [],
    'selected_box_idx': None,
    'dragging_mode': None,
}


# ==========================================
# Lab 顯示更新
# ==========================================
def update_text_display():
    colors_Lab = COLORS_LAB_REF

    if global_data['text_widget'] is None:
        return

    text_widget = global_data['text_widget']
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)

    content = "=" * 75 + "\n"
    content += "24 color - Lab value with CCM Adjusted RGB\n"
    content += "=" * 75 + "\n\n"

    current_ccm = global_data['current_ccm'].astype(np.float32)

    for i, (lab, name) in enumerate(zip(global_data['lab_values'], global_data['color_names'])):
        lab_org = colors_Lab[i]
        deltaE = math.sqrt(((lab_org[0] - lab[0])**2) + ((lab_org[1] - lab[1])**2) + ((lab_org[2] - lab[2])**2))
        deltaC_real = math.sqrt((lab[1]**2) + (lab[2]**2))
        deltaC_org = math.sqrt((lab_org[1])**2 + (lab_org[2])**2)
        deltaC = deltaC_real - deltaC_org

        if i < len(global_data['colors_rgb_original']):
            rgb_org = global_data['colors_rgb_original'][i]
            color_float = np.array(rgb_org, dtype=np.float32).reshape(1, 1, 3)
            corrected_color = cv2.transform(color_float, current_ccm)
            corrected_color_clipped = np.clip(corrected_color[0, 0], 0, 255).astype(np.uint8)
            r_norm = corrected_color_clipped[0] / 255.0
            g_norm = corrected_color_clipped[1] / 255.0
            b_norm = corrected_color_clipped[2] / 255.0
            rgb_max = max(r_norm, g_norm, b_norm)
            rgb_min = min(r_norm, g_norm, b_norm)
            rgb_delta = rgb_max - rgb_min
            if rgb_max == 0:
                sat_value = 0
            else:
                sat_value = (rgb_delta / rgb_max) * 255
        else:
            sat_value = 0

        content += f"【色塊 #{i+1:2d}】{name:15s}\n"
        content += f"  L*: {lab[0]:4.2f}  a*: {lab[1]:4.2f}  b*: {lab[2]:4.2f}"
        content += f"  ΔE: {deltaE:4.2f}  ΔC: {deltaC:4.2f}  Sat: {sat_value:4.2f}\n"
        content += "  " + "-" * 75 + "\n"

    text_widget.insert('1.0', content)
    text_widget.config(state=tk.DISABLED)


def update_lab_display(colors_rgb):
    global_data['lab_values'] = []
    global_data['color_names'] = get_color_names()
    global_data['colors_rgb_original'] = colors_rgb

    for color_rgb in colors_rgb:
        lab = rgb_to_lab(color_rgb)
        global_data['lab_values'].append(lab)

    update_text_display()


# ==========================================
# 自動色塊檢測
# ==========================================
def detect_color_blocks_kmeans(image_rgb, num_clusters=24):
    h, w = image_rgb.shape[:2]
    pixels = image_rgb.reshape(-1, 3)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels.astype(np.float32),
        num_clusters,
        None,
        criteria,
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )

    labels = labels.flatten()

    box_positions = []
    for cluster_id in range(num_clusters):
        mask = (labels == cluster_id)
        if not mask.any():
            continue

        y_coords, x_coords = np.where(mask.reshape(h, w))
        if len(y_coords) == 0:
            continue

        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()

        box_width = max(x_max - x_min, 10)
        box_height = max(y_max - y_min, 10)

        box_positions.append({
            'x': x_min,
            'y': y_min,
            'width': box_width,
            'height': box_height,
            'cluster_id': cluster_id
        })

    if box_positions:
        box_positions.sort(key=lambda b: (b['y'], b['x']))

    return box_positions[:24]


def create_initial_boxes(ax_adjusted, num_boxes=24):
    global_data['color_boxes'] = []
    global_data['box_positions'] = []
    global_data['selected_box_idx'] = None

    ax_width = ax_adjusted.get_xlim()[1] - ax_adjusted.get_xlim()[0]
    ax_height = ax_adjusted.get_ylim()[1] - ax_adjusted.get_ylim()[0]

    cols = 6
    rows = 4
    box_width = ax_width / cols * 0.95
    box_height = ax_height / rows * 0.95

    for i in range(num_boxes):
        row = i // cols
        col = i % cols

        x = col * (ax_width / cols) + (ax_width / cols - box_width) / 2
        y = row * (ax_height / rows) + (ax_height / rows - box_height) / 2

        rect = Rectangle((x, y), box_width, box_height,
                         linewidth=2, edgecolor='cyan',
                         facecolor='none', picker=True)
        ax_adjusted.add_patch(rect)
        global_data['color_boxes'].append(rect)

        global_data['box_positions'].append({
            'x': x,
            'y': y,
            'width': box_width,
            'height': box_height,
            'index': i
        })


# ==========================================
# 圖片操作
# ==========================================
def open_image_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="選擇圖片",
        filetypes=[
            ("圖片文件", "*.jpg *.jpeg *.png *.bmp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("所有文件", "*.*")
        ]
    )

    root.destroy()

    if not file_path:
        return False

    img_bgr = cv2.imread(file_path)
    if img_bgr is None:
        messagebox.showerror("錯誤", "無法讀取圖片文件")
        return False

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    target_height = 400
    target_width = 400

    h, w = img_rgb.shape[:2]
    scale = min(target_width / w, target_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    img_rgb_resized = cv2.resize(img_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)

    global_data['user_image'] = img_rgb_resized
    global_data['is_manual_mode'] = True

    return True


def load_user_image_to_plot(ax_adjusted):
    if global_data['user_image'] is None:
        return False

    for rect in global_data['color_boxes']:
        rect.remove()
    global_data['color_boxes'] = []
    global_data['box_positions'] = []
    global_data['selected_box_idx'] = None

    if global_data['user_image_display'] is not None:
        global_data['user_image_display'].remove()

    global_data['user_image_display'] = ax_adjusted.imshow(global_data['user_image'])
    ax_adjusted.set_title("User Image - Click to Select Box", fontsize=12, fontweight='bold')

    try:
        box_positions = detect_color_blocks_kmeans(global_data['user_image'], 24)

        for pos in box_positions:
            rect = Rectangle((pos['x'], pos['y']), pos['width'], pos['height'],
                            linewidth=2, edgecolor='cyan',
                            facecolor='none', picker=True)
            ax_adjusted.add_patch(rect)
            global_data['color_boxes'].append(rect)
            global_data['box_positions'].append(pos)

        if len(global_data['color_boxes']) == 0:
            create_initial_boxes(ax_adjusted, 24)

    except Exception as e:
        print(f"自動檢測失敗: {e}")
        create_initial_boxes(ax_adjusted, 24)

    # 初始化 Lab 值 (標準色卡參考)
    global_data['colors_rgb_original'] = []
    global_data['lab_values'] = []
    global_data['color_names'] = get_color_names()
    for i in range(len(global_data['color_boxes'])):
        global_data['colors_rgb_original'].append((128, 128, 128))
        global_data['lab_values'].append(rgb_to_lab((128, 128, 128)))

    return True


# ==========================================
# Lab 分析窗口
# ==========================================
def create_lab_window():
    root = tk.Tk()
    root.title("24 色色彩卡 Lab 值分析")
    root.geometry("750x850")

    title_label = tk.Label(root, text="24 色色彩卡 - L*a*b 色彩空間數據", font=("Consolas", 14, "bold"))
    title_label.pack(pady=10)

    text_widget = scrolledtext.ScrolledText(root, width=85, height=45, font=("Courier", 10))
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    global_data['text_widget'] = text_widget

    update_text_display()

    root.mainloop()


# ==========================================
# 主程式
# ==========================================
IMAGE_PATH = 'sample.jpg'

img_bgr = cv2.imread(IMAGE_PATH)

if img_bgr is None:
    print("\n已改用 24 色色彩卡進行演示。\n")
    img_bgr, colors_rgb = create_24_color_chart_with_labels()
else:
    colors_rgb = None

img_rgb_original = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

if colors_rgb:
    update_lab_display(colors_rgb)
    lab_thread = threading.Thread(target=create_lab_window, daemon=True)
    lab_thread.start()
    print("24 color blocks Lab value automatically calculated")
    print("已開啟 Lab 分析視窗 (獨立窗口)")
    print()

# --- Matplotlib 介面 ---
fig, (ax_original, ax_adjusted) = plt.subplots(1, 2, figsize=(16, 10))
plt.subplots_adjust(left=0.10, right=0.95, bottom=0.60)

ax_original.imshow(img_rgb_original)
ax_original.set_title("Original Color Chart", fontsize=14, fontweight='bold')
ax_original.axis('off')

img_display = ax_adjusted.imshow(img_rgb_original)
ax_adjusted.set_title("Adjusted Color Chart (CCM)", fontsize=14, fontweight='bold')
ax_adjusted.axis('off')

global_data['img_display'] = img_display
global_data['ax_adjusted'] = ax_adjusted

# --- 菜單欄 ---
manager = fig.canvas.manager
if manager and hasattr(manager, 'window'):
    root_window = manager.window

    menubar = tk.Menu(root_window)
    root_window.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    def on_open_image():
        if open_image_file():
            load_user_image_to_plot(ax_adjusted)
            fig.canvas.draw_idle()

    def on_close_image():
        global_data['user_image'] = None
        global_data['user_image_display'] = None
        global_data['is_manual_mode'] = False

        for rect in global_data['color_boxes']:
            rect.remove()
        global_data['color_boxes'] = []
        global_data['box_positions'] = []
        global_data['selected_box_idx'] = None

        if global_data['img_display'] is not None:
            global_data['img_display'].remove()

        global_data['img_display'] = ax_adjusted.imshow(img_rgb_original)
        ax_adjusted.set_title("Adjusted Color Chart (CCM)", fontsize=14, fontweight='bold')

        fig.canvas.draw_idle()

    file_menu.add_command(label="Open Image (JPEG/PNG/BMP)", command=on_open_image)
    file_menu.add_command(label="Close Image File", command=on_close_image)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root_window.quit)


# --- 初始 CCM 矩陣 & 滑桿控制 ---
initial_ccm = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
])

axcolor = 'lightgoldenrodyellow'
sliders = []
buttons_inc = []
buttons_dec = []
input_boxes = []
add_ccm_boxes = []

labels_ccm = ['R_r', 'R_g', 'R_b', 'G_r', 'G_g', 'G_b', 'B_r', 'B_g', 'B_b']

slider_ranges = [
    (0, 2.0),      # R_r
    (-1.0, 1.0),   # R_g
    (-1.0, 1.0),   # R_b
    (-1.0, 1.0),   # G_r
    (0, 2.0),      # G_g
    (-1.0, 1.0),   # G_b
    (-1.0, 1.0),   # B_r
    (-1.0, 1.0),   # B_g
    (0, 2.0),      # B_b
]

focused_input_idx = None


def update_ccm_sum_display():
    row_sums = [
        sliders[0].val + sliders[1].val + sliders[2].val,
        sliders[3].val + sliders[4].val + sliders[5].val,
        sliders[6].val + sliders[7].val + sliders[8].val,
    ]
    for row_idx, total in enumerate(row_sums):
        if row_idx < len(add_ccm_boxes):
            add_ccm_boxes[row_idx].set_text(f'Add: {total:.2f}')


for i in range(3):
    for j in range(3):
        idx = i * 3 + j

        sax = plt.axes([0.15 + j * 0.27, 0.32 - i * 0.10, 0.20, 0.03], facecolor=axcolor)
        slider_range = slider_ranges[idx]
        slider = Slider(sax, labels_ccm[idx], slider_range[0], slider_range[1],
                        valinit=initial_ccm[i, j], valstep=0.01)
        sliders.append(slider)

        # 減少按鍵
        dec_ax = plt.axes([0.15 + j * 0.27, 0.27 - i * 0.10, 0.04, 0.03])
        btn_dec = Button(dec_ax, '-', color='lightcoral', hovercolor='red')
        buttons_dec.append(btn_dec)

        # 輸入框
        input_ax = plt.axes([0.22 + j * 0.27, 0.27 - i * 0.10, 0.08, 0.03])
        input_ax.axis('off')
        input_box = plt.text(0.5, 0.5, f'{initial_ccm[i, j]:.2f}',
                            ha='center', va='center', fontsize=10,
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                                      edgecolor='gray', linewidth=1),
                            transform=input_ax.transAxes,
                            picker=True)
        input_boxes.append({'text': input_box, 'ax': input_ax, 'idx': idx})

        # 增加按鍵
        inc_ax = plt.axes([0.31 + j * 0.27, 0.27 - i * 0.10, 0.04, 0.03])
        btn_inc = Button(inc_ax, '+', color='lightgreen', hovercolor='green')
        buttons_inc.append(btn_inc)

    # 每行加總顯示
    add_ccm_ax = plt.axes([0.87, 0.32 - (i / 10), 0.25, 0.04])
    add_ccm_ax.axis('off')
    add_ccm_box = plt.text(0.3, 0.3, 'Add: 1.00',
                      ha='center', va='center', fontsize=10, fontweight='bold',
                      bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral',
                                edgecolor='blue', linewidth=2),
                      transform=add_ccm_ax.transAxes)
    add_ccm_boxes.append(add_ccm_box)


# --- ΔE, ΔC, SAT 統計顯示 ---
avg_deltaE_ax = plt.axes([0.15, 0.40, 0.25, 0.04])
avg_deltaE_ax.axis('off')
avg_deltaE_box = plt.text(0.5, 0.5, 'Avg ΔE: 0.00',
                          ha='center', va='center', fontsize=12, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue',
                                    edgecolor='blue', linewidth=2),
                          transform=avg_deltaE_ax.transAxes)

max_deltaE_ax = plt.axes([0.30, 0.40, 0.25, 0.04])
max_deltaE_ax.axis('off')
max_deltaE_box = plt.text(0.5, 0.5, 'Max ΔE: 0.00',
                          ha='center', va='center', fontsize=12, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral',
                                    edgecolor='red', linewidth=2),
                          transform=max_deltaE_ax.transAxes)

avg_deltaC_ax = plt.axes([0.45, 0.40, 0.25, 0.04])
avg_deltaC_ax.axis('off')
avg_deltaC_box = plt.text(0.5, 0.5, 'Avg ΔC: 0.00',
                          ha='center', va='center', fontsize=12, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue',
                                    edgecolor='blue', linewidth=2),
                          transform=avg_deltaC_ax.transAxes)

max_deltaC_ax = plt.axes([0.60, 0.40, 0.25, 0.04])
max_deltaC_ax.axis('off')
max_deltaC_box = plt.text(0.5, 0.5, 'Max ΔC: 0.00',
                          ha='center', va='center', fontsize=12, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral',
                                    edgecolor='red', linewidth=2),
                          transform=max_deltaC_ax.transAxes)

avg_saturation_ax = plt.axes([0.75, 0.40, 0.25, 0.04])
avg_saturation_ax.axis('off')
avg_saturation_box = plt.text(0.5, 0.5, 'Avg SAT: 0.00',
                          ha='center', va='center', fontsize=12, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral',
                                    edgecolor='red', linewidth=2),
                          transform=avg_saturation_ax.transAxes)


# --- 按鍵回調 ---
def create_button_callbacks():
    def make_increment_callback(idx):
        def on_inc_clicked(event):
            slider_range = slider_ranges[idx]
            current_val = sliders[idx].val
            new_val = min(current_val + 0.05, slider_range[1])
            sliders[idx].set_val(new_val)
            update_ccm_sum_display()
        return on_inc_clicked

    def make_decrement_callback(idx):
        def on_dec_clicked(event):
            slider_range = slider_ranges[idx]
            current_val = sliders[idx].val
            new_val = max(current_val - 0.05, slider_range[0])
            sliders[idx].set_val(new_val)
            update_ccm_sum_display()
        return on_dec_clicked

    for idx, btn_inc in enumerate(buttons_inc):
        btn_inc.on_clicked(make_increment_callback(idx))

    for idx, btn_dec in enumerate(buttons_dec):
        btn_dec.on_clicked(make_decrement_callback(idx))


create_button_callbacks()
update_ccm_sum_display()


# ==========================================
# 方框交互功能 (手動模式)
# ==========================================
box_drag_data = {'start_x': None, 'start_y': None}


def on_box_pick_event(event):
    if not global_data['is_manual_mode']:
        return
    for i, rect in enumerate(global_data['color_boxes']):
        if event.artist == rect:
            _select_box(i)
            return


def _select_box(idx):
    if idx < 0 or idx >= len(global_data['color_boxes']):
        return
    if global_data['selected_box_idx'] is not None:
        prev = global_data['selected_box_idx']
        if prev < len(global_data['color_boxes']):
            global_data['color_boxes'][prev].set_edgecolor('cyan')
            global_data['color_boxes'][prev].set_linewidth(2)
    global_data['selected_box_idx'] = idx
    global_data['color_boxes'][idx].set_edgecolor('red')
    global_data['color_boxes'][idx].set_linewidth(3)
    fig.canvas.draw_idle()


def on_mouse_press(event):
    if not global_data['is_manual_mode']:
        return
    if event.inaxes != global_data['ax_adjusted']:
        return
    if event.xdata is None or event.ydata is None:
        return

    box_drag_data['start_x'] = event.xdata
    box_drag_data['start_y'] = event.ydata

    for i, rect in enumerate(global_data['color_boxes']):
        x, y = rect.get_xy()
        w = rect.get_width()
        h = rect.get_height()
        if x <= event.xdata <= x + w and y <= event.ydata <= y + h:
            if global_data['selected_box_idx'] != i:
                _select_box(i)
            return


def on_mouse_release(event):
    if not global_data['is_manual_mode']:
        return
    box_drag_data['start_x'] = None
    box_drag_data['start_y'] = None


def on_mouse_motion(event):
    if not global_data['is_manual_mode']:
        return
    if event.inaxes != global_data['ax_adjusted']:
        return
    if box_drag_data['start_x'] is None:
        return

    if global_data['selected_box_idx'] is not None:
        box_idx = global_data['selected_box_idx']
        dx = event.xdata - box_drag_data['start_x']
        dy = event.ydata - box_drag_data['start_y']

        if event.key == 'shift':
            new_w = max(10, global_data['color_boxes'][box_idx].get_width() + dx)
            new_h = max(10, global_data['color_boxes'][box_idx].get_height() + dy)
            global_data['color_boxes'][box_idx].set_width(new_w)
            global_data['color_boxes'][box_idx].set_height(new_h)
            global_data['box_positions'][box_idx]['width'] = new_w
            global_data['box_positions'][box_idx]['height'] = new_h
        else:
            new_x = global_data['color_boxes'][box_idx].get_xy()[0] + dx
            new_y = global_data['color_boxes'][box_idx].get_xy()[1] + dy
            global_data['color_boxes'][box_idx].set_xy((new_x, new_y))
            global_data['box_positions'][box_idx]['x'] = new_x
            global_data['box_positions'][box_idx]['y'] = new_y

        box_drag_data['start_x'] = event.xdata
        box_drag_data['start_y'] = event.ydata

        update_manual_mode_display()
        fig.canvas.draw_idle()


def update_manual_mode_display():
    if not global_data['is_manual_mode'] or global_data['user_image'] is None:
        return

    global_data['lab_values'] = []
    global_data['colors_rgb_original'] = []

    user_image = global_data['user_image']

    for box_pos in global_data['box_positions']:
        x = int(box_pos['x'])
        y = int(box_pos['y'])
        w = int(box_pos['width'])
        h = int(box_pos['height'])

        x = max(0, min(x, user_image.shape[1] - 1))
        y = max(0, min(y, user_image.shape[0] - 1))
        w = min(w, user_image.shape[1] - x)
        h = min(h, user_image.shape[0] - y)

        roi = user_image[y:y+h, x:x+w]
        if roi.size == 0:
            avg_color = (128, 128, 128)
        else:
            avg_color = tuple(roi.reshape(-1, 3).mean(axis=0).astype(int))

        global_data['colors_rgb_original'].append(avg_color)
        lab = rgb_to_lab(avg_color)
        global_data['lab_values'].append(lab)

    update_text_display()


# ==========================================
# CCM 輸入框編輯
# ==========================================
input_editing_data = {'idx': None, 'text': ''}


def on_pick_event(event):
    global focused_input_idx
    for i, input_box_info in enumerate(input_boxes):
        if event.artist == input_box_info['text']:
            focused_input_idx = i
            input_editing_data['idx'] = input_box_info['idx']
            input_editing_data['text'] = str(sliders[input_box_info['idx']].val)
            input_box_info['text'].set_bbox(dict(boxstyle='round,pad=0.3', facecolor='lightcyan',
                                                  edgecolor='blue', linewidth=2))
            fig.canvas.draw_idle()
            break


def on_key_event(event):
    if input_editing_data['idx'] is None:
        return
    idx = input_editing_data['idx']
    text = input_editing_data['text']
    slider_range = slider_ranges[idx]

    if event.key == 'backspace':
        input_editing_data['text'] = text[:-1] if text else ''
    elif event.key == 'escape':
        input_editing_data['idx'] = None
        for input_box_info in input_boxes:
            if input_box_info['idx'] == idx:
                input_box_info['text'].set_bbox(dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                                                      edgecolor='gray', linewidth=1))
        fig.canvas.draw_idle()
        return
    elif event.key == 'enter':
        try:
            new_val = float(input_editing_data['text'])
            new_val = max(slider_range[0], min(new_val, slider_range[1]))
            sliders[idx].set_val(new_val)
        except ValueError:
            pass
        input_editing_data['idx'] = None
        for input_box_info in input_boxes:
            if input_box_info['idx'] == idx:
                input_box_info['text'].set_bbox(dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                                                      edgecolor='gray', linewidth=1))
        fig.canvas.draw_idle()
        return
    elif event.character and (event.character.isdigit() or event.character in '.-+'):
        input_editing_data['text'] += event.character

    for input_box_info in input_boxes:
        if input_box_info['idx'] == idx:
            input_box_info['text'].set_text(input_editing_data['text'])
            break
    fig.canvas.draw_idle()


# ==========================================
# 色塊編號輸入框
# ==========================================
color_block_label_ax = plt.axes([0.15, 0.025, 0.15, 0.04])
color_block_label_ax.axis('off')
plt.text(0.5, 0.5, 'Color Block (1-24):',
         ha='center', va='center', fontsize=11, fontweight='bold',
         transform=color_block_label_ax.transAxes)

color_block_input_ax = plt.axes([0.30, 0.025, 0.08, 0.04])
color_block_input_ax.axis('off')
global_data['color_block_input_text'] = plt.text(0.5, 0.5, '1',
                                                  ha='center', va='center', fontsize=11,
                                                  bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                                                            edgecolor='gray', linewidth=1),
                                                  transform=color_block_input_ax.transAxes,
                                                  picker=True)


def on_select_color_block(event=None):
    try:
        block_num = int(global_data['color_block_input_text'].get_text())
        if not (1 <= block_num <= 24):
            messagebox.showwarning("警告", "請輸入1-24之間的數字")
            return

        for rect in global_data['color_boxes']:
            rect.set_edgecolor('cyan')
            rect.set_linewidth(2)

        if global_data['is_manual_mode'] and len(global_data['color_boxes']) > 0:
            idx = min(block_num - 1, len(global_data['color_boxes']) - 1)
            if idx < len(global_data['color_boxes']):
                global_data['color_boxes'][idx].set_edgecolor('red')
                global_data['color_boxes'][idx].set_linewidth(3)
                global_data['selected_box_idx'] = idx

        fig.canvas.draw_idle()
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的數字")


select_block_ax = plt.axes([0.39, 0.025, 0.08, 0.04])
select_block_btn = Button(select_block_ax, 'Select', color=axcolor, hovercolor='0.975')
select_block_btn.on_clicked(on_select_color_block)

color_block_editing = {'active': False, 'text': '1'}


def on_color_block_pick(event):
    try:
        if hasattr(event, 'artist') and event.artist == global_data['color_block_input_text']:
            color_block_editing['active'] = True
            color_block_editing['text'] = global_data['color_block_input_text'].get_text()
            global_data['color_block_input_text'].set_bbox(dict(boxstyle='round,pad=0.4', facecolor='lightcyan',
                                                                  edgecolor='blue', linewidth=2))
            fig.canvas.draw_idle()
    except Exception:
        pass


def on_color_block_key(event):
    if not color_block_editing['active']:
        return

    text = color_block_editing['text']

    if event.key == 'backspace':
        color_block_editing['text'] = text[:-1] if text else ''
    elif event.key == 'escape':
        color_block_editing['active'] = False
        color_block_editing['text'] = '1'
        global_data['color_block_input_text'].set_text('1')
        global_data['color_block_input_text'].set_bbox(dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                                                              edgecolor='gray', linewidth=1))
        fig.canvas.draw_idle()
        return
    elif event.key == 'enter':
        color_block_editing['active'] = False
        try:
            block_num = int(color_block_editing['text'])
            if 1 <= block_num <= 24:
                on_select_color_block(None)
            else:
                messagebox.showwarning("警告", "請輸入1-24之間的數字")
                color_block_editing['text'] = '1'
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")
            color_block_editing['text'] = '1'

        global_data['color_block_input_text'].set_text(color_block_editing['text'])
        global_data['color_block_input_text'].set_bbox(dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                                                              edgecolor='gray', linewidth=1))
        fig.canvas.draw_idle()
        return
    elif event.character:
        if event.character.isdigit():
            current_text = color_block_editing['text']
            if current_text == '1' and len(current_text) == 1:
                if event.character == '0':
                    color_block_editing['text'] = '1'
                else:
                    color_block_editing['text'] = event.character
            elif len(current_text) < 2:
                new_num_str = current_text + event.character
                new_num = int(new_num_str)
                if new_num > 24:
                    color_block_editing['text'] = event.character
                else:
                    color_block_editing['text'] = new_num_str

    global_data['color_block_input_text'].set_text(color_block_editing['text'])
    fig.canvas.draw_idle()


# --- 統一的 pick / key 事件處理 ---
fig.canvas.mpl_connect('pick_event', lambda e: (on_color_block_pick(e), on_pick_event(e), on_box_pick_event(e)))
fig.canvas.mpl_connect('button_press_event', on_mouse_press)
fig.canvas.mpl_connect('button_release_event', on_mouse_release)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_motion)

fig.canvas.mpl_connect('key_press_event', lambda e: (on_color_block_key(e), on_key_event(e)))


# ==========================================
# 滑桿更新
# ==========================================
def update(val):
    global global_data

    new_ccm = np.array([
        [sliders[0].val, sliders[1].val, sliders[2].val],
        [sliders[3].val, sliders[4].val, sliders[5].val],
        [sliders[6].val, sliders[7].val, sliders[8].val]
    ])

    global_data['current_ccm'] = new_ccm.copy()

    for input_box_info in input_boxes:
        idx = input_box_info['idx']
        input_box_info['text'].set_text(f'{sliders[idx].val:.2f}')

    if global_data['is_manual_mode'] and global_data['user_image'] is not None:
        corrected_img = apply_ccm(global_data['user_image'], new_ccm)
        global_data['user_image_display'].set_data(corrected_img)
    else:
        corrected_img = apply_ccm(img_rgb_original, new_ccm)
        img_display.set_data(corrected_img)

    if global_data['colors_rgb_original']:
        global_data['lab_values'] = []
        ccm_matrix = new_ccm.astype(np.float32)

        deltaE_values = []
        for idx, color_rgb in enumerate(global_data['colors_rgb_original']):
            color_float = np.array(color_rgb, dtype=np.float32).reshape(1, 1, 3)
            corrected_color = cv2.transform(color_float, ccm_matrix)
            corrected_color_clipped = np.clip(corrected_color[0, 0], 0, 255).astype(np.uint8)
            lab = rgb_to_lab(tuple(corrected_color_clipped))
            global_data['lab_values'].append(lab)
            lab_org = COLORS_LAB_REF[idx]
            deltaE = math.sqrt(((lab_org[0] - lab[0])**2) + ((lab_org[1] - lab[1])**2) + ((lab_org[2] - lab[2])**2))
            deltaE_values.append(deltaE)

        deltaC_values = []
        for idx, color_rgb in enumerate(global_data['colors_rgb_original']):
            color_float = np.array(color_rgb, dtype=np.float32).reshape(1, 1, 3)
            corrected_color = cv2.transform(color_float, ccm_matrix)
            corrected_color_clipped = np.clip(corrected_color[0, 0], 0, 255).astype(np.uint8)
            lab = rgb_to_lab(tuple(corrected_color_clipped))
            lab_org = COLORS_LAB_REF[idx]
            deltaC = math.sqrt(((lab_org[1] - lab[1])**2) + ((lab_org[2] - lab[2])**2))
            deltaC_values.append(deltaC)

        avg_deltaE = np.mean(deltaE_values)
        max_deltaE = np.max(deltaE_values)
        avg_deltaC = np.mean(deltaC_values)
        max_deltaC = np.max(deltaC_values)

        saturation_values = []
        for idx, color_rgb in enumerate(global_data['colors_rgb_original']):
            color_float = np.array(color_rgb, dtype=np.float32).reshape(1, 1, 3)
            corrected_color = cv2.transform(color_float, ccm_matrix)
            corrected_color_clipped = np.clip(corrected_color[0, 0], 0, 255).astype(np.uint8)
            r_norm = corrected_color_clipped[0] / 255.0
            g_norm = corrected_color_clipped[1] / 255.0
            b_norm = corrected_color_clipped[2] / 255.0
            rgb_max = max(r_norm, g_norm, b_norm)
            rgb_min = min(r_norm, g_norm, b_norm)
            rgb_delta = rgb_max - rgb_min
            if rgb_max == 0:
                sat_value = 0
            else:
                sat_value = (rgb_delta / rgb_max) * 255
            saturation_values.append(sat_value)

        avg_saturation = np.mean(saturation_values)

        avg_deltaE_box.set_text(f'Avg ΔE: {avg_deltaE:.2f}')
        max_deltaE_box.set_text(f'Max ΔE: {max_deltaE:.2f}')
        avg_deltaC_box.set_text(f'Avg ΔC: {avg_deltaC:.2f}')
        max_deltaC_box.set_text(f'Max ΔC: {max_deltaC:.2f}')
        avg_saturation_box.set_text(f'Avg SAT: {avg_saturation:.2f}')

        update_text_display()

    update_ccm_sum_display()
    fig.canvas.draw_idle()


for slider in sliders:
    slider.on_changed(update)


# --- 重置按鈕 ---
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset Identity', color=axcolor, hovercolor='0.975')


def reset(event):
    idx = 0
    for i in range(3):
        for j in range(3):
            sliders[idx].set_val(initial_ccm[i, j])
            idx += 1


button.on_clicked(reset)

plt.show()

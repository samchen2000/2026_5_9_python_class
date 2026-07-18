import sys
from datetime import datetime

import yfinance as yf
import pandas as pd
import numpy as np

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QGroupBox,
    QTextEdit,
    QSplitter,
    QListWidget,
    QLineEdit,
    QAbstractItemView,
    QFrame,
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, QThread, Signal

import pyqtgraph as pg
from pyqtgraph import ImageView


# ============ 台股資料庫 ============

TW_STOCK_DB = {
    "2330.TW": "台積電",
    "2303.TW": "聯電",
    "2454.TW": "聯發科",
    "2317.TW": "鴻海",
    "2412.TW": "中華電",
    "2881.TW": "富邦金",
    "2882.TW": "國泰金",
    "2308.TW": "台達電",
    "2884.TW": "玉山金",
    "2886.TW": "兆豐金",
    "2891.TW": "中信金",
    "2880.TW": "華南金",
    "2885.TW": "元大金",
    "2892.TW": "第一金",
    "2357.TW": "華碩",
    "2382.TW": "廣達",
    "2395.TW": "研華",
    "3034.TW": "聯詠",
    "2379.TW": "瑞昱",
    "3008.TW": "大立光",
    "2409.TW": "友達",
    "2002.TW": "中鋼",
    "1301.TW": "台塑",
    "1303.TW": "南亞",
    "1326.TW": "台化",
    "1216.TW": "統一",
    "2912.TW": "統一超",
    "3045.TW": "台灣大",
    "4904.TW": "遠傳",
    "2345.TW": "智邦",
    "3231.TW": "緯創",
    "2327.TW": "國巨",
    "2376.TW": "技嘉",
    "2383.TW": "台光電",
    "3711.TW": "日月光投控",
    "2408.TW": "南亞科",
    "2344.TW": "華邦電",
    "6505.TW": "台塑化",
    "3037.TW": "欣興",
    "2301.TW": "光寶科",
    "2324.TW": "仁寶",
    "2377.TW": "微星",
    "5871.TW": "中租-KY",
    "5880.TW": "合庫金",
    "2834.TW": "臺企銀",
    "2890.TW": "永豐金",
    "3023.TW": "信邦",
    "2356.TW": "英業達",
    "2399.TW": "環泰",
    "3443.TW": "創意",
    "2402.TW": "鋰泰",
    "8046.TW": "網石",
    "3653.TW": "健策",
    "2328.TW": "廣宇",
    "3661.TW": "世芯-KY",
    "6669.TW": "緯穎",
    "2373.TW": "世界",
    "3017.TW": "旭隼",
    "6415.TW": "矽力-KY",
    "2306.TW": "藍天",
    "3529.TW": "力旺",
    "2347.TW": "精英",
    "6488.TW": "環球晶",
    "2459.TW": "旺宏",
    "3532.TW": "幸康",
    "5347.TW": "世界",
    "3293.TW": "鉅祥",
    "2301.TW": "光寶科",
    "2474.TW": "可成",
    "3035.TW": "智原",
    "6150.TW": "撼訊",
    "3530.TW": "頻微",
    "6239.TW": "三商電",
    "3039.TW": "宇瞻",
    "4953.TW": "緯軟",
    "2388.TW": "威盛",
    "3022.TW": "威剛",
    "3669.TW": "圓展",
    "2380.TW": "虹光",
    "2401.TW": "凌陽",
    "3576.TW": "聯合再生",
    "8150.TW": "南茂",
    "3481.TW": "群豐",
    "6285.TW": "啟碁",
    "2307.TW": "雙鴻",
    "3016.TW": "嘉晶",
    "1590.TW": "亞德客",
    "2049.TW": "上銀",
    "6531.TW": "愛普生",
    "3652.TW": "精材",
    "2352.TW": "鴻準",
    "3217.TW": "優群",
    "6176.TW": "瑞儀",
    "1503.TW": "士電",
    "3518.TW": "新唐",
    "6182.TW": "合晶",
    "6416.TW": "立積",
    "3014.TW": "聯陽",
    "6770.TW": "力積電",
    "2603.TW": "長榮",
    "2609.TW": "陽明",
    "2615.TW": "萬海",
    "2618.TW": "長榮航",
    "2610.TW": "華航",
    "2611.TW": "張貿",
    "2617.TW": "台航",
    "2613.TW": "中櫃",
    "2612.TW": "中遠",
    "2605.TW": "新興",
    "2614.TW": "東森",
    "00878.TW": "國泰永續高股息",
    "0050.TW": "元大台灣50",
    "0056.TW": "元大高股息",
    "00881.TW": "國泰台灣5G+",
    "00692.TW": "富邦公司治理",
    "006208.TW": "富邦台50",
    "00929.TW": "復華台灣科技優息",
    "00891.TW": "中信關鍵半導體",
    "00904.TW": "新光台灣投資級債",
    "00713.TW": "元大台灣高息低波",
    "00757.TW": "統一FANG+",
    "00928.TW": "兆豐台灣電子工業",
    "00919.TW": "群益台灣精選高息",
    "00905.TW": "FT台灣Smart",
    "00903.TW": "富邦特選台灣高股息30",
    "00850.TW": "元大ESG永續",
    "00772.TW": "中信中國50",
    "00670L.TW": "富邦NASDAQ反1",
    "00631L.TW": "元大台灣50正2",
    "00632R.TW": "元大台灣50反1",
    "00751L.TW": "元大NASDAQ正2",
    "00677L.TW": "國泰加權正2",
    "00664R.TW": "國泰加權反1",
}


def search_stock(query: str) -> list:
    """搜尋股票，回傳 [(name, ticker), ...]"""
    query = query.strip().upper()
    results = []
    for ticker, name in TW_STOCK_DB.items():
        if query in ticker.upper() or query in name.upper():
            results.append((name, ticker))
    return results[:20]


# ============ 背景資料抓取與計算 ============


class StockDataWorker(QThread):
    finished = Signal(object, object, object, str, list)
    error = Signal(str)

    def __init__(self, stock_list):
        super().__init__()
        self.stock_list = stock_list

    def run(self):
        if len(self.stock_list) < 2:
            self.error.emit("至少需要選擇兩檔股票才能計算相關係數。")
            return

        try:
            tickers = [t for _, t in self.stock_list]
            names = [n for n, _ in self.stock_list]

            data = yf.download(
                tickers,
                start="2006-01-01",
                interval="1d",
                auto_adjust=True,
            )

            close = data["Close"]
            code_to_name = {t: n for n, t in self.stock_list}
            close = close.rename(columns=code_to_name)

            returns = close.pct_change().dropna()
            corr = returns.corr()

            now_str = datetime.today().strftime("%Y-%m-%d")
            report = f"資料更新時間：{now_str}\n"
            report += f"分析期間：2006-01-01 至今\n"
            report += f"股票數：{len(self.stock_list)}\n\n"
            report += "收盤價最後 5 筆：\n"
            report += close.tail().to_string()
            report += "\n\n日報酬率相關係數：\n"
            report += corr.round(3).to_string()

            self.finished.emit(close, returns, corr, report, names)

        except Exception as e:
            self.error.emit(str(e))


# ============ 熱力圖自訂 ImageView ============


class HeatmapView(pg.GraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = pg.ImageView(self)
        self.layout().addWidget(self.ui)
        self.vb = self.ui.view
        self.img = None

    def set_data(self, data, labels):
        self.ui.clear()
        self.ui.setImage(data.astype(np.float32))

        self.vb.getAxis("bottom").setTicks(
            [(i, n) for i, n in enumerate(labels)]
        )
        self.vb.getAxis("left").setTicks(
            [(i, n) for i, n in enumerate(labels)]
        )
        self.vb.setLabel("bottom", "")
        self.vb.setLabel("left", "")
        self.vb.setTitle("")


# ============ 主視窗 ============


class StockCorrelationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("台股相關係數視覺化")
        self.resize(1280, 800)

        self.close_df = None
        self.returns_df = None
        self.corr_df = None

        self.stock_list = [
            ("台積電", "2330.TW"),
            ("聯電", "2303.TW"),
            ("聯發科", "2454.TW"),
            ("鴻海", "2317.TW"),
        ]

        self.search_results = []
        self.init_ui()
        self.worker = None
        self.refresh_stock_list_widget()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # ===== 標題 =====
        title = QLabel("台股相關係數分析")
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold; padding: 8px; "
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #1a237e, stop:1 #4a148c); "
            "color: white; border-radius: 6px;"
        )
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # ===== 上半部：股票清單 + 搜尋 =====
        top_splitter = QSplitter(Qt.Horizontal)

        # -- 左側：已選股票 --
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame{border:1px solid #ccc; border-radius:8px;}")
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        list_group = QGroupBox("已選股票")
        list_layout = QVBoxLayout()
        self.stock_list_widget = QListWidget()
        self.stock_list_widget.setStyleSheet(
            "QListWidget{font-size:13px; padding:4px;}"
            "QListWidget::item{padding:6px; border-bottom:1px solid #eee;}"
            "QListWidget::item:selected{background:#bbdefb; color:black;}"
        )
        self.stock_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        list_layout.addWidget(self.stock_list_widget)

        btn_row = QHBoxLayout()
        self.remove_btn = QPushButton("移除選取")
        self.remove_btn.setStyleSheet(
            "QPushButton{background:#ef5350; color:white; padding:6px 12px; border-radius:4px;}"
            "QPushButton:hover{background:#c62828;}"
        )
        self.remove_btn.clicked.connect(self.remove_stock)
        self.clear_btn = QPushButton("全部清除")
        self.clear_btn.setStyleSheet(
            "QPushButton{background:#757575; color:white; padding:6px 12px; border-radius:4px;}"
            "QPushButton:hover{background:#424242;}"
        )
        self.clear_btn.clicked.connect(self.clear_stocks)
        btn_row.addWidget(self.remove_btn)
        btn_row.addWidget(self.clear_btn)
        list_layout.addLayout(btn_row)

        list_group.setLayout(list_layout)
        left_layout.addWidget(list_group)

        count_label = QLabel()
        count_label.setObjectName("countLabel")
        left_layout.addWidget(count_label)

        top_splitter.addWidget(left_panel)

        # -- 中間：搜尋新增股票 --
        mid_panel = QFrame()
        mid_panel.setStyleSheet("QFrame{border:1px solid #ccc; border-radius:8px;}")
        mid_layout = QVBoxLayout()
        mid_panel.setLayout(mid_layout)

        search_group = QGroupBox("搜尋並新增股票")
        search_layout = QVBoxLayout()

        # 搜尋框
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("輸入代號或名稱："))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("例如：2330、台積電、台")
        self.search_edit.setStyleSheet(
            "QLineEdit{padding:8px; font-size:13px; border:2px solid #1a237e; border-radius:4px;}"
        )
        self.search_edit.textChanged.connect(self.on_search_changed)
        h1.addWidget(self.search_edit)
        search_layout.addLayout(h1)

        # 搜尋結果列表
        self.search_list = QListWidget()
        self.search_list.setStyleSheet(
            "QListWidget{font-size:13px; border:1px solid #bbb; border-radius:4px;}"
            "QListWidget::item{padding:6px;}"
            "QListWidget::item:hover{background:#e3f2fd;}"
            "QListWidget::item:selected{background:#1a237e; color:white;}"
        )
        self.search_list.setMaximumHeight(220)
        self.search_list.itemDoubleClicked.connect(self.on_search_selected)
        search_layout.addWidget(QLabel("搜尋結果（雙擊加入清單）："))
        search_layout.addWidget(self.search_list)

        # 快捷按鈕
        quick_row = QHBoxLayout()
        quick_label = QLabel("快速加入：")
        quick_row.addWidget(quick_label)
        quick_stocks = [
            ("台積電", "2330.TW"),
            ("鴻海", "2317.TW"),
            ("聯發科", "2454.TW"),
            ("台達電", "2308.TW"),
            ("中華電", "2412.TW"),
            ("富邦金", "2881.TW"),
            ("國泰金", "2882.TW"),
            ("0050", "0050.TW"),
        ]
        for name, ticker in quick_stocks:
            btn = QPushButton(f"{name}")
            btn.setToolTip(ticker)
            btn.setStyleSheet(
                "QPushButton{background:#1a237e; color:white; padding:4px 8px; border-radius:3px; font-size:11px;}"
                "QPushButton:hover{background:#283593;}"
            )
            btn.clicked.connect(
                lambda checked=False, n=name, t=ticker: self.quick_add(n, t)
            )
            quick_row.addWidget(btn)
        quick_row.addStretch()
        search_layout.addLayout(quick_row)

        search_group.setLayout(search_layout)
        mid_layout.addWidget(search_group)

        top_splitter.addWidget(mid_panel)

        # -- 右側：功能按鈕 --
        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame{border:1px solid #ccc; border-radius:8px;}")
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        self.load_btn = QPushButton("載入資料\n並計算相關係數")
        self.load_btn.setStyleSheet(
            "QPushButton{background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #1a237e,stop:1 #4a148c);"
            "color:white; font-size:15px; font-weight:bold; padding:20px 16px; border-radius:8px;}"
            "QPushButton:hover{background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #283593,stop:1 #6a1b9a);}"
            "QPushButton:disabled{background:#9e9e9e;}"
        )
        self.load_btn.clicked.connect(self.start_load_data)
        right_layout.addWidget(self.load_btn)

        right_layout.addStretch()

        top_splitter.addWidget(right_panel)
        top_splitter.setStretchFactor(0, 2)
        top_splitter.setStretchFactor(1, 3)
        top_splitter.setStretchFactor(2, 1)

        main_layout.addWidget(top_splitter)

        # ===== 下半部：報告 + 表格 + 熱力圖 =====
        bot_splitter = QSplitter(Qt.Horizontal)

        # 左側：報告
        left_bot = QFrame()
        left_bot.setStyleSheet("QFrame{border:1px solid #ccc; border-radius:8px;}")
        lb_layout = QVBoxLayout()
        left_bot.setLayout(lb_layout)

        report_group = QGroupBox("文字報告")
        rl = QVBoxLayout()
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setStyleSheet("QTextEdit{font-size:12px; padding:6px;}")
        rl.addWidget(self.report_text)
        report_group.setLayout(rl)
        lb_layout.addWidget(report_group)

        bot_splitter.addWidget(left_bot)

        # 中間：表格
        mid_bot = QFrame()
        mid_bot.setStyleSheet("QFrame{border:1px solid #ccc; border-radius:8px;}")
        mb_layout = QVBoxLayout()
        mid_bot.setLayout(mb_layout)

        table_group = QGroupBox("相關係數表格")
        tl = QVBoxLayout()
        self.corr_table = QTableWidget()
        self.corr_table.setStyleSheet(
            "QTableWidget{font-size:12px;}"
            "QHeaderView::section{background:#1a237e; color:white; padding:6px; border:1px solid #1a237e;}"
        )
        tl.addWidget(self.corr_table)
        table_group.setLayout(tl)
        mb_layout.addWidget(table_group)

        bot_splitter.addWidget(mid_bot)

        # 右側：熱力圖
        right_bot = QFrame()
        right_bot.setStyleSheet("QFrame{border:1px solid #ccc; border-radius:8px;}")
        rb_layout = QVBoxLayout()
        right_bot.setLayout(rb_layout)

        chart_group = QGroupBox("相關係數熱力圖")
        cl = QVBoxLayout()
        self.corr_heatmap = ImageView()
        self.corr_heatmap.setStyleSheet("border-radius:4px;")
        cl.addWidget(self.corr_heatmap)
        chart_group.setLayout(cl)
        rb_layout.addWidget(chart_group)

        bot_splitter.addWidget(right_bot)

        bot_splitter.setStretchFactor(0, 1)
        bot_splitter.setStretchFactor(1, 1)
        bot_splitter.setStretchFactor(2, 1)

        main_layout.addWidget(bot_splitter)

        self.update_count_label()

    # ===== 搜尋功能 =====

    def on_search_changed(self, text: str):
        self.search_list.clear()
        if len(text.strip()) < 1:
            return
        results = search_stock(text)
        self.search_results = results
        for name, ticker in results:
            in_list = any(t == ticker for _, t in self.stock_list)
            suffix = "  ✓已加入" if in_list else ""
            self.search_list.addItem(f"{name}  ({ticker}){suffix}")

    def on_search_selected(self, item):
        idx = self.search_list.row(item)
        if idx < len(self.search_results):
            name, ticker = self.search_results[idx]
            self.add_stock_direct(name, ticker)

    def quick_add(self, name: str, ticker: str):
        self.add_stock_direct(name, ticker)

    def add_stock_direct(self, name: str, ticker: str):
        for n, t in self.stock_list:
            if t.upper() == ticker.upper():
                QMessageBox.information(self, "提示", f"{name} ({ticker}) 已在清單中。")
                return
        self.stock_list.append((name, ticker))
        self.refresh_stock_list_widget()
        self.update_count_label()

    # ===== 清單管理 =====

    def refresh_stock_list_widget(self):
        self.stock_list_widget.clear()
        for name, ticker in self.stock_list:
            self.stock_list_widget.addItem(f"{name}  ({ticker})")

    def update_count_label(self):
        lbl = self.findChild(QLabel, "countLabel")
        if lbl:
            n = len(self.stock_list)
            lbl.setText(f"共 {n} 檔股票（至少需要 2 檔）")
            if n >= 2:
                lbl.setStyleSheet("color:#2e7d32; font-weight:bold; padding:4px;")
            else:
                lbl.setStyleSheet("color:#c62828; font-weight:bold; padding:4px;")

    def remove_stock(self):
        selected = self.stock_list_widget.selectedItems()
        if not selected:
            QMessageBox.information(self, "提示", "請先選取要刪除的股票。")
            return
        indexes = sorted(
            [self.stock_list_widget.row(i) for i in selected], reverse=True
        )
        for idx in indexes:
            self.stock_list.pop(idx)
        self.refresh_stock_list_widget()
        self.update_count_label()

    def clear_stocks(self):
        self.stock_list.clear()
        self.refresh_stock_list_widget()
        self.update_count_label()

    # ===== 載入資料 =====

    def start_load_data(self):
        if len(self.stock_list) < 2:
            QMessageBox.warning(self, "警告", "至少需要兩檔股票才能計算相關係數。")
            return

        self.load_btn.setEnabled(False)
        self.load_btn.setText("載入中...")
        self.report_text.clear()
        self.corr_table.setRowCount(0)
        self.corr_table.setColumnCount(0)
        self.corr_heatmap.clear()

        self.worker = StockDataWorker(self.stock_list.copy())
        self.worker.finished.connect(self.on_data_loaded)
        self.worker.error.connect(self.on_data_error)
        self.worker.start()

    def on_data_loaded(self, close_df, returns_df, corr_df, report_text, names):
        self.close_df = close_df
        self.returns_df = returns_df
        self.corr_df = corr_df

        self.report_text.setPlainText(report_text)
        self.fill_correlation_table(corr_df)
        self.draw_heatmap(corr_df, names)

        self.load_btn.setEnabled(True)
        self.load_btn.setText("載入資料\n並計算相關係數")

    def on_data_error(self, err_msg):
        QMessageBox.critical(self, "載入錯誤", f"無法載入股價資料：\n{err_msg}")
        self.load_btn.setEnabled(True)
        self.load_btn.setText("載入資料\n並計算相關係數")

    def fill_correlation_table(self, corr_df: pd.DataFrame):
        names = list(corr_df.columns)
        n = len(names)
        self.corr_table.setRowCount(n)
        self.corr_table.setColumnCount(n)
        self.corr_table.setHorizontalHeaderLabels(names)
        self.corr_table.setVerticalHeaderLabels(names)
        self.corr_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(n):
            for j in range(n):
                val = corr_df.iloc[i, j]
                item = QTableWidgetItem(f"{val:.3f}")
                item.setTextAlignment(Qt.AlignCenter)

                # 根據數值上色
                if i == j:
                    item.setBackground(QColor("#1a237e"))
                    item.setForeground(QColor("white"))
                else:
                    abs_val = abs(val)
                    if abs_val > 0.7:
                        color = QColor("#c62828") if val > 0 else QColor("#1565c0")
                    elif abs_val > 0.4:
                        color = QColor("#ef5350") if val > 0 else QColor("#42a5f5")
                    else:
                        color = QColor("#fff9c4") if val > 0 else QColor("#e3f2fd")
                    item.setBackground(color)
                    item.setForeground(QColor("black"))

                self.corr_table.setItem(i, j, item)

    def draw_heatmap(self, corr_df: pd.DataFrame, names):
        arr = corr_df.to_numpy()
        self.corr_heatmap.setImage(arr.astype(np.float32))
        self.corr_heatmap.view.getAxis("bottom").setTicks(
            [(i, n) for i, n in enumerate(names)]
        )
        self.corr_heatmap.view.getAxis("left").setTicks(
            [(i, n) for i, n in enumerate(names)]
        )
        self.corr_heatmap.view.setLabel("bottom", "")
        self.corr_heatmap.view.setLabel("left", "")
        self.corr_heatmap.view.setTitle("相關係數熱力圖")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font = QFont("Microsoft JhengHei", 10)
    app.setFont(font)

    app.setStyleSheet(
        """
        QMainWindow { background: #f5f5f5; }
        QGroupBox {
            font-weight: bold;
            font-size: 13px;
            border: 1px solid #ccc;
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 6px;
        }
        QPushButton {
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
        }
        """
    )

    win = StockCorrelationWindow()
    win.show()
    sys.exit(app.exec())

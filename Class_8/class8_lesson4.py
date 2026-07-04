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
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal

import pyqtgraph as pg
from pyqtgraph import ImageView


# ============ 背景資料抓取與計算（放在 QThread 裡） ============

class StockDataWorker(QThread):
    finished = Signal(object, object, object, str, list)
    error = Signal(str)

    def __init__(self, stock_list):
        """
        stock_list: [(name, ticker), ...]
        """
        super().__init__()
        self.stock_list = stock_list

    def run(self):
        if len(self.stock_list) < 2:
            self.error.emit("至少需要選擇兩檔股票才能計算相關係數。")
            return

        try:
            tickers = [t for _, t in self.stock_list]
            names = [n for n, _ in self.stock_list]

            # 抓 2006 年至今的歷史資料
            data = yf.download(
                tickers,
                start="2006-01-01",
                interval="1d",
                auto_adjust=True,
            )

            # 只取收盤價
            close = data["Close"]

            # 把欄位名稱從股票代號改成中文公司名
            code_to_name = {t: n for n, t in self.stock_list}
            close = close.rename(columns=code_to_name)

            # 計算每日報酬率
            returns = close.pct_change().dropna()

            # 計算相關係數
            corr = returns.corr()

            # 產生簡短文字報告
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


# ============ 主視窗 ============

class StockCorrelationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("台股相關係數視覺化（PySide6）")
        self.resize(1200, 750)

        self.close_df = None
        self.returns_df = None
        self.corr_df = None

        # 預設股票清單：[(名稱, 代號), ...]
        self.stock_list = [
            ("台積電", "2330.TW"),
            ("聯電", "2303.TW"),
            ("聯發科", "2454.TW"),
            ("鴻海", "2317.TW"),
        ]

        self.init_ui()
        self.worker = None

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # 標題
        title_label = QLabel("台股大型股：收盤價與日報酬率相關係數")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # 上方：股票選擇區 + 按鈕區
        top_splitter = QSplitter(Qt.Horizontal)

        # 左側：股票清單與新增股票
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # 股票清單
        stock_list_group = QGroupBox("分析股票清單")
        stock_list_layout = QVBoxLayout()
        self.stock_list_widget = QListWidget()
        self.stock_list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        stock_list_layout.addWidget(self.stock_list_widget)
        stock_list_group.setLayout(stock_list_layout)

        # 新增股票
        add_stock_group = QGroupBox("新增股票")
        add_stock_layout = QVBoxLayout()

        add_layout1 = QHBoxLayout()
        add_layout1.addWidget(QLabel("名稱："))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("例如：台積電")
        add_layout1.addWidget(self.name_edit)

        add_layout2 = QHBoxLayout()
        add_layout2.addWidget(QLabel("代號："))
        self.ticker_edit = QLineEdit()
        self.ticker_edit.setPlaceholderText("例如：2330.TW")
        add_layout2.addWidget(self.ticker_edit)

        self.add_stock_btn = QPushButton("加入清單")
        self.add_stock_btn.clicked.connect(self.add_stock)

        self.remove_stock_btn = QPushButton("移除選取")
        self.remove_stock_btn.clicked.connect(self.remove_stock)

        add_stock_layout.addLayout(add_layout1)
        add_stock_layout.addLayout(add_layout2)
        add_stock_layout.addWidget(self.add_stock_btn)
        add_stock_layout.addWidget(self.remove_stock_btn)
        add_stock_group.setLayout(add_stock_layout)

        left_layout.addWidget(stock_list_group)
        left_layout.addWidget(add_stock_group)

        top_splitter.addWidget(left_panel)

        # 右側：功能按鈕
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        self.load_btn = QPushButton("載入股價資料並計算相關係數")
        self.load_btn.clicked.connect(self.start_load_data)

        right_layout.addWidget(self.load_btn)
        right_layout.addStretch()

        top_splitter.addWidget(right_panel)
        top_splitter.setStretchFactor(0, 1)
        top_splitter.setStretchFactor(1, 0)

        main_layout.addWidget(top_splitter)

        # 分割視窗：左邊表格 / 右邊圖表
        splitter = QSplitter(Qt.Horizontal)

        # 左側：文字報告 + 相關係數表格
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        # 文字報告
        report_group = QGroupBox("文字報告")
        report_layout = QVBoxLayout()
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        report_layout.addWidget(self.report_text)
        report_group.setLayout(report_layout)

        # 相關係數表格
        table_group = QGroupBox("相關係數表格")
        table_layout = QVBoxLayout()
        self.corr_table = QTableWidget()
        table_layout.addWidget(self.corr_table)
        table_group.setLayout(table_layout)

        left_layout.addWidget(report_group)
        left_layout.addWidget(table_group)

        splitter.addWidget(left_widget)

        # 右側：相關係數熱力圖（pyqtgraph）
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        chart_group = QGroupBox("相關係數熱力圖")
        chart_layout = QVBoxLayout()
        self.corr_view = ImageView()
        chart_layout.addWidget(self.corr_view)
        chart_group.setLayout(chart_layout)

        right_layout.addWidget(chart_group)

        splitter.addWidget(right_widget)

        # 左右比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # 初始化股票清單顯示
        self.refresh_stock_list_widget()

    def refresh_stock_list_widget(self):
        self.stock_list_widget.clear()
        for name, ticker in self.stock_list:
            self.stock_list_widget.addItem(f"{name} ({ticker})")

    def add_stock(self):
        name = self.name_edit.text().strip()
        ticker = self.ticker_edit.text().strip()

        if not name or not ticker:
            QMessageBox.warning(
                self,
                "警告",
                "請輸入股票名稱與代號（例如：台積電、2330.TW）"
            )
            return

        # 檢查是否已存在相同代號
        for n, t in self.stock_list:
            if t.upper() == ticker.upper():
                QMessageBox.warning(
                    self,
                    "警告",
                    f"代號 {ticker} 已存在於清單中（{n}）。"
                )
                return

        self.stock_list.append((name, ticker))
        self.refresh_stock_list_widget()

        self.name_edit.clear()
        self.ticker_edit.clear()
        self.name_edit.setFocus()

    def remove_stock(self):
        selected = self.stock_list_widget.selectedItems()
        if not selected:
            QMessageBox.information(
                self,
                "提示",
                "請先從清單中選取要刪除的股票。"
            )
            return

        # 由後往前刪，避免索引跑掉
        indexes = sorted(
            [self.stock_list_widget.row(i) for i in selected],
            reverse=True
        )
        for idx in indexes:
            self.stock_list.pop(idx)

        self.refresh_stock_list_widget()

    def start_load_data(self):
        if len(self.stock_list) < 2:
            QMessageBox.warning(
                self,
                "警告",
                "至少需要兩檔股票才能計算相關係數。"
            )
            return

        self.load_btn.setEnabled(False)
        self.report_text.clear()
        self.corr_table.setRowCount(0)
        self.corr_table.setColumnCount(0)
        self.corr_view.clear()

        # 複製一份目前的股票清單給 worker
        self.worker = StockDataWorker(self.stock_list.copy())
        self.worker.finished.connect(self.on_data_loaded)
        self.worker.error.connect(self.on_data_error)
        self.worker.start()

    def on_data_loaded(self, close_df, returns_df, corr_df, report_text, names):
        self.close_df = close_df
        self.returns_df = returns_df
        self.corr_df = corr_df

        # 顯示文字報告
        self.report_text.setPlainText(report_text)

        # 填充相關係數表格
        self.fill_correlation_table(corr_df)

        # 畫熱力圖
        self.draw_correlation_heatmap(corr_df, names)

        self.load_btn.setEnabled(True)

    def on_data_error(self, err_msg):
        QMessageBox.critical(
            self,
            "資料載入錯誤",
            f"無法載入股價資料：\n{err_msg}"
        )
        self.load_btn.setEnabled(True)

    def fill_correlation_table(self, corr_df: pd.DataFrame):
        names = list(corr_df.columns)
        n = len(names)

        self.corr_table.setRowCount(n)
        self.corr_table.setColumnCount(n)
        self.corr_table.setHorizontalHeaderLabels(names)
        self.corr_table.setVerticalHeaderLabels(names)

        self.corr_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        for i, row_name in enumerate(names):
            for j, col_name in enumerate(names):
                val = corr_df.iloc[i, j]
                item = QTableWidgetItem(f"{val:.3f}")
                item.setTextAlignment(Qt.AlignCenter)
                self.corr_table.setItem(i, j, item)

    def draw_correlation_heatmap(self, corr_df: pd.DataFrame, names):
        arr = corr_df.to_numpy()

        # pyqtgraph ImageView 期待 (row, col) 的 2D 陣列
        self.corr_view.setImage(arr.astype(np.float32))

        # 設定座標軸標籤（用 tick 方式）
        self.corr_view.view.getAxis("bottom").setTicks(
            [(i, name) for i, name in enumerate(names)]
        )
        self.corr_view.view.getAxis("left").setTicks(
            [(i, name) for i, name in enumerate(names)]
        )
        self.corr_view.view.setLabel("bottom", "股票")
        self.corr_view.view.setLabel("left", "股票")
        self.corr_view.view.setTitle("相關係數熱力圖")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 設定中文字型（Windows 環境）
    font = QFont("Microsoft JhengHei", 10)
    app.setFont(font)

    win = StockCorrelationWindow()
    win.show()
    sys.exit(app.exec())
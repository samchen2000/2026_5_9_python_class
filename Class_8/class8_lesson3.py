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
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal

import pyqtgraph as pg
from pyqtgraph import ImageView


# ============ 背景資料抓取與計算（放在 QThread 裡） ============

class StockDataWorker(QThread):
    finished = Signal(object, object, object, str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.tickers = {
            "台積電": "2330.TW",
            "聯電": "2303.TW",
            "聯發科": "2454.TW",
            "鴻海": "2317.TW",
        }

    def run(self):
        try:
            # 抓 2006 年至今的歷史資料
            data = yf.download(
                list(self.tickers.values()),
                start="2006-01-01",
                interval="1d",
                auto_adjust=True,
            )

            # 只取收盤價
            close = data["Close"]

            # 把欄位名稱從股票代號改成中文公司名
            code_to_name = {v: k for k, v in self.tickers.items()}
            close = close.rename(columns=code_to_name)

            # 計算每日報酬率
            returns = close.pct_change().dropna()

            # 計算相關係數
            corr = returns.corr()

            # 產生簡短文字報告
            now_str = datetime.today().strftime("%Y-%m-%d")
            report = f"資料更新時間：{now_str}\n"
            report += f"分析期間：2006-01-01 至今\n"
            report += f"股票數：{len(self.tickers)}\n\n"
            report += "收盤價最後 5 筆：\n"
            report += close.tail().to_string()
            report += "\n\n日報酬率相關係數：\n"
            report += corr.round(3).to_string()

            self.finished.emit(close, returns, corr, report)

        except Exception as e:
            self.error.emit(str(e))


# ============ 主視窗 ============

class StockCorrelationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("台股相關係數視覺化（PySide6）")
        self.resize(1100, 700)

        self.close_df = None
        self.returns_df = None
        self.corr_df = None

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

        # 按鈕區
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("載入股價資料並計算相關係數")
        self.load_btn.clicked.connect(self.start_load_data)
        btn_layout.addWidget(self.load_btn)
        main_layout.addLayout(btn_layout)

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

    def start_load_data(self):
        self.load_btn.setEnabled(False)
        self.report_text.clear()
        self.corr_table.setRowCount(0)
        self.corr_table.setColumnCount(0)
        self.corr_view.clear()

        self.worker = StockDataWorker()
        self.worker.finished.connect(self.on_data_loaded)
        self.worker.error.connect(self.on_data_error)
        self.worker.start()

    def on_data_loaded(self, close_df, returns_df, corr_df, report_text):
        self.close_df = close_df
        self.returns_df = returns_df
        self.corr_df = corr_df

        # 顯示文字報告
        self.report_text.setPlainText(report_text)

        # 填充相關係數表格
        self.fill_correlation_table(corr_df)

        # 畫熱力圖
        self.draw_correlation_heatmap(corr_df)

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

    def draw_correlation_heatmap(self, corr_df: pd.DataFrame):
        names = list(corr_df.columns)
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
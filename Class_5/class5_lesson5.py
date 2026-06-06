import requests
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# YouBike JSON 資料網址
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

def download_youbike_data():
    """下載 JSON 資料並存檔"""
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("下載成功")

        # 建立資料夾
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # 使用當天日期時間命名檔案
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = data_dir / f"youbike_{now_str}.json"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"JSON 檔案已儲存：{json_file}")

        return data
    else:
        print("下載失敗", response.status_code)
        return None

def data_to_pdf(data):
    """整理資料並產生 PDF 表格"""
    if not data:
        print("沒有資料可生成 PDF")
        return

    # 轉成 DataFrame
    df = pd.DataFrame(data)

    # 只取重要欄位
    columns = ["sno", "sna", "tot", "sbi", "bemp", "lat", "lng", "mday"]
    df = df[columns]

    # 建立 PDF
    pdf_dir = Path("pdf")
    pdf_dir.mkdir(exist_ok=True)
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_file = pdf_dir / f"youbike_{now_str}.pdf"

    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    # 將 DataFrame 轉成 list of list
    data_for_pdf = [df.columns.tolist()] + df.values.tolist()

    table = Table(data_for_pdf, repeatRows=1)
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ])
    table.setStyle(style)

    doc.build([table])
    print(f"PDF 已產生：{pdf_file}")

def main():
    data = download_youbike_data()
    data_to_pdf(data)

if __name__ == '__main__':
    main()
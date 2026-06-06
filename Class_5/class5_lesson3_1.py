import requests
import json
import shutil
from pathlib import Path
from datetime import datetime
import pandas as pd

url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

def main():
    print("這裡是 main function 的命名空間")

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("下載成功")

        # 建立資料夾
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # 產生時間格式檔名
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = data_dir / f"youbike_{now_str}.json"

        # 儲存 JSON
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"檔案已儲存：{filename}")

        print(type(data))
        print(len(data))
        print(data[0])

    else:
        print("下載失敗")
        print(response.status_code)

def delete_file():
    file_path = Path("example.txt")

    # 檢查檔案存在與否再刪除
    if file_path.is_file():
        file_path.unlink()
        print("檔案已刪除")
    else:
        print("檔案不存在")

def delete_folder():
    folder_path = "data"
    shutil.rmtree(folder_path) # 會連同資料夾內的所有檔案與子目錄一併強制刪除

if __name__ == '__main__':
    delete_folder()
    main()
import tkinter as tk
from tkinter import ttk

import requests
import pandas as pd

from pathlib import Path

window = tk.Tk()
window.title("YouBike 即時資訊")
window.geometry("1200x700")

columns = ("編號", "站名", "區域", "地址", "剩餘數量")

tree = ttk.Treeview(
    window,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(fill="both", expand=True)

class YouBikeModel:  # Model : YouBikeModel 負責下載資料

    URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    def load_data(self):

        response = requests.get(self.URL, timeout=10)

        if response.status_code == 200:

            data = response.json()

            return pd.DataFrame(data)

        return pd.DataFrame()

class YouBikeView(tk.Tk): #View : YouBikeView 負責畫面

    def __init__(self):

        super().__init__()

        self.title("YouBike 即時資訊")
        self.geometry("1400x700")

        self.create_widgets()
        
class YouBikeController:

    def __init__(self):

        self.model = YouBikeModel()

        self.view = YouBikeView()

        self.df = pd.DataFrame()

        self.bind_events()

        self.refresh_data()

def show_data(df):

    tree.delete(*tree.get_children())

    for _, row in df.iterrows():

        tree.insert(
            "",
            "end",
            values=(
                row["sno"],
                row["sna"],
                row["sarea"],
                row["ar"],
                row["available_rent_bikes"]
            )
        )


def load_data():

    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data)

        show_data(df)


btn = tk.Button(
    window,
    text="下載YouBike資料",
    command=load_data
)

btn.pack()

window.mainloop()
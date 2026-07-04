## 2026/6/27 課程
- Matplotlib繪圖基礎-繪圖和視覺展示
- Pandas整合視覺化 -直接使用Pandas繪制圖表
### 2020/6/27 上課影片
#### 2026_6_27_早上
https://www.youtube.com/watch?v=V-78xARVSig
#### 2026_6_27_下午
https://youtube.com/live/hzTcwBLsypc
### 上課內容 :  

### 上課筆記 :  
1. 你直接用 python .\pie_chart_app.py 執行 Streamlit 程式時，  
會看到一堆 missing ScriptRunContext 的警告，這是正常的；  
Streamlit 必須用 streamlit run 啟動才能在瀏覽器中正確顯示。

### 為什麼會這樣？
用 python 直接執行時，Streamlit 的某些內部物件（例如 ScriptRunContext）沒有被建立，所以幫你印出警告。

這些警告本身不會阻擋程式執行，但你会看不到 Streamlit 的網頁介面，也無法互動。

正確啟動方式
在你的 PowerShell 裡，把命令改成：
```
streamlit run .\pie_chart_app.py
```
通常你會看到類似：
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```
然後在瀏覽器打開 http://localhost:8501 即可看到你的 pie chart app。
### 回家學習心得 :  
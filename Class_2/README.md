## 2026/5/16 課程
- 物件導向與模組應用-Python物件和類別	
- 使用Requests獲取開放資料-使用Python requests套件下載政府開放平台資料		
### 2020/5/16 上課影片
#### 2026_5_16_早上
https://www.youtube.com/watch?v=Fnd2LahWlk8
#### 2026_5_16_下午
https://www.youtube.com/watch?v=9LU0ccfbGp0
### 上課內容 :  
1. 安裝 VS code
2. 何謂.toml file
- toml 是 Tom's Obvious, Minimal Language 的縮寫，是一種語意化且極簡的設定檔格式。它的主要設計目標是讓人易讀、易寫，並且能夠無歧義地被轉換為程式語言中的雜湊表
## - 核心特性
- 鍵值對與區塊：使用 key = value 的結構，並透過 [section] 來區分不同模組。
- 原生資料型態：明確支援字串、整數、浮點數、布林值、陣列及日期時間。
- 支援註解：可使用 # 來撰寫註解以增加程式碼可讀性。
## 常見應用場景
- Python 專案：.toml（如 pyproject.toml）已成為現代 Python 專案的標準設定檔，用於管理建構依賴與專案元資料。
- Rust 生態系：Cargo 套件管理器的設定檔（Cargo.toml）即使用此格式。
## 語法範例
``` toml
# 這是註解
title = "TOML 範例"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00Z # 日期時間格式

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true
```
### 上課筆記 :  

### 回家學習心得 :  
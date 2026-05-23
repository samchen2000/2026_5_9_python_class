## 2026/5/16 課程
- 物件導向與模組應用-Python物件和類別	
- 使用Requests獲取開放資料-使用Python requests套件下載政府開放平台資料		
### 2026/5/16 上課影片
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
3. 安裝 uv
 - 如何安裝   

## linux & mac ##
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
## Windows ##
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

 ```
 - 驗證安裝
 ```
uv --version
```
- 管理 Python 版本
```
# 查看可用與已安裝的 Python 版本
uv python list
# 安裝最新版本的 Python
uv python install
# 安裝特定版本，例如 3.12
uv python install 3.12
# 一次裝多個版本
uv python install 3.11 3.12 3.13
```
- 建立與啟用虛擬環境
```
mkdir my-project
cd my-project
```
- 建立一個虛擬環境（預設叫 .venv）：
```
uv venv
# 或指定使用某版本 Python
uv venv --python 3.12
```
### 這會在目前資料夾底下建立 .venv 子資料夾 ###
- 啟用虛擬環境：
Windows（PowerShell）：
```
.\.venv\Scripts\activate
```
- 要離開虛擬環境：
```
deactivate
```
### 環境名稱就會消失，回到系統原本狀態。 ###


### 上課筆記 :  
## 1. 安裝完 uv
### - 1. uv init
### - 2. uv venv
### - 3. uv sync
### - 4. .venv\Scripts\activate
### 如果執行 " .\.venv\Scripts\activate" 出現錯誤  
```
".\\.venv\\Scripts\\activate : 因為這個系統上已停用指令碼執行，所以無法載入 D:\\IQ app\\GitHUB\\2026_5_9
_python_class\\Class_2\\lesson1\\.venv\\Scripts\\activate.ps1 檔案。如需詳細資訊，請參閱 about_Executi
on_Policies，網址為 https:/go.microsoft.com/fwlink/?LinkID=135170。
位於 線路:1 字元:1
+ .\\.venv\\Scripts\\activate
+ ~~~~~~~~~~~~~~~~~~~~~~~~
+ CategoryInfo : SecurityError: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess" 
```
### 如何解決.

### 原因 :
這個錯誤是因為「PowerShell 預設禁止執行指令碼」，所以你的 .venv\Scripts\activate.ps1 被擋下來，不是 uv 或 Python 壞掉。要解決只要調整 PowerShell 的「執行原則」即可。

### 解決方式 :
### 1. 把執行原則改成 RemoteSigned
在powershell 輸入
```powershell
Set-ExecutionPolicy RemoteSigned
```
- 出現提示時，輸入 Y 再按 Enter。
- 這會允許本機建立的 ps1 檔執行（例如 .venv\Scripts\activate.ps1），是微軟官方文件也建議的常見設定之一。

### 2. 如果你只想暫時允許
這樣只會對「目前這個 PowerShell 視窗」放寬限制，關掉視窗就恢復原本設定。之後在同一個視窗再執行
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```
### 3. 不改 PowerShell 的簡單替代方案
- 開啟「命令提示字元」（搜尋 cmd）。
- 切到你的專案資料夾：
```
cd /d "D:\IQ app\GitHUB\2026_5_9_python_class\Class_2\lesson1"
```
- 執行：
```
.venv\Scripts\activate.bat
```

## 2. 安裝 git
- 設定
- git config --global user.name "sam_class"
- git config --global user.email "your.email@exampl"
### 回家學習心得 :  
1. uv
- 管理多個 Python 版本（類似 pyenv）。
- 建立、啟用虛擬環境（類似 venv、virtualenv）。
- 安裝、更新、移除套件（取代 pip / pip-tools）。
- 安裝 CLI 工具（取代 pipx）。
- 幫腳本自動處理依賴並執行（uv run）。


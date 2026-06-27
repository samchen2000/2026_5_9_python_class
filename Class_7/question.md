# 程式執行問題紀錄

## 1. 檢查情況
我檢查了目前 Windows PowerShell 的執行原則，結果如下：

- MachinePolicy：Undefined
- UserPolicy：Undefined
- Process：Undefined
- CurrentUser：Undefined
- LocalMachine：Undefined

另外，我也嘗試直接啟動虛擬環境腳本，系統顯示：

- `activate script not found`

這表示目前工作區內沒有可直接使用的對應啟動腳本，因此無法在此環境中直接重現該啟動流程。

## 2. 發生原因
根據專案中的說明文件 [Class_2/README.md](Class_2/README.md) ，若出現以下錯誤：

> 因為這個系統上已停用指令碼執行，所以無法載入 ... .ps1 檔案

通常是因為 PowerShell 的執行原則限制了腳本執行，導致 `.ps1` 檔案被阻擋，進而無法正常啟動虛擬環境。

## 3. 處理方式
可以採用以下方法處理：

1. 暫時性處理（只對目前視窗有效）
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   ```

2. 永久性處理（建議）
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```
   之後輸入 `Y` 確認即可。

3. 不修改 PowerShell 設定時
   可以改用命令提示字元執行：
   ```cmd
   .venv\Scripts\activate.bat
   ```

## 4. 結論
這次檢查的重點是：

- 問題主要來自 PowerShell 的腳本執行政策限制；
- 不是 Python 本身或虛擬環境安裝失敗；
- 透過調整執行原則或改用 `.bat` 啟動方式即可處理。

# 🔐 專屬密碼管理器 (Secure Password Manager)

本專案是一個兼具命令行 (CLI) 與圖形化介面 (GUI) 的本機安全密碼管理器。本軟體完全運行於本機環境，無任何網路傳輸，並採用 AES 級別 (Fernet) 的對稱加密技術來儲存密碼。

---

## ✨ 核心特色與防護功能

1. **圖形化桌面 App**
   - 基於 `customtkinter` 庫開發，具備現代感的 UI 圓角與平滑動畫。
   - 支援系統主題同步，可自動/手動切換 **深色模式 (Dark)** 與 **淺色模式 (Light)**。

2. **動態防螢幕截圖與防側錄**
   - 整合 Windows 系統 `SetWindowDisplayAffinity` API。
   - 當進入 **「所有密碼清單」**、彈出 **「主密碼驗證」** 或 **「編輯」** 視窗時，防截圖與防側錄機制將自動啟用（擷取的畫面將呈現全黑或隱形，有效防範 Windows 內建剪取、OBS、Zoom 或 Discord 等畫面投影側錄）。
   - 在其他安全分頁（如登入、新增帳密、系統設定）則會自動解鎖，兼顧使用便利性。

3. **雙重主密碼驗證**
   - 清單上的所有敏感按鈕（顯示/隱藏密碼、一鍵複製帳號、一鍵複製密碼、編輯、刪除）點擊後，皆需輸入系統主密碼（`admin596196`）驗證成功後才能執行操作。

4. **15 秒限時檢視與動態倒數**
   - 密碼明文解鎖後，**僅會顯示 15 秒**。
   - 眼球按鈕上會動態顯示剩餘倒數秒數（例如 `15s` ➔ `14s` ... ➔ `1s`）。時間歸零後，密碼將會自動重新隱藏（回復為 `*`）。
   - 您亦可在倒數期間隨時再次點擊按鈕來提前關閉明文。

5. **環境防窺安全提示**
   - 當您點入「密碼清單」分頁時，會彈出視窗並在頂部顯示橘色警示：**「⚠️ 請先觀察周圍是否有人在看！」**，提醒您隨時注意環境安全。

6. **隨機強密碼生成器**
   - 新增密碼時，提供一鍵隨機生成高強度的 16 位英數與特殊字元密碼，並自動填入輸入框。

---

## 📂 檔案結構說明

- `gui.py`：桌面圖形化 App 主程式。
- `dist/專屬密碼管理器.exe`：已編譯完成的獨立 Windows 執行檔，免安裝 Python 即可點擊使用。
- `passwords.txt`：已加密的密碼文字檔（預設存儲於 `C:\Users\USER\OneDrive\Desktop\Report\passwords.txt`，並提供當前目錄 fallback 讀取）。

---

## 🚀 快速開始

### 方式一：直接執行編譯好的 App (.exe)
打開本機資料夾，點擊進入 `dist` 目錄，雙擊打開 **[專屬密碼管理器.exe](file:///c:/Users/USER/OneDrive/Desktop/Report/dist/專屬密碼管理器.exe)** 即可直接啟動程式。

### 方式二：在 Python 環境中執行
1. **建立虛擬環境 (venv) 並安裝依賴**：
   如果您尚未建立虛擬環境，請打開終端機並切換至專案根目錄，依序執行以下命令：
   ```powershell
   # 1. 建立虛擬環境
   python -m venv .venv

   # 2. 啟用虛擬環境
   .venv\Scripts\activate

   # 3. 安裝依賴套件
   pip install customtkinter cryptography pyinstaller
   ```
2. **執行 App**：
   ```powershell
   python gui.py
   ```
3. **執行 CLI 版本**：
   ```powershell
   python main.py
   ```

### ⚙️ 系統預設登入憑證
- **帳號**：`admin`
- **主密碼**：`admin596196`

---

## 🛠️ 如何重新打包為 `.exe` 執行檔

若您後續有修改 `gui.py` 原始碼，可使用 PyInstaller 重新編譯為無控制台視窗的獨立執行檔：
```powershell
.venv\Scripts\pyinstaller --noconsole --onefile --name "專屬密碼管理器" gui.py
```
編譯完成後，最新生成的 `.exe` 檔會自動輸出至 `dist/` 目錄中。

import base64
import hashlib
import os
import random
import string
import sys
from cryptography.fernet import Fernet
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

def set_screenshot_prevention(window, enable):
    # 啟用或停用視窗的防止螢幕截圖與錄影功能 (僅支援 Windows 系統)
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        window.update_idletasks()
        hwnd_tk = window.winfo_id()
        # GA_ROOT = 2，取得最外層根視窗控制代碼
        hwnd_root = ctypes.windll.user32.GetAncestor(hwnd_tk, 2)
        # WDA_EXCLUDEFROMCAPTURE = 0x00000011 (防止截圖且在擷取畫面中隱形), WDA_NONE = 0
        affinity = 0x00000011 if enable else 0x00000000
        result = ctypes.windll.user32.SetWindowDisplayAffinity(hwnd_root, affinity)
        return result != 0
    except Exception:
        return False

# 設置 CustomTkinter 的外觀主題與色彩
ctk.set_appearance_mode("System")  # System, Dark, Light
ctk.set_default_color_theme("blue")  # Blue, Green, Dark-blue

DEFAULT_FILE_PATH = r"C:\Users\USER\OneDrive\Desktop\python\Report\passwords.txt"

def get_file_path():
    # 取得密碼檔案路徑，支援 fallback 到當前目錄
    if os.path.exists(DEFAULT_FILE_PATH):
        return DEFAULT_FILE_PATH
    
    # 檢查該路徑的資料夾是否存在，若存在則建立檔案
    dir_path = os.path.dirname(DEFAULT_FILE_PATH)
    if os.path.exists(dir_path):
        return DEFAULT_FILE_PATH
        
    # 本地備用路徑
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "passwords.txt")

def get_cipher():
    # 利用主密碼產生加密鑰匙 (Fernet)
    master_pass = "admin596196"
    key = base64.urlsafe_b64encode(hashlib.sha256(master_pass.encode('utf-8')).digest())
    return Fernet(key)

class EditDialog(ctk.CTkToplevel):
    # 自訂的密碼修改對話框
    def __init__(self, parent, account, password, callback):
        super().__init__(parent)
        self.title("✏️ 修改帳密紀錄")
        self.geometry("400x280")
        self.resizable(False, False)
        
        # 視窗置中於父視窗
        self.transient(parent)
        self.grab_set()
        
        # 防止螢幕截圖
        set_screenshot_prevention(self, True)
        
        self.callback = callback
        
        # 標題
        title_label = ctk.CTkLabel(self, text="修改帳密紀錄", font=("Microsoft JhengHei", 18, "bold"))
        title_label.pack(pady=15)
        
        # 帳號輸入
        self.account_entry = ctk.CTkEntry(self, width=280, placeholder_text="帳號或網站名稱")
        self.account_entry.insert(0, account)
        self.account_entry.pack(pady=10)
        
        # 密碼輸入
        self.password_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.password_frame.pack(pady=10)
        
        self.password_entry = ctk.CTkEntry(self.password_frame, width=240, placeholder_text="密碼", show="*")
        self.password_entry.insert(0, password)
        self.password_entry.pack(side="left")
        
        self.show_pass = False
        self.eye_btn = ctk.CTkButton(self.password_frame, text="👁️", width=35, fg_color="transparent", 
                                      hover_color=("#dbdbdb", "#2b2b2b"), text_color=("black", "white"), command=self.toggle_password)
        self.eye_btn.pack(side="left", padx=5)
        
        # 按鈕區
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(btn_frame, text="儲存修改", width=120, fg_color="#2ecc71", hover_color="#27ae60", command=self.save)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(btn_frame, text="取消", width=120, fg_color="#7f8c8d", hover_color="#95a5a6", command=self.destroy)
        cancel_btn.pack(side="left", padx=10)
        
    def toggle_password(self):
        self.show_pass = not self.show_pass
        self.password_entry.configure(show="" if self.show_pass else "*")
        self.eye_btn.configure(text="🔒" if self.show_pass else "👁️")
        
    def save(self):
        new_acc = self.account_entry.get().strip()
        new_pwd = self.password_entry.get().strip()
        if not new_acc or not new_pwd:
            messagebox.showerror("錯誤", "帳號與密碼欄位不可為空！")
            return
        self.callback(new_acc, new_pwd)
        self.destroy()

class VerifyMasterPasswordDialog(ctk.CTkToplevel):
    # 主密碼驗證對話框
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("🔒 安全驗證")
        self.geometry("350x200")
        self.resizable(False, False)
        
        # 視窗置中於父視窗
        self.transient(parent)
        self.grab_set()
        
        # 防止螢幕截圖
        set_screenshot_prevention(self, True)
        
        self.callback = callback
        
        title_label = ctk.CTkLabel(self, text="🔑 需要安全驗證", font=("Microsoft JhengHei", 16, "bold"))
        title_label.pack(pady=15)
        
        desc_label = ctk.CTkLabel(self, text="請輸入系統主密碼以確認執行此操作:", font=("Microsoft JhengHei", 12))
        desc_label.pack(pady=2)
        
        self.pwd_entry = ctk.CTkEntry(self, width=220, placeholder_text="請輸入主密碼", show="*")
        self.pwd_entry.pack(pady=10)
        self.pwd_entry.focus()
        self.pwd_entry.bind("<Return>", lambda e: self.verify())
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ok_btn = ctk.CTkButton(btn_frame, text="確認", width=90, fg_color="#2b76fb", command=self.verify)
        ok_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(btn_frame, text="取消", width=90, fg_color="#7f8c8d", command=self.destroy)
        cancel_btn.pack(side="left", padx=5)
        
    def verify(self):
        master_pass = "admin596196"
        if self.pwd_entry.get().strip() == master_pass:
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("驗證失敗", "主密碼錯誤！無法執行此動作。")
            self.pwd_entry.delete(0, "end")
            self.pwd_entry.focus()

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 基本視窗設定
        self.title("🔒 專屬密碼管理器")
        self.geometry("850x580")
        self.resizable(True, True)
        
        # 預設不防止螢幕截圖
        set_screenshot_prevention(self, False)
        
        # 初始化狀態
        self.attempts = 0
        self.max_attempts = 10
        self.entries = []
        
        # 初始顯示登入畫面
        self.show_login_screen()
        
    def center_window(self, width, height):
        # 將視窗置中顯示
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def clear_screen(self):
        # 清除當前視窗的所有元件
        for widget in self.winfo_children():
            widget.destroy()

    # ==================== 登入畫面 ====================
    def show_login_screen(self):
        # 登入畫面不防止螢幕截圖
        set_screenshot_prevention(self, False)
        self.clear_screen()
        self.center_window(450, 400)
        
        # 卡片容器
        card = ctk.CTkFrame(self, width=380, height=340, corner_radius=15)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        # 標題
        title_label = ctk.CTkLabel(card, text="🔑 專屬密碼管理器", font=("Microsoft JhengHei", 22, "bold"))
        title_label.place(relx=0.5, rely=0.15, anchor="center")
        
        sub_label = ctk.CTkLabel(card, text="安全加密存儲技術", font=("Microsoft JhengHei", 12), text_color="gray")
        sub_label.place(relx=0.5, rely=0.25, anchor="center")
        
        # 帳號輸入框
        self.login_user = ctk.CTkEntry(card, width=260, height=35, placeholder_text="使用者帳號")
        self.login_user.place(relx=0.5, rely=0.42, anchor="center")
        self.login_user.bind("<Return>", lambda e: self.login_pass.focus())
        
        # 密碼輸入框
        self.login_pass = ctk.CTkEntry(card, width=260, height=35, placeholder_text="系統主密碼", show="*")
        self.login_pass.place(relx=0.5, rely=0.57, anchor="center")
        self.login_pass.bind("<Return>", lambda e: self.check_login())
        
        # 錯誤訊息顯示
        self.error_label = ctk.CTkLabel(card, text="", font=("Microsoft JhengHei", 12), text_color="#e74c3c")
        self.error_label.place(relx=0.5, rely=0.70, anchor="center")
        
        # 登入按鈕
        login_btn = ctk.CTkButton(card, text="登入系統", width=260, height=38, font=("Microsoft JhengHei", 14, "bold"), command=self.check_login)
        login_btn.place(relx=0.5, rely=0.82, anchor="center")

    def check_login(self):
        master_user = "admin"
        master_pass = "admin596196"
        
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()
        
        if username == master_user and password == master_pass:
            self.show_main_screen()
        else:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            if remaining <= 0:
                self.error_label.configure(text="🔒 嘗試次數過多，系統已鎖定。")
                self.login_user.configure(state="disabled")
                self.login_pass.configure(state="disabled")
            else:
                self.error_label.configure(text=f"❌ 帳號或密碼錯誤。還剩 {remaining} 次機會。")
                self.login_pass.delete(0, "end")
                self.login_pass.focus()

    # ==================== 主功能畫面 ====================
    def show_main_screen(self):
        self.clear_screen()
        self.geometry("850x580")
        self.center_window(850, 580)
        
        # 配置主要 Grid 佈局
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 建立側邊導覽欄 (Sidebar)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)  # 彈性空白推動下方按鈕
        
        # 側邊欄標題
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🔒 密碼管理器", font=("Microsoft JhengHei", 18, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=25)
        
        # 側邊導覽按鈕
        self.btn_list = ctk.CTkButton(self.sidebar_frame, text="📋 所有密碼清單", font=("Microsoft JhengHei", 13), 
                                      height=40, anchor="w", fg_color="transparent", text_color=("gray10", "gray90"),
                                      hover_color=("#dbdbdb", "#2b2b2b"), command=lambda: self.select_tab("list"))
        self.btn_list.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_add = ctk.CTkButton(self.sidebar_frame, text="➕ 新增帳密紀錄", font=("Microsoft JhengHei", 13), 
                                     height=40, anchor="w", fg_color="transparent", text_color=("gray10", "gray90"),
                                     hover_color=("#dbdbdb", "#2b2b2b"), command=lambda: self.select_tab("add"))
        self.btn_add.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        
        self.btn_settings = ctk.CTkButton(self.sidebar_frame, text="⚙️ 系統設定", font=("Microsoft JhengHei", 13), 
                                          height=40, anchor="w", fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("#dbdbdb", "#2b2b2b"), command=lambda: self.select_tab("settings"))
        self.btn_settings.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        
        # 登出按鈕
        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="🚪 安全登出", font=("Microsoft JhengHei", 12),
                                        fg_color="#e74c3c", hover_color="#c0392b", height=32, command=self.logout)
        self.btn_logout.grid(row=5, column=0, padx=15, pady=20, sticky="ew")
        
        # 建立右側主顯示容器 (Main Area)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        
        # 載入資料
        self.load_data()
        
        # 預設選取第一個分頁
        self.select_tab("list")

    def select_tab(self, tab_name):
        # 切換目前分頁與反打側邊按鈕樣式
        # 僅在進入清單分頁時啟用防截圖，其他分頁則關閉防截圖
        set_screenshot_prevention(self, tab_name == "list")
        # 重設按鈕樣式
        self.btn_list.configure(fg_color="transparent" if tab_name != "list" else ("#d4d4d4", "#2f2f2f"))
        self.btn_add.configure(fg_color="transparent" if tab_name != "add" else ("#d4d4d4", "#2f2f2f"))
        self.btn_settings.configure(fg_color="transparent" if tab_name != "settings" else ("#d4d4d4", "#2f2f2f"))
        
        # 清除主區域內容
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # 依照標籤名稱建立對應的分頁內容
        if tab_name == "list":
            self.create_list_tab()
        elif tab_name == "add":
            self.create_add_tab()
        elif tab_name == "settings":
            self.create_settings_tab()

    def logout(self):
        # 登出並重設狀態
        self.attempts = 0
        self.entries = []
        self.show_login_screen()

    # ==================== 資料儲存與載入核心 ====================
    def load_data(self):
        # 讀取檔案並將密碼解密，載入到記憶體中
        file_path = get_file_path()
        cipher = get_cipher()
        self.entries = []
        
        if not os.path.exists(file_path):
            return
            
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    decrypted = cipher.decrypt(line_str.encode('utf-8')).decode('utf-8')
                    if ". 帳號: " in decrypted and " | 密碼: " in decrypted:
                        parts = decrypted.split(". 帳號: ", 1)
                        orig_id = parts[0]
                        rem = parts[1]
                        account, password = rem.split(" | 密碼: ", 1)
                        self.entries.append({
                            "id": len(self.entries) + 1,
                            "account": account,
                            "password": password,
                            "raw_line": line_str,
                            "error": False
                        })
                    else:
                        self.entries.append({
                            "id": len(self.entries) + 1,
                            "account": decrypted,
                            "password": "",
                            "raw_line": line_str,
                            "error": False
                        })
                except Exception:
                    self.entries.append({
                        "id": len(self.entries) + 1,
                        "account": "[無法解密資料]",
                        "password": "",
                        "raw_line": line_str,
                        "error": True
                    })

    def save_data(self):
        # 將記憶體中的帳密資料重新加密並存檔
        file_path = get_file_path()
        cipher = get_cipher()
        lines_to_write = []
        
        for idx, entry in enumerate(self.entries):
            if entry.get("error"):
                lines_to_write.append(entry["raw_line"] + "\n")
            else:
                new_id = idx + 1
                plain_text = f"{new_id}. 帳號: {entry['account']} | 密碼: {entry['password']}"
                encrypted = cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')
                lines_to_write.append(encrypted + "\n")
                
        # 確保目標資料夾存在
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines_to_write)
            
        # 重新載入，確保記憶體狀態與硬碟檔案完全同步
        self.load_data()

    # ==================== 分頁一：查詢與管理 ====================
    def create_list_tab(self):
        # 顯示彈出式安全提示
        messagebox.showwarning("安全提示", "⚠️ 請先觀察周圍是否有人在看！")
        
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(3, weight=1) # 讓 scroll frame 自動填滿
        
        # 標題與簡介
        title_label = ctk.CTkLabel(self.main_container, text="📋 已儲存的密碼清單", font=("Microsoft JhengHei", 20, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # 提示橫幅
        warning_label = ctk.CTkLabel(self.main_container, text="⚠️ 安全提示：請時刻觀察周圍是否有人在看！", 
                                     font=("Microsoft JhengHei", 13, "bold"), text_color="#e67e22")
        warning_label.grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        # 搜尋區域
        search_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        search_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 輸入關鍵字以即時篩選帳號或網站...", height=35)
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_entries())
        
        # 捲動視窗容器 (Scrollable Frame)
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container)
        self.scroll_frame.grid(row=3, column=0, sticky="nsew")
        
        # 載入所有資料並呈呈現列表中
        self.render_list(self.entries)

    def render_list(self, items_to_render):
        # 清空舊有的列表項目
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        if not items_to_render:
            empty_label = ctk.CTkLabel(self.scroll_frame, text="📭 沒有找到符合的紀錄", font=("Microsoft JhengHei", 14), text_color="gray")
            empty_label.pack(pady=40)
            return
            
        for entry in items_to_render:
            # 建立一個大卡片 (Card Frame)
            card = ctk.CTkFrame(self.scroll_frame, height=65, corner_radius=8)
            card.pack(fill="x", pady=6, padx=2)
            
            # 使用 Grid 配置卡片內部元件
            card.grid_columnconfigure(0, weight=3) # 帳號/網站名稱
            card.grid_columnconfigure(1, weight=3) # 密碼顯示/隱藏
            card.grid_columnconfigure(2, weight=0) # 複製與編輯/刪除按鈕
            card.grid_rowconfigure(0, weight=1)
            
            # 1. 顯示 ID 與 網站帳號
            is_err = entry.get("error", False)
            display_title = f"#{entry['id']}  {entry['account']}"
            title_color = "#e74c3c" if is_err else ("black", "white")
            
            title_lbl = ctk.CTkLabel(card, text=display_title, font=("Microsoft JhengHei", 13, "bold"), text_color=title_color, anchor="w")
            title_lbl.grid(row=0, column=0, padx=15, sticky="w")
            
            if is_err:
                err_lbl = ctk.CTkLabel(card, text="[解密失敗]", font=("Microsoft JhengHei", 11), text_color="#e74c3c")
                err_lbl.grid(row=0, column=1, padx=5, sticky="w")
                continue
                
            # 2. 密碼欄位與切換顯示按鈕
            pwd_container = ctk.CTkFrame(card, fg_color="transparent")
            pwd_container.grid(row=0, column=1, padx=10, sticky="ew")
            
            # 密碼 Entry (預設唯讀且隱藏)
            pwd_entry = ctk.CTkEntry(pwd_container, height=28, width=150, border_width=0, fg_color="transparent", font=("Segoe UI", 12), show="*")
            pwd_entry.insert(0, entry["password"])
            pwd_entry.configure(state="readonly")
            pwd_entry.pack(side="left", fill="x", expand=True)
            
            # 切換顯示/隱藏按鈕
            eye_btn = ctk.CTkButton(pwd_container, text="👁️", width=25, height=25, fg_color="transparent", 
                                    hover_color=("#dcdcdc", "#333333"), text_color=("black", "white"))
            eye_btn.configure(command=lambda p=pwd_entry, b=eye_btn: VerifyMasterPasswordDialog(self, lambda: self.toggle_visible(p, b)))
            eye_btn.pack(side="right", padx=2)
            
            # 3. 功能操作按鈕區
            actions_container = ctk.CTkFrame(card, fg_color="transparent")
            actions_container.grid(row=0, column=2, padx=10, sticky="e")
            
            # 一鍵複製帳號
            copy_acc_btn = ctk.CTkButton(actions_container, text="👤 複製帳號", width=75, height=28, font=("Microsoft JhengHei", 11),
                                         fg_color=("#e6f0fa", "#2a3f5a"), text_color=("#1f538d", "#8ab4f8"), hover_color=("#cce0f5", "#3a567c"),
                                         command=lambda a=entry["account"]: VerifyMasterPasswordDialog(self, lambda: self.copy_to_clipboard(a, "帳號已成功複製到剪貼簿！")))
            copy_acc_btn.pack(side="left", padx=3)
            
            # 一鍵複製密碼
            copy_pwd_btn = ctk.CTkButton(actions_container, text="🔑 複製密碼", width=75, height=28, font=("Microsoft JhengHei", 11),
                                         fg_color=("#eafaf1", "#224a34"), text_color=("#2ecc71", "#81c995"), hover_color=("#d4f5e1", "#336d4c"),
                                         command=lambda p=entry["password"]: VerifyMasterPasswordDialog(self, lambda: self.copy_to_clipboard(p, "密碼已成功複製到剪貼簿！")))
            copy_pwd_btn.pack(side="left", padx=3)
            
            # 編輯按鈕
            edit_btn = ctk.CTkButton(actions_container, text="✏️ 編輯", width=55, height=28, font=("Microsoft JhengHei", 11),
                                     fg_color=("#fdf3e7", "#4d3419"), text_color=("#e67e22", "#ffb066"), hover_color=("#fbe7d0", "#6b4924"),
                                     command=lambda e=entry: VerifyMasterPasswordDialog(self, lambda: self.open_edit_dialog(e)))
            edit_btn.pack(side="left", padx=3)
            
            # 刪除按鈕
            del_btn = ctk.CTkButton(actions_container, text="❌ 刪除", width=55, height=28, font=("Microsoft JhengHei", 11),
                                    fg_color=("#fdedec", "#4c1c1a"), text_color=("#e74c3c", "#f28b82"), hover_color=("#fadbd8", "#6e2926"),
                                    command=lambda e=entry: VerifyMasterPasswordDialog(self, lambda: self.delete_entry(e)))
            del_btn.pack(side="left", padx=3)

    def toggle_visible(self, entry_widget, eye_btn):
        # 切換密碼顯示狀態，並啟動 15 秒倒數計時
        state = entry_widget.cget("show")
        entry_widget.configure(state="normal")
        if state == "*":
            # 顯示密碼
            entry_widget.configure(show="")
            # 啟動 15 秒倒數計時
            self.start_countdown(entry_widget, eye_btn, 15)
        else:
            # 手動隱藏密碼
            entry_widget.configure(show="*")
            eye_btn.configure(text="👁️")
        entry_widget.configure(state="readonly")

    def start_countdown(self, entry_widget, eye_btn, seconds_left):
        # 遞迴更新倒數計時器
        try:
            # 確保視窗元件依然存在
            if not entry_widget.winfo_exists() or not eye_btn.winfo_exists():
                return
                
            # 若使用者在此期間手動點擊隱藏，則停止計時
            if entry_widget.cget("show") == "*":
                eye_btn.configure(text="👁️")
                return

            if seconds_left > 0:
                eye_btn.configure(text=f"{seconds_left}s")
                self.after(1000, lambda: self.start_countdown(entry_widget, eye_btn, seconds_left - 1))
            else:
                self.hide_password(entry_widget, eye_btn)
        except Exception:
            pass

    def hide_password(self, entry_widget, eye_btn):
        # 自動將密碼改回隱藏狀態
        try:
            if entry_widget.winfo_exists():
                entry_widget.configure(state="normal")
                entry_widget.configure(show="*")
                entry_widget.configure(state="readonly")
            if eye_btn.winfo_exists():
                eye_btn.configure(text="👁️")
        except Exception:
            pass

    def copy_to_clipboard(self, text, message):
        # 複製內容到系統剪貼簿
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # 強制更新，確保寫入剪貼簿
        
        # 顯示通知 (在右下角快速閃爍小提醒或彈出視窗)
        messagebox.showinfo("系統提示", message)

    def filter_entries(self):
        # 即時過濾密碼清單
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            self.render_list(self.entries)
            return
            
        filtered = []
        for entry in self.entries:
            if not entry.get("error"):
                if keyword in entry["account"].lower() or keyword in entry["password"].lower():
                    filtered.append(entry)
            else:
                if keyword in entry["account"].lower():
                    filtered.append(entry)
                    
        self.render_list(filtered)

    def open_edit_dialog(self, entry):
        # 開啟編輯彈出視窗
        def save_callback(new_acc, new_pwd):
            # 尋找該項目在 entries 中的索引
            for idx, item in enumerate(self.entries):
                if item["id"] == entry["id"]:
                    self.entries[idx]["account"] = new_acc
                    self.entries[idx]["password"] = new_pwd
                    break
            self.save_data()
            self.filter_entries() # 刷新畫面
            messagebox.showinfo("成功", f"編號 {entry['id']} 的資料已成功更新！")
            
        EditDialog(self, entry["account"], entry["password"], save_callback)

    def delete_entry(self, entry):
        # 刪除指定帳密項目
        confirm = messagebox.askyesno("⚠️ 確認刪除", f"您確定要刪除此帳密紀錄嗎？\n\n帳號/網站: {entry['account']}")
        if confirm:
            # 從記憶體列表中移除
            self.entries = [item for item in self.entries if item["id"] != entry["id"]]
            
            # 重新編排 ID 順序
            for idx, item in enumerate(self.entries):
                item["id"] = idx + 1
                
            self.save_data()
            self.filter_entries() # 刷新畫面
            messagebox.showinfo("成功", "資料已成功刪除，並自動重新排定編號！")

    # ==================== 分頁二：新增帳密 ====================
    def create_add_tab(self):
        # 讓容器元件往中心靠攏
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # 標題
        title_label = ctk.CTkLabel(self.main_container, text="➕ 新增帳密紀錄", font=("Microsoft JhengHei", 20, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # 表單容器
        form_frame = ctk.CTkFrame(self.main_container, width=500, corner_radius=12)
        form_frame.grid(row=1, column=0, sticky="n", pady=10, padx=20)
        
        # 加點 padding
        inner_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        inner_frame.pack(padx=30, pady=25)
        
        # 帳號或網站名稱輸入
        lbl_acc = ctk.CTkLabel(inner_frame, text="帳號或網站名稱:", font=("Microsoft JhengHei", 13, "bold"))
        lbl_acc.pack(anchor="w", pady=(5, 2))
        self.add_acc_entry = ctk.CTkEntry(inner_frame, width=400, height=35, placeholder_text="例如: Google, Github, 銀行帳號等...")
        self.add_acc_entry.pack(pady=(0, 15))
        
        # 密碼輸入
        lbl_pwd = ctk.CTkLabel(inner_frame, text="密碼內容:", font=("Microsoft JhengHei", 13, "bold"))
        lbl_pwd.pack(anchor="w", pady=(5, 2))
        
        pwd_input_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        pwd_input_frame.pack(fill="x", pady=(0, 5))
        
        self.add_pwd_entry = ctk.CTkEntry(pwd_input_frame, width=350, height=35, placeholder_text="請輸入密碼或生成隨機密碼", show="*")
        self.add_pwd_entry.pack(side="left", fill="x", expand=True)
        
        self.add_show_pass = False
        self.add_eye_btn = ctk.CTkButton(pwd_input_frame, text="👁️", width=35, height=35, fg_color="transparent",
                                         hover_color=("#dbdbdb", "#2b2b2b"), text_color=("black", "white"), command=self.toggle_add_password)
        self.add_eye_btn.pack(side="left", padx=5)
        
        # 隨機密碼與儲存按鈕
        btn_action_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        btn_action_frame.pack(fill="x", pady=(15, 5))
        
        gen_btn = ctk.CTkButton(btn_action_frame, text="🎲 隨機密碼生成", font=("Microsoft JhengHei", 12), fg_color="#f39c12", hover_color="#d35400", 
                                height=35, command=self.generate_random_password)
        gen_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(btn_action_frame, text="儲存帳密 💾", font=("Microsoft JhengHei", 12, "bold"), fg_color="#2b76fb", hover_color="#1a5ecc",
                                 height=35, command=self.submit_new_entry)
        save_btn.pack(side="left", fill="x", expand=True)

    def toggle_add_password(self):
        self.add_show_pass = not self.add_show_pass
        self.add_pwd_entry.configure(show="" if self.add_show_pass else "*")
        self.add_eye_btn.configure(text="🔒" if self.add_show_pass else "👁️")

    def generate_random_password(self):
        # 生成一個強健的 16 位隨機密碼
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(random.choice(chars) for _ in range(16))
        
        # 自動填入並切換為明文顯示以利使用者記錄
        self.add_pwd_entry.delete(0, "end")
        self.add_pwd_entry.insert(0, pwd)
        
        # 確保密碼顯示出來
        self.add_show_pass = True
        self.add_pwd_entry.configure(show="")
        self.add_eye_btn.configure(text="🔒")
        
        messagebox.showinfo("隨機密碼生成器", f"已成功生成高強度密碼！\n密碼：{pwd}\n\n(已自動填入輸入框)")

    def submit_new_entry(self):
        # 送出新增紀錄
        account = self.add_acc_entry.get().strip()
        password = self.add_pwd_entry.get().strip()
        
        if not account or not password:
            messagebox.showerror("錯誤", "帳號與密碼欄位皆不可為空！")
            return
            
        new_entry = {
            "id": len(self.entries) + 1,
            "account": account,
            "password": password,
            "raw_line": "",
            "error": False
        }
        self.entries.append(new_entry)
        
        # 儲存
        self.save_data()
        
        # 清空欄位
        self.add_acc_entry.delete(0, "end")
        self.add_pwd_entry.delete(0, "end")
        self.add_show_pass = False
        self.add_pwd_entry.configure(show="*")
        self.add_eye_btn.configure(text="👁️")
        
        messagebox.showinfo("成功", f"已成功為「{account}」新增密碼！")
        
        # 切換到清單分頁看結果
        self.select_tab("list")

    # ==================== 分頁三：系統設定 ====================
    def create_settings_tab(self):
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # 標題
        title_label = ctk.CTkLabel(self.main_container, text="⚙️ 系統設定與資訊", font=("Microsoft JhengHei", 20, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # 設定區容器
        set_frame = ctk.CTkFrame(self.main_container, width=500, corner_radius=12)
        set_frame.grid(row=1, column=0, sticky="n", pady=10)
        
        # 加點 padding
        inner_frame = ctk.CTkFrame(set_frame, fg_color="transparent")
        inner_frame.pack(padx=30, pady=25)
        
        # 主題模式設定
        lbl_theme = ctk.CTkLabel(inner_frame, text="介面主題模式:", font=("Microsoft JhengHei", 13, "bold"))
        lbl_theme.pack(anchor="w", pady=(5, 5))
        
        self.theme_menu = ctk.CTkOptionMenu(inner_frame, values=["System", "Dark", "Light"], command=self.change_theme_mode, width=200)
        self.theme_menu.set(ctk.get_appearance_mode())
        self.theme_menu.pack(anchor="w", pady=(0, 20))
        
        # 儲存路徑資訊
        lbl_path_title = ctk.CTkLabel(inner_frame, text="密碼存儲檔案路徑:", font=("Microsoft JhengHei", 13, "bold"))
        lbl_path_title.pack(anchor="w", pady=(5, 2))
        
        # 唯讀顯示檔案路徑
        path_box = ctk.CTkEntry(inner_frame, width=420)
        path_box.insert(0, get_file_path())
        path_box.configure(state="readonly")
        path_box.pack(anchor="w", pady=(0, 20))
        
        # 安全宣告與關於
        about_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        about_frame.pack(fill="x", pady=10)
        
        lbl_about = ctk.CTkLabel(about_frame, text="⚠️ 系統安全宣告\n本密碼管理器採用 AES-like (Fernet) 加密算法，資料儲存在本機環境，請妥善保管您的電腦與主密碼。軟體不會進行任何網路傳輸，百分之百保護您的隱私安全。", 
                                 font=("Microsoft JhengHei", 11), text_color="gray", justify="left")
        lbl_about.pack(anchor="w")

    def change_theme_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()

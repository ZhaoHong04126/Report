def system_login():
    # 預設的帳號與主密碼
    master_user = "admin"
    master_pass = "admin596196"

    max_attempts = 10  # 限制最多嘗試 10 次
    attempts = 0

    print("=== 歡迎使用專屬密碼管理器 ===")

    # 判斷使用者
    while attempts < max_attempts:
        # 取得使用者輸入
        username_input = input("請輸入帳號: ")
        password_input = input("請輸入主密碼: ")

        # 檢查帳號密碼是否相符
        if username_input == master_user and password_input == master_pass:
            print("\n✅ 登入成功！正在進入系統...")
            return True  # 登入成功，回傳 True 給主程式
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"❌ 帳號或密碼錯誤。您還有 {remaining} 次機會。\n")

    print("🔒 嘗試次數過多，系統已鎖定。")
    return False  # 登入失敗，回傳 False 給主程式

def AP(Account, Password):
    # 將帳號與密碼儲存到指定桌面的文字檔中
    # 讓 Python 不亂編譯
    file_path = r"C:\Users\USER\OneDrive\Desktop\Report\passwords.txt"
    
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"帳號: {Account} | 密碼: {Password}\n")
    
    print(f"✅ 成功儲存帳號：{Account}")
    
# 程式的起點
if __name__ == "__main__":
    is_logged_in = system_login()

    if is_logged_in:
        while True:
            print("\n--- 密碼管理器主選單 ---")
            print("1. 新增帳號密碼")
            print("2. 離開系統")
            
            choice = input("請選擇你要執行的動作 (輸入數字): ")
            
            if choice == "1":
                new_account = input("請輸入要儲存的帳號 (或網站名稱): ")
                new_password = input("請輸入對應的密碼: ")
                # 呼叫你定義的函數來儲存
                AP(new_account, new_password)
                
            elif choice == "2":
                print(">> 系統已安全登出，再見！")
                break # 結束 while 迴圈，關閉程式
                
            else:
                print("❌ 無效的選項，請重新輸入。")
    else:
        print(">> 程式自動結束運行。")

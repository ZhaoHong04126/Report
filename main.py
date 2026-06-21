import base64
import hashlib
from cryptography.fernet import Fernet

def get_cipher():
    # 利用主密碼產生加密鑰匙
    master_pass = "admin596196"
    key = base64.urlsafe_b64encode(hashlib.sha256(master_pass.encode('utf-8')).digest())
    return Fernet(key)

def system_login():
    master_user = "admin"
    master_pass = "admin596196"

    max_attempts = 10
    attempts = 0

    print("=== 歡迎使用專屬密碼管理器 ===")

    while attempts < max_attempts:
        username_input = input("請輸入帳號: ")
        password_input = input("請輸入主密碼: ")

        if username_input == master_user and password_input == master_pass:
            print("\n✅ 登入成功！正在解密並進入系統...")
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"❌ 帳號或密碼錯誤。您還有 {remaining} 次機會。\n")

    print("🔒 嘗試次數過多，系統已鎖定。")
    return False

def AP(Account, Password):
    file_path = r"C:\Users\USER\OneDrive\Desktop\python\Report\passwords.txt"
    cipher = get_cipher()
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            current_lines = len(file.readlines())
    except FileNotFoundError:
        current_lines = 0  
        
    new_id = current_lines + 1  
    
    plain_text = f"{new_id}. 帳號: {Account} | 密碼: {Password}"
    encrypted_text = cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')
    
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(encrypted_text + "\n")
    
    print(f"✅ 成功儲存帳號：{Account} (檔案內已加密保護)")

def query_passwords(keyword):
    file_path = r"C:\Users\USER\OneDrive\Desktop\python\Report\passwords.txt"
    cipher = get_cipher()
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            found = False
            print(f"\n🔍 搜尋「{keyword}」的結果：")
            print("-" * 30)
            
            for line in file:
                try:
                    decrypted_line = cipher.decrypt(line.strip().encode('utf-8')).decode('utf-8')
                    if keyword.lower() in decrypted_line.lower():
                        print(decrypted_line) 
                        found = True
                except Exception:
                    pass
                    
            print("-" * 30)
            if not found:
                print("❌ 找不到符合的帳號或密碼紀錄。")
                
    except FileNotFoundError:
        print("❌ 找不到密碼檔案，您可能還沒新增過任何帳密。")

def list_all_passwords():
    file_path = r"C:\Users\USER\OneDrive\Desktop\python\Report\passwords.txt"
    cipher = get_cipher()
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            print("\n📋 所有已儲存的帳密清單：")
            print("-" * 30)
            
            content_found = False
            for line in file:
                try:
                    decrypted_line = cipher.decrypt(line.strip().encode('utf-8')).decode('utf-8')
                    print(decrypted_line)
                    content_found = True
                except Exception:
                    print("⚠️ [系統警告] 偵測到無法解密的資料，檔案可能遭竄改或包含舊版明文。")
                
            if not content_found:
                print("📭 目前檔案是空的，沒有任何紀錄。")
                
            print("-" * 30)
            
    except FileNotFoundError:
        print("❌ 找不到密碼檔案，您可能還沒新增過任何帳密。")

def update_password():
    file_path = r"C:\Users\USER\OneDrive\Desktop\python\Report\passwords.txt"
    cipher = get_cipher()
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        if not lines:
            print("📭 目前檔案是空的，沒有任何紀錄可以更新。")
            return
            
        target_id_str = input("請輸入要更新的資料編號 (數字): ")
        
        if not target_id_str.isdigit():
            print("❌ 輸入格式錯誤，請輸入數字。")
            return
            
        target_id = int(target_id_str)
        target_idx = target_id - 1 
        
        if 0 <= target_idx < len(lines):
            old_encrypted_line = lines[target_idx].strip()
            try:
                old_decrypted_line = cipher.decrypt(old_encrypted_line.encode('utf-8')).decode('utf-8')
            except Exception:
                print("❌ 無法解密該行資料，請確認是否為舊版未加密的明文。")
                return
                
            print(f"\n✏️ 您要修改的目前紀錄為: {old_decrypted_line}")
            new_account = input("請輸入新的帳號 (或網站名稱): ")
            new_password = input("請輸入新的密碼: ")
            
            plain_text = f"{target_id}. 帳號: {new_account} | 密碼: {new_password}"
            encrypted_text = cipher.encrypt(plain_text.encode('utf-8')).decode('utf-8')
            lines[target_idx] = encrypted_text + "\n"
            
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(lines)
                
            print(f"✅ 成功更新編號 {target_id} 的資料！")
        else:
            print("❌ 找不到此編號的紀錄，請確認後再試。")
            
    except FileNotFoundError:
        print("❌ 找不到密碼檔案，您可能還沒新增過任何帳密。")

def delete_password():
    # 新增：刪除舊有帳密的功能
    file_path = r"C:\Users\USER\OneDrive\Desktop\python\Report\passwords.txt"
    cipher = get_cipher()
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        if not lines:
            print("📭 目前檔案是空的，沒有任何紀錄可以刪除。")
            return
            
        target_id_str = input("請輸入要刪除的資料編號 (數字): ")
        
        if not target_id_str.isdigit():
            print("❌ 輸入格式錯誤，請輸入數字。")
            return
            
        target_id = int(target_id_str)
        target_idx = target_id - 1 
        
        if 0 <= target_idx < len(lines):
            old_encrypted_line = lines[target_idx].strip()
            try:
                # 先解密顯示給使用者確認，避免誤刪
                old_decrypted_line = cipher.decrypt(old_encrypted_line.encode('utf-8')).decode('utf-8')
            except Exception:
                print("❌ 無法解密該行資料，請確認是否為舊版未加密的明文。")
                return
                
            print(f"\n⚠️ 您確定要刪除此紀錄嗎？: {old_decrypted_line}")
            confirm = input("確認刪除請輸入 'y'，取消請按其他任意鍵: ").lower()
            
            if confirm == 'y':
                # 1. 移除選定的那行資料
                lines.pop(target_idx)
                
                # 2. 自動重新排序剩餘資料的內嵌編號 (Re-indexing)
                new_lines = []
                for idx, line in enumerate(lines):
                    try:
                        decrypted = cipher.decrypt(line.strip().encode('utf-8')).decode('utf-8')
                        if ". " in decrypted:
                            parts = decrypted.split(". ", 1)
                            content_part = parts[1] # 取得切分後的 "帳號: ... | 密碼: ..."
                            
                            new_id = idx + 1 # 重製新編號
                            new_plain_text = f"{new_id}. {content_part}"
                            # 重新加密
                            new_encrypted = cipher.encrypt(new_plain_text.encode('utf-8')).decode('utf-8') + "\n"
                            new_lines.append(new_encrypted)
                        else:
                            new_lines.append(line)
                    except Exception:
                        new_lines.append(line)
                
                # 3. 寫回文字檔中
                with open(file_path, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)
                    
                print(f"✅ 成功刪除編號 {target_id} 的資料，並已自動重新編排其餘資料的編號！")
            else:
                print(" 刪除已取消。")
        else:
            print("❌ 找不到此編號的紀錄，請確認後再試。")
            
    except FileNotFoundError:
        print("❌ 找不到密碼檔案，您可能還沒新增過任何帳密。")

# 程式的起點
if __name__ == "__main__":
    is_logged_in = system_login()

    if is_logged_in:
        while True:
            print("\n--- 密碼管理器主選單 ---")
            print("1. 新增帳密 ➕")
            print("2. 查詢帳密 🔍")
            print("3. 列出所有帳密 📋") 
            print("4. 更新舊帳密 ✏️") 
            print("5. 刪除帳密 ❌") # 新增選項
            print("0. 離開系統")
            
            choice = input("請選擇你要執行的動作 (輸入數字): ")
            
            if choice == "1":
                new_account = input("請輸入要儲存的帳號 (或網站名稱): ")
                new_password = input("請輸入對應的密碼: ")
                AP(new_account, new_password)
                
            elif choice == "2":
                search_keyword = input("請輸入要查詢的帳號、網站名稱或關鍵字: ")
                query_passwords(search_keyword)
                
            elif choice == "3":
                list_all_passwords()
                
            elif choice == "4":
                update_password()
                
            elif choice == "5":
                # 呼叫刪除功能
                delete_password()

            elif choice == "0":
                print(">> 系統已安全登出，再見！")
                break
                
            else:
                print("❌ 無效的選項，請重新輸入。")
    else:
        print(">> 程式自動結束運行。")

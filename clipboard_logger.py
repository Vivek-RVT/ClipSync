import os, time, json, pyperclip, subprocess
from clipboard_utils import encrypt_data
from password_manager import get_saved_password

SAVE_FILE = os.path.expanduser("~/.clip_sync/clipboard_data.json.aes")

# Auto get saved password (no user input)
password = get_saved_password()

# Load existing data if file exists
clipboard_data = []
if os.path.exists(SAVE_FILE):
    try:
        with open(SAVE_FILE, "rb") as f:
            encrypted = f.read()
        from clipboard_utils import decrypt_data
        decrypted = decrypt_data(encrypted, password)
        clipboard_data = json.loads(decrypted)
    except Exception as e:
        print("⚠️ Could not load old data:", e)
        clipboard_data = []

# Setup
print("✅ ClipSync Logger Started (no password)")
last_clip = ""

def get_window_title():
    try:
        result = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
        return result.decode().strip()
    except:
        return "Unknown"

while True:
    try:
        text = pyperclip.paste()
        if text and text != last_clip:
            last_clip = text
            source = get_window_title()
            item = {
                "id": len(clipboard_data) + 1,
                "text": text,
                "source": source,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            clipboard_data.append(item)

            # Save encrypted
            try:
                encrypted = encrypt_data(json.dumps(clipboard_data), password)
                with open(SAVE_FILE, "wb") as f:
                    f.write(encrypted)
                print(f"📋 #{item['id']} saved")
            except Exception as e:
                print("❌ Error saving:", e)

        time.sleep(1)
    except KeyboardInterrupt:
        print("👋 Logger stopped")
        break

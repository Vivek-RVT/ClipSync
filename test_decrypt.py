import os, json
from clipboard_utils import decrypt_data
from password_manager import verify_password_offline

SAVE_FILE = os.path.expanduser("~/.clip_sync/clipboard_data.json.aes")

password = input("🔐 Enter password to test: ")
if not verify_password_offline(password):
    print("❌ Incorrect password")
    exit()

if not os.path.exists(SAVE_FILE):
    print("❌ clipboard_data.json.aes not found!")
    exit()

with open(SAVE_FILE, "rb") as f:
    encrypted = f.read()

try:
    decrypted = decrypt_data(encrypted, password)
    data = json.loads(decrypted)
    print(f"✅ Decryption successful! Found {len(data)} clips.")
except Exception as e:
    print("❌ Decryption failed:", str(e))

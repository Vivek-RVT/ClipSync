📋 ClipSync - Local Clipboard Saver + Viewer 
────────────────────────────────────────────────────────────

👨‍💻 Created By: Vivek Rawat (RVT)
📁 Location: ~/.clip_sync/
🔐 All data is encrypted with your own password

────────────────────────────────────────────────────────────
uto-saves everything you copy (in background)
✅ Encrypts and stores it offline
🛠️ Features:
────────────────
✅ Auto-saves everything you copy (in background)
✅ Encrypts and stores it offline
✅ Silent restore via terminal (copy 2nd, 3rd item)
✅ Clean GUI for viewing, searching, filtering
✅ Password-protected & private
✅ Works 100% offline (except for sync)

────────────────────────────────────────────────────────────

🖥️ Usage:
────────────
▶️ Start Clipboard Logger (background):
  $ python3 ~/.clip_sync/clipboard_logger.py

▶️ Paste 2nd latest clipboard:
  $ python3 ~/.clip_sync/clipboard_logger.py --paste 2

▶️ View all in GUI:
  $ python3 ~/.clip_sync/viewer_gui.py


🧠 Tip: Use `alias clip2=...` to make fast command shortcuts.

────────────────────────────────────────────────────────────

🔑 Password & Recovery:
────────────────────────
First-time setup:
  $ python3 -c "from password_manager import setup_password; setup_password()"

Reset password (if you forgot):
  $ python3 -c "from password_manager import reset_password; reset_password()"

────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────

⚙️ Auto Start on Boot:
────────────────────────
Create autostart file:

$ nano ~/.config/autostart/ClipboardSaver.desktop

Paste this:

  [Desktop Entry]
  Name=Clipboard Saver
  Exec=python3 /home/YOUR_USER/.clip_sync/clipboard_logger.py
  Type=Application
  X-GNOME-Autostart-enabled=true

────────────────────────────────────────────────────────────

📦 Dependencies:
─────────────────
$ pip install pyperclip cryptography --break-system-packages
$ pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 --break-system-packages

────────────────────────────────────────────────────────────

👑 Thank You for Using ClipSync
────────────────────────────────
Stay safe, stay private.
Built by you — customized by you 💙

────────────────────────────────────────────────────────────

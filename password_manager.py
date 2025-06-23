import os

PASSWORD_FILE = os.path.expanduser("~/.clip_sync/password.txt")

def setup_password():
    password = input("🔐 Set your ClipSync password: ").strip()
    if not password:
        print("❌ Password cannot be empty.")
        return
    with open(PASSWORD_FILE, "w") as f:
        f.write(password)
    os.chmod(PASSWORD_FILE, 0o600)
    print("✅ Password saved.")

def get_saved_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            password = f.read().strip()
            if password:
                return password
    print("⚠️ No saved password found!")
    return None

def verify_password_offline(input_password):
    saved = get_saved_password()
    return saved == input_password

def reset_password_gui():
    from tkinter import simpledialog, messagebox

    new_pass = simpledialog.askstring("🔁 New Password", "Enter a new ClipSync password:", show="*")
    confirm_pass = simpledialog.askstring("🔁 Confirm Password", "Confirm new password:", show="*")

    if not new_pass or new_pass != confirm_pass:
        messagebox.showerror("❌ Mismatch", "Passwords do not match.")
        return

    with open(PASSWORD_FILE, "w") as f:
        f.write(new_pass)
    os.chmod(PASSWORD_FILE, 0o600)
    messagebox.showinfo("✅ Done", "Password changed successfully.")

def reset_password():
    if os.path.exists(PASSWORD_FILE):
        os.remove(PASSWORD_FILE)
        print("🧹 Old password file removed.")
    setup_password()

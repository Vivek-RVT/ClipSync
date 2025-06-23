import os, json
from tkinter import *
from tkinter import messagebox, simpledialog
from clipboard_utils import decrypt_data
from password_manager import verify_password_offline, reset_password_gui

SAVE_FILE = os.path.expanduser("~/.clip_sync/clipboard_data.json.aes")

# GUI start
win = Tk()
win.withdraw()  # Hide until password correct

# Ask for password in GUI
password = simpledialog.askstring("🔐 Enter Password", "Enter your ClipSync password:", show="*")
if not verify_password_offline(password):
    messagebox.showerror("❌ Wrong Password", "Password is incorrect!")
    win.destroy()
    exit()

# Load clipboard history
try:
    with open(SAVE_FILE, "rb") as f:
        encrypted = f.read()
    decrypted = decrypt_data(encrypted, password)
    clipboard_data = json.loads(decrypted)
except Exception as e:
    messagebox.showerror("Error", f"Could not load clipboard data:\n{e}")
    win.destroy()
    exit()

clipboard_data = sorted(clipboard_data, key=lambda x: x['id'], reverse=True)

win.deiconify()
win.title("📋 ClipSync")
win.geometry("980x600")
win.configure(bg="#f6f7f9")

# ─ Menu ─
menubar = Menu(win)
settings_menu = Menu(menubar, tearoff=0)
settings_menu.add_command(label="🔁 Reset Password", command=reset_password_gui)
settings_menu.add_separator()
settings_menu.add_command(label="❌ Exit", command=win.quit)
menubar.add_cascade(label="⚙ Settings", menu=settings_menu)

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="📘 How to Use", command=lambda: messagebox.showinfo("Help", "Just copy anything, open ClipSync, and view!"))
help_menu.add_command(label="🍎 About ClipSync", command=lambda: messagebox.showinfo("About", "ClipSync v1.0 by Vivek\nSecure, offline clipboard manager.\nInspired by Apple design."))
menubar.add_cascade(label="❓ Help", menu=help_menu)
win.config(menu=menubar)

# ─ Left Panel ─
left_frame = Frame(win, width=340, bg="#ffffff", relief=GROOVE, bd=1)
left_frame.pack(side=LEFT, fill=Y, padx=8, pady=8)

# ─ Search Bar ─
search_var = StringVar()
search_entry = Entry(left_frame, textvariable=search_var, width=33, font=("Helvetica", 10), relief=FLAT, bg="#f1f1f1", fg="#444", insertbackground="#000")
search_entry.insert(0, "🔍 Search history...")
search_entry.pack(pady=12, padx=12)

def clear_placeholder(event):
    if search_entry.get() == "🔍 Search history...":
        search_entry.delete(0, END)

search_entry.bind("<FocusIn>", clear_placeholder)

# ─ Listbox + Scrollbar ─
listbox_frame = Frame(left_frame, bg="#ffffff")
listbox_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

scroll_y = Scrollbar(listbox_frame)
scroll_y.pack(side=RIGHT, fill=Y)

listbox = Listbox(listbox_frame, width=45, height=30, yscrollcommand=scroll_y.set,
                  bg="#ffffff", font=("Courier New", 10), bd=0, selectbackground="#d1eaff", activestyle="dotbox")
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scroll_y.config(command=listbox.yview)

# ─ Right Panel ─
right_frame = Frame(win, bg="#f6f7f9")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=8, pady=8)

detail_title = Label(right_frame, text="📋 Select a clip to view", font=("Helvetica", 14, "bold"), bg="#f6f7f9", fg="#222")
detail_title.pack(pady=(10, 2))

detail_info = Label(right_frame, text="", justify=LEFT, anchor="w", bg="#f6f7f9", fg="#444", font=("Helvetica", 10))
detail_info.pack(pady=2)

content_frame = Frame(right_frame, bg="#ffffff", bd=1, relief=SOLID)
content_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

text_area = Text(content_frame, wrap=WORD, font=("Helvetica", 11), bg="#ffffff", fg="#222", bd=0, padx=10, pady=10)
text_area.pack(side=LEFT, fill=BOTH, expand=True)

scroll = Scrollbar(content_frame, command=text_area.yview)
scroll.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroll.set)

def copy_selected():
    if not listbox.curselection():
        return
    index = listbox.curselection()[0]
    item_text = listbox.get(index)
    item_id = int(item_text.split('|')[0][1:].strip())
    selected = next((x for x in clipboard_data if x["id"] == item_id), None)
    if selected:
        try:
            import pyperclip
            pyperclip.copy(selected["text"])
            status_label.config(text="✅ Copied again to clipboard.")
        except:
            status_label.config(text="⚠️ pyperclip not installed.")

copy_button = Button(right_frame, text="📋 Copy Again", bg="#007AFF", fg="white", font=("Helvetica", 10, "bold"), padx=15, pady=5, bd=0, relief=FLAT, command=copy_selected)
copy_button.pack(pady=8)

status_label = Label(right_frame, text="🖥️ Local Mode • Secure", bg="#f6f7f9", fg="gray", font=("Helvetica", 9))
status_label.pack(side=BOTTOM, pady=8)

# ─ Logic ─
def update_list():
    listbox.delete(0, END)
    term = search_var.get().lower()
    for item in clipboard_data:
        if term in item['text'].lower() or term in item['source'].lower():
            preview = item['text'].replace("\n", " ")[:30] + ("..." if len(item['text']) > 30 else "")
            id_str = f"#{item['id']: <3}"
            time_str = item['time'][-8:]
            line = f"{id_str} | {preview: <30} | {time_str}"
            listbox.insert(END, line)

def on_select(event):
    if not listbox.curselection():
        return
    index = listbox.curselection()[0]
    item_text = listbox.get(index)
    item_id = int(item_text.split('|')[0][1:].strip())
    selected = next((x for x in clipboard_data if x["id"] == item_id), None)
    if selected:
        detail_title.config(text=f"📌 Clip #{selected['id']}")
        detail_info.config(text=f"🕒 {selected['time']} • 💻 {selected['source']}")
        text_area.delete(1.0, END)
        text_area.insert(END, selected["text"])

search_var.trace_add("write", lambda *args: update_list())
listbox.bind("<<ListboxSelect>>", on_select)

update_list()
win.mainloop()

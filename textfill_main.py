import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
from pynput import keyboard
import pyautogui
import json
import time
import platform
from pathlib import Path
import subprocess

shortcuts = {}
typed = ""
is_expanding = False

type_delay = 0.0
backspace_delay = 0.0
backspace_speed = 1
type_speed = 1

APP_NAME = "TextFill"


def get_save_path():
    system = platform.system()

    if system == "Windows":
        base = Path.home() / "AppData" / "Roaming" / APP_NAME
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        base = Path.home() / ".local" / "share" / APP_NAME

    base.mkdir(parents=True, exist_ok=True)
    return base / "text_fill_save_data.json"


SAVE_FILE = get_save_path()


def save_data():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(shortcuts, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Save failed:", e)


def load_data():
    global shortcuts
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            shortcuts = json.load(file)
    except Exception:
        shortcuts = {}


def open_accessibility_settings():
    if platform.system() != "Darwin":
        return

    subprocess.run([
        "open",
        "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
    ])


def ensure_permissions():
    if platform.system() != "Darwin":
        return

    messagebox.showinfo(
        "Permission Required",
        "Enable Accessibility for TextFillUI in System Settings if keyboard input does not work."
    )


def refresh_list():
    listbox.delete(0, tk.END)
    for key, value in shortcuts.items():
        listbox.insert(tk.END, f"{key} -> {value}")


def add_shortcut():
    key = simpledialog.askstring("Add Shortcut", "Shortcut:")
    if not key:
        return

    value = simpledialog.askstring("Add Shortcut", "Phrase:")
    if value is None:
        return

    shortcuts[key] = value
    save_data()
    refresh_list()


def remove_shortcut():
    selection = listbox.curselection()
    if not selection:
        return

    index = selection[0]
    key = list(shortcuts.keys())[index]

    del shortcuts[key]
    save_data()
    refresh_list()


def modify_shortcut():
    selection = listbox.curselection()
    if not selection:
        return

    index = selection[0]
    old_key = list(shortcuts.keys())[index]

    new_key = simpledialog.askstring("Modify Shortcut", "New Shortcut:", initialvalue=old_key)
    if not new_key:
        return

    new_value = simpledialog.askstring("Modify Shortcut", "New Phrase:", initialvalue=shortcuts[old_key])
    if new_value is None:
        return

    del shortcuts[old_key]
    shortcuts[new_key] = new_value

    save_data()
    refresh_list()


def clear_shortcuts():
    if not messagebox.askyesno("Clear Shortcuts", "Delete all shortcuts?"):
        return

    answer = simpledialog.askstring("Confirm", "Type 'clear all shortcuts' to confirm:")
    if answer is None or answer.lower() != "clear all shortcuts":
        return

    shortcuts.clear()
    save_data()
    refresh_list()


def show_settings():
    settings_panel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
    settings_panel.lift()
    settings_panel.update_idletasks()


def close_settings():
    settings_panel.place_forget()


def set_backspace_delay(val):
    global backspace_delay
    backspace_delay = float(val)


def set_type_delay(val):
    global type_delay
    type_delay = float(val)


def set_type_speed(val):
    global type_speed
    type_speed = float(val)


def set_backspace_speed(val):
    global backspace_speed
    backspace_speed = float(val)


def on_press(key):
    global typed, is_expanding

    if is_expanding:
        return

    if key == keyboard.Key.backspace:
        typed = typed[:-1]
        return

    try:
        char = key.char
    except:
        char = None

    if char:
        typed += char

        max_length = max((len(s) for s in shortcuts), default=20)
        typed = typed[-max_length:]

        for shortcut, replacement in list(shortcuts.items()):
            if typed.endswith(shortcut):
                is_expanding = True

                time.sleep(backspace_delay)

                pyautogui.PAUSE = 0
                for _ in range(len(shortcut)):
                    pyautogui.press("backspace", interval=(1.0 - backspace_speed))

                time.sleep(type_delay)
                pyautogui.write(replacement, interval=(1.0 - type_speed))

                typed = ""
                is_expanding = False
                break


def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


load_data()

root = tk.Tk()
root.title("TextFillUI")
root.geometry("600x400")

ensure_permissions()

title = tk.Label(root, text="TextFill", font=("Arial", 16, "bold"))
title.pack(pady=10)

listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add", command=add_shortcut).pack(side="left", padx=5)
tk.Button(button_frame, text="Modify", command=modify_shortcut).pack(side="left", padx=5)
tk.Button(button_frame, text="Remove", command=remove_shortcut).pack(side="left", padx=5)
tk.Button(button_frame, text="Clear", command=clear_shortcuts).pack(side="left", padx=5)
tk.Button(button_frame, text="Settings", command=show_settings).pack(side="left", padx=5)

settings_panel = tk.Frame(root, bd=3, relief="solid")

top_bar = tk.Frame(settings_panel)
top_bar.pack(fill="x")

tk.Label(top_bar, text="Settings", font=("Arial", 16, "bold")).pack(pady=5)

tk.Button(settings_panel, text="X", command=close_settings).place(
    relx=1.0, rely=0, anchor="ne", x=-5, y=5
)

settings_container = tk.Frame(settings_panel)
settings_container.pack(fill="both", expand=True, padx=7, pady=7)

scrollbar = tk.Scrollbar(settings_container)
scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(settings_container)
canvas.pack(side="left", fill="both", expand=True)

scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

settings_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=settings_frame, anchor="nw")


def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_inner_frame(event):
    canvas.itemconfig(canvas_window, width=event.width)


canvas.bind("<Configure>", resize_inner_frame)
settings_frame.bind("<Configure>", update_scroll_region)

tk.Label(settings_frame, text="Backspace Delay").pack()
tk.Scale(settings_frame, from_=0, to=1, resolution=0.05,
         command=set_backspace_delay).pack()

tk.Label(settings_frame, text="Type Delay").pack()
tk.Scale(settings_frame, from_=0, to=1, resolution=0.05,
         command=set_type_delay).pack()

tk.Label(settings_frame, text="Type Speed").pack()
tk.Scale(settings_frame, from_=0, to=1, resolution=0.05,
         command=set_type_speed).pack()

tk.Label(settings_frame, text="Delete Speed").pack()
tk.Scale(settings_frame, from_=0, to=1, resolution=0.05,
         command=set_backspace_speed).pack()

threading.Thread(target=start_listener, daemon=True).start()

refresh_list()
root.mainloop()
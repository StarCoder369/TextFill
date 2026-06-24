import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
from pynput import keyboard
import pyautogui
import json
import os
import time

shortcuts = {}
typed = ""
is_expanding = False

type_delay = 0.0
backspace_delay = 0.0
backspace_speed = 1
type_speed = 1


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(SCRIPT_DIR, "text_fill_save_data.json")

def save_data():
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(shortcuts, file, indent=4)


def load_data():
    global shortcuts

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            shortcuts = json.load(file)
    except:
        shortcuts = {}


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
    
    answer = simpledialog.askstring("Please type 'clear all shortcuts' to clear.", "Type here: ")

    if answer is None:
        return
    
    if not answer.lower() == "clear all shortcuts":
        return

    shortcuts.clear()

    save_data()
    refresh_list()

def show_settings():
    settings_panel.place(relx = 0.5, rely = 0.5, relwidth = 0.8, relheight = 0.8, anchor="center")
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
                for i in range(len(shortcut)):
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
root.title("Text Fill")
root.geometry("600x400")

title = tk.Label(root, text="Text Fill", font=("Arial", 16, "bold"))
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

settings_title = tk.Label(top_bar, text="Settings", font=("Arial", 16, "bold"))
settings_title.pack(pady=5)

settings_button = tk.Button(settings_panel, text="X", command=close_settings)
settings_button.place(relx=1.0, rely=0, anchor="ne", x=-5, y=5.2)

settings_container = tk.Frame(settings_panel)
settings_container.pack(fill="both", expand=True, padx=7.5, pady=7.5)

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
    
def on_mousewheel(event):
    canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

settings_panel.bind_all("<MouseWheel>", on_mousewheel)

settings_frame.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", resize_inner_frame)
canvas.bind_all("<MouseWheel>", on_mousewheel)

backspace_delay_label = tk.Label(settings_frame, text="Backspace Delay")
backspace_delay_label.pack(side="top", padx=5, pady=(5,0))

backspace_delay_slider = tk.Scale(settings_frame, from_=0, to=1, length=100, orient="horizontal", tickinterval=1, resolution=0.05, command=set_backspace_delay)
backspace_delay_slider.set(0.1)
set_backspace_delay(0.1)
backspace_delay_slider.pack(side="top", padx=5, pady=(0,5))

type_delay_label = tk.Label(settings_frame, text="Type Delay")
type_delay_label.pack(side="top", padx=5, pady=(5,0))

type_delay_slider = tk.Scale(settings_frame, from_=0, to=1, length=100, orient="horizontal", tickinterval=1, resolution=0.05, command=set_type_delay)
type_delay_slider.set(0)
set_type_delay(0)
type_delay_slider.pack(side="top", padx=5, pady=(0,5))

type_speed_label = tk.Label(settings_frame, text="Type Speed")
type_speed_label.pack(side="top", padx=5, pady=(5,0))

type_speed_slider = tk.Scale(settings_frame, from_=0, to=1, length=100, orient="horizontal", tickinterval=1, resolution=0.05, command=set_type_speed)
type_speed_slider.set(0.9)
set_type_speed(0.9)
type_speed_slider.pack(side="top", padx=5, pady=(0,5))

backspace_speed_label = tk.Label(settings_frame, text="Delete Speed")
backspace_speed_label.pack(side="top", padx=5, pady=(5,0))

backspace_speed_slider = tk.Scale(settings_frame, from_=0, to=1, length=100, orient="horizontal", tickinterval=1, resolution=0.05, command=set_backspace_speed)
backspace_speed_slider.set(0.9)
set_backspace_speed(0.9)
backspace_speed_slider.pack(side="top", padx=5, pady=(0,5))

threading.Thread(target=start_listener, daemon=True).start()


refresh_list()

root.mainloop()
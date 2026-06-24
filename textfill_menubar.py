import rumps
import threading
from pynput import keyboard
import pyautogui
import json
import os
import time
import AppKit

shortcuts = {}
typed = ""
is_expanding = False

type_delay = 0.0
backspace_delay = 0.0
backspace_speed = 1
type_speed = 1

from threading import Event
is_replacing = Event()
is_replacing.clear()

listener = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(SCRIPT_DIR, "menu_text_fill_save_data.json")


def save_data():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(shortcuts, f, indent=4)


def load_data():
    global shortcuts
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            shortcuts = json.load(f)
    except:
        shortcuts = {}


def expand_if_needed():
    global typed, is_expanding, is_replacing

    if is_expanding:
        return
    
    if not is_replacing.is_set():
        return

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


def on_press(key):
    global typed, is_expanding

    if not is_replacing.is_set():
        return

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

        max_len = max((len(k) for k in shortcuts), default=50)
        typed = typed[-max_len:]

        expand_if_needed()


def start_listener():
    global listener, listener_thread
    if listener is not None:
        return

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    listener_thread = threading.Thread(target=lambda: listener.join(), daemon=True)
    listener_thread.start()


def stop_listener():
    global listener

    if listener is not None:
        try:
            listener.stop()
        except:
            pass

        time.sleep(0.2)

        listener = None

def hard_shutdown():
    stop_listener()
    time.sleep(0.3)
    os._exit(0)

def top_alert(title, message):
    import AppKit
    AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    rumps.alert(title, message)

def top_window(title, message):
    AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)

    return rumps.Window(
        title=title,
        message=message,
    ).run()

class MyMenuApp(rumps.App):

    def update_status(self):
        if is_replacing.is_set():
            self.status_item.title = "Status: Running"
        else:
            self.status_item.title = "Status: Stopped"
    def __init__(self):
        super(MyMenuApp, self).__init__(
            name="TextFill",
            title="Text Fill",
            quit_button=None
        )

        self.status_item = rumps.MenuItem("Status: Stopped")

        self.menu = [
            self.status_item,
            None,
            "Add Shortcut",
            "Remove Shortcut",
            "Clear All",
            None,
            "Show Shortcuts",
            None,
            "Start Replacer",
            "Stop Replacer",
            None,
            "Quit"
        ]
        self.update_status()

    @rumps.clicked("Add Shortcut")
    def add_shortcut(self, _):
        key = top_window(
            title="Add Shortcut",
            message="Shortcut key:",
        ).text

        if not key:
            return

        value = top_window(
            title="Add Shortcut",
            message="Replacement text:",
        ).text

        if not value:
            return

        shortcuts[key] = value
        save_data()

        rumps.notification("TextFill", "Saved", f"{key} → {value}")

    @rumps.clicked("Remove Shortcut")
    def remove_shortcut(self, _):
        key = top_window(
            title="Remove Shortcut",
            message="Enter shortcut key:",
        ).text

        if key in shortcuts:
            del shortcuts[key]
            save_data()
            rumps.notification("TextFill", "Removed", key)

    @rumps.clicked("Clear All")
    def clear_all(self, _):
        shortcuts.clear()
        save_data()
        rumps.notification("TextFill", "Cleared", "All shortcuts removed")

    @rumps.clicked("Show Shortcuts")
    def show_shortcuts(self, _):
        if not shortcuts:
            top_alert("No shortcuts set", "Set shortcuts using 'Add Shortcut'")
            return

        text = "\n".join([f"{k} → {v}" for k, v in shortcuts.items()])
        top_alert("These are your current shortcuts", text)

    @rumps.clicked("Start Replacer")
    def start_replacer(self, _):
        is_replacing.set()
        self.update_status()
        rumps.notification("TextFill", "Running", "Replacer enabled")

    @rumps.clicked("Stop Replacer")
    def stop_replacer(self, _):
        is_replacing.clear()
        self.update_status()
        rumps.notification("TextFill", "Stopped", "Replacer disabled")

    @rumps.clicked("Quit")
    def quit_app(self, _):
        hard_shutdown()


if __name__ == "__main__":
    load_data()
    start_listener()
    MyMenuApp().run()
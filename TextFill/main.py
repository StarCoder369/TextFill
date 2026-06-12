import threading
from pynput import keyboard
import pyautogui
import json
import os

shortcuts = {
}

typed = ""
is_expanding = False

print("Running text fill...")
print("ESC to quit")

def mode_manager():
    while True:
        mode = input("Select a mode below if you want to modify shortcuts. [1-6]\nWhat do you want to do?\n1. Add Shortcut | 2. Remove Shortcut | 3. Clear Shortcuts | 4. Modify Shortcut | 5. Show Shortcuts | 6. Settings\n")

        if mode == "1":
            add_shortcuts()
        elif mode == "2":
            remove_shortcuts()
        elif mode == "3":
            clear_shortcuts()
        elif mode == "4":
            modify_shortcuts()
        elif mode == "5":
            show_shortcuts()
        elif mode == "6":
            #Settings
            pass
        else:
            return


def save_data():
    global shortcuts
    with open("text_fill_save_data.json", "w", encoding="utf-8") as file:
        json.dump(shortcuts, file, indent=4)
    
    print("Data saved")

def load_data():
    global shortcuts

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(script_dir, "text_fill_save_data.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            loaded_state = json.load(file)
            shortcuts = loaded_state
            print("Data loaded") 
    except (FileNotFoundError, json.JSONDecodeError):
        print("No save data found")


def add_shortcuts():
    global shortcuts

    print("Add shortcuts mode")

    while True:
        shortcut = input("Shortcut: ")
        phrase = input("Phrase: ")

        shortcuts[shortcut] = phrase
        print(f"Added: {shortcut} -> {phrase}")
        save_data()

        add_another = input("Do you want to add another shortcut? (Y/N): ")

        if add_another.upper() != "Y":
            break


def remove_shortcuts():
    global shortcuts

    print("Remove shortcuts mode\n")

    keys = list(shortcuts.keys())
    values = list(shortcuts.values())

    for i, (key, value) in enumerate(shortcuts.items(), start=1):
        print(f"{i}. {key} -> {value}")

    while True:
        shortcut_to_remove = int(input(f"\nChoose shortcut (1 - {len(keys)}): "))

        if shortcut_to_remove < 0 or shortcut_to_remove > len(keys):
            print("Invalid index")
            return

        del shortcuts[keys[shortcut_to_remove-1]]
        print(f"Removed Shortcut: {keys[shortcut_to_remove-1]}, Removed Value: {values[shortcut_to_remove-1]}")
        save_data()

        remove_another = input("Do you want to remove another shortcut? (Y/N): ")

        if remove_another.upper() != "Y":
            break


def clear_shortcuts():
    global shortcuts

    print("Clear Shortcuts mode")
    print("----WARNING: THIS ACTION CANNOT BE REVERSED----")

    continue_or_not = input("Are you sure? (Y/N): ")

    if continue_or_not.upper() == "Y":
        confirm = input("Type 'clear all shortcuts' to confirm: ")
        if confirm.lower() == "clear all shortcuts":
            shortcuts.clear()
            print("All shortcuts have been cleared")
            save_data()
        else:
            print("Aborting...")
    else:
        print("Aborting...")


def modify_shortcuts():
    global shortcuts

    print("Modify Shortcuts mode")

    keys = list(shortcuts.keys())

    for i, (key, value) in enumerate(shortcuts.items(), start=1):
        print(f"{i}. {key} -> {value}")

    modify_index = int(input(f"\nChoose shortcut (1 - {len(keys)}): "))

    if modify_index < 0 or modify_index > len(keys):
        print("Invalid index")
        return

    old_key = keys[modify_index-1]

    new_key = input("New key: ")
    new_value = input("New value: ")

    del shortcuts[old_key]
    shortcuts[new_key] = new_value

    print("\nSuccessfully modified")
    save_data()


def show_shortcuts():
    print("\nBelow are your current shortcuts: \n")
    for i, (key, value) in enumerate(shortcuts.items(), start=1):
        print(f"{i}. {key} -> {value}")

def on_press(key):
    global typed, is_expanding, shortcuts

    if key == keyboard.Key.esc:
        return False

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
        typed = typed[-20:]

        for shortcut, replacement in shortcuts.items():
            if typed.endswith(shortcut):
                is_expanding = True

                pyautogui.write("\b" * len(shortcut))

                pyautogui.write(replacement)

                typed = ""
                is_expanding = False
                break


load_data()

threading.Thread(target=mode_manager, daemon=True).start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

#
# TextFill

A Python text auto fill tool that lets users create shortcuts that will automatically fill in with pre-defined text to make tasks more efficient.

[Screenshot]

## Demo

**Demo Video:** [Link]

---

## Quick Start

### UI Version (Windows and Mac)

1. Download the files from the demo link (Github Release).
2. Launch:

   - `TextFill.exe` on Windows
   - `TextFill.app` on Mac

### Menu Bar Version (Only Mac)

1. Download the files from the demo link (Github Release).
2. Launch: `TextFill.app`

---

## Features

* Create and manage reusable text shortcuts.
* Easily add, remove, and modify shortcuts.
* Cross-platform GUI app for Windows and Mac.
* Streamlined Mac menu bar version for fast access.

---

## Run from Source

Use this section if you want to run or modify the project directly from the code.

---

## Requirements

- Python 3.11 or higher installed
- pip (included with Python)
- Supported OS:
  - Windows 10/11 (GUI version)
  - macOS (GUI and menu bar versions)

---

## Step 1: Download the project

### Option 1: Clone the repository

```
git clone <repo-url>
cd TextFill
```

### Option 2: Download ZIP

- Download the project as ZIP from GitHub
- Extract it
- Open the extracted folder in a terminal

---

## Step 2: Install dependencies

### GUI version (Windows + macOS)

```
pip install -r main_requirements.txt
```

### macOS Menu Bar version

```
pip install -r menu_bar_requirements.txt
```

---

## Step 3: Run the application

### GUI version (Windows + macOS)

```
python textfill_main.py
```

### macOS Menu Bar version

```
python textfill_menubar.py
```

---

## Notes

- Run all commands from the project root directory
- If `python` does not work, try `python3`
- If installation fails, try updating pip:

```
python -m pip install --upgrade pip
```
## How It Works

TextFill stores created text shortcuts and provides quick access to them through either a normal UI or a mac menu bar application. Users can create shortcuts, that automatically replace with anything they want.

The project includes both a Windows+Mac GUI version and a Mac menu bar version.

The GUI version includes a settings menu, that provides additional customizability, while the Mac version is more of a streamlined version.

**Usage Example**
If a user creates a shortcut with the key '/email', and the phrase, 'example@gmail.com', then wherever they type '/email', it will automatically fill in with 'example@gmail.com'.

---

## Project Structure

```
TextFill/
├── textfill_main.py
├── textfill_menubar.py
├── main_requirements.txt
├── menu_bar_requirements.txt
└── README.md
```

---

## Important Info
There are some things you have to do to make sure the device allows the app to work.
### Mac steps

---

## Additional Info

This project uses the following open-source libraries:

* PyAutoGUI
* pynput
* pyperclip
* rumps
* pyobjc

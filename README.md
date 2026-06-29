# TextFill

A Python text auto fill tool that lets users create shortcuts that will automatically fill in with pre-defined text to make tasks more efficient.

The below picture shows screenshots of the streamlined menu bar version and the ui version.

<img width="133" height="278" alt="Screenshot 2026-06-28 at 6 06 59 PM" src="https://github.com/user-attachments/assets/b7cb880b-9613-4d1b-98b1-988c3d3cbd7e" />
<img width="450" height="319" alt="Screenshot 2026-06-28 at 8 46 55 PM" src="https://github.com/user-attachments/assets/267b0a21-746a-4133-b014-108550d2651a" />

## Demo
Below are the links for the different versions.

(**Check [Quick Start](#quick-start) for more instructions**)

(The Mac Menubar version is recommended for users who want a streamlined version and are on Mac)

### Textfill UI version (Windows + Mac)

 - [Mac + Windows Release - UI](https://github.com/StarCoder369/TextFill/releases/tag/v1.0.0-ui)

Make sure to download the correct version depending on your device. Download the `textfill.ui.windows.zip` version if you are on windows, and download the `textfill.ui.mac.zip` version if you are on mac.

### Textfill Menubar Version (Mac only)
 - [Mac Release - Menubar](https://github.com/StarCoder369/TextFill/releases/tag/v1.0.0-menubar)

Assets other than .zip files are not part of the app or executable, and can be ignored. They have been automatically added by GitHub Releases.

---

## Quick Start

### UI Version (Windows and Mac)

1. Download the files from the demo link (Github Release).
2. Launch:

   - `TextFill_UI.exe` on Windows
   - `TextFill_UI.app` on Mac

### Menu Bar Version (Only Mac)

1. Download the files from the demo link (Github Release).
2. Launch: `TextFill_MenuBar.app`

**Please check the [Important Info](#important-info) section if you encounter any problems running the application**

---

## Features

* Create and manage reusable text shortcuts.
* Easily add, remove, and modify shortcuts.
* Cross-platform UI app for Windows and Mac.
* Streamlined Mac menu bar version for fast access.
* Settings menu for further customization in the UI version.

---

## Run from Source

Use this section if you want to run or modify the project directly from the code.

---

## Requirements

- Python 3.10 or higher recommended, Python 3 and higher should work fine.
- pip (included with Python)
- Supported OS:
  - Windows 10/11 (UI version)
  - macOS 11 recommended(UI and menu bar versions)

---

## Step 1: Download the project

### Option 1: Clone the repository

```
git clone <https://github.com/StarCoder369/TextFill>
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

The project includes both a Windows+Mac UI version and a Mac menu bar version.

The UI version includes a settings menu, that provides additional customizability, while the Mac version is more of a streamlined version.

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

# Important Info

There are some things you have to do to make sure the device allows the app to work. If you are on Mac, follow the Mac instructions. If you are on Windows, follow the Windows instructions.

## Mac instructions

When you double-click the app for the first time, macOS may show a warning that it “cannot be opened because it was not downloaded from the App Store” or that the developer cannot be verified.

If this happens:

1. Click **Cancel**
2. Open **System Settings**
3. Go to **Privacy & Security**
4. Scroll down to the **Security** section
5. You should see a message about the blocked app (`TextFill_Menubar` or `TextFill_UI`)
6. Click **Open Anyway**
7. Confirm by clicking **Open**

---

After the app launches, Mac will likely request permissions for keyboard input features used by TextFill. (Even if it doesn't, you'll most likely have to follow the steps below)

If you see a prompt for **Input Monitoring** or **Accessibility**, follow the steps below.

### Enable Input Monitoring

1. Click **Open System Settings** in the prompt (or go to System Settings manually)
2. Go to **Privacy & Security**
3. Click **Input Monitoring**
4. Enable **TextFill_Menubar** (or TextFill_UI)
5. Authenticate with Touch ID or password if required

---

### Enable Accessibility (required)

1. Stay in **Privacy & Security**
2. Scroll to **Accessibility**
3. Enable **TextFill_Menubar** (and/or TextFill_UI)
4. Authenticate if required

---

### Optional permissions

1. Go back to **Privacy & Security**
2. Open **Notifications**
3. Enable **TextFill** if you want system notifications

---

### Mac Notes

- Both Input Monitoring and Accessibility are required for text replacement to work
- The app runs in the Mac menu bar, and has no visible windows.
- Shortcuts are stored locally and persist between launches
- If replacements do not work, re-check Accessibility and Input Monitoring permissions

---

## Windows instructions

When you open the `.exe` file for the first time, Windows may show a SmartScreen warning saying “Windows protected your PC”.

If this happens:

1. Click **More info**
2. Click **Run anyway**

---

After the app opens, Windows may require permission for keyboard access features used by TextFill.

If the app does not function correctly (shortcuts do not trigger), follow these steps:

### Enable required permissions

1. Open **Settings**
2. Go to **Privacy & security**
3. Scroll down and open **Input**
4. Enable access for apps that require keyboard input monitoring (if available on your Windows version)

---

### If antivirus or Defender blocks the app

Sometimes Windows Defender may restrict `.exe` files built with PyInstaller:

1. Open **Windows Security**
2. Go to **Virus & threat protection**
3. Open **Protection history**
4. Find the blocked TextFill entry
5. Click **Allow on device**

---

### Windows Notes

- No installation is required - the app runs directly from the `.exe`
- Shortcuts are saved locally and persist between launches
- If nothing triggers, ensure the app is running with normal user permissions (not blocked by antivirus or system protection)

## How it Works
I used Python to create TextFill. The UI version uses a package called Tkinter for the UI, and the menu bar version uses Rumps and pyobjc(AppKit) for the UI on the menu bar. Both use PyAutoGUI and pynput for the main text fill functionality, and they both have been packaged using PyInstaller.

## Additional Info

This project mainly uses the following open-source libraries:

* PyAutoGUI
* pynput
* rumps
* pyobjc

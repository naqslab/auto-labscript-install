import pygetwindow as gw
import pyautogui
import time
import cv2

# target_string = "the labscript suite"
# filtered_windows = []
# script_order = ['runmanager', 'blacs', 'lyse', 'runviewer']

# for window in all_windows:
#     if target_string in window.title:
#         filtered_windows.append(window)

# for window in filtered_windows:
#     print(f"Found window: {window.title}")
#     if window.isMinimized:
#         window.restore()
#     window.activate()

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

script_order = ['runmanager', 'blacs', 'lyse', 'runviewer']
target_string = "the labscript suite"
button_map = {
    'runmanager': ['runmanager-engage'],
    'blacs': [],
    'lyse': [],
    'runviewer': []
}

def find_labscript_windows():
    all_windows = gw.getAllWindows()
    matching = {}
    for window in all_windows:
        title = window.title.lower()
        if target_string in title:
            for app in script_order:
                if app in title:
                    matching[app] = window
    return matching

def process_app(app_name, window):
    print(f"\nActivating {app_name.title()}")

    if window.isMinimized:
        window.restore()
    window.activate()
    time.sleep(1.0)

    for button in button_map.get(app_name, []):
        print(f"Attempting to click '{button}'")
        if not click_button(button):
            print(f"Failed to find or click '{button}'")
        else:
            time.sleep(0.5)

def click_button(button_text, confidence=0.8, max_attempts=3):
    image_path = f"imgs/{button_text.replace(' ', '_').lower()}.png"
    for attempt in range(max_attempts):
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            print(f"Clicked '{button_text}' at {location}")
            return True
        time.sleep(0.5)
    return False

def main():
    print("Locating labscript suite windows")
    lab_windows = find_labscript_windows()

    for app in script_order:
        if app in lab_windows:
            process_app(app, lab_windows[app])
        else:
            print(f"Window for '{app}' not found!")

    print("\nAutomation pipeline complete.")

if __name__ == "__main__":
    main()

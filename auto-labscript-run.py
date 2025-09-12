import sys

if sys.platform == "win32":
    import pygetwindow as gw
elif sys.platform == "linux":
    import pywinctl as pwc
import pyautogui
import time
import os
import configparser
import subprocess
from labscript_utils import labconfig


lc = labconfig.LabConfig()

# labconfig_path = labconfig.LabConfig

app_saved_configs_dir = lc.get("DEFAULT", "app_saved_configs")
apparatus = "example_apparatus"


def format_img_path(img_name):
    return os.path.join("imgs", f"{img_name.replace(' ', '_').lower()}.png")


def locate_image(img_path, confidence=0.8):
    try:
        return pyautogui.locateCenterOnScreen(img_path, confidence=confidence)
    except Exception as e:
        print(f"Error locating image '{img_path}': {e}")
        return None


def tick_box(unticked_img, ticked_img, confidence=0.8, max_attempts=3):
    """Only ticks box if already unticked

    Args:
        unticked_img (str): _description_
        ticked_img (str): _description_
        confidence (float, optional): _description_. Defaults to 0.8.
        max_attempts (int, optional): _description_. Defaults to 3.

    Returns:
        bool: True if checkbox was found, False if not
    """
    unticked_path = format_img_path(unticked_img)
    ticked_path = format_img_path(ticked_img)

    for attempt in range(max_attempts):
        tick_loc = locate_image(ticked_path, confidence)
        if tick_loc:
            print("Box already ticked")
            return True

        untick_loc = locate_image(unticked_path, confidence)
        if untick_loc:
            print("Ticking box")
            pyautogui.click(untick_loc)
            return True

        time.sleep(0.5)

    print("Tickbox not found.")
    return False


def fill_empty_field(
    empty_img, filled_img, text_to_type, confidence=0.8, max_attempts=3
):
    empty_path = format_img_path(empty_img)
    filled_path = format_img_path(filled_img)

    for attempt in range(max_attempts):
        filled_loc = locate_image(filled_path, confidence)
        if filled_loc:
            print("Field already filled")
            return True

        empty_loc = locate_image(empty_path, confidence)
        if empty_loc:
            print(f"Filling field with {text_to_type}")
            pyautogui.write(text_to_type)
            return True

        time.sleep(0.5)

    print("Field not found.")
    return False


def click_button(button_text, confidence=0.8, max_attempts=3):
    image_path = format_img_path(button_text)

    for _ in range(max_attempts):
        confidence -= 0.1
        loc = locate_image(image_path, confidence)
        if loc:
            pyautogui.click(loc)
            print(f"Clicked '{button_text}' at {loc}")
            return True
        time.sleep(0.5)

    print(f"Failed to locate button: {button_text}")
    return False


def activate_window(window):
    if window.isMinimized:
        window.restore()
    window.activate()
    window.maximize()  # test?
    time.sleep(1.5)


def find_labscript_windows(target_string, script_order):

    if sys.platform == "win32":
        all_windows = gw.getAllWindows()
    elif sys.platform == "linux":
        all_windows = pwc.getAllWindows()
    matching = {}
    for window in all_windows:
        title = window.title.lower()
        if target_string in title:
            for app in script_order:
                if app in title:
                    matching[app] = window
    return matching


def get_config(inipath):
    config = configparser.ConfigParser()
    config.read(inipath)
    print(config.sections())
    return config


def runmanager_routine():

    print("[Runmanager] Executing routine")
    time.sleep(0.5)

    config_override = configparser.ConfigParser()
    config_override["runmanager_state"] = {
        "send_to_runviewer": "True",
        "send_to_blacs": "True",
    }

    time.sleep(0.5)

    pyautogui.press("f5")  # engage keyboard shortcut


def blacs_routine():
    print("[Blacs] Executing routine")
    # if tick_box('blacs-lyse-server-empty', 'blacs-lyse-server-local'):
    #     pyautogui.write('127.0.0.1')
    # fill_empty_field(
    #     empty_img="blacs-lyse-server-empty",
    #     filled_img="blacs-lyse-server-local",
    #     text_to_type="127.0.0.1",
    # )
    # assert blacs sent a shot??? maybe that's going to be timing based screenshot matching aka bad


def lyse_routine():
    print("[Lyse] Executing routine")
    # activate_window('1 - example_analysis_script.py')
    pass


def runviewer_routine():
    print("[Runviewer] Executing routine")
    tick_box(
        "runviewer-checkbox-withtext-unticked", "runviewer-checkbox-withtext-ticked"
    )


ROUTINES = {
    "runmanager": runmanager_routine,
    "blacs": blacs_routine,
    "lyse": lyse_routine,
    "runviewer": runviewer_routine,
}


def main():

    print("Locating labscript suite windows")
    windows = find_labscript_windows(TARGET_STRING, SCRIPT_ORDER)

    for app in SCRIPT_ORDER:
        win = windows.get(app)
        if not win:
            print(f"[{app.title()}] Window not found!")
            continue

        print(f"\n[{app.title()}] Activating")
        activate_window(win)
        routine = ROUTINES.get(app)
        if routine:
            routine()
            time.sleep(3) # wait for routine to finish - will try different time values
        else:
            print(f"[{app.title()}] No routine defined.")

    print("\n=== Auto labscript complete ===")


# SCRIPT_ORDER = ["runmanager", "blacs", "lyse", "runviewer"]
SCRIPT_ORDER = ["runmanager"]
TARGET_STRING = "the labscript suite"

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    main()

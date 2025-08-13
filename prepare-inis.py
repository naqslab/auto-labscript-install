import os
import configparser
from labscript_utils import labconfig
import sys


def update_labscript_ini(app_name, apparatus_name, updates):
    """
    Update settings in a labscript-suite application .ini file.

    Parameters
    ----------
    app_name : str
        Name of the app (e.g. 'runmanager', 'blacs', 'lyse', 'runviewer').
    apparatus_name : str
        Name of the apparatus (e.g. 'example_apparatus').
    updates : dict
        Nested dict of {section: {option: value}} to update.
    """
    lc = labconfig.LabConfig()
    app_saved_configs_dir = lc.get("DEFAULT", "app_saved_configs")

    ini_path = os.path.join(app_saved_configs_dir, app_name, f"{app_name}.ini")
    if not os.path.exists(ini_path):
        raise FileNotFoundError(f"Could not find {ini_path}")

    print(f"[prepare-inis] - Updating {ini_path}")

    config = configparser.ConfigParser()
    config.read(ini_path)

    for section, opts in updates.items():
        if section not in config:
            config[section] = {}
        for key, value in opts.items():
            config[section][key] = str(value)

    with open(ini_path, "w") as f:
        config.write(f)

    print(f"[prepare-inis] - Updated settings in {app_name}.ini successfully")


update_labscript_ini(
    app_name="runmanager",
    apparatus_name="example_apparatus",
    updates={"runmanager_state": {"send_to_runviewer": True, "send_to_blacs": True}},
)

script = os.path.abspath("example_analysis_script.py")
if sys.platform == "win32":
    print("[prepare-inis] - double backslash for Windows path")
    script = script.replace("\\", "\\\\")  # double backslashes in the string

singleshot_value = f"[('{script}', True)]"

update_labscript_ini(
    app_name="lyse",
    apparatus_name="example_apparatus",
    updates={"lyse_state": {"singleshot": singleshot_value}},
)

update_labscript_ini(
    app_name="runviewer",
    apparatus_name="example_apparatus",
    updates={"runviewer_state": {"pseudoclock_clock_line": "True"}},
)
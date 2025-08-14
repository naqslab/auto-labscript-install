import os
import configparser
from labscript_utils import labconfig
import sys


lc = labconfig.LabConfig()
app_saved_configs_dir = lc.get("DEFAULT", "app_saved_configs")
userlib_dir = lc.get("DEFAULT", "userlib")
labscriptlib_dir = lc.get("DEFAULT", "labscriptlib")

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

example_experiment_file = os.path.join(labscriptlib_dir, "example_apparatus", "example_experiment.py")
example_analysis_script = os.path.abspath(os.path.join("example_files", "example_analysis_script.py")) # doesn't come with labscript
if sys.platform == "win32":
    print("[prepare-inis] - double backslash for Windows path")
    example_experiment_file = script.replace("\\", "\\\\")  # double backslashes in the string
    example_analysis_script = script.replace("\\", "\\\\")  # double backslashes in the string

current_labscript_file_value = f"[('{example_experiment_file}', True)]"
singleshot_value = f"[('{example_analysis_script}', True)]"

update_labscript_ini(
    app_name="runmanager",
    apparatus_name="example_apparatus",
    updates={"runmanager_state": {
                "send_to_runviewer": True, 
                "send_to_blacs": True,
                "current_labscript_file": current_labscript_file_value
}},
)

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


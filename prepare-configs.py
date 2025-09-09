import os
import configparser
from labscript_utils import labconfig
import sys
import h5py
import glob
import ast


lc = labconfig.LabConfig()
app_saved_configs_dir = lc.get("DEFAULT", "app_saved_configs")
userlib_dir = lc.get("DEFAULT", "userlib")
labscriptlib_dir = lc.get("DEFAULT", "labscriptlib")

def update_labscript_ini(app_name, updates):
    """
    Update settings in a labscript-suite application .ini file.

    Parameters
    ----------
    app_name : str
        Name of the app (e.g. 'runmanager', 'blacs', 'lyse', 'runviewer').
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
    example_experiment_file = example_experiment_file.replace("\\", "\\\\")  # double backslashes in the string
    example_analysis_script = example_analysis_script.replace("\\", "\\\\")  # double backslashes in the string

current_labscript_file_value = f"[('{example_experiment_file}', True)]"
singleshot_value = f"[('{example_analysis_script}', True)]"

# Update configs in [runmanager, blacs, lyse, runviewer] order

update_labscript_ini(
    app_name="runmanager",
    updates={"runmanager_state": {
                "send_to_runviewer": True, 
                "send_to_blacs": True,
                "current_labscript_file": current_labscript_file_value
}},
)

h5file_path = glob.glob(os.path.join(app_saved_configs_dir, 'blacs', '*.h5'))[0]

with h5py.File(h5file_path, 'r+') as hdf5_file:
    print(hdf5_file.keys())
    dataset = hdf5_file['front_panel/_notebook_data']
    
    # this returns as a str, but we need to reassign a field's value
    server_attrs = dataset.attrs['analysis_data']
    res = ast.literal_eval(server_attrs)
    
    print(res, type(res))
    
    res['server'] = '127.0.0.1'
    res['send_to_server'] = False
    dataset.attrs['analysis_data'] = str(res)
    
update_labscript_ini(
    app_name="lyse",
    updates={"lyse_state": {"singleshot": singleshot_value}},
)

update_labscript_ini(
    app_name="runviewer",
    updates={"runviewer_state": {"pseudoclock_clock_line": "True"}},
)

import subprocess
import time
import sys

print("[Main Script] - Preparing config files")
subprocess.run(["python", "prepare-inis.py"])

print("[Main Script] - Launching launch.py")
# Ensure windows stay open via detached process and new session
if sys.platform == 'win32':
    launch_process = subprocess.Popen(
        ["python", "launcher.py"],
        creationflags=subprocess.DETACHED_PROCESS,
        start_new_session=True,
    )
elif sys.platform == 'linux':
    launch_process = subprocess.Popen(
        ["python", "launcher.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
)

time.sleep(8)  # wait for windows to appear

print("[Main Script] - Starting GUI automation")
subprocess.run(["python", "auto-labscript-run.py"])

print("[Main Script] - GUI automation finished.")

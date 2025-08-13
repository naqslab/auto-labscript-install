import subprocess
import time

print("[Main Script] - Launching launch.py")
# Ensure windows stay open via detached process and new session
launch_process = subprocess.Popen(
    ["python", "launch.py"],
    creationflags=subprocess.DETACHED_PROCESS,
    start_new_session=True,
)

time.sleep(8)  # wait for windows to appear

print("[Main Script] - Starting GUI automation")
subprocess.run(["python", "auto-labscript-run.py"])

print("[Main Script] - GUI automation finished.")

import subprocess
import time

"""Launch labscript gui apps via python subprocess"""

commands = [
    "runmanager",
    "blacs",
    "lyse",
    "runviewer",
]

processes = []
print("[launcher] - Starting subprocesses...")
for cmd in commands:
    process = subprocess.Popen(cmd)
    processes.append(process)

print("[launcher] - All subprocesses launched. Waiting for them to complete...")
for process in processes:
    process.wait()

print("[launcher] - All subprocesses finished.")

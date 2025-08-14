

import pywinctl as pwc
#import subproccess

windows = pwc.getWindowsWithTitle('the labscript suite', condition=pwc.Re.CONTAINS, flags=pwc.Re.IGNORECASE)

if windows:
    for w in windows:
        w.activate()

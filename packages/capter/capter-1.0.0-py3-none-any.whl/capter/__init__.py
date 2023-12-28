import os
import subprocess
import random
import string
from pathlib import Path

import pwd

USER_NAME = pwd.getpwuid(os.getuid()).pw_name
DEFAULT_FILE_NAME = "output.png"
file = f"/Users/deepakdewani1/Documents/screenshots/{DEFAULT_FILE_NAME}"
screenshot_file = Path(file)
if screenshot_file.is_file():
    random_str = "".join(
        random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5)
    )
    file_name = f"output-{random_str}.png"
    file = f"/Users/deepakdewani1/Documents/screenshots/{file_name}"
SCREENSHOT_CMD = f"screenshot -w on_screen_only Terminal -f {file}"
COPY_CMD = ["osascript", "-e"]


def run():
    Path(f"/Users/{USER_NAME}/Documents/screenshots").mkdir(parents=True, exist_ok=True)
    clipboard = (
        'set the clipboard to (read (POSIX file "/Users/%s/Documents/screenshots/output.png") as {«class PNGf»})'
        % (USER_NAME)
    )
    COPY_CMD.append(clipboard)
    os.system(SCREENSHOT_CMD)
    subprocess.run(COPY_CMD)

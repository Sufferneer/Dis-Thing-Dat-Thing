import sys

import cx_Freeze

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executable = [cx_Freeze.Executable("game.py", base = base, icon = "game.ico")]

cx_Freeze.setup(
    name = "Dis Thing Dat Thing with CCC",
    version = "0.1",
    author = "Sufferneer",
    description = "A biology vocabulary educational game.",
    options = {
        "build_exe": {
            "packages": [
                "json",
                "os",
                "string",
                "sys",
                "math",
                "random",
                "pygame"
            ],
            "include_files": ["assets/"]
        }
    },
    executables = executable
)
"""
    PRIPS: Python Runtime Interface Plugin of SPONGE
"""
from pathlib import Path
__version__ = "1.4b1"

message = f"""
Usage:
    1. Copy the path printed above
    2. Paste it to the value of the command "plugin" of SPONGE
"""

try:
    import cupy
except ModuleNotFoundError:
    message = """
Error: 
    PRIPS replies on the python package "cupy".
    Please install cupy
"""

print(f"""
  PRIPS: Python Runtime Interface Plugin of SPONGE

Version: {__version__}
Path: {Path(__file__).parent / "_prips.so"}
{message}
""")

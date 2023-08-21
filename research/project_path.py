"""  Convenience file to easily get the full path of the project. """

import sys
from pathlib import Path

# Find module path
file_path = Path(__file__).parent
module_path = file_path
# traverse through all folder levels above until we find a folder with .gitignore
# file. if it is more then 9 folder deep, stop the loop (as probably something
# went wrong, i.e. the main folder of the package is not found)
for _ in range(9):
    gitignore_pathfile = module_path / '.gitignore'
    if not gitignore_pathfile.exists():
        # if .gitignore not in the folder, traverse one level higher
        module_path = module_path.parent
    else:
        # if .gitignore exists in folder, traverse stop the loop
        break

if module_path not in sys.path:
    sys.path.append(str(module_path))


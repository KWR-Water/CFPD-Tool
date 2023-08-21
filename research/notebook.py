# <markdowncell>
# # You can use this type of cells to explain the code below

# <codecell>
# with the codecell tag, you can run code int his cell by clicking "run cell"
# above it or by pressing "Shift+ enter" when your cursor is in the cell
#
# first import some packages
import pandas as pd

# <markdowncell>
# now ensure that we can import the code of our tool / model in the
# "package_name" folder we need to add it to the working directory of python
# Some IDE's do it automatically, some dont. By importing `project_path`
# file, this is automatically done as well. moreover, path where project_path
# is located can be imported as well. THis is useful, as it is the same as
# the path of the current file (`notebook.py`)
# <codecell>
from project_path import file_path
# <markdowncell>
# This allows importing the model
# <codecell>
from package_name.model import Model
model = Model

# %%

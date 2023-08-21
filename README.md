Use this repository as a template. Do a global search in all files to 'package_name' and replace it with the actual package name.

rename the folder 'package_name' to the name of your package as well

Make a list of all the packages required to run your code in requirements.txt. If this repository depends on any package
that should be installed by conda instead of pip, add that package in requirements_conda.yml; also specify your
python version in that file.

After that, create a conda environment by navigating your command prompt to the folder containing `requirements_conda.yml`,
that is, the same folder as this file. Then type the command `conda env create -n <package_name> --file requirements_conda.yml` where
<package_name> should again be replaced by the name of your package.

the folders have the following purpose:
- tests: contains unit tests. Using pytest is adviced
- documentation: contains documentation which can be created (and updated) by running make.bat; the result is in `documentation/build/html`
- <package_name>: contains the code that consists the models and scripts that other people should be able to use
- research: contains files that run the code in <package_name> to perform research with the models or investigate how
  the model behaves. By doing this, script to run the model are seperated from the actual code that consists the model.
  This keeps the model code much more tidy.

Be sure to pick a LICENCE

after this, you should remove all the text in this file and replace it with a small description on your repositories
content.
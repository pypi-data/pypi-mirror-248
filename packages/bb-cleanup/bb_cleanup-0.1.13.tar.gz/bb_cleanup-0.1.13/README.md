# cleanup
Match and clean files using Unix shell style wildcards.
# Installing with pip
```commandline
pip install bb_cleanup
```
# # Installing with building
```
python -m build
pip install .\dist\bb_cleanup-0.1.11-py3-none-any.whl
```
# Command
```
cleanup --help
```
# Using .clean
```
# wildcards of directories to clean
dir_patterns = dist,log,__pycache__,tmp,.pytest_cache
# wildcards of files to clean
file_patterns = *.pyc
# Avoid paths that start with the following when clearing
exclude_patterns = ./venv/*
```

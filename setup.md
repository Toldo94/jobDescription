# Setup You virtual enviroment first

## First install virtualenv to current python instalation

Linux: `python3 -m pip install --user virtualenv`

Windows: `py -m pip install --user virtualenv`

## Create new virtual enviroment

Linux: `python3 -m venv Path/To/New/Env/envName`

Windows: `py -m venv Path/To/New/Env/envName`


## Activate virtual enviroment

Linux: `source env/bin/activate`

Windwos: `.\env\Scripts\activate`

## Install required packages

If **requiremnets.txt** exists, install all packages from it with command:

`pip install -r requirements.txt`

## Create requirement.txt

Save all the packages in the file with: `pip freeze > requirements.txt`.

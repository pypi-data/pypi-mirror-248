# core-tests
_______________________________________________________________________________

This project contains basic elements for testing purposes and the ability 
to run tests and coverage as a command...

## Execution Environment

### Install libraries
```commandline
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```commandline
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```commandline
source .venv/bin/activate
```

### Install required libraries.
```commandline
pip install .
```

### Check tests and coverage...
```commandline
python manage.py run-test
python manage.py run-coverage
```

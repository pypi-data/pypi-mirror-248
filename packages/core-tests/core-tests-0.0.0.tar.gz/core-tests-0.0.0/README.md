# project-name

_______________________________________________________________________________

Project description...

### Create and activate virtual environment.

```commandline
pip install --upgrade pip virtualenv
virtualenv --python=python3.11 .venv
source .venv/bin/activate
```

### Install required libraries.

```commandline
pip install '.[tests]'
```

### Check tests and coverage...

```commandline
python manage.py test
python manage.py coverage
```

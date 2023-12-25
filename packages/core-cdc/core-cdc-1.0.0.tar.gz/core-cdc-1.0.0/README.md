# core-cdc (CDC a.k.a Change Data Capture)
_______________________________________________________________________________

It provides the core mechanism and required resources to 
implement "Change Data Capture" services...

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
python manager.py run-test
python manager.py run-coverage
```

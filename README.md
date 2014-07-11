# Policy Compass Services
Web Services for the Policy Compass


## Manual

This manual is tested under Ubuntu 14.04!

### Requirements

* Python 3 should be already installed, but make sure with the following command:
```shell
  python3
```
* Install the following packages:
```shell
  apt-get install python-virtualenv python3-dev libpq-dev
```
* If you want to use PostgreSQL for development install it:
```shell
  apt-get install postgresql
```
* Note: You can also develop with a SQLite Database

### Installation
* Create a new directory for the project
```shell
  mkdir services
```
* Create a Python Virtual Environment with Python 3 and activate it
```shell
  virtualenv services --python=python3
  cd services
  source bin/activate
```
* Clone the repository including submodules
* Note: The submodule are configured for use with SSH, so configure your access to GitHub: https://help.github.com/articles/generating-ssh-keys
```shell
  git clone git@github.com:policycompass/policycompass-services.git
  cd policycompass-services
  git submodule init
  git submodule update
```
* Install the Requirements
```shell
  pip install -r requirements.txt
```
* Create a local settings file
```shell
  cp config/settings.sample.py config/settings.py
```
* Edit the settings.py according to your needs. See: https://docs.djangoproject.com/en/1.6/ref/settings/#databases
* Initialize the Database
```shell
	python manage.py syncdb
	python manage.py migrate
	python manage.py loaddata metrics users
```

* Start the application
```shell
	python manage.py runserver
```
* Browse for example to: http://localhost:8000/api/v1/metrics


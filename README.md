
# Data Unique Challenge

  

This simple Dash based app is a part of an challenge requested by data unique branch.

## Get Started
This get started refers a **Linux** environment.
Before Continue, make sure you have your environment correctly setted up with all dependencies installed.
This project depends on:
1. Python installation
	* Click [here](https://realpython.com/installing-python/) to see a tutorial
2. Last version of Anaconda
	* [Install Anaconda](https://docs.anaconda.com/anaconda/install/)
3. A Postgre database running
	* [Install Postgre](https://www.postgresql.org/download/)

#### Pip
We'll need install the python package manager to install some python dependencies in which this project depends on. After installing [it](https://pip.pypa.io/en/stable/installing/) , run these commands to install python dependencies:
```console
	pip install dash
	pip install pandas
	pip install sqlalchemy
```

## Configuring Database

To create our database schema, we'll need some environment variables to have been setted up, ir wich are:
* DB_USER
* DB_PASS
* DB_PORT

Set those variables to be your user, password, and port in which your database is currently running. After exported it up, just run:
```console
	python database_config/config.py
```
From the root of this project to create schema and seeding it database

## Running project first time
In the root of the project, just run:
```console
	python start.py
```
and access the local address provided in the terminal to see project running.

## Any problem?
Send me an email at <hfashigor@hotmail.com>
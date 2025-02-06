# mini-rag
This is a mini RAG model application 

## Requirements
 - Python 3.8 or later

### Python installation
1) Dawnload and install python from [here](https://www.python.org/downloads/)

2) Creating a new enviroment:
```bash
$ cd path/to/your/project
$ python -m venv venv
```

3) Activate the enviroment(windows):
```bash
$ ./.venv\Scripts\Activate.ps1
```
## Installation

### Install required packages
```bash
$ cd src
$ pip install -r requirments.txt
```
### Setup the enviroments variables
```bash
$ cd src
$ cp .env.example .env 
```
Setup your enviroemnts varibale in the .env file

## Run Docker Compose Services
```bash
  $ cd docker
  $ cp .env.example .env
```
### update .evn with your values
```bash
  $ cd docker
  $ docker compose up -d
``` 

## Running the application

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

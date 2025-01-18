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
$ pip install -r requirments.txt
```
### Setup the enviroments variables
```bash
$ cp .env.example .env 
```
Setup your enviroemnts varibale in the .env file

## Running the application

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

# Documentation

This project retrieve and update customers invoices payments by using REST APIs.

It was built using Python 3.9, [FastAPI](https://fastapi.tiangolo.com/), [pytest](https://docs.pytest.org/en/7.0.x/), and [uvicorn](https://www.uvicorn.org/) as ASGI implementation server. Please find more details in `pyproject.toml`

The following SQLite [database](https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql) is used to get customers and invoice payments data. The DB was filled using the `db/Chinook_Sqlite.sql` script.

## Requirements

Python 3.9+

You need to have [**Poetry**](https://python-poetry.org/docs/) installed, as Python packaging manager.

## Installation

Once poetry is installed, to create the virtual environment and install all the Python packages listed in the `pyproject.toml` file, you need to run

```bash
poetry install
```

Then, activate the virtual environment running

```bash
poetry shell
```

When you need to deactivate the venv, just run `exit`

## How to run

You can use Uvicorn with hot realod by running

```
uvicorn rest_api_sqlite.service:app --host 0.0.0.0 --port 80 --reload
```

Or you can use Docker as well:

```
docker build -t rest_api_sqlite .
docker run --name rest_api_sqlite_container -p 80:80 rest_api_sqlite
```

The API `/invoices` retrieve all the customers' data and invoices payments, sorted by `total_paid` amount in descending order: invoices can be filtered for a specific time periods using start and end dates (optional)

```
curl -X 'GET' \
  'http://0.0.0.0:80/invoices?start=2011-01-01&end=2011-06-01' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json'
```

## Test

Run app test with:

```
pytest test/test_main.py
```

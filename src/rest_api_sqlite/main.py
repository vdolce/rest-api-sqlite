""" Main file """
import argparse
import json
import os
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import List, Tuple

from dateutil.parser import isoparse

from rest_api_sqlite.queries import FILTERED_INVOICES_QUERY


def is_date(string: str) -> bool:
    """
    Return whether the string is an iso date (YYYY-MM-DD) or not
    """
    try:
        if string and isinstance(string, str):
            isoparse(string)
            return True
        return False
    except ValueError:
        return False


def valid_dates(start_date: str, end_date: str) -> bool:
    """
    This function verify is the end date is greater or equal to the start date
    """
    return datetime.fromisoformat(start_date) <= datetime.fromisoformat(end_date)


def current_time_string() -> str:
    """
    Return a string with the UTC datetime in the following format YYYYMMDD_hh_mm_ss
    """
    return datetime.utcnow().strftime("%Y%m%d_%H_%M_%S")


def write_json(dict_data: List[dict], filename: str) -> None:
    """
    Dump a dictionary into a json file in the `/dumps` folder
    The filename has the current datetime (UTC format)
    """
    json_object = json.dumps(dict_data, indent=4)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
        print(f"Created file {filename}")


def open_db_connection() -> Tuple[
    sqlite3.Connection,
    sqlite3.Cursor,
]:
    """
    Return a cursor to make queries
    """
    try:
        db_name = Path("db").joinpath("Chinook_Sqlite_db.sqlite")
        db_connection = sqlite3.connect(db_name, uri=True)
        db_cursor = db_connection.cursor()
        print("Database created and Successfully Connected to SQLite")
        return db_connection, db_cursor
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        raise


def execute_query(
    db_cursor: sqlite3.Cursor, query: str, query_params: dict
) -> sqlite3.Cursor:
    """
    Return a cursor with the query result
    """
    try:
        return db_cursor.execute(query, query_params)
    except sqlite3.Error as error:
        print("Error while executing the query", error)
        raise


def close_db_connection(connection: sqlite3.Connection) -> None:
    """
    Close DB connection
    """
    if connection:
        connection.close()
        print("The SQLite connection is closed")


def cursor_to_dict(cursor: sqlite3.Cursor) -> List[dict]:
    """
    From a cursor, it creates a list of dictionaries,
    where each dictionary has all the customer's data and invoices' information
    """
    final_list = []

    current_customer = None

    for row in cursor:
        if current_customer is None or current_customer != row[0]:
            current_customer = row[0]
            customer_dict = {}
            customer_dict["customer_id"] = row[0]
            customer_dict["first_name"] = row[1]
            customer_dict["last_name"] = row[2]
            customer_dict["total_paid"] = str(row[3])
            customer_dict["invoices"] = []
            final_list.append(customer_dict)

        invoice_dict = {
            "date": row[4],
            "amount": str(row[5]),
        }
        final_list[-1]["invoices"].append(invoice_dict)

    return final_list


def get_filtered_invoices(start=None, end=None):
    """
    Get all invoices filtered by start and end dates
    """

    if start is None:
        start = "1900-01-01"

    if end is None:
        end = date.today().isoformat()

    if not (is_date(start) and is_date(end)):
        raise ValueError("Please provide valide dates in the format YYYY-MM-DDDD")
    if not valid_dates(start, end):
        raise ValueError("The end date must be greater than or equal to the start date")

    sqlite_connection, cursor = open_db_connection()

    print(f"Querying from {start} to {end}")
    params = {"start": start, "end": end}
    results = execute_query(cursor, FILTERED_INVOICES_QUERY, params)
    dict_output = cursor_to_dict(results)

    close_db_connection(sqlite_connection)

    return dict_output


def save_json(start: str, end: str) -> None:
    """Save result into a JSON File"""
    output = get_filtered_invoices(start, end)
    filename = f"dumps/invoice_payments_{current_time_string()}.json"
    write_json(output, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get customer payments and write them to a JSON file."
    )
    parser.add_argument(
        "-s", "--start", help="get payments on or after this date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "-e", "--end", help="get payments before this date (YYYY-MM-DD)"
    )
    args = parser.parse_args()

    save_json(start=args.start, end=args.end)

""" API Endpoints made with Fast API """
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException

from rest_api_sqlite.main import get_filtered_invoices

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()


@app.get("/items")
def read_item(item_id: Optional[str] = None, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/invoices")
def get_invoices(start: Optional[str] = None, end: Optional[str] = None):
    """Given optional start and end date, this API return a list of invoices of all customers"""

    logger.info("API `/invoices` with start=%s and end=%s", start, end)

    try:
        response = get_filtered_invoices(start=start, end=end)
        logger.info("Query executed successfully")
    except ValueError as error:
        logger.error("Dates not valid")
        raise HTTPException(status_code=400, detail="Dates not valid") from error

    return response

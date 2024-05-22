# main.py

import asyncio
import logging
import requests
import random

from fastapi import FastAPI, HTTPException, status
app = FastAPI()


logging.basicConfig(level=logging.INFO)

@app.get("/health")
async def health():
    logging.warning('GET /health received')
    return {'service':'fastapi', 'result':'ok'}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if item_id % 2 == 0:
        # mock io - wait for x seconds
        seconds = random.uniform(0, 3)
        await asyncio.sleep(seconds)
    return {"item_id": item_id, "q": q}


@app.get("/invalid")
async def invalid():
    raise ValueError("Invalid ")


@app.get("/exception")
async def exception():
    try:
        raise ValueError("sadness")
    except Exception as ex:
        logging.error(ex, exc_info=True)
        # span = trace.get_current_span()

        # generate random number
        seconds = random.uniform(0, 30)

        # record_exception converts the exception into a span event. 
        exception = IOError("Failed at " + str(seconds))
        # span.record_exception(exception)
        # span.set_attributes({'est': True})
        # Update the span status to failed.
        # span.set_status(Status(StatusCode.ERROR, "internal error"))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Got sadness")

@app.get("/external-api")
def external_api():
    logging.warning('GET /external-api received')
    seconds = random.uniform(0, 3)
    logging.info(f'/external-api - calling httpbin.org with {seconds} sec delay')
    response = requests.get(f"https://httpbin.org/delay/{seconds}")
    response.close()
    return "ok"

# app.mount("/", StaticFiles(directory="dist",html = True), name="dist")

# @app.get("/")
# async def read_index():
#    return FileResponse('index.html')


@app.get("/")
async def root():
 return {"greeting":"Hello world"}


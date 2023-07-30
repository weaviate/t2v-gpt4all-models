from logging import getLogger
from fastapi import FastAPI, Response, status
from gpt4all import Embed4All
from vectorizer import VectorizeRequest, Vectorizer
from meta import Meta


app = FastAPI()
logger = getLogger('uvicorn')
meta_config: Meta
vectorizer: Vectorizer


@app.on_event("startup")
def startup_event():
    global vectorizer
    global meta_config
    logger.info("Loading model...")
    vectorizer = Vectorizer()
    meta_config = Meta()
    logger.info("Running model on CPU")


@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
async def live_and_ready(response: Response):
    response.status_code = status.HTTP_204_NO_CONTENT


@app.get("/meta")
def meta():
    return meta_config.get()


@app.post("/vectorize")
async def read_item(item: VectorizeRequest, response: Response):
    try:
        return await vectorizer.vectorize(item)
    except Exception as e:
        logger.exception(
            'Something went wrong while vectorizing data.'
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}

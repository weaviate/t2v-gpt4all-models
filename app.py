from logging import getLogger
from fastapi import FastAPI, Response, status
from gpt4all import Embed4All
from meta import Meta


async def get_vector_from_text(text):
    output = embedder.embed(text)
    return output


class VectorInput():
    text: str


app = FastAPI()
logger = getLogger('uvicorn')
meta_config: Meta
embedder: Embed4All


@app.on_event("startup")
def startup_event():
    global meta_config
    global embedder
    logger.info("Loading model...")
    embedder = Embed4All()
    logger.info("Running model on CPU")
    meta_config = Meta()


@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
async def live_and_ready(response: Response):
    response.status_code = status.HTTP_204_NO_CONTENT


@app.get("/meta")
def meta():
    return meta_config.get()


@app.post("/vectors")
@app.post("/vectors/")
async def read_item(item: dict, response: Response):
    try:
        vector = await get_vector_from_text(item['text'])
        return {"text": item['text'], "vector": vector, "dim": len(vector)}
    except Exception as e:
        logger.exception(
            'Something went wrong while vectorizing data.'
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}

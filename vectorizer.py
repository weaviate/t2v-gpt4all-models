import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from pydantic import BaseModel
from gpt4all import Embed4All

class VectorizeRequest(BaseModel):
    text: str

class VectorizeResponse(BaseModel):
    text: str
    vector: list[float]
    dim: int

class Vectorizer:
    lock: Lock
    executor: ThreadPoolExecutor
    embedder: Embed4All

    def __init__(self):
        self.lock = Lock()
        self.executor = ThreadPoolExecutor()
        self.embedder = Embed4All()

    def _vectorize(self, input: VectorizeRequest) -> VectorizeResponse:
        with self.lock:
            vector = self.embedder.embed(input.text)
            return VectorizeResponse(text=input.text, vector=vector, dim=len(vector))

    async def vectorize(self, input: VectorizeRequest) -> VectorizeResponse:
        return await asyncio.wrap_future(self.executor.submit(self._vectorize, input))

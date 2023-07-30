from gpt4all import Embed4All


class Meta:
    embedder: Embed4All

    def __init__(self):
        self.embedder = Embed4All()

    def get(self):
        return self.embedder.gpt4all.config

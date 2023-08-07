# GPT4All inference module (for Weaviate)

🎯 Overview
-----------

This is the the inference container which is used by the Weaviate
`text2vec-gpt4all` module. You can download it directly from Dockerhub
using one of the pre-built images or built your own (as outlined below).

It is built in a way to support basic CPU model inference from your disk.

This makes this an easy way to deploy your Weaviate-optimized CPU
NLP inference model to production using Docker or Kubernetes.

📚 Documentation
-----------------

Documentation for this module can be found [here](https://weaviate.io/developers/weaviate/current/retriever-vectorizer-modules/text2vec-gpt4all.html).

📦 Requirements
----------------

1. Create a new virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

2. Install all module and test dependencies

```sh
pip3 install -r requirements.txt
pip3 install -r requirements-test.txt
```

3. Download the model locally

```sh
python3 download.py
```

5. Run the inference server

```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```

💡 Testing
----------

For sanity checks that to check that all works properly you can run our smoke tests against your server

```sh
python3 smoke_tests.py
```

🐳 Docker support
-----------------

In order to build locally a docker image one can run this command in project's root folder

```sh
LOCAL_REPO="local-gpt4all" ./cicd/build.sh
```

In order to test the built docker image run this command in project's root folder

```sh
LOCAL_REPO="local-gpt4all" ./cicd/test.sh
```

🔗 Useful Resources
--------------------

- [GPT4All Embeddings](https://docs.gpt4all.io/gpt4all_python_embedding.html)
- [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

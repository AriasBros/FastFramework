import logging

import uvicorn
from fastframework.application import Application
from bootstrap.providers import providers

logger = logging.getLogger("FastApp")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

app = Application(logger, *providers)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

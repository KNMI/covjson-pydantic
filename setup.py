import logging
import os

import setuptools

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

if __name__ == "__main__":
    setuptools.setup()

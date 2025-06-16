import os
import logging
from backend.config.settings import settings


def configure_logging():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),  # console
            logging.FileHandler("logs/app.log", mode="a"),  # optional
        ],
    )

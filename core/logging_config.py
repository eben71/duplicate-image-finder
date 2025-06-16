import logging
from backend.config.settings import settings


def configure_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

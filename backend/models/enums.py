from enum import Enum

class IngestionMode(str, Enum):
    SCRAPE = "scrape"
    API = "api"
    UPLOAD = "upload"
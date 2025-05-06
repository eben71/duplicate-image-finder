import enum

class IngestionMode(enum.Enum):
    SCRAPE = "scrape"
    UPLOAD = "upload"
    API = "api"

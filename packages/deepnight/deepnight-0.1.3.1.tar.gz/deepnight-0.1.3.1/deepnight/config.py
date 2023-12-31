# config.py
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls.api_key = None
            cls.api_version = None
            cls.timeout = None
            cls.max_retries = None
            # Initialize other config variables here
        return cls._instance

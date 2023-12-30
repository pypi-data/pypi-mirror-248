import os as _os
from typing_extensions import override

# Assuming that _globals.py defines these constants:
from ._globals import DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES, BASE_URL
from .errors import (
    DEEPNIGHTError,
    APIKeyError
)
from . import chat, completions, embeddings
from .audio import Audio

# print(DEFAULT_TIMEOUT)

# Initialize variables with None or default values
class DEEPNIGHT:
    apikey: str
    organization: str
    audio: Audio
    api_version: str
    timeout: int
    def __init__(
            self,
            *,
            apikey: str | None = None,
            api_version: str | None = None,
            organization: str | None = None,
            base_url: str | None = BASE_URL,
            timeout: int | None = DEFAULT_TIMEOUT
    ) -> None:
        if apikey == None:
            apikey = _os.environ.get("DEEPNIGHT_API_KEY")
        if apikey == None:
            raise DEEPNIGHTError(
                "The apikey option must be set either by passing apikey to the client or by setting the DEEPNIGHT_API_KEY environment variable"
            )
        
        self.apikey = apikey
        self.api_version = api_version
        self.organization = organization
        self.timeout = timeout
        self.audio = Audio(apikey, api_version, timeout)
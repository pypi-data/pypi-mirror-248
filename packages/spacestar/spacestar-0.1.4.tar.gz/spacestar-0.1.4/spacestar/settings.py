from typing import Optional

from ormspace.settings import SpaceSettings
from pydantic import ConfigDict


class SpaceStarSettings(SpaceSettings):
    session_secret: Optional[str] = None
    csrf_secret: Optional[str] = None
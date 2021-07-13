"""Project package."""

from .containers import Container
from project_config import settings


container = Container()
container.config.from_dict(settings.__dict__)

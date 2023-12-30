from enum import Enum
from typing import Any

from pydantic.main import BaseModel


class Spec(BaseModel):
    name: str
    spec: Any


class AISpec(BaseModel):
    system: str
    host: str


class CommandType(str, Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    REPLACE = "REPLACE"
    RENAME = "RENAME"
    UNDELETE = "UNDELETE"
    FAIL = "FAIL"
    UPDATE = "UPDATE"

    def __str__(self):
        return self._name_


class OverwriteType(str, Enum):
    """
    Overwrite/delete behavior

    from the least to the most destructive:
      - `never`: never delete or overwrite, allows creating new objects only
      - `default`: allow to overwrite or delete if change doesn't affect data and is non-breaking (default)
      - `force`: force delete/overwrite even if data will be lost
      - `always`: always destroy and recreate everything
    """

    always = "always"
    never = "never"
    default = "default"
    force = "force"

    def __str__(self):
        return self.value

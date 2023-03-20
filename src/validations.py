from src.logs import *
from src.settings import SETTINGS


def validate_non_empty(
    name: str,
    x: str
  ):
  """
  Validate that the given string is not empty.
  """
  x = x.strip()

  if not x:
    raise Exception(f'"{name}" can not be empty!')

  return x


def validate_email(
    name: str,
    s: str,
    required: bool = True
  ):
  """
  Validate that the given string is a valid email for `SETTINGS.BASE_DOMAIN`.
  """
  s = s.strip()

  if required and not s:
    raise Exception(f'"{name}" can not be empty!')

  if s and not s.endswith(f'@{SETTINGS.BASE_DOMAIN}'):
    if required and s.starswith(f'@{SETTINGS.BASE_DOMAIN}'):
      raise Exception(f'"{name}" should be a valid e-Mail!')
    else:
      s = ""

  return s

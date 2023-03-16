from src.logs import *
from src.settings import SETTINGS

log_title('Validations')

def validate_non_empty(
    name: str,
    x: str
  ):
  x = x.strip()

  if not x:
    raise Exception(f'"{name}" can not be empty!')

  return x


def validate_email(
    name: str,
    s: str,
    required: bool = True
  ):
  s = s.strip()

  if required and not s:
    raise Exception(f'"{name}" can not be empty!')

  if s and not s.endswith(f'@{SETTINGS.BASE_DOMAIN}'):
    if required and s.starswith(f'@{SETTINGS.BASE_DOMAIN}'):
      raise Exception(f'"{name}" should be a valid e-Mail!')
    else:
      s = ""

  return s

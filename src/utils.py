import re
from src.settings import SETTINGS

def email_base(user_email: str):
  """
  Get the base of an email address.
  """
  return re.sub(SETTINGS.EMAIL_BASE_CLEAN_REGEX, '', user_email)

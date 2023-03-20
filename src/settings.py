class _Settings():
  BASE_DOMAIN: str = 'patagoniansys.com',
  """
  Base company domain.
  """

  DRIVE_FOLDER_OWNER: str = f'patagonian.drive@patagoniansys.com',
  """
  Company folders Owner.

  All folders will be owned by this user by default
  if an Owner was not defined.
  """

  EMAIL_BASE_CLEAN_REGEX: str = r'(sys)?\.(com|it)$'
  """
  At Patagonian we have domains "@patagoniansys.com", "@patagonian.it" and "@patagonian.com".
  To check if a user is already on the permissions list, we need to examine
  the first part of their email address.
  To do this, we'll use a RegExp to strip away ani variations in the email address and
  only keep the beginning part of the address.
  """


SETTINGS = _Settings()
"""
Settings.
"""


def setup(
    base_domain: str = None,
    drive_folder_owner: str = None,
    email_base_clean_regex = None
  ):
  """
  Initialize settings.
  """
  
  if base_domain != None:
    SETTINGS.BASE_DOMAIN = base_domain

  if drive_folder_owner != None:
    SETTINGS.DRIVE_FOLDER_OWNER = drive_folder_owner

  if email_base_clean_regex != None:
    SETTINGS.EMAIL_BASE_CLEAN_REGEX = email_base_clean_regex

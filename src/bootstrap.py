from googleapiclient.discovery import build
from google.colab import auth
from src.logs import *

log_title('Bootstrap')

# Authenticate and build the Drive API client
auth.authenticate_user()
service = build('drive', 'v3')

# Current user e-Mail
about = service.about().get(fields='user').execute()
CURRENT_USER_EMAIL = email = about['user']['emailAddress']

log(f'Logged in with "{CURRENT_USER_EMAIL}"')

if not CURRENT_USER_EMAIL:
  log(about)
  raise Exception('Can not get the user e-Mail')

from src.settings import *
from src.logs import *
from src.validations import *
from src.bootstrap import *
from src.utils import *

log_title('Utilities')

def remove_permissions(
    folder_id: str,
    user_email: str
  ):
  """Remove access from folder

  Args:
    folder_id: Folder ID
    user_email: User e-Mail | Domain | *
  """
  if user_email:
    log_start(f'ℹRemoving {user_email} from {folder_id}...')

    folder_permissions = service\
      .permissions()\
      .list(
          fileId=folder_id
        )\
      .execute()\
      .get('permissions')

    remove_all = user_email == '*'

    if remove_all:
      log(f'‼️ Remove all permissions from {folder_id}!')
      log(folder_permissions)

    for p in folder_permissions:
      user_permission = service.permissions().get(
          fileId=folder_id,
          permissionId=p['id'],
          fields='id, type, emailAddress, domain, pendingOwner' # fields='*'
        ).execute()

      if (
          not user_permission.get('pendingOwner', False)
          and (
            (
              (
                user_permission['type'] == 'user'
                or user_permission['type'] == 'group'
              ) and (
                user_permission['emailAddress'].startswith(
                  email_base(user_email)
                )
                or remove_all
              )
            ) or (
              user_permission['type'] == 'domain'
              and (
                user_email == SETTINGS.BASE_DOMAIN
                or remove_all
              )
            )
          )
        ):
        if remove_all:
          log(f'‼️ Remove permission...')
          log(user_permission)

        try:
          service.permissions().delete(
              fileId=folder_id,
              permissionId=user_permission['id']
            ).execute()
        except Exception as ex:
          log(f'Can not remove following permission:')
          log(user_permission)
          log(f'Details: {ex}')

        if not remove_all:
          break

    log_end(f'Permission removed for {user_email} at {folder_id}!')


def add_permissions(folder_id: str, permission):
  if permission:
    is_owner = permission.get('role', None) == 'owner'
    role = permission.get('role', 'R?')
    name = permission.get('emailAddress', permission.get('domain', None))

    if name:
      log(f'Add {name} ({role}) permission to folder {folder_id}')

      if is_owner:
        log('👑 Owner')
    else:
      log(f'Add permission to folder {folder_id}')
      log(permission)

    service.permissions().create(
        fileId=folder_id,
        body=permission,
        transferOwnership=is_owner,
        sendNotificationEmail=is_owner
      ).execute()


def create_folder(
    parent_folder_id: str,
    name: str,
    permissions = None,
    remove_emails = None
  ):
  """Create folder.

  Args:
    name: Folder name
    permissions: Array of permissions
    remove_emails: Array of e-Mail addresses

  Returns: created folder ID.
  """
  log_start(f'Creating folder "{name}" at {parent_folder_id}...')

  # Create the folder
  folder = {
      'name': name,
      'mimeType': 'application/vnd.google-apps.folder',
      'parents': [ parent_folder_id ],
      'domain': SETTINGS.BASE_DOMAIN
    }
  folder = service.files().create(
      body=folder,
      fields='id'
    ).execute()
  folder_id = folder.get('id')

  # Remove permissions from users (if provided)
  if remove_emails:
    log('Remove permissions from users')
    for user_email in remove_emails:
      remove_permissions(folder_id, user_email)

  # Grant permissions to users
  if permissions:
    log('Grant permissions to users')
    for permission in permissions:
      add_permissions(folder_id, permission)

  # Owner
  add_permissions(
    folder_id,
    user_p(SETTINGS.DRIVE_FOLDER_OWNER, 'owner')
  )

  # Remove current user
  if (
      CURRENT_USER_EMAIL != SETTINGS.DRIVE_FOLDER_OWNER
      and (
        not permissions
        or not any(
            p and p.get('emailAddress', '') == CURRENT_USER_EMAIL
            for p in permissions
          )
      )
    ):
    remove_permissions(folder_id, CURRENT_USER_EMAIL)

  log_end(f'Folder "{name}" ({folder_id}) created at {parent_folder_id}!')

  return folder_id


def get_folder_id(
    parent_folder_id: str,
    folder_name: str
  ):
  parent_folder_content = list_folder(parent_folder_id)
  folder_id = ''

  for c in parent_folder_content:
    if c['name'].lower() == folder_name.lower():
      folder_id = c['id']
      break;

  return folder_id


def create_folder_if_not_exists(
    parent_folder_id: str,
    folder_name: str,
    permissions = None,
    remove_emails = None
  ):
  client_folder_id = get_folder_id(parent_folder_id, folder_name)

  if client_folder_id:
    log(f'Using existing "{folder_name}" ({client_folder_id}) folder')
  else:
    log_start(f'Creating folder "{folder_name}"...')
    client_folder_id = create_folder(
        parent_folder_id,
        folder_name,
        permissions,
        remove_emails
      )
    log_end(f'Folder "{folder_name}" ({client_folder_id}) created!')
    
  return client_folder_id


def list_folder(folder_id: str):
  files = []
  page_token = None

  while True:
    response = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and trashed = false and '{folder_id}' in parents",
        spaces='drive',
        fields='nextPageToken, files(id, name)',
        pageToken=page_token
      ).execute()

    files.extend(response.get('files', []))
    page_token = response.get('nextPageToken', None)

    if page_token is None:
      break

  return files


def build_p(p_type: str, email: str, role: str):
  """Build permissions object.

  Args:
    p_type: user | group | domain | anyone
    email: e-Mail.
    role: owner | organizer | fileOrganizer | writer | commenter | reader

  See: https://developers.google.com/drive/api/v3/reference/permissions
  """
  if not email:
    return None

  return {
      'type': p_type,
      'role': role,
      'emailAddress': email
    }


def user_p(user_email: str, role: str = 'writer'):
  """
  User permissions object.

  Args:
    user_email: e-Mail.
    role: owner | organizer | fileOrganizer | writer | commenter | reader
  """
  return build_p('user', user_email, role)


def group_p(group_email: str, role: str = 'writer'):
  """
  Group permissions object.

  Args:
    group_email: e-Mail.
    role: owner | organizer | fileOrganizer | writer | commenter | reader
  """
  return build_p('group', group_email, role)


def domain_p(role: str = 'reader'):
  """
  Domain permissions object.

  Args:
    role: owner | organizer | fileOrganizer | writer | commenter | reader
  """
  return {
      'type': 'domain',
      'role': role,
      'domain': SETTINGS.BASE_DOMAIN
    }


def create_folder_tree(parent_folder_id, folder_tree):
  root_folder_id = ''

  for folder_name, data in folder_tree.items():
    log_start(f'🏗️ Creating folder tree for "{folder_name}"...')

    folder_id = create_folder(
        parent_folder_id,
        folder_name,
        data.get('permissions', None),
        data.get('remove_emails', None)
      )

    if 'folders' in data:
      create_folder_tree(
          folder_id,
          data.get('folders', [])
        )
      
    log_end(f'🏗️ Folder tree for {folder_name} ({folder_id}) done!')

    # Save first folder ID reference
    if not root_folder_id:
      root_folder_id = folder_id

  return root_folder_id

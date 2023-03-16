![ ! -d google-colab-create-project-structure ] || ( cd google-colab-create-project-structure && git pull --rebase >/dev/null )
![ -d google-colab-create-project-structure ] || git clone https://github.com/PatagonianTech/google-colab-create-project-structure.git
!google-colab-create-project-structure/setup.sh

import mod_cfs

mod_cfs.setup(
  base_domain='patagoniansys.com',
  drive_folder_owner=f'patagonian.drive@patagoniansys.com'
)


#region Params
#############################################

# Client name (root folder name)
CLIENT_NAME = "***" #@param {type:"string"}
CLIENT_NAME = mod_cfs.validate_non_empty('CLIENT_NAME', CLIENT_NAME)

# Project title (inside the client folder)
PROJECT_TITLE = "***" #@param {type:"string"}
PROJECT_TITLE = mod_cfs.validate_non_empty('PROJECT_TITLE', PROJECT_TITLE)

# PM user
PM = "ji***ez@patagoniansys.com" #@param {type:"string"}
PM = mod_cfs.validate_email('PM', PM)

# TL user
_TL = "and***ll@patagoniansys.com" #@param {type:"string"}
_TL = mod_cfs.validate_email('_TL', _TL, False)

# Dev Team Group
DEV_TEAM_GROUP = "con***cas@patagoniansys.com" #@param {type:"string"}
DEV_TEAM_GROUP = mod_cfs.validate_email('DEV_TEAM_GROUP', DEV_TEAM_GROUP)

# QA Team Group
_QA_TEAM_GROUP = "con***icas@patagoniansys.com" #@param {type:"string"}
_QA_TEAM_GROUP = mod_cfs.validate_email('_QA_TEAM_GROUP', _QA_TEAM_GROUP, False)

# This user will be able to edit all project details
_ADMIN_USER = "ag***er@patagoniansys.com" #@param {type:"string"}
_ADMIN_USER = mod_cfs.validate_email('_ADMIN_USER', _ADMIN_USER, False)

#endregion


#region Google Groups
#############################################

GOOGLE_GROUPS = {
  'info': f'info@patagoniansys.com',
  'developer': f'eduardo.cuomo@patagoniansys.com'
}

# Connect to specific folder using its ID
# /Patagonian/Technology/Delivery
# https://drive.google.com/drive/u/1/folders/1UpL06o***HdRIWvDe7
ROOT_FOLDER_ID = '1UpL06o***HdRIWvDe7'

#endregion

#region Run
#############################################

client_folder_id = mod_cfs.get_folder_id(ROOT_FOLDER_ID, CLIENT_NAME)

if client_folder_id and mod_cfs.get_folder_id(client_folder_id, PROJECT_TITLE):
  raise Exception(f'Project "{PROJECT_TITLE}" already exists for Client "{CLIENT_NAME}"!')


mod_cfs.log_title('Folders structure creation')

# Client folder
client_folder_id = mod_cfs.create_folder_if_not_exists(
    ROOT_FOLDER_ID,
    # Start form `CLIENT_NAME` value.
    CLIENT_NAME,
    [
      mod_cfs.domain_p(),
      mod_cfs.group_p(GOOGLE_GROUPS['engineering']),
      mod_cfs.group_p(GOOGLE_GROUPS['board'], 'commenter'),
      mod_cfs.group_p(PM, 'commenter'),
      mod_cfs.group_p(DEV_TEAM_GROUP, 'commenter'),
      mod_cfs.group_p(_TL, 'commenter'),
      mod_cfs.group_p(_QA_TEAM_GROUP, 'commenter'),
      mod_cfs.group_p(_ADMIN_USER, 'commenter')
    ]
  )

root_project_folder_id = mod_cfs.create_folder_tree(client_folder_id, {
    # Start form `PROJECT_TITLE` value.
    PROJECT_TITLE: {
      'permissions': [
        mod_cfs.group_p(GOOGLE_GROUPS['pms']),
        mod_cfs.group_p(GOOGLE_GROUPS['pmo']),
        mod_cfs.group_p(GOOGLE_GROUPS['sales'], 'reader'),
        mod_cfs.group_p(PM)
      ],
      'folders': {
        '⚜️ Product Design': {
          'permissions': [
            mod_cfs.group_p(GOOGLE_GROUPS['product'])
          ],
          'folders': {
            '🔍 Discovery': {
              '⚜️ Product Design': {},
              '🏗️ Architecture': {
                'permissions': [
                  mod_cfs.group_p(GOOGLE_GROUPS['architecture']),
                  mod_cfs.group_p(GOOGLE_GROUPS['product'], 'reader'),
                  mod_cfs.group_p(GOOGLE_GROUPS['pms'], 'reader'),
                  mod_cfs.group_p(GOOGLE_GROUPS['pmo'], 'reader')
                ]
              },
              '👷 PMs': {
                'remove_emails': [
                  '*'
                ],
                'permissions': [
                  mod_cfs.group_p(GOOGLE_GROUPS['pms']),
                  mod_cfs.group_p(GOOGLE_GROUPS['pmo']),
                  mod_cfs.group_p(GOOGLE_GROUPS['sales'])
                ]
              }
            },
            '⚜️ UI/UX': {
              'permissions': [
                mod_cfs.group_p(GOOGLE_GROUPS['product']),
                mod_cfs.group_p(GOOGLE_GROUPS['pms'], 'reader'),
                mod_cfs.group_p(GOOGLE_GROUPS['pmo'], 'reader')
              ]
            },
            '🏗️ Architecture': {
              'permissions': [
                mod_cfs.group_p(GOOGLE_GROUPS['architecture']),
                mod_cfs.group_p(GOOGLE_GROUPS['product'], 'reader'),
                mod_cfs.group_p(GOOGLE_GROUPS['pms'], 'reader'),
                mod_cfs.group_p(GOOGLE_GROUPS['pmo'], 'reader')
              ]
            },
            '👷 POs': {
              'remove_emails': [
                '*'
              ],
              'permissions': [
                mod_cfs.group_p(GOOGLE_GROUPS['pmo']),
                mod_cfs.group_p(GOOGLE_GROUPS['sales'])
              ]
            }
          }
        },

        '🏗️ Architecture': {
          'permissions': [
            mod_cfs.group_p(GOOGLE_GROUPS['architecture']),
            mod_cfs.group_p(GOOGLE_GROUPS['product'], 'reader'),
            mod_cfs.group_p(GOOGLE_GROUPS['pms'], 'reader'),
            mod_cfs.group_p(GOOGLE_GROUPS['pmo'], 'reader'),
            mod_cfs.group_p(_TL),
            mod_cfs.group_p(_ADMIN_USER)
          ],
        },

        '👷 PMs': {
          'remove_emails': [
            '*'
          ],
          'permissions': [
            mod_cfs.group_p(GOOGLE_GROUPS['pms']),
            mod_cfs.group_p(GOOGLE_GROUPS['pmo']),
            mod_cfs.group_p(GOOGLE_GROUPS['sales']),
            mod_cfs.group_p(_ADMIN_USER)
          ]
        }

        '👨‍💻 Development': {
          'permissions': [
            mod_cfs.group_p(GOOGLE_GROUPS['tls']),
            mod_cfs.group_p(GOOGLE_GROUPS['product'], 'reader'),
            mod_cfs.group_p(GOOGLE_GROUPS['pms'], 'reader'),
            mod_cfs.group_p(GOOGLE_GROUPS['pmo'], 'reader'),
            mod_cfs.group_p(DEV_TEAM_GROUP),
            mod_cfs.group_p(_TL),
            mod_cfs.group_p(_ADMIN_USER)
          ],
        },

        '👁️‍🗨️ QA': {
          'permissions': [
            mod_cfs.group_p(GOOGLE_GROUPS['tls']),
            mod_cfs.group_p(GOOGLE_GROUPS['product'], 'reader'),
            mod_cfs.group_p(GOOGLE_GROUPS['pms'], 'reader'),
            mod_cfs.group_p(GOOGLE_GROUPS['pmo'], 'reader'),
            mod_cfs.group_p(_QA_TEAM_GROUP),
            mod_cfs.group_p(_TL),
            mod_cfs.group_p(_ADMIN_USER)
          ],
        },

        '🛠️ DevOps': {
          'permissions': [
            mod_cfs.group_p(GOOGLE_GROUPS['devops']),
            mod_cfs.group_p(GOOGLE_GROUPS['pms'], 'reader'),
            mod_cfs.group_p(GOOGLE_GROUPS['pmo'], 'reader'),
            mod_cfs.group_p(PM),
            mod_cfs.group_p(_TL),
            mod_cfs.group_p(_ADMIN_USER)
          ],
          'folders': {
            '🔐 Secrets': {
              'remove_emails': [
                '*'
              ],
              'permissions': [
                mod_cfs.group_p(GOOGLE_GROUPS['devops']),
                mod_cfs.group_p(GOOGLE_GROUPS['engineering']),
                mod_cfs.group_p(PM),
                mod_cfs.group_p(_TL),
                mod_cfs.group_p(_ADMIN_USER)
              ]
            }
          }
        },

        '🪦 Post-Mortem': {
          'permissions': [
            mod_cfs.group_p(GOOGLE_GROUPS['board']),
            mod_cfs.group_p(GOOGLE_GROUPS['sales.team']),
            mod_cfs.group_p(GOOGLE_GROUPS['pmo']),
            mod_cfs.group_p(GOOGLE_GROUPS['pms']),
            mod_cfs.group_p(PM),
            mod_cfs.group_p(_ADMIN_USER)
          ],
          'remove_emails': [
            '*'
          ]
        }
      }
    }
  })

#endregion

#region Finish
#############################################

print('✅✅✅ F I N I S H ✅✅✅')

print(f'Link to Drive: https://drive.google.com/drive/folders/{root_project_folder_id}')

#endregion

#!/usr/bin/python
# ===================  Misc vars =================== ##
OPENPILOT_TOOLS_VER = "0.1"                 # This Softwares Version
#SHOW_CONSOLE_OUTPUT = False                # Show the console output when 'make' is called?
VERBOSE = False
DEVMODE = False
DEV_PLATFORM = ""
IS_AFFIRMATIVE_YES = ['yes', 'ye', 'y', '1', "j", "ja", "si", "s"]
IS_AFFIRMATIVE_UNSURE = ['i guess', 'sure', 'fine', 'whatever', 'idk', 'why', "uh", "um", "...", "bite me", "eat my shorts"]

# ==============  Backup related vars ============== ##
BACKUPS_DIR = '/storage/emulated/0/optools-backups' if not DEVMODE else './test-tools-backups'
BACKUP_OPTIONS = []

# =============  get_aval_themes() vars ============= ##
MIN_SIM_THRESHOLD = 0.25      # user's input needs to be this percent or higher similar to a theme to select it

# =========== Get OP Ver & Location vars =========== ##
OP_Version = 0.0
OP_Location = ''

# ===================== Texts ====================== ##
WELCOME_TEXT = ['Created By: Colton (Brandon) S @D3ADCRU7R',
                'Happy Tooling!',
                'It\'s your EON/C3, do what you want!',
                'Version {}'.format(OPENPILOT_TOOLS_VER)]
UTIL_WELCOME_TEXT = ['Created By: Colton (Brandon) S @D3ADCRU7R',
                'Happy Tooling!',
                'It\'s your EON/C3, do what you want!',
                'Version {}'.format(OPENPILOT_TOOLS_VER)]
CLEANUP_TEXT = ['Welcome to the uninstall - cleanup utility',
                'Version {}'.format(OPENPILOT_TOOLS_VER),
                ' ',
                    "I'm sad to see you go... :",
                  'This program removes the following files not stored in the main directory:',
                    '- WARNING!!!! ALL BACKUPS!!! Stored in /sdcard/optools-backups',
                    '- op_tools_used.txt in /sdcard used as a marker to the auto installer',
                  ' ',
                  'It does not remove:',
                    '- The main project directory']
#!/usr/bin/env python3
###################################################################################
#                                  VER 0.1                                        #
 #                                                                                #
 #      Permission is granted to anyone to use this software for any purpose,     #
 #     excluding commercial applications, and to alter it and redistribute it     #
 #               freely, subject to the following restrictions:                   #
 #                                                                                #
 #    1. The origin of this software must not be misrepresented; you must not     #
 #    claim that you wrote the original software. If you use this software        #
 #    in a product, an acknowledgment in the product documentation is required.   #
 #                                                                                #
 #    2. Altered source versions must be plainly marked as such, and must not be  #
 #    misrepresented as being the original software.                              #
 #                                                                                #
 #    3. This notice may not be removed or altered from any source                #
 #    distribution.                                                               #
 #                                                                                #
 #                                                                                #
 #  ===  Created by Colton (Brandon) S. (@Coltonton / @D3ADCRU7R) for all!  ===   #
 #                                                                                #
 ##################################################################################
 #                                                                                #
 #                     To Get Started WIth OpenPilot Tools:                       #
 #                                                                                #
 #                              SSH into your EON:                                #
 #https://github.com/commaai/openpilot/wiki/SSH#option-3---githubs-official-instructions#   
 #                                                                                #
 #              Type the following command if using the main project              #
 #                     exec /data/OpenPilot-Tools/optools.py                      #
 #                                                                                #
 #               Now follow the prompts and make your selections!                 #
 #                  Everything will be done automagically!!!!!                    #
 #                                                                                #
 #                      Don't forget to tell your friends!!                       #
 #                           Love, Cole (@D3ADCRU&R)                              #
 #                                                                                #
 #                                                                                #
##################################################################################
from support.support_variables import OPENPILOT_TOOLS_VER
print('OpenPilot Tools Version '+ OPENPILOT_TOOLS_VER)

import os
import time, subprocess
from os import path
from support.support_functions import *
from support.support_variables import CLEANUP_TEXT, UTIL_WELCOME_TEXT

######################################################################################################
##======================= CODE START ================================================================#
######################################################################################################
os.chdir(os.path.dirname(os.path.realpath(__file__)))  # __file__ is safer since it doesn't change based on where this file is called from
print_text(UTIL_WELCOME_TEXT)
DEV_CHECK()                               # Check if running on unsupported PC/MAC
DeviceData = get_device_data()            # Init Device Data dict with device info

class ToolUtility:
    def __init__(self):              #Init
        while True:
            util_options = ['Set Static IP', 'Cleanup for uninstall', '-Reboot-', '-Quit-']
            selected_util = selector_picker(util_options, 'This Is a Test')

            if   selected_util == 'Set Static IP':
                self.SetStaticIP()
            elif selected_util == 'Cleanup for uninstall':
                self.Cleanup_Files()
            elif selected_util == '-Reboot-':
                REBOOT()
            elif selected_util == '-Quit-':
                QUIT_PROG()

    def SetStaticIP(self):
        # Get current connection name
        current_conn = subprocess.check_output("nmcli -t -f NAME,DEVICE connection show | grep wlan0 | cut -d: -f1", shell=True, text=True).strip()
        # Get all connection names
        all_con = subprocess.check_output("nmcli -t -f NAME connection show", shell=True, text=True).strip().splitlines()
        all_con = [c for c in all_con if "connection" in c]
        stripped_all_con = [c.split("connection", 1)[1].strip() for c in all_con]
        stripped_all_con.append('-Reboot-')
        stripped_all_con.append('-Quit-')

        print(current_conn)
        print(all_con)

        #Ask users what resources to install
        print('\n*\nWhat connection would you like to set static IP for?')
        for idx, conn in enumerate(stripped_all_con):
            print('{}. {}'.format(idx + 1, conn))
        indexChoice = int(input("Enter Index Value: "))
        indexChoice -= 1 
        selected_option = stripped_all_con[indexChoice]
        print(selected_option)
        
        if selected_option   == 1:
            print("selected inedx 1")
        elif selected_option == '-Reboot-':
            REBOOT()
        elif selected_option == '-Quit-' or selected_option is None:
            QUIT_PROG()        

        SET_STATIC_IP(DeviceData)

    '''def Install_From_Loc(self):      #Install a custom theme from custom location
        backup_dir = make_backup_folder()
        theme_options = []
 
        print('\n*')
        print('What is the full path to your custom theme folder? ')
        print('ex. /sdcard/mythemefolder')
        install_folder = input('?: ')
        
        # cd /data/eon-custom-themes && exec ./theme_utils.py
        # /data/eon-custom-themes/contributed-themes/Subaru
        if path.exists('{}/OP3T-Logo/LOGO'.format(install_folder)) and DeviceData["EON_TYPE"] == 'OP3T':
            theme_options.append('OP3T Boot Logo')
        if path.exists('{}/LeEco-Logo/SPLASH'.format(install_folder)) and DeviceData["EON_TYPE"] == 'LeEco':
            theme_options.append('LeEco Boot Logo')
        if path.exists('{}/bootanimation.zip'.format(install_folder)):
            theme_options.append('Boot Animation')
        if path.exists('{}/spinner/img_spinner_comma.png'.format(install_folder)) or path.exists('{}/img_spinner_track.png'.format(install_folder)) or path.exists('{}/spinner.c'.format(install_folder)):
            theme_options.append('OP Spinner')
        theme_options.append('-Reboot-')
        theme_options.append('-Quit-')
    
        while 1:
            options = list(theme_options)  # this only contains available options from self.get_available_options
            if not len(options):
                print('\n*\nThe selected theme has no resources available for your device! Try another.')
                time.sleep(2)
                return
        
            #Ask users what resources to install
            print('\n*\nWhat resources do you want to install for the Custom theme?')
            for idx, theme in enumerate(options):
                print('{}. {}'.format(idx + 1, theme))
            indexChoice = int(input("Enter Index Value: "))
            indexChoice -= 1 

            selected_option = theme_options[indexChoice]

            if selected_option  in ['Boot Animation', 'OP3T Boot Logo', 'LeEco Boot Logo', 'OP Spinner']:    
                ##Confirm user wants to install asset
                print('\nSelected to install the Custom {}. Continue?'.format(selected_option))
                if not is_affirmative():
                    continue       
    
            if selected_option   == 'Boot Animation':
                ##Check if there was a boot ani backup already this session to prevent accidental overwrites
                #Returns false if okay to proceed. Gets self.backup_dir & asset type name
                if backup_overide_check(backup_dir, 'bootanimation.zip') == True:
                    break

                #Backup And install new bootanimation
                install_from_path = (install_folder)
                if Dev_DoInstall():
                    INSTALL_BOOTANIMATION(backup_dir, install_from_path,)
                    mark_self_installed()        # Create flag in /sdcard so auto installer knows there is a self installation
                    print('Press enter to continue!')
                    input()  
            elif selected_option == 'OP Spinner':
                ##Check if there was a spinner backup already this session to prevent accidental overwrites
                #Returns false if okay to proceed. Gets self.backup_dir & asset type name
                if backup_overide_check(backup_dir, 'spinner') == True:
                    break

                OP_INFO = get_OP_Ver_Loc()
                DebugPrint("Got OP Location: {} and Version 0.{}".format(OP_INFO["OP_Location"], OP_INFO["OP_Version"]))

                #Backup & Install
                install_from_path = ("{}/spinner".format(install_folder))
                #Function to ask before installing for use in dev to not screw up my computer, and test logic
                if Dev_DoInstall():
                    INSTALL_QT_SPINNER(backup_dir, OP_INFO, install_from_path)
                    mark_self_installed()        # Create flag in /sdcard so auto installer knows there is a self installation
                    print('Press enter to continue!')
                    input()   
            elif selected_option == '-Reboot-':
                REBOOT()
            elif selected_option == '-Quit-' or selected_option is None:
                QUIT_PROG()        
            elif selected_option == 'OP3T Boot Logo' or selected_option == 'LeEco Boot Logo':
                ##Check if there was a Boot Logo backup already this session to prevent accidental overwrites
                #Returns false if okay to proceed. Gets self.backup_dir & asset type name
                if backup_overide_check(backup_dir, DeviceData["BOOT_LOGO_NAME"]) == True:
                    break

                #Backup & install new
                install_from_path = ('{}/{}'.format(install_folder, DeviceData["BOOT_LOGO_THEME_PATH"]))
                if Dev_DoInstall():
                    INSTALL_BOOT_LOGO(DeviceData, backup_dir, install_from_path)
                    mark_self_installed()       # Create flag in /sdcard so auto installer knows there is a self installation
                    print('Press enter to continue!')
                    input()'''

    def Cleanup_Files(self):         #Remove all traces of OP Tools
        #Print hAllo message
        print_text(CLEANUP_TEXT)
        print('\nHave you read and understand the warning above and wish to proceed?')
        if not is_affirmative():
            print('Canceling...')
            time.sleep(1.5)
            exit()                 #Fix ??

        print('\nStarting.....')
        if os.path.exists("/storage/emulated/0/optools-backup") and os.path.isdir("/storage/emulated/0/optools-backup"):
            os.system('cd /storage/emulated/0 && rm -rf optools-backups')
            print('Removed the optools-backups directory')
        else:
            print('Could not find optools-backups directory. Does it exist?')
        if os.path.exists("/storage/emulated/0/op_tools_used.txt") and os.path.isdir("/storage/emulated/0/oop_tools_used.txt"):
            os.system('cd /storage/emulated/0 && rm -r op_tools_used.txt')
            print('Removed op_tools_used.txt')
        else:
            print('Could not find op_tools_used.txt. Does it exist?')
        print('\nPlease take a look and make sure the file and directory is removed....')
        os.system('cd /storage/emulated/0 && ls')
        print("\n\nThank you! You will be missed; don't forget to run...")
        print('cd /data && rm -rf OpenPilot-Tools')
        print('to finish your complete un-installation')
        print('Until we meet again.....')
        exit()

if __name__ == '__main__':
    tu = ToolUtility()
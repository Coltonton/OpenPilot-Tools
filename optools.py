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
from support.support_variables import OPENPILOT_TOOLS_VER, IP_OPTIONS, MENU_LIST
print('OpenPilot Tools Version '+ OPENPILOT_TOOLS_VER)

import os, time, subprocess, importlib.util
from os import path
from support.support_functions import *
from support.support_variables import CLEANUP_TEXT, UTIL_WELCOME_TEXT

check_colorama()
from colorama import Fore, Back, Style

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
            util_options = ['IP Configuration (IPV4)', 'Cleanup for uninstall', '-Reboot-', '-Quit-']
            selected_util = selector_picker(util_options, '\033[31m**Main Menu**\033[0m\nSelect a Tool:')

            if   selected_util == 'IP Configuration (IPV4)':
                self.IPV4_Config()
            elif selected_util == 'Cleanup for uninstall':
                self.Cleanup_Files()
            elif selected_util == '-Reboot-':
                REBOOT()
            elif selected_util == '-Quit-':
                QUIT_PROG()

    def IPV4_Config(self):
        is_editing_active=False
        conn_ip="0.0.0.0"
        
        current_conn = subprocess.check_output("nmcli -t -f NAME,DEVICE connection show | grep wlan0 | cut -d: -f1", shell=True, text=True).strip()            # Get current connection name
        all_connections = [c for c in subprocess.check_output("nmcli -t -f NAME connection show", shell=True, text=True).strip().splitlines() if "connection" in c]    # Get all actual connection names                                                                    
        stripped_all_connections = [c.split("connection", 1)[1].strip() for c in all_connections]                                                                              # Strip Out SSID's

        #Ask users what resources to do
        print(Fore.CYAN + '\n*\nWhat connection would you like to edit?' + Style.RESET_ALL)
        indexChoice = PRINT_MENU(stripped_all_connections)
        user_selection = stripped_all_connections[indexChoice]
        
        if user_selection in MENU_LIST or None:                                      #If user selection is a Menu Item
            HANDLE_MENU(user_selection)                                                  #Handle the menu selection
        else:                                                                        #If user selection is not a Menu Item but a program selection
            connection_to_edit = all_connections[indexChoice]                            #Set the Connection_to_edit var based on the corrosponding all_connections index
            if(user_selection == current_conn.split("connection", 1)[1].strip()):        #If the user has chosen to edit the config of the current connection
                is_editing_active=True                                                                #Var to set if user is editing active configuration
                conn_ip = subprocess.check_output("nmcli -g IP4.ADDRESS device show wlan0 | cut -d/ -f1", shell=True, text=True).strip() # Get current connection IP
                print(Fore.RED + '\n\n**WARNING: You are currently editing the active connection, connection WILL drop upon submission!!')
            print(Fore.CYAN + '\n*\nWhat to do with [{}]:'.format(connection_to_edit) + Style.RESET_ALL)
            indexChoice = PRINT_MENU(IP_OPTIONS)                                         #Print the given selections in a menu format and save the index choice
            ip_mode = IP_OPTIONS[indexChoice]                                            #Set the ip_mode var based on the corrosponding IP_OPTIONS index

            if user_selection in MENU_LIST or None:                                      #If user selection is a Menu Item
                HANDLE_MENU(user_selection)                                                 #Handle the menu selection
            elif(ip_mode=="Static"):                                                     #If user selection is not a Menu Item but a program selection
                user_ip      = input(f"Enter IP or ENTER for [{conn_ip}]: ") or conn_ip
                user_subnet  = input(f"Enter Subnet or ENTER for [{"255.255.255.0"}]: ") or "255.255.255.0"
                user_gateway = input(f"Enter Gateway (Router) or ENTER for [{"192.168.1.1"}]: ") or "192.168.1.1"
                user_ip_cidr = get_cidr(user_ip, user_subnet)
                if(is_editing_active):
                    print(Fore.RED + "\n\n**WARNING: CONNECTION MAY DROP, AND DEVICE WILL REBOOT!")
                SET_IP('Static', connection_to_edit, is_editing_active, user_ip_cidr, user_gateway)       #Call the Set_IP Function as Static to begin, requires MODE[Static/DHCP], Selected Connection Name, IP in CIDR format, and Gateway
            elif(ip_mode=="DHCP"):
                if(is_editing_active):
                    print(Fore.RED + "\n\n**WARNING: CONNECTION MAY DROP, AND DEVICE WILL REBOOT!")
                SET_IP('DHCP', connection_to_edit, is_editing_active, "", "")                                 #Call the Set_IP Function as DHCP to begin, requires MODE[Static/DHCP] and Selected Connection Name
            

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
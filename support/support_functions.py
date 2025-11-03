#!/usr/bin/env python3
import os, sys, time, platform, difflib, json, ipaddress, subprocess, importlib.util
from os import path
from datetime import datetime
from support.support_variables import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))  # __file__ is safer since it doesn't change based on where this file is called from

#########################################################
##===================== Shared ======================= ##
#########################################################
def get_device_data(onprocess='null'):         # Get and set the data based on device
    DebugPrint('Getting Device Data...', 'sf')
    devicedata = dict
    with open("/data/params/d/ApiCache_Device") as f:
        info = json.load(f)

    DEVICE_TYPE=info["device_type"]
    devicedata = {
            "DEVICE_TYPE"          : info["device_type"]                   # EON type
        }
    print('Detected device: {}'.format(devicedata["DEVICE_TYPE"]))
    print('IMPORTANT: {}-bricking is possible if this detection is incorrect!'.format("Soft" if not DEVMODE else "SEVERE"))

    if not DEVMODE:
        time.sleep(4)  # Pause for suspense, and so can be read
  
    cycle = 0
    for x in devicedata.keys():
        DebugPrint('{} = {}'.format(x, devicedata[x]), overide="sf" ,multi=1 if cycle <1 else 2)
        cycle = cycle +1
    return devicedata

def is_affirmative(key1="Yes", key2="No", output="Not installing..."): # Ask user for confirmation
    #DebugPrint('Asking to confirm', 'sf')
    key1_l = key1.lower().strip()                   # lowercase key1 for compare
    key2_lf = key2.lower().strip()[0]               # lowercase first char key2 for compare
    key1_lf = key1_l[0] if key1_l[0] not in ["n", key2_lf] else "y" # Get first letter key1(lower), if is "n" (same as no) or same as key2 ignore...
    afirm = input('[1.{} / 2.{}]: '.format(key1,key2)).lower().strip()
    DebugPrint('Got {}'.format(afirm), 'sf')
    if ((afirm in IS_AFFIRMATIVE_YES) or (afirm in [key1_l, key1_lf])): 
        return True
    if afirm in IS_AFFIRMATIVE_UNSURE:
        print("WTF do you mean {}... I'm going to assume NO so I dont brick ya shi...".format(afirm))
    if afirm in ['i dont talk to cops without my lawyer present']: # Do you like your eggs real or plastic?
        print("Attaboy Ope!") # Please tell me you watched the Andy Griffith Show... I was only born in '99...
    
    if output != "silent": print('{}'.format(output))
    time.sleep(1.5) 
    return False

def print_text(showText, withver=0):                 # This center formats text automatically
    max_line_length = max([len(line) for line in showText]) + 4
    print(''.join(['+' for _ in range(max_line_length)]))
    for line in showText:
        padding = max_line_length - len(line) - 2
        padding_left = padding // 2
        print('+{}+'.format(' ' * padding_left + line + ' ' * (padding - padding_left)))
    print(''.join(['+' for _ in range(max_line_length)]))

def selector_picker(listvar, printtext):             # Part of smart picker
    options = list(listvar)      # this only contains available options from self.get_available_options
    if not len(options):
        print('No options were given')
        time.sleep(2)
        return
        
    print('\n{}'.format(printtext))
    for idx, select in enumerate(options):
        print('{}. {}'.format(idx + 1, select))
    indexChoice = int(input("Enter Index Value: "))
    indexChoice -= 1 

    selected_option = listvar[indexChoice]
    return selected_option

def check_colorama():
    if not importlib.util.find_spec("colorama") is not None:
        print("colorama is NOT installed") 
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--user", "colorama"
        ])

def HANDLE_MENU(selection):
    pass
    
def PRINT_MENU(menu_opts):
    for idx, var in enumerate(menu_opts + MENU_LIST):
        print('{}. {}'.format(idx + 1, var))
    index = int(input("Enter Index Value: ")) - 1
    try:
        value = menu_opts[index]
    except IndexError:
        selection = (menu_opts + MENU_LIST)[index]
        if selection == "-Main Menu-":
            return
        elif selection == "-Reboot-":
            REBOOT()
        elif selection == "-Quit-":
            QUIT_PROG()
        else:
            print("No Input recived...")
            return
    return index

def APPLY_CHANGES():
    print('\nApply changes?')
    if not is_affirmative():
        print('Canceling...')
        time.sleep(1.5)
        return False
    else:
        return True
#########################################################
## ============= Installer Support Funcs ============= ##
#########################################################
def get_cidr(IP, SUBNET):
    # Convert to prefix length automatically
    prefix_length = ipaddress.IPv4Network(f"0.0.0.0/{SUBNET}").prefixlen

    cidr = f"{IP}/{prefix_length}"
    DebugPrint('generated CIDR: {}'.format(cidr), fromprocess_input="sf")
    return(cidr)
def get_wlan_connections():
    current_conn = subprocess.check_output("nmcli -t -f NAME,DEVICE connection show | grep wlan0 | cut -d: -f1", shell=True, text=True).strip()            # Get current connection name
    all_connections = [c for c in subprocess.check_output("nmcli -t -f NAME connection show", shell=True, text=True).strip().splitlines() if "connection" in c]    # Get all actual connection names                                                                    
    stripped_all_connections = [c.split("connection", 1)[1].strip() for c in all_connections]                                                                              # Strip Out SSID's

#########################################################
##================= Installer Code =================== ##
#########################################################


def SET_IP(mode, selected_conn_name, is_editing_active, ip_cidr, gateway):
    if(mode=="Static"):
        if(ip_cidr or gateway == ""):
            print('**WARNING: Required Variables Not Passed In!!!')
            print("\n\n\033[31m**WARNING: Required Variables Not Passed In!!!\033[0m   ")
            return
        if(is_editing_active):
            print("\n\n\033[31m**WARNING: CONNECTION MAY DROP, AND DEVICE WILL REBOOT!\033[0m   ")
        subprocess.run(f'nmcli con mod "{selected_conn_name}" ipv4.addresses {ip_cidr} 'f'ipv4.gateway {gateway} ipv4.method manual', shell=True, check=True)
        print("\nSet Static IP [{}] on connection: [{}]".format(ip_cidr, selected_conn_name))
        REBOOT()
    elif(mode=="DHCP"):
        subprocess.run(f'nmcli con mod "{selected_conn_name}" ipv4.method auto', shell=True, check=True)
        print("\nSet DHCP on connection: [{}]".format(selected_conn_name))
        REBOOT()

def SET_DNS():
    pass

#########################################################
## ====================== Misc ======================= ##
#########################################################
def REBOOT():                   #Reboot EON Device
    print('\nRebooting.... Thank You, Come Again!!!\n\n########END OF PROGRAM########\n')
    os.system('sudo systemctl reboot')
    sys.exit()

def QUIT_PROG():                # Terminate Program friendly
    print('\nThank you come again! You may need to reboot to see changes!\n\n########END OF PROGRAM########\n')
    sys.exit()  

def str_sim(a, b):              # Part of get_aval_themes code
    return difflib.SequenceMatcher(a=a, b=b).ratio()

#########################################################
## ==================== DEV/Debug ==================== ##
#########################################################
def setVerbose(a=False):        #Set Verbosity (DEPRICATED)
    if a == True:
        con_output = ' >/dev/null 2>&1'  # string to surpress output
    else:
        con_output = ''  # string to surpress output
    print('[DEBUG MSG]: Verbose ' + a)

def DebugPrint(msg, fromprocess_input="null", overide=0, multi=0):  #My own utility for debug msgs
    if VERBOSE == True or DEVMODE == True or overide == 1:
        now = datetime.now()
        debugtime = now.strftime("%m/%d %I:%M.%S")
        runprocess = "theme_install.py"
        fromprocess_input = runprocess if fromprocess_input == "null" else fromprocess_input
        if fromprocess_input == "sf":
            runprocess = (runprocess.strip(".py")+"/support/support_functions.py")

        if type(multi) == list:
            print("\n##[DEBUG][{} {}] || GOT MULTIPLE DATA".format(debugtime, runprocess))
            print("##[DEBUG] {}".format(msg))
            for x in range(len(multi)):
                print("--> {}".format(multi[x])),
        else:
            print("##[DEBUG][{} {}] || {}".format(debugtime, runprocess, msg))#] #Debug Msg ()s

def DEV_CHECK():                #Hault Program If Ran On PC/Mac
    global DEV_PLATFORM, DEVMODE, VERBOSE
    # Simple if PC check, not needed but nice to have
    DEV_PLATFORM = platform.system()
    if DEV_PLATFORM in ['Windows', 'Darwin']:
        print(DEV_PLATFORM)
        print("This program only works on Comma EONS & Comma Two, sorry...")
        print("Press enter to exit.")
        u = input('')
        if u == "override":
            print('EON DEVMODE enabled, proceed with great caution!')
            VERBOSE = True
            DEVMODE = True
        else:
            sys.exit()

def Dev_DoInstall():            #Function to ask before installing for use in dev to not screw up my computer, and test logic
    if DEVMODE == True:
        DebugPrint("Developer Mode enabled do you actually want to install?", overide="sf")
        DebugPrint("Type 'install' to install or press enter to skip.", overide="sf")
        askinstall = input("## ").lower().strip()
        if askinstall == "install":
            return True
        else:
            DebugPrint("Install Skipped...", overide="sf")
            return False
    else:
        return True

###############################################
### CHANGE THESE VARIABLES FOR CUSTOM BUILD ###
###############################################
webhook_url = "hawkeye_placeholder_webhook"
__version__ = "v1.2 (beta)"
###############################################
###############################################
###############################################

import os
import sys
import hashlib

if getattr(sys, 'frozen', False):
    application_path = sys.executable
    application_compiled = True
else:
    application_path = os.path.abspath(__file__)
    application_compiled = False

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
script_hash = md5(application_path)

import shutil
import time
import getpass
from discord_webhook import DiscordWebhook, DiscordEmbed

###########
### GUI ###
###########
username = None

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def titlebar(text: str, character: str = "=", offset: int = 3) -> str:
    """
    Makes a titlebar styled for the text given.

    ### Arguments
    `text: str` Text to make a titlebar with.
    `character: str = "="` Character used to make the titlebar.
    `offset: int = 3` Offset of characters used to center text.

    ### Expected output
    `titlebar: str` Titlebar as `str`.
    """
    
    text_offset = f"{character * offset} {text} {character * offset}"
    bars = character * len(text_offset)
    titlebar = f"{bars}\n{text_offset}\n{bars}"
    return titlebar

def set_username():
    while True:
        clear()
        print(titlebar("Set Username"))
        username = input("Please enter your username: ")
        print(username)
        if 3 <= len(username) and len(username) <= 15 and all(c.isalnum() or c == '_' for c in username):
            return username
        else:
            clear()
            print(titlebar("Set Username"))
            getpass.getpass("Invalid username. Press ENTER to try again.")

while True:
    clear()
    print(titlebar("Welcome to Tierlist Hawkeye"))
    if not username:
        username_repr = "No username set."
    else:
        username_repr = username
    print(f"Username: {username_repr}\n")
    print("1) Set Username")
    print("2) Submit Result")
    print("3) Exit")
    choice = input("\nSelect an option: ")

    if choice == "1":
        username = set_username()
    elif choice == "2":
        if username:
            break
        else:
            print("Please set a username first.")
    elif choice == "3":
        print("Exiting.")
        sys.exit()
    else:
        print("Invalid choice. Please select a valid option.")

###########
###########
###########

clear()
print(titlebar("Submit Result"))
roaming = os.path.expandvars("%APPDATA%")
temp_folder = os.path.expandvars("%TEMP%")
output_name = f"tierlisthawkeye_{int(time.time() * 1000)}"
output_zip = os.path.join(temp_folder, f"{output_name}.zip")
output_folder = os.path.join(temp_folder, output_name)

def find_logs_folders(root: str) -> list:
    """
    Finds all "logs" folders recursively in the specified root folder.

    ### Arguments
    `root: str` Root string.

    ### Expected output
    `matching_folders: list` List of matching folders
    """
    matching_folders = []
    for dirpath, dirnames, _ in os.walk(root):
        if "logs" in dirnames:
            matching_folders.append(os.path.join(dirpath, "logs"))
    return matching_folders

print("= Finding .folders...", end=" ")
dot_folders = [folder for folder in os.listdir(roaming) if folder.startswith(".")]
logs_folders = []
print("done.")

print("= Searching for required files...", end=" ")
for dot_folder in dot_folders:
    full_dot_path = os.path.join(roaming, dot_folder)
    logs_folders.extend(find_logs_folders(full_dot_path))
print("done.")

os.makedirs(output_folder, exist_ok=True)

print("= Gathering required files...", end=" ")
for logs_folder_path in logs_folders:
    logs_relative_path = os.path.relpath(logs_folder_path, roaming)
    output_subfolder = os.path.join(output_folder, logs_relative_path)
    shutil.copytree(logs_folder_path, output_subfolder, dirs_exist_ok=True)
print("done.")

print("= Packaging...", end=" ")
shutil.copy2(application_path, output_folder)
package = shutil.make_archive(output_folder, "zip", output_folder)
package_data = f"platform `{os.name}` compiled `{application_compiled}`"
print("done.")

print("= Sending package over...", end=" ")
filename = os.path.basename(package)
webhook = DiscordWebhook(url=webhook_url)
embed = DiscordEmbed()
embed.set_title('Tierlist Hawkeye Result')
embed.set_description(f"""**Version:** `{__version__}`
**Script MD5:** `{script_hash}`
**Package:** `{filename}` *({package_data})*
**Username**: `{username}`""")
with open(package, 'rb') as f: 
    file_data = f.read() 
webhook.add_file(file_data, filename)
webhook.add_embed(embed)
try:
    response = webhook.execute()
except Exception:
    print("failed.")
    print("Failed to upload. Please check your internet connection or notify staff.")
    sys.exit(1)
print("done.")

print("Cleaning up...", end=" ")
shutil.rmtree(output_folder)
os.remove(package)
print("done.")

print("\nSuccess! Please wait while we recieve the package and analyze it.")
getpass.getpass("Press ENTER to exit.")

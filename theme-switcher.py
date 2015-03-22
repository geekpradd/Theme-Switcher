import sublime
import sublime_plugin
import os
import zipfile
import json
import sys
import shutil
import threading
MENU_BASE = """
[
    {
        "id": "preferences",
        "children":
        [{
            "caption": "Themes",
            "mnemonic": "t",
            "id": "themes"

        }]
    }
]
""".strip()

def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

def create_menu():
    PACKAGE_FOLDER = os.path.join(sublime.packages_path(), "theme switch")
    if not os.path.isdir(PACKAGE_FOLDER):
        os.makedirs(PACKAGE_FOLDER)
    MENU_LOCATION = os.path.join(PACKAGE_FOLDER, "Main.sublime-menu")
    if not os.path.isfile(MENU_LOCATION):
        open(MENU_LOCATION, "w").close()
    return modify_menu(MENU_LOCATION)


def plugin_loaded():
    files = create_menu()
    # t = threading.Thread(target=watchFiles,args=(files,)) 
    # t.start()

def watchFiles(number):
    print ("Watching Package path in a separate thread")

    @setInterval(3)
    def watch():
        print ("Running every 3 seconds")
        theme_files = list(filter(lambda a: "Theme" in a, os.listdir(get_path())))
        if len(theme_files)!=number:
            print ("doing this")
            number = len(theme_files)
            create_menu()
    s = watch()
    
def plugin_unloaded():
    PACKAGE_FOLDER = os.path.join(sublime.packages_path(), "theme switch")
    MENU_LOCATION = os.path.join(PACKAGE_FOLDER, "Main.sublime-menu")
    os.remove(MENU_LOCATION)

def get_path():
    return os.path.join(os.path.dirname(sublime.packages_path()), "Installed Packages") 

def is_theme_file(name):
    return "sublime-theme" == name.split('.')[-1]

def sanitized(n):
    return n.replace("." + n.split('.')[-1],"")

def read(file):
    with open(file, 'r') as f:
        return f.read()

def menufy(dic):
    new = []
    for key in dic:
        temp = {}
        temp['caption'] = key
        temp['children'] = [{"caption":a, "command":"theme", "args": {"name":a+".sublime-theme"}} for a in dic[key]]
        new.append(temp)
    return new

def get_files():
    theme_files = list(filter(lambda a: "Theme" in a, os.listdir(get_path())))
    collection = {}
    for theme in theme_files:
        Zip = zipfile.ZipFile(os.path.join(get_path(),theme)) 
        files = list(map(sanitized, list(filter(is_theme_file, Zip.namelist()))))
        collection[sanitized(theme)] = files
    return collection 

def modify_menu(LOCATION):
    files = get_files()
    
    menu = json.loads(MENU_BASE)
    menu[0]['children'][0]['children'] = menufy(files) 
    with open(LOCATION,"w") as f:
        f.write(json.dumps(menu,indent=4, sort_keys=True))
    return len(files)
class themeCommand(sublime_plugin.WindowCommand):
    def run(self,name):
        USER_FOLDER = os.path.join(sublime.packages_path(), "User")
        pref = os.path.join(USER_FOLDER, "Preferences.sublime-settings")
        with open(pref, 'r') as f:
            data = json.loads(f.read())
        data['theme'] = name 
        with open(pref, 'w') as f:
            f.write(json.dumps(data,indent=4, sort_keys=True))

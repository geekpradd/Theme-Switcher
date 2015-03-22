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

def create_menu():
    PACKAGE_FOLDER = os.path.join(sublime.packages_path(), "theme switch")
    if not os.path.isdir(PACKAGE_FOLDER):
        os.makedirs(PACKAGE_FOLDER)
    MENU_LOCATION = os.path.join(PACKAGE_FOLDER, "Main.sublime-menu")
    if not os.path.isfile(MENU_LOCATION):
        open(MENU_LOCATION, "w").close()
    modify_menu(MENU_LOCATION)


def plugin_loaded():
    create_menu()


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
        temp['children'] = [{"caption":a, "command":"themeswitch", "args": {"name":a+".sublime-theme"}} for a in dic[key]]
        new.append(temp)
    new.append({"caption": "Refresh Theme Cache", "command": "refreshthemes"})
    print(new)
    return new

def get_files():
    theme_files = list(filter(lambda a: "Theme " in a, os.listdir(get_path())))
    collection = {}
    for theme in theme_files:
        Zip = zipfile.ZipFile(os.path.join(get_path(),theme)) 
        files = list(map(sanitized, list(filter(is_theme_file, Zip.namelist()))))
        collection[sanitized(theme)] = files
    user_path = os.path.join(sublime.packages_path(), "User")
    user_themes = list(filter(is_theme_file, os.listdir(user_path)))
    if len(user_themes):
        collection["User"] = user_themes
    return collection 

def modify_menu(LOCATION):
    files = get_files()
    
    menu = json.loads(MENU_BASE)
    menu[0]['children'][0]['children'] = menufy(files)
    with open(LOCATION,"w") as f:
        f.write(json.dumps(menu,indent=4, sort_keys=True))
    
class themeswitchCommand(sublime_plugin.WindowCommand):
    def run(self,name):
        USER_FOLDER = os.path.join(sublime.packages_path(), "User")
        pref = os.path.join(USER_FOLDER, "Preferences.sublime-settings")
        with open(pref, 'r') as f:
            data = json.loads(f.read())
        data['theme'] = name 
        with open(pref, 'w') as f:
            f.write(json.dumps(data,indent=4, sort_keys=True))

class refreshthemesCommand(sublime_plugin.WindowCommand):
    def run(self):
        create_menu()
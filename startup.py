import getpass
import os
USER_NAME = getpass.getuser() # a0919


def add_to_startup():
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__)) # 獲取現在位置
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'cd "%s" ' % file_path + '\n')
        bat_file.write(r'.\GUIASSISTANT.py')

add_to_startup()

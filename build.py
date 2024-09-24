import os

import PyInstaller.__main__
import shutil
import subprocess

if __name__ == '__main__':
    try:
        shutil.rmtree("build")
    except Exception as e:
        print(e)

    try:
        shutil.rmtree("dist")
    except Exception as e:
        print(e)

    PyInstaller.__main__.run(["main.py",
                              "--onefile",
                              "--icon=resources/img/app_icon_colored.ico",
                              "--add-data=resources/img/titlebar;resources/img/titlebar",
                              "--add-data=resources/img;resources/img",
                              "--add-data=resources/markdown;resources/markdown",
                              "--add-data=resources/themes;resources/themes",
                              "--add-data=resources;resources",
                              "--hidden-import=chardet",
                              "--icon=resources/img/app_icon_colored.ico",
                              "--noconsole",
                              "-n", "WarnoModEditor"
                              ])

    # sign exe
    try:
        cwd = os.getcwd()
        os.chdir(r'C:\Program Files (x86)\Windows Kits\10\bin\x86')
        cmd = "signtool.exe sign /n \"Open Source Developer, Jonas Trappe\" /t http://time.certum.pl /fd sha256 /v \"" \
              + os.path.join(cwd, "dist\\WarnoModEditor.exe\"")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = proc.communicate()
    except Exception as e:
        print(f"Error while signing .exe: {e}")

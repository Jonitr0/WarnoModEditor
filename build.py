import PyInstaller.__main__
import shutil

if __name__ == '__main__':
    try:
        shutil.rmtree("build")
        shutil.rmtree("dist")
    except Exception as e:
        print(e)

    PyInstaller.__main__.run(["main.py",
                              "--onefile",
                              "--add-data=resources/img/titlebar;resources/img/titlebar",
                              "--add-data=resources/img;resources/img",
                              "--add-data=resources/markdown;resources/markdown",
                              "--add-data=resources/themes;resources/themes",
                              "--add-data=resources;resources",
                              "--icon=resources/img/app_icon_colored.ico",
                              "--noconsole",
                              "-n", "WarnoModEditor"
                              ])

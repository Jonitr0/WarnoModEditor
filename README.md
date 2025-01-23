WARNO Mod Editor (WME) is a modding tool for Eugen System's real-time tactics game [WARNO](https://store.steampowered.com/app/1611600/WARNO/). WME offers a graphical user interface from which mods can be created, edited and managed. It is written in Python and uses PySide6 for the GUI.

![preview](./resources/markdown/wme_preview.png) 

### Getting and running WME

##### Requirements

WME runs on Windows 10. I have not yet tested it for Windows 11, but it should run. In any case, WME requires a WARNO installation to be present on your machine.

##### Running WME as .exe

Head to [releases](https://github.com/Jonitr0/WarnoModEditor/releases) and download the latest version. It is an executable that you can use right away, no installation required.

##### Running or Building WME from source

In order to run or build WME from source, you need to have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Python 3.10](https://www.python.org/downloads/windows/) installed on your machine.

Open a new cmd.exe and clone the repository:

````
git clone https://github.com/Jonitr0/WarnoModEditor.git
````

Create a virtual environment in the directory:

````
cd WarnoModEditor
python -m venv .\venv
````

Start the virtual environment and install the requirements:

````
.\venv\Scripts\activate.bat
pip install -r requirements.txt
````

To run WME, make sure your venv is still running and execute **main.py**:

````
python main.py
````

To build WME, make sure your venv is still running and execute **build.py**:

````
python build.py
````

You find the .exe file in the **dist** directory.
If you open the Project in PyCharm, “Run WME” and “Build WME” configurations should be recognized automatically.

##### First steps

When you first start WME, you might get asked to enter the path to your WARNO installation. 

Please refer to the [Quickstart Guide](https://github.com/Jonitr0/WarnoModEditor/blob/main/resources/markdown/Quickstart.md) to learn how to use WME.

##### Paths

WME saves data to and/or loads data from in the following locations:

- Exported configurations from tools are saved in **Users\\[your_username]\Documents\WarnoModEditor**
- Custom scripts for the Script Runner are loaded from **Users\\[your_username]\Documents\WarnoModEditor\Scripts** (more documentation on these is coming soon)
- The log file (*wme.log)*, WME’s config file (*wme_config.json*) and cached data are saved to **Users\\[your_username]\AppData\\Roaming\WarnoModEditor**

### Feedback

If you encounter any bugs, errors or if something does not work as you think it should, please open a new issue [here](https://github.com/Jonitr0/WarnoModEditor/issues), if your problem has not been reported already.

### Acknowledgements

Thanks to Eugen Systems for making WARNO and giving it such extensive support for mods.

Thanks to the WARNO modding community for making many awesome mods and helping newcomers.

Thanks to Ulibos for making [ndf-parse](https://github.com/Ulibos/ndf-parse), a powerful and well-documented tool for automating WARNO modding.
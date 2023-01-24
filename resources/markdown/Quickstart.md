# Quickstart

Welcome to WARNO mod editor (WME)! This guide will explain how you can create, generate and upload your first mod.

### Creating a new mod

Open the "File" menu in the top-left corner and click "New Mod". You will be asked to enter a name. Once you confirm it, the mod will be created and loaded. You now see all files in the mod directory on the left side of the WME main window in the **project explorer**.

### Editing files

Search for files you want to edit using the search bar at the top of the project explorer. Double click a file to open it in the **text editor**. A new tab will open and let you edit the selected file. For more information about tools like the text editor, right-click the tab and select "Help" from the context menu.

### Generating a mod

Once you have saved some changes and want to apply them in-game, you will need to generate your mod. This step creates binary files which WARNO can read from the text files you edited. To generate your mod, click "Edit" > "Generate Mod". This will launch a separate application and might take some time to complete. Once finished, a message box will appear, informing you that the mod was successfully generated or that the process was aborted if there were any errors. If the generation was successful, you can launch WARNO and activate your mod in the Mod Center to see your changes in-game.

After the mod has been generated, you can edit it's configuration by clicking "Edit" > "Edit Mod Configuration".

### Uploading a mod to Steam Workshop

You can upload your mod to Steam Workshop if you want other people to be able to play it. To do that, simply click "Edit" > "Upload Mod". This will again launch another application and display a message box on success.

### Troubleshooting

- *mod upload fails:* No message box is displayed after uploading and the mod does not appear on your Steam Workshop page. In this case, delete the mod config file ("Edit" > "Delete Mod Configuration"), generate and upload the mod again.
- *"update mod" takes long:* The update feature might not work as indented yet. You can check the log file ("wme.log", created in the directory in which you run WME) to see if the script reported any errors.

If you encounter any bugs, errors or if something does not work as you think it should, please open a new issue [here](https://github.com/Jonitr0/WarnoModEditor/issues), if your problem has not been reported already.
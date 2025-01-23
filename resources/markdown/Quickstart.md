Welcome to WARNO mod editor (WME)! This guide will explain how you can create, generate and upload your first mod.

### Creating a new mod

Open the "File" menu in the top-left corner and click "New Mod". You will be asked to enter a name. Once you confirm it, the mod will be created and loaded. You now see all files in the mod directory on the left side of the WME main window in the **Project Explorer**.

### Editing files

Search for files you want to edit using the search bar at the top of the project explorer. Double click a file to open it in the **Text Editor**. A new tab will open and let you edit the selected file. For more information about tools like the text editor, right-click the tab and select "Help" from the context menu or press *Alt + H*. To understand which files control what, [WARNO-DATA](https://github.com/Dreamfarer/WARNO-DATA) is a good starting point.

### Assets

Since WARNO now supports custom text, images and meshes for mods, WME also has systems to import and manage assets:

- To add a new string (piece of text), select “Assets” > “Add String”, choose the CSV file the string should be added to and the token to represent it. To use custom string tokens in the text editor, right click to open the context menu, select “Insert String Token” and select the matching CSV file and token/value.
- To import an image, select “Assets” > “Add Image”. The dialog will let you select and scale an image, which will then by copied to your selected location.

### Visualizing changes

To compare your mod to the unmodded game files, a different mod or an existing backup, open the **Diff Page** (“Add Tab” > “Diff Page”), select the desired target and click “Compare”. WME takes some time to run the comparison, after which you will see a list of added, deleted and changed files and directories.

You can see the changes on individual files by clicking the buttons right of the file name. Hover over them to see what they do. “Show differences (Plain Text)” shows the as-are differences between both files. “Show differences (Parser based)” runs both files through [ndf-parse](https://github.com/Ulibos/ndf-parse) before comparing them. This shows only actual differences and ignores formatting and comments, however, line numbers will likely not match with the original files anymore. Upon clicking one of those buttons, a new view will open that shows both versions of the file side by side and highlights differences.

### Generating a mod

Once you have saved some changes and want to apply them in-game, you will need to generate your mod. This step creates binary files which WARNO can read from the text files you edited. To generate your mod, click "Edit" > "Generate Mod". This will launch a separate application and might take some time to complete. Once finished, a message box will appear, informing you that the mod was successfully generated or that the process was aborted if there were any errors. If the generation was successful, you can launch WARNO and activate your mod in the Mod Center to see your changes in-game.

After the mod has been generated, you can edit it's configuration by clicking "Edit" > "Edit Mod Configuration".

### Uploading a mod to Steam Workshop

You can upload your mod to Steam Workshop if you want other people to be able to play it. To do that, simply click "Edit" > "Upload Mod". This will again launch another application and display a message box on success.

### Feedback

If you encounter any bugs, errors or if something does not work as you think it should, please open a new issue [here](https://github.com/Jonitr0/WarnoModEditor/issues), if your problem has not been reported already.
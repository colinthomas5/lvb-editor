# lvb-editor
A basic editor for .lvb files from games that use the WayForward Engine

## Project Information
The goal of this project is to be a basic level editor for games made by WayForward that use the .lvb level format. This project is made specifically for compatability with .lvb files from Adventure Time: Secret of the Nameless Kingdom, however it may function with over WayForward games that use .lvb files.

## Development Log
2/18/25 - New saveHandler.py created, which handles the process of saving changes to the .lvb file once the save button is pressed. The save button now has functionality, saving any changes made to entities. Numerous bugs were also squashed and some entities are now not able to be modified (some due to not being able to be modified YET, some due to not being able to be modified PERIOD).

Part 2: Support for opening and saving to .pak files is now added. Now that changes are easier to test, unknown values for entities should be determined and implemented. Additionally, support for modifying type-specific properties should be implemented, as well as showing types as words rather than their respective hex values.

The next step for me is to include support for saving directly to the games' .pak files rather than saving to the extracted .lvb file and then having to use QuickBMS to reimport the .lvb file into a .pak file. This would allow a modder to more quickly test changes to whatever entities they are modifying

2/17/25 - New main.py created, which serves as the GUI for lvb-editor utilizing tkinter. This GUI currently allows you to open a .lvb file, view all four layers, the entities within those layers, and the header info for all entities. Old main.py repurposed into fileHandler.py and still serves the same function as the old main.py.

Part 2: Entity values edited in the main window now save to entitiy objects. Saving back to the .lvb file is not implemented, but a save button has been added.

2/16/25 - Project created. This includes the creation of main.py, which separates a .lvb file into four distinct layers (five counting name layer) and separates the layers into entities. All entities also utilize the fifth layer, which is exclusively used for the storing of entity names.

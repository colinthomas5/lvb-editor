# lvb-editor
A basic editor for .lvb files from games that use the WayForward Engine

## Project Information
The goal of this project is to be a basic level editor for games made by WayForward that use the .lvb level format. This project is made specifically for compatability with .lvb files from Adventure Time: Secret of the Nameless Kingdom, however it may function with over WayForward games that use .lvb files.

## Development Log
2/17/25 - New main.py created, which serves as the GUI for lvb-editor utilizing tkinter. This GUI currently allows you to open a .lvb file, view all four layers, the entities within those layers, and the header info for all entities. Old main.py repurposed into fileHandler.py and still serves the same function as the old main.py.

2/16/25 - Project created. This includes the creation of main.py, which separates a .lvb file into four distinct layers (five counting name layer) and separates the layers into entities. All entities also utilize the fifth layer, which is exclusively used for the storing of entity names.

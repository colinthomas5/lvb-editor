import os
import sys
import io
import fileHandler
import entityTypes
import saveHandler
from tkinter import *
from tkinter import font
from tkinter import filedialog

# Creating root window
root = Tk()
root.title("LVB-Edit: No File")
root.resizable(False, False)

# Determines absolute path to a resource; Functions during dev and after PyInstaller build
def resourcePath(relativePath):
        try:
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath(".")
        return os.path.join(basePath, relativePath)

root.iconbitmap(resourcePath(r'snail.ico'))

layerList = []
global file
file = None

# Clears all values under the "value" column in the properties frame and everything in the type properties frame. This also resets background colors to white. Called when changing entities, layers, and files.
def clearValues():
    valueNameEntry.delete(0, END)
    valueTypeEntry.delete(0, END)
    valueUnknown1Entry.delete(0, END)
    valueIndexEntry.delete(0, END)
    valueUnknown2Entry.delete(0, END)
    valuePosXEntry.delete(0, END)
    valuePosYEntry.delete(0, END)
    valuePosZEntry.delete(0, END)
    valueUnknown3Entry.delete(0, END)
    valueUnknown4Entry.delete(0, END)
    valueUnknown5Entry.delete(0, END)
    valueUnknown6Entry.delete(0, END)
    valueUnknown7Entry.delete(0, END)
    valueUnknown8Entry.delete(0, END)
    valueUnknown9Entry.delete(0, END)
    valueUnknown10Entry.delete(0, END)
    valueHeaderEndEntry.delete(0, END)
    valueTypePropertiesHex.delete("1.0", END)
    valueTypePropertiesText.delete("1.0", END)

    #valueNameEntry.configure(background="white")
    valueUnknown1Entry.configure(background="white")
    #valueIndexEntry.configure(background="white")
    valueUnknown2Entry.configure(background="white")
    valuePosXEntry.configure(background="white")
    valuePosYEntry.configure(background="white")
    valuePosZEntry.configure(background="white")
    valueUnknown3Entry.configure(background="white")
    valueUnknown4Entry.configure(background="white")
    valueUnknown5Entry.configure(background="white")
    valueUnknown6Entry.configure(background="white")
    valueUnknown7Entry.configure(background="white")
    valueUnknown8Entry.configure(background="white")
    valueUnknown9Entry.configure(background="white")
    valueUnknown10Entry.configure(background="white")
    valueTypePropertiesHex.configure(background="white")
    valueTypePropertiesText.configure(background="white")

# Disables all values under the "value" column in the properties frame. Commented values do not support editing (currently or in general, will note)
def disableValues():
    valueNameEntry.configure(state=DISABLED) # Changing name of entity not currently supported
    valueTypeEntry.configure(state=DISABLED) # Type can not be changed
    valueUnknown1Entry.configure(state=DISABLED)
    valueIndexEntry.configure(state=DISABLED) # Changing of order in layers not currently supported
    valueUnknown2Entry.configure(state=DISABLED)
    valuePosXEntry.configure(state=DISABLED)
    valuePosYEntry.configure(state=DISABLED)
    valuePosZEntry.configure(state=DISABLED)
    valueUnknown3Entry.configure(state=DISABLED)
    valueUnknown4Entry.configure(state=DISABLED)
    valueUnknown5Entry.configure(state=DISABLED)
    valueUnknown6Entry.configure(state=DISABLED)
    valueUnknown7Entry.configure(state=DISABLED)
    valueUnknown8Entry.configure(state=DISABLED)
    valueUnknown9Entry.configure(state=DISABLED)
    valueUnknown10Entry.configure(state=DISABLED)
    valueHeaderEndEntry.configure(state=DISABLED) # Header End can not be changed
    valueTypePropertiesHex.configure(state=DISABLED)
    valueTypePropertiesText.configure(state=DISABLED)

# Enables all values under the "value" column in the properties frame. Commented values do not support editing (currently or in general, will note)
def enableValues():
    valueNameEntry.configure(state=NORMAL) # Changing name of entity not currently supported
    valueTypeEntry.configure(state=NORMAL) # Type can not be changed
    valueUnknown1Entry.configure(state=NORMAL)
    valueIndexEntry.configure(state=NORMAL) # Changing of order in layers not currently supported
    valueUnknown2Entry.configure(state=NORMAL)
    valuePosXEntry.configure(state=NORMAL)
    valuePosYEntry.configure(state=NORMAL)
    valuePosZEntry.configure(state=NORMAL)
    valueUnknown3Entry.configure(state=NORMAL)
    valueUnknown4Entry.configure(state=NORMAL)
    valueUnknown5Entry.configure(state=NORMAL)
    valueUnknown6Entry.configure(state=NORMAL)
    valueUnknown7Entry.configure(state=NORMAL)
    valueUnknown8Entry.configure(state=NORMAL)
    valueUnknown9Entry.configure(state=NORMAL)
    valueUnknown10Entry.configure(state=NORMAL)
    valueHeaderEndEntry.configure(state=NORMAL) # Header End can not be changed
    valueTypePropertiesHex.configure(state=NORMAL)
    valueTypePropertiesText.configure(state=NORMAL)

# Function for opening a .lvb file. Command opens the file, makes a list of the layers from the file for the user to modify, then closes the file. The file is reopened for saving during saveFile()
def openFile():
    global file
    global filePath
    global fileName
    filePath = filedialog.askopenfilename(title="Select .lvb or .pak file", filetypes=[("*.lvb", ".lvb"), ("*.pak", ".pak")])
    try:
        file = open(filePath, 'rb')
        fileExtension = filePath.split(".", 1)[1]
        openLevel = fileHandler.openLevelFile(file, fileExtension)
        fileName = os.path.split(filePath)[1]
    except FileNotFoundError:
        print("No file was selected; The current file will remain open.")
        return
    except OSError:
        print("The selected file is unable to be modified; The current file will remain open.")
        return
    layerListbox.event_generate("<<ListboxUnselect>>")
    entityListbox.event_generate("<<ListboxUnselect>>")
    layerListbox.delete(0, END)
    entityListbox.delete(0, END)
    clearValues()
    global lvbType
    lvbType = openLevel[0]
    showProperties(lvbType)
    global layerList
    layerList = openLevel[1]
    global fileOffset
    fileOffset = openLevel[2]
    global originalLayerList
    originalLayerList = layerList
    layerNumber=1
    for Layer in layerList:
        if Layer.type == "entity":
            layerListbox.insert(END, "Layer " + str(layerNumber))
            layerNumber+=1
    layerListbox.select_set(0)
    layerListbox.event_generate("<<ListboxSelect>>")
    root.title("LVB-Edit: " + fileName)
    global fileChanges
    fileChanges = []
    file.close()
    closeFileButton.configure(state=NORMAL)
    entitySearchEntry.configure(state=NORMAL)
    print(fileName + ": File opened.")

# Function for closing the currently-open .lvb file. Now that the file is closed during openFile() and reopened during saveFile(), this only has a visual purpose
def closeFile():
    layerListbox.event_generate("<<ListboxUnselect>>")
    entityListbox.event_generate("<<ListboxUnselect>>")
    #file.close() # File now closed during openFile() and reopened during saveFile() for saving
    layerListbox.delete(0, END)
    entityListbox.delete(0, END)
    entitySearchEntry.delete(0, END)
    clearValues()
    disableValues()
    clearProperties()
    global currentEntity
    global selectedLayer
    currentEntity = None
    selectedLayer = None
    closeFileButton.configure(state=DISABLED)
    saveFileButton.configure(state=DISABLED)
    entitySearchEntry.configure(state=DISABLED)
    root.title("LVB-Edit: No File")
    global file
    file = None
    global fileName
    print(fileName + ": File closed.")

# Function to save the currently-open .lvb file. Opens the file with write permissions, save changes, then closes the file again.
def saveFile():
    global layerList
    global fileChanges
    global file
    global fileOffset
    global filePath
    global fileName
    file = open(filePath, 'r+b')
    saveHandler.saveLevelFile(layerList, fileChanges, file, fileOffset)
    file.close()
    fileChanges.clear()
    saveFileButton.configure(state=DISABLED)
    print(fileName + ": File saved.")

# Frame that holds open and close file buttons
fileButtonFrame = LabelFrame(root, padx=5, pady=5)
fileButtonFrame.grid(row=0, column=0, columnspan=3, sticky="W")

# Button to open a .lvb file
openFileButton = Button(fileButtonFrame, text="Open File", state=NORMAL, padx=10, pady=5, command=openFile)
openFileButton.grid(row=0, column=0)

# Button to close a .lvb file
closeFileButton = Button(fileButtonFrame, text="Close File", state=DISABLED, padx=10, pady=5, command=closeFile)
closeFileButton.grid(row=0, column=1)

# Button to close a .lvb file
saveFileButton = Button(fileButtonFrame, text="Save File", state=DISABLED, padx=10, pady=5, command=saveFile)
saveFileButton.grid(row=0, column=2)

# Section to print the terminal to users. This serves to give the user feedback on what actions they are taking
systemMessageFrame = LabelFrame(root, text="System Messages", padx=5, pady=5)
systemMessageFrame.grid(row=3, column=0, columnspan=6, sticky="EW")

class OutputRedirector(io.TextIOBase):
    def __init__(self, textWidget):
        self.textWidget = textWidget

    def write(self, string):
        self.textWidget.insert(END, string)
        self.textWidget.see(END)  # Auto-scroll to the bottom

    def flush(self):
        pass

systemMessageText = Text(systemMessageFrame, height=5, width=108)
systemMessageText.grid(row=0, column=1, sticky="EW")
systemMessageText.bind("<Key>", lambda e: "break")
sys.stdout = OutputRedirector(systemMessageText)

# Scrollbar for above text
systemMessageScrollbar = Scrollbar(systemMessageFrame, orient="vertical", command=systemMessageText.yview)
systemMessageScrollbar.grid(row=0, column=0, sticky="NS")
systemMessageText.configure(yscrollcommand=systemMessageScrollbar.set)

# Frame that shows all entity layers
layerFrame = LabelFrame(root, text="Layers", padx=5, pady=5)
layerFrame.grid(row=2, column=0, sticky="W")

# Frame that shows all entities in a layer
entityFrame = LabelFrame(root, text="Entities", padx=5, pady=5)
entityFrame.grid(row=2, column=1, sticky="W")

# Causes the values Entry widgets to populate with information about each Entity. This is long and messy.
def onEntitySelect():
    global selectedLayer
    if entityListbox.curselection():
        enableValues()
        clearValues()
    for selection in entityListbox.curselection():
        global currentEntity
        currentEntity = selectedLayer.entityList[selection]
        refreshValues()

# Refreshes all values for the current entity
def refreshValues():
    global currentEntity
    clearValues()
    valueNameEntry.insert(0, currentEntity.name)
    valueTypeEntry.insert(0, entityTypes.getTypeName(currentEntity.type, lvbType))
    valueUnknown1Entry.insert(0, currentEntity.unknown1)
    valueIndexEntry.insert(0, currentEntity.index)
    valueUnknown2Entry.insert(0, currentEntity.unknown2)
    valuePosXEntry.insert(0, currentEntity.posX)
    valuePosYEntry.insert(0, currentEntity.posY)
    valuePosZEntry.insert(0, currentEntity.posZ)
    valueUnknown3Entry.insert(0, currentEntity.unknown3)
    valueUnknown4Entry.insert(0, currentEntity.unknown4)
    valueUnknown5Entry.insert(0, currentEntity.unknown5)
    valueUnknown6Entry.insert(0, currentEntity.unknown6)
    valueUnknown7Entry.insert(0, currentEntity.unknown7)
    valueUnknown8Entry.insert(0, currentEntity.unknown8)
    valueUnknown9Entry.insert(0, currentEntity.unknown9)
    valueUnknown10Entry.insert(0, currentEntity.unknown10)
    valueHeaderEndEntry.insert(0, currentEntity.headerEnd)
    propertiesTagColor = "white"
    propertiesTagCount = 0
    typeProperties = currentEntity.typeProperties
    for char in typeProperties:
        if propertiesTagCount == 2:
            propertiesTagCount = 0
            if propertiesTagColor == "white":
                propertiesTagColor = "gray"
            elif propertiesTagColor == "gray":
                propertiesTagColor = "white"
        valueTypePropertiesHex.insert(END, char, propertiesTagColor)
        propertiesTagCount+=1
    #valueTypePropertiesHex.insert("1.0", currentEntity.typeProperties)
    propertiesTagColor = "white"
    propertiesTagCount = 0
    typeProperties = bytearray.fromhex(currentEntity.typeProperties).decode('cp1252').replace('\x00', '•')
    for char in typeProperties:
        if propertiesTagCount == 1:
            propertiesTagCount = 0
            if propertiesTagColor == "white":
                propertiesTagColor = "gray"
            elif propertiesTagColor == "gray":
                propertiesTagColor = "white"
        valueTypePropertiesText.insert(END, char, propertiesTagColor)
        propertiesTagCount+=1
    #valueTypePropertiesText.insert("1.0", bytearray.fromhex(currentEntity.typeProperties).decode('cp1252').replace('\x00', '•'))

# Listbox that shows all entity layers
entityListbox = Listbox(entityFrame, selectmode = SINGLE, width=40, height=20)
entityListbox.grid(row=1, column=0, columnspan=2, sticky="W")
entityListbox.bind("<<ListboxSelect>>", lambda e: onEntitySelect())
entityListbox.bind("<<Activate>>", lambda e: onEntitySelect())

# Scrollbar for above listbox
entityScrollbar = Scrollbar(entityFrame, orient="vertical", command=entityListbox.yview)
entityScrollbar.grid(row=1, column=2, sticky="NS")
entityListbox.configure(yscrollcommand=entityScrollbar.set)

# Searches current values in the entity list to jump to the first entity that matches what is written in entitySearchEntry
def entitySearch(searchTerm):
    global entitySearchLastEntry
    global entitySearchLastIndex
    if entitySearchLastEntry == searchTerm and len(entityListbox.curselection()) != 0 and entitySearchLastIndex == entityListbox.curselection()[0]:
        entityIndex = entitySearchLastIndex + 1
    else:
        entityIndex = 0
    entries = entityListbox.get(entityIndex, END)
    for entity in entries:
        if searchTerm.lower() in entity.decode().lower():
            entityListbox.selection_clear(0, END)
            entityListbox.selection_set(entityIndex)
            entityListbox.see(entityIndex)
            entityListbox.activate(entityIndex)
            onEntitySelect()
            entitySearchLastEntry = searchTerm
            entitySearchLastIndex = entityIndex
            return
        entityIndex+=1
    entitySearchEntry.configure(background = "red")

entitySearchLabel = Label(entityFrame, text="Search:")
entitySearchLabel.grid(row=0, column=0, sticky="E")

# Entry widget that allows for searching through the layer based on entity name. Pressing enter once searches the typed term, and pressing enter more times while still on the same entity will go to the next applicable entity for the typed term
global entitySearchLastEntry
entitySearchLastEntry = ""
global entitySearchLastIndex
entitySearchLastIndex = 0
entitySearchEntry = Entry(entityFrame, width=31, state=DISABLED)
entitySearchEntry.grid(row=0, column=1, sticky="E")
entitySearchEntry.bind("<Return>", lambda e: entitySearch(entitySearchEntry.get()))
entitySearchEntry.bind("<FocusOut>", lambda e: entitySearchEntry.configure(background="white"))
entitySearchEntry.bind("<Key>", lambda e: entitySearchEntry.configure(background="white"))

# Causes the Entity listbox to populate with entities from a given layer when a layer is selected in the Layer listbox
def onLayerSelect(self):
    global layerList
    if layerListbox.curselection():
        entityListbox.delete(0, END)
        clearValues()
        disableValues()
        for selection in layerListbox.curselection():
            currentLayer = int(selection)
            global selectedLayer
            selectedLayer = layerList[currentLayer]
            for entity in selectedLayer.entityList:
                entityListbox.insert(END, entity.name)

# Refreshes the entity list. Used when updating any values in an entity. Makes sure names dynamically update in entity list
## Currently not referenced, as the main purpose would be to dynamically update names in layers and renaming entities is not currently supported.
def entityListRefresh():
    entityScrollbar.configure(state=DISABLED) # The "state" option does not exist on scrollbars. However for some reason, this fixes a bug where the scrollbar would scroll back to the top on every entityListRefresh(), so it'll stay here despite throwing internal errors
    global selectedLayer
    global currentEntity
    tempEntity = currentEntity
    entityListbox.delete(0, END)
    for Entity in selectedLayer.entityList:
        entityListbox.insert(END, Entity.name)
    currentEntity = tempEntity

# Listbox that shows all entity layers
layerListbox = Listbox(layerFrame, selectmode = SINGLE, width=10, height=20)
layerListbox.grid(row=0, column=0, sticky="W")
layerListbox.bind("<<ListboxSelect>>", onLayerSelect)

# Frame that holds both property and value fields for properties that all entities have, regardless of type
propertyFrame = LabelFrame(root, text="Properties", padx=5, pady=2)
propertyFrame.grid(row=2, column=2, sticky="W")

# List of properties that each entity has despite type
propertyLabel = Label(propertyFrame, text="Property", justify=CENTER)
propertyLabel.grid(row=0, column=0)
propertyLabelFrame = LabelFrame(propertyFrame, width=8)
propertyLabelFrame.grid(row=1, column=0, sticky="NS")

# Show list of properties next to the editable values. This method sucks and uses so many lines but sadly using a listbox has the properties and values not line up so this was my best implementation of this.
property1Entry = Entry(propertyLabelFrame, width=12)
property1Entry.bind("<Key>", lambda e: "break")
property1Entry.pack()

property2Entry = Entry(propertyLabelFrame, width=12)
property2Entry.bind("<Key>", lambda e: "break")
property2Entry.pack()

property3Entry = Entry(propertyLabelFrame, width=12)
property3Entry.bind("<Key>", lambda e: "break")
property3Entry.pack()

property4Entry = Entry(propertyLabelFrame, width=12)
property4Entry.bind("<Key>", lambda e: "break")
property4Entry.pack()

property5Entry = Entry(propertyLabelFrame, width=12)
property5Entry.bind("<Key>", lambda e: "break")
property5Entry.pack()

property6Entry = Entry(propertyLabelFrame, width=12)
property6Entry.bind("<Key>", lambda e: "break")
property6Entry.pack()

property7Entry = Entry(propertyLabelFrame, width=12)
property7Entry.bind("<Key>", lambda e: "break")
property7Entry.pack()

property8Entry = Entry(propertyLabelFrame, width=12)
property8Entry.bind("<Key>", lambda e: "break")
property8Entry.pack()

property9Entry = Entry(propertyLabelFrame, width=12)
property9Entry.bind("<Key>", lambda e: "break")
property9Entry.pack()

property10Entry = Entry(propertyLabelFrame, width=12)
property10Entry.bind("<Key>", lambda e: "break")
property10Entry.pack()

property11Entry = Entry(propertyLabelFrame, width=12)
property11Entry.bind("<Key>", lambda e: "break")
property11Entry.pack()

property12Entry = Entry(propertyLabelFrame, width=12)
property12Entry.bind("<Key>", lambda e: "break")
property12Entry.pack()

property13Entry = Entry(propertyLabelFrame, width=12)
property13Entry.bind("<Key>", lambda e: "break")
property13Entry.pack()

property14Entry = Entry(propertyLabelFrame, width=12)
property14Entry.bind("<Key>", lambda e: "break")
property14Entry.pack()

property15Entry = Entry(propertyLabelFrame, width=12)
property15Entry.bind("<Key>", lambda e: "break")
property15Entry.pack()

property16Entry = Entry(propertyLabelFrame, width=12)
property16Entry.bind("<Key>", lambda e: "break")
property16Entry.pack()

propertyHeaderEndEntry = Entry(propertyLabelFrame, width=12)
propertyHeaderEndEntry.insert(16, "HeaderEnd")
propertyHeaderEndEntry.bind("<Key>", lambda e: "break")
#propertyHeaderEndEntry.pack() # Unable to be edited so not presented to user

def showProperties(type):
    if type == 1: #Not researched yet; Using values from Type 2
        property1Entry.insert(0, "Name")
        property2Entry.insert(1, "Type")
        property3Entry.insert(2, "Unknown1")
        property4Entry.insert(3, "Index")
        property5Entry.insert(4, "Unknown2")
        property6Entry.insert(5, "PositionX")
        property7Entry.insert(6, "PositionY")
        property8Entry.insert(7, "PositionZ")
        property9Entry.insert(8, "Unknown3")
        property10Entry.insert(9, "Unknown4")
        property11Entry.insert(10, "Unknown5")
        property12Entry.insert(11, "Unknown6")
        property13Entry.insert(12, "Unknown7")
        property14Entry.insert(13, "Unknown8")
        property15Entry.insert(14, "Unknown9")
        property16Entry.insert(15, "Unknown10")
    if type == 2:
        property1Entry.insert(0, "Name")
        property2Entry.insert(1, "Type")
        property3Entry.insert(2, "Unknown1")
        property4Entry.insert(3, "Index")
        property5Entry.insert(4, "Unknown2")
        property6Entry.insert(5, "PositionX")
        property7Entry.insert(6, "PositionY")
        property8Entry.insert(7, "PositionZ")
        property9Entry.insert(8, "Unknown3")
        property10Entry.insert(9, "Unknown4")
        property11Entry.insert(10, "Unknown5")
        property12Entry.insert(11, "Unknown6")
        property13Entry.insert(12, "Unknown7")
        property14Entry.insert(13, "Unknown8")
        property15Entry.insert(14, "Unknown9")
        property16Entry.insert(15, "Unknown10")

def clearProperties():
    property1Entry.delete(0, END)
    property2Entry.delete(0, END)
    property3Entry.delete(0, END)
    property4Entry.delete(0, END)
    property5Entry.delete(0, END)
    property6Entry.delete(0, END)
    property7Entry.delete(0, END)
    property8Entry.delete(0, END)
    property9Entry.delete(0, END)
    property10Entry.delete(0, END)
    property11Entry.delete(0, END)
    property12Entry.delete(0, END)
    property13Entry.delete(0, END)
    property14Entry.delete(0, END)
    property15Entry.delete(0, END)
    property16Entry.delete(0, END)

# Writes any values changed back to the currently-selected entity object
def writeValue(property, entryBox, value):
    global currentEntity
    for key in currentEntity.__dict__.keys():
            if key == property:
                if len(value) == len(currentEntity.__dict__.get(key)):
                    try:
                        int(value, 16)
                    except ValueError:
                        refreshValues()
                        entryBox.configure(background = "red")
                        print(currentEntity.name.decode('cp1252') + ": The value of " + property + " was not updated; Value of \"" + value + "\" is invalid.")
                        return
                    if currentEntity.__dict__.get(key) != value:
                        print(currentEntity.name.decode('cp1252') + ": Value of " + property + " updated from \"" + currentEntity.__dict__.get(key) + "\" to \"" + value + "\".")
                        currentEntity.__dict__.update({key : value})
                        if len(fileChanges) == 0:
                            fileChanges.append(currentEntity)
                        else:
                            for entity in fileChanges:
                                if entity != currentEntity:
                                    fileChanges.append(currentEntity)
                        saveFileButton.configure(state=NORMAL)
                else:
                    refreshValues()
                    entryBox.configure(background = "red")
                    print(currentEntity.name.decode('cp1252') + ": The value of " + property + " was not updated; Length of \"" + value + "\" is invalid.")
                    return       
    refreshValues()

        #entityListRefresh() # Commented out due to not having a functional purpose until renaming entities is a function of this program

# List of Entries for viewing and modifying entity properties. This is also messy like the property Entries but maybe I'll fix it when Nova yells at me later about it. (Hi Nova :3)
# Also the Entries with the events commented out are not editable, but should be one day.
valueLabel = Label(propertyFrame, text="Value", justify=CENTER)
valueLabel.grid(row=0, column=1)
valueFrame = LabelFrame(propertyFrame)
valueFrame.grid(row=1, column=1)

valueNameEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
#valueNameEntry.bind("<FocusOut>", lambda e: valueNameEntry.configure(background="white"))
#valueNameEntry.bind("<FocusOut>", lambda e: writeValue("name", valueNameEntry, bytes(valueNameEntry.get(), "utf-8")), add="+")
#valueNameEntry.bind("<Return>", lambda e: writeValue("name", valueNameEntry, bytes(valueNameEntry.get(), "utf-8")))
#valueNameEntry.bind("<Key>", lambda e: valueNameEntry.configure(background="white"))
#valueNameEntry.bind("<Button-1>", lambda e: valueNameEntry.configure(background="white"))
valueNameEntry.bind("<Key>", lambda e: "break")
valueNameEntry.pack()

valueTypeEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
valueTypeEntry.bind("<Key>", lambda e: "break")
valueTypeEntry.pack()

valueUnknown1Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown1Entry.bind("<FocusOut>", lambda e: valueUnknown1Entry.configure(background="white"))
valueUnknown1Entry.bind("<FocusOut>", lambda e: writeValue("unknown1", valueUnknown1Entry, valueUnknown1Entry.get()), add="+")
valueUnknown1Entry.bind("<Return>", lambda e: writeValue("unknown1", valueUnknown1Entry, valueUnknown1Entry.get()))
valueUnknown1Entry.bind("<Key>", lambda e: valueUnknown1Entry.configure(background="white"))
valueUnknown1Entry.bind("<Button-1>", lambda e: valueUnknown1Entry.configure(background="white"))
valueUnknown1Entry.pack()

valueIndexEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
#valueIndexEntry.bind("<FocusOut>", lambda e: valueIndexEntry.configure(background="white"))
#valueIndexEntry.bind("<FocusOut>", lambda e: writeValue("index", valueIndexEntry, valueIndexEntry.get()), add="+")
#valueIndexEntry.bind("<Return>", lambda e: writeValue("index", valueIndexEntry, valueIndexEntry.get()))
#valueIndexEntry.bind("<Key>", lambda e: valueIndexEntry.configure(background="white"))
#valueIndexEntry.bind("<Button-1>", lambda e: valueIndexEntry.configure(background="white"))
valueIndexEntry.bind("<Key>", lambda e: "break")
valueIndexEntry.pack()

valueUnknown2Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown2Entry.bind("<FocusOut>", lambda e: valueUnknown2Entry.configure(background="white"))
valueUnknown2Entry.bind("<FocusOut>", lambda e: writeValue("unknown2", valueUnknown2Entry, valueUnknown2Entry.get()), add="+")
valueUnknown2Entry.bind("<Return>", lambda e: writeValue("unknown2", valueUnknown2Entry, valueUnknown2Entry.get()))
valueUnknown2Entry.bind("<Key>", lambda e: valueUnknown2Entry.configure(background="white"))
valueUnknown2Entry.bind("<Button-1>", lambda e: valueUnknown2Entry.configure(background="white"))
valueUnknown2Entry.pack()

valuePosXEntry = Entry(valueFrame, width=30, state=DISABLED)
valuePosXEntry.bind("<FocusOut>", lambda e: valuePosXEntry.configure(background="white"))
valuePosXEntry.bind("<FocusOut>", lambda e: writeValue("posX", valuePosXEntry, valuePosXEntry.get()), add="+")
valuePosXEntry.bind("<Return>", lambda e: writeValue("posX", valuePosXEntry, valuePosXEntry.get()))
valuePosXEntry.bind("<Key>", lambda e: valuePosXEntry.configure(background="white"))
valuePosXEntry.bind("<Button-1>", lambda e: valuePosXEntry.configure(background="white"))
valuePosXEntry.pack()

valuePosYEntry = Entry(valueFrame, width=30, state=DISABLED)
valuePosYEntry.bind("<FocusOut>", lambda e: valuePosYEntry.configure(background="white"))
valuePosYEntry.bind("<FocusOut>", lambda e: writeValue("posY", valuePosYEntry, valuePosYEntry.get()), add="+")
valuePosYEntry.bind("<Return>", lambda e: writeValue("posY", valuePosYEntry, valuePosYEntry.get()))
valuePosYEntry.bind("<Key>", lambda e: valuePosYEntry.configure(background="white"))
valuePosYEntry.bind("<Button-1>", lambda e: valuePosYEntry.configure(background="white"))
valuePosYEntry.pack()

valuePosZEntry = Entry(valueFrame, width=30, state=DISABLED)
valuePosZEntry.bind("<FocusOut>", lambda e: valuePosZEntry.configure(background="white"))
valuePosZEntry.bind("<FocusOut>", lambda e: writeValue("posZ", valuePosZEntry, valuePosZEntry.get()), add="+")
valuePosZEntry.bind("<Return>", lambda e: writeValue("posZ", valuePosZEntry, valuePosZEntry.get()))
valuePosZEntry.bind("<Key>", lambda e: valuePosZEntry.configure(background="white"))
valuePosZEntry.bind("<Button-1>", lambda e: valuePosZEntry.configure(background="white"))
valuePosZEntry.pack()

valueUnknown3Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown3Entry.bind("<FocusOut>", lambda e: valueUnknown3Entry.configure(background="white"))
valueUnknown3Entry.bind("<FocusOut>", lambda e: writeValue("unknown3", valueUnknown3Entry, valueUnknown3Entry.get()), add="+")
valueUnknown3Entry.bind("<Return>", lambda e: writeValue("unknown3", valueUnknown3Entry, valueUnknown3Entry.get()))
valueUnknown3Entry.bind("<Key>", lambda e: valueUnknown3Entry.configure(background="white"))
valueUnknown3Entry.bind("<Button-1>", lambda e: valueUnknown3Entry.configure(background="white"))
valueUnknown3Entry.pack()

valueUnknown4Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown4Entry.bind("<FocusOut>", lambda e: valueUnknown4Entry.configure(background="white"))
valueUnknown4Entry.bind("<FocusOut>", lambda e: writeValue("unknown4", valueUnknown4Entry, valueUnknown4Entry.get()), add="+")
valueUnknown4Entry.bind("<Return>", lambda e: writeValue("unknown4", valueUnknown4Entry, valueUnknown4Entry.get()))
valueUnknown4Entry.bind("<Key>", lambda e: valueUnknown4Entry.configure(background="white"))
valueUnknown4Entry.bind("<Button-1>", lambda e: valueUnknown4Entry.configure(background="white"))
valueUnknown4Entry.pack()

valueUnknown5Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown5Entry.bind("<FocusOut>", lambda e: valueUnknown5Entry.configure(background="white"))
valueUnknown5Entry.bind("<FocusOut>", lambda e: writeValue("unknown5", valueUnknown5Entry, valueUnknown5Entry.get()), add="+")
valueUnknown5Entry.bind("<Return>", lambda e: writeValue("unknown5", valueUnknown5Entry, valueUnknown5Entry.get()))
valueUnknown5Entry.bind("<Key>", lambda e: valueUnknown5Entry.configure(background="white"))
valueUnknown5Entry.bind("<Button-1>", lambda e: valueUnknown5Entry.configure(background="white"))
valueUnknown5Entry.pack()

valueUnknown6Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown6Entry.bind("<FocusOut>", lambda e: valueUnknown6Entry.configure(background="white"))
valueUnknown6Entry.bind("<FocusOut>", lambda e: writeValue("unknown6", valueUnknown6Entry, valueUnknown6Entry.get()), add="+")
valueUnknown6Entry.bind("<Return>", lambda e: writeValue("unknown6", valueUnknown6Entry, valueUnknown6Entry.get()))
valueUnknown6Entry.bind("<Key>", lambda e: valueUnknown6Entry.configure(background="white"))
valueUnknown6Entry.bind("<Button-1>", lambda e: valueUnknown6Entry.configure(background="white"))
valueUnknown6Entry.pack()

valueUnknown7Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown7Entry.bind("<FocusOut>", lambda e: valueUnknown7Entry.configure(background="white"))
valueUnknown7Entry.bind("<FocusOut>", lambda e: writeValue("unknown7", valueUnknown7Entry, valueUnknown7Entry.get()), add="+")
valueUnknown7Entry.bind("<Return>", lambda e: writeValue("unknown7", valueUnknown7Entry, valueUnknown7Entry.get()))
valueUnknown7Entry.bind("<Key>", lambda e: valueUnknown7Entry.configure(background="white"))
valueUnknown7Entry.bind("<Button-1>", lambda e: valueUnknown7Entry.configure(background="white"))
valueUnknown7Entry.pack()

valueUnknown8Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown8Entry.bind("<FocusOut>", lambda e: valueUnknown8Entry.configure(background="white"))
valueUnknown8Entry.bind("<FocusOut>", lambda e: writeValue("unknown8", valueUnknown8Entry, valueUnknown8Entry.get()), add="+")
valueUnknown8Entry.bind("<Return>", lambda e: writeValue("unknown8", valueUnknown8Entry, valueUnknown8Entry.get()))
valueUnknown8Entry.bind("<Key>", lambda e: valueUnknown8Entry.configure(background="white"))
valueUnknown8Entry.bind("<Button-1>", lambda e: valueUnknown8Entry.configure(background="white"))
valueUnknown8Entry.pack()

valueUnknown9Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown9Entry.bind("<FocusOut>", lambda e: valueUnknown9Entry.configure(background="white"))
valueUnknown9Entry.bind("<FocusOut>", lambda e: writeValue("unknown9", valueUnknown9Entry, valueUnknown9Entry.get()), add="+")
valueUnknown9Entry.bind("<Return>", lambda e: writeValue("unknown9", valueUnknown9Entry, valueUnknown9Entry.get()))
valueUnknown9Entry.bind("<Key>", lambda e: valueUnknown9Entry.configure(background="white"))
valueUnknown9Entry.bind("<Button-1>", lambda e: valueUnknown9Entry.configure(background="white"))
valueUnknown9Entry.pack()

valueUnknown10Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown10Entry.bind("<FocusOut>", lambda e: valueUnknown10Entry.configure(background="white"))
valueUnknown10Entry.bind("<FocusOut>", lambda e: writeValue("unknown10", valueUnknown10Entry, valueUnknown10Entry.get()), add="+")
valueUnknown10Entry.bind("<Return>", lambda e: writeValue("unknown10", valueUnknown10Entry, valueUnknown10Entry.get()))
valueUnknown10Entry.bind("<Key>", lambda e: valueUnknown10Entry.configure(background="white"))
valueUnknown10Entry.bind("<Button-1>", lambda e: valueUnknown10Entry.configure(background="white"))
valueUnknown10Entry.pack()

valueHeaderEndEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
valueHeaderEndEntry.bind("<Key>", lambda e: "break")
#valueHeaderEndEntry.pack() # Unable to be edited so not presented to user

# Monospaced font that is used for the type properties windows
try:
    monoFont = font.Font(family="Courier New", size=12)
except TclError:
    monoFont = font.Font(family="Monospace", size=12)
    print("Courier New font not installed; Value in \"Type Properties\" window may not be aligned properly.")

# Frame that holds both property and value fields for properties specific to types
typePropertiesFrame = LabelFrame(root, text="Type Properties", padx=5, pady=3)
typePropertiesFrame.grid(row=2, column=3, sticky="W")

# Type properties are shown using two text boxes: One in hex and one encoded into text. This allows the user to edit certain type properties either by changing hex values or writing in names in text depending on the situation.
valueTypePropertiesHex = Text(typePropertiesFrame, height=18, width=16, state=DISABLED, font=monoFont)
valueTypePropertiesHex.grid(row=0, column=0)
valueTypePropertiesHex.tag_configure("white", background="white")
valueTypePropertiesHex.tag_configure("gray", background="lightgray")
valueTypePropertiesHex.tag_raise("sel")
valueTypePropertiesHex.bind("<FocusOut>", lambda e: valueTypePropertiesHex.configure(background="white"))
valueTypePropertiesHex.bind("<FocusOut>", lambda e: writeValue("typeProperties", valueTypePropertiesHex, valueTypePropertiesHex.get("1.0", END).rstrip('\n')), add="+") # Text widgets automatically put a new line char '\n' at the end of the new lines, so each of these are stripped of their new line chars before being checked during writeValue().
valueTypePropertiesHex.bind("<Return>", lambda e: writeValue("typeProperties", valueTypePropertiesHex, valueTypePropertiesHex.get("1.0", END).rstrip('\n'))) 
valueTypePropertiesHex.bind("<Key>", lambda e: valueTypePropertiesHex.configure(background="white"))
valueTypePropertiesHex.bind("<Button-1>", lambda e: valueTypePropertiesHex.configure(background="white"))

valueTypePropertiesText = Text(typePropertiesFrame, height=18, width=8, state=DISABLED, font=monoFont)
valueTypePropertiesText.grid(row=0, column=1)
valueTypePropertiesText.tag_configure("white", background="white")
valueTypePropertiesText.tag_configure("gray", background="lightgray")
valueTypePropertiesText.tag_raise("sel")
valueTypePropertiesText.bind("<FocusOut>", lambda e: valueTypePropertiesHex.configure(background="white"))
valueTypePropertiesText.bind("<FocusOut>", lambda e: writeValue("typeProperties", valueTypePropertiesText, (valueTypePropertiesText.get("1.0", END).rstrip('\n').replace('•', '\x00').encode('cp1252').hex())), add="+")
valueTypePropertiesText.bind("<Return>", lambda e: writeValue("typeProperties", valueTypePropertiesText, (valueTypePropertiesText.get("1.0", END).rstrip('\n').replace('•', '\x00').encode('cp1252').hex())))
valueTypePropertiesText.bind("<Key>", lambda e: valueTypePropertiesHex.configure(background="white"))
valueTypePropertiesText.bind("<Button-1>", lambda e: valueTypePropertiesHex.configure(background="white"))

# Functions to scroll both the hex and text Text Widgets at the same time. First functions handles the scroll bar, second function handles the mouse wheel
def typePropertiesScrollTogetherBar(*args):
    valueTypePropertiesHex.yview(*args)
    valueTypePropertiesText.yview(*args)

def typePropertiesScrollTogetherWheel(event):
    valueTypePropertiesHex.yview_scroll(int(-1*(event.delta/120)), "units")
    valueTypePropertiesText.yview_scroll(int(-1*(event.delta/120)), "units")
    return "break"

typePropertiesScrollbar = Scrollbar(typePropertiesFrame, orient="vertical")
typePropertiesScrollbar.grid(row=0, column=2, sticky="NS")
typePropertiesScrollbar.configure(command=typePropertiesScrollTogetherBar)
valueTypePropertiesHex.configure(yscrollcommand=typePropertiesScrollbar.set)
valueTypePropertiesText.configure(yscrollcommand=typePropertiesScrollbar.set)

valueTypePropertiesHex.bind("<MouseWheel>", typePropertiesScrollTogetherWheel)
valueTypePropertiesText.bind("<MouseWheel>", typePropertiesScrollTogetherWheel)

# Main loop of program
root.mainloop()
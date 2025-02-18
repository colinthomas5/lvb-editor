import os
import fileHandler
import saveHandler
from tkinter import *
from tkinter import filedialog

# Creating root window
root = Tk()
root.title("LVB-Edit: No File")
root.resizable(False, False)
layerList = []

# Clears all values under the "value" column in the properties frame. Called when changing entities, layers, and files.
def clearValues():
    valueNameEntry.delete(0, END)
    valueTypeEntry.delete(0, END)
    valueUnknown1Entry.delete(0, END)
    valueIndexEntry.delete(0, END)
    valueUnknown2Entry.delete(0, END)
    valuePosXEntry.delete(0, END)
    valuePosYEntry.delete(0, END)
    valuePosZEntry.delete(0, END)
    valueStretchXEntry.delete(0, END)
    valueUnknown4Entry.delete(0, END)
    valueUnknown5Entry.delete(0, END)
    valueUnknown6Entry.delete(0, END)
    valueUnknown7Entry.delete(0, END)
    valueUnknown8Entry.delete(0, END)
    valueUnknown9Entry.delete(0, END)
    valueUnknown10Entry.delete(0, END)
    valueHeaderEndEntry.delete(0, END)

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
    valueStretchXEntry.configure(state=DISABLED)
    valueUnknown4Entry.configure(state=DISABLED)
    valueUnknown5Entry.configure(state=DISABLED)
    valueUnknown6Entry.configure(state=DISABLED)
    valueUnknown7Entry.configure(state=DISABLED)
    valueUnknown8Entry.configure(state=DISABLED)
    valueUnknown9Entry.configure(state=DISABLED)
    valueUnknown10Entry.configure(state=DISABLED)
    valueHeaderEndEntry.configure(state=DISABLED) # Header End can not be changed

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
    valueStretchXEntry.configure(state=NORMAL)
    valueUnknown4Entry.configure(state=NORMAL)
    valueUnknown5Entry.configure(state=NORMAL)
    valueUnknown6Entry.configure(state=NORMAL)
    valueUnknown7Entry.configure(state=NORMAL)
    valueUnknown8Entry.configure(state=NORMAL)
    valueUnknown9Entry.configure(state=NORMAL)
    valueUnknown10Entry.configure(state=NORMAL)
    valueHeaderEndEntry.configure(state=NORMAL) # Header End can not be changed

# Command for opening a .lvb file
def openFile():
    global filePath
    filePath = filedialog.askopenfilename(title="Select .lvb file", filetypes=[("*.lvb", ".lvb")])
    fileName = os.path.split(filePath)[1]
    global file
    layerListbox.event_generate("<<ListboxUnselect>>")
    entityListbox.event_generate("<<ListboxUnselect>>")
    file = open(filePath, 'r+b')
    layerListbox.delete(0, END)
    entityListbox.delete(0, END)
    clearValues()
    global layerList
    layerList = fileHandler.openLVBFile(file)
    global originalLayerList
    originalLayerList = layerList
    layerNumber=1
    for Layer in layerList:
        if Layer.type == "entity":
            layerListbox.insert(END, "Layer "+str(layerNumber))
            layerNumber+=1
    layerListbox.select_set(0)
    layerListbox.event_generate("<<ListboxSelect>>")
    root.title("LVB-Edit: "+fileName)
    global fileChanges
    fileChanges = []

# Command for closing the currently-open .lvb file
def closeFile():
    global file
    layerListbox.event_generate("<<ListboxUnselect>>")
    entityListbox.event_generate("<<ListboxUnselect>>")
    file.close()
    layerListbox.delete(0, END)
    entityListbox.delete(0, END)
    clearValues()
    disableValues()
    global currentEntity
    global selectedLayer
    currentEntity = None
    selectedLayer = None
    root.title("LVB-Edit: No File")

# Function to save the currently-open .lvb file
def saveFile():
    global filePath
    global layerList
    global file
    saveHandler.saveLVBFile(filePath, layerList, fileChanges, file)
    #print("To be implemented")

# Frame that holds open and close file buttons
fileButtonFrame = LabelFrame(root, padx=5, pady=5)
fileButtonFrame.grid(row=0, column=0, columnspan=3, sticky="W")

# Button to open a .lvb file
openFileButton = Button(fileButtonFrame, text="Open File", state=NORMAL, padx=10, pady=5, command=openFile)
openFileButton.grid(row=0, column=0)

# Button to close a .lvb file
closeFileButton = Button(fileButtonFrame, text="Close File", state=NORMAL, padx=10, pady=5, command=closeFile)
closeFileButton.grid(row=0, column=1)

# Button to close a .lvb file
saveFileButton = Button(fileButtonFrame, text="Save File", state=NORMAL, padx=10, pady=5, command=saveFile)
saveFileButton.grid(row=0, column=2)

# Frame that shows all entity layers
layerFrame = LabelFrame(root, text="Layers", padx=5, pady=5)
layerFrame.grid(row=2, column=0, sticky="W")

# Frame that shows all entities in a layer
entityFrame = LabelFrame(root, text="Entities", padx=5, pady=5)
entityFrame.grid(row=2, column=1, sticky="W")

# Causes the values Entry widgets to populate with information about each Entity. This is long and messy.
def onEntitySelect(self):
    global selectedLayer
    if entityListbox.curselection():
        enableValues()
        clearValues()
    for selection in entityListbox.curselection():
        global currentEntity
        currentEntity = selectedLayer.entityList[selection]
        valueNameEntry.insert(0, currentEntity.name)
        valueTypeEntry.insert(1, currentEntity.type)
        valueUnknown1Entry.insert(2, currentEntity.unknown1)
        valueIndexEntry.insert(3, currentEntity.index)
        valueUnknown2Entry.insert(4, currentEntity.unknown2)
        valuePosXEntry.insert(5, currentEntity.posX)
        valuePosYEntry.insert(6, currentEntity.posY)
        valuePosZEntry.insert(7, currentEntity.posZ)
        valueStretchXEntry.insert(8, currentEntity.stretchX)
        valueUnknown4Entry.insert(9, currentEntity.unknown4)
        valueUnknown5Entry.insert(10, currentEntity.unknown5)
        valueUnknown6Entry.insert(11, currentEntity.unknown6)
        valueUnknown7Entry.insert(12, currentEntity.unknown7)
        valueUnknown8Entry.insert(13, currentEntity.unknown8)
        valueUnknown9Entry.insert(14, currentEntity.unknown9)
        valueUnknown10Entry.insert(15, currentEntity.unknown10)
        valueHeaderEndEntry.insert(16, currentEntity.headerEnd)

# Listbox that shows all entity layers
entityListbox = Listbox(entityFrame, width=40, height=21)
entityListbox.grid(row=0, column=1, sticky="W")
entityListbox.bind("<<ListboxSelect>>", onEntitySelect)

# Scrollbar for above listbox
entityScrollbar = Scrollbar(entityFrame, orient="vertical", command=entityListbox.yview)
entityScrollbar.grid(row=0, column=0, sticky="NS")
entityListbox.configure(yscrollcommand=entityScrollbar.set)

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
            for Entity in selectedLayer.entityList:
                entityListbox.insert(END, Entity.name)

# Refreshes the entity list. Used when updating any values in an entity. Makes sure names dynamically update in entity list
def entityListRefresh():
    global selectedLayer
    global currentEntity
    tempEntity = currentEntity
    entityListbox.delete(0, END)
    for Entity in selectedLayer.entityList:
        entityListbox.insert(END, Entity.name)
    currentEntity = tempEntity

# Listbox that shows all entity layers
layerListbox = Listbox(layerFrame, width=10, height=21)
layerListbox.grid(row=0, column=0, sticky="W")
layerListbox.bind("<<ListboxSelect>>", onLayerSelect)

# Frame that holds both property and value fields
propertyFrame = LabelFrame(root, text="Properties", padx=5, pady=4)
propertyFrame.grid(row=2, column=2, sticky="W")

# List of properties that each entity has despite type
propertyLabel = Label(propertyFrame, text="Property", width=8)
propertyLabel.grid(row=0, column=0, sticky="NW")
propertyLabelFrame = LabelFrame(propertyFrame, width=8)
propertyLabelFrame.grid(row=1, column=0, sticky="NS")

# Show list of properties next to the editable values. This method sucks and uses so many lines but sadly using a listbox has the properties and values not line up so this was my best implementation of this.
propertyNameEntry = Entry(propertyLabelFrame, width=12)
propertyNameEntry.insert(0, "Name")
propertyNameEntry.bind("<Key>", lambda e: "break")
propertyNameEntry.pack()

propertyTypeEntry = Entry(propertyLabelFrame, width=12)
propertyTypeEntry.insert(1, "Type")
propertyTypeEntry.bind("<Key>", lambda e: "break")
propertyTypeEntry.pack()

propertyUnknown1Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown1Entry.insert(2, "Unknown1")
propertyUnknown1Entry.bind("<Key>", lambda e: "break")
propertyUnknown1Entry.pack()

propertyIndexEntry = Entry(propertyLabelFrame, width=12)
propertyIndexEntry.insert(3, "Index")
propertyIndexEntry.bind("<Key>", lambda e: "break")
propertyIndexEntry.pack()

propertyUnknown2Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown2Entry.insert(4, "Unknown2")
propertyUnknown2Entry.bind("<Key>", lambda e: "break")
propertyUnknown2Entry.pack()

propertyPosXEntry = Entry(propertyLabelFrame, width=12)
propertyPosXEntry.insert(5, "PositionX")
propertyPosXEntry.bind("<Key>", lambda e: "break")
propertyPosXEntry.pack()

propertyPosYEntry = Entry(propertyLabelFrame, width=12)
propertyPosYEntry.insert(6, "PositionY")
propertyPosYEntry.bind("<Key>", lambda e: "break")
propertyPosYEntry.pack()

propertyPosZEntry = Entry(propertyLabelFrame, width=12)
propertyPosZEntry.insert(7, "PositionZ")
propertyPosZEntry.bind("<Key>", lambda e: "break")
propertyPosZEntry.pack()

propertyStretchXEntry = Entry(propertyLabelFrame, width=12)
propertyStretchXEntry.insert(8, "StretchX")
propertyStretchXEntry.bind("<Key>", lambda e: "break")
propertyStretchXEntry.pack()

propertyUnknown4Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown4Entry.insert(9, "Unknown4")
propertyUnknown4Entry.bind("<Key>", lambda e: "break")
propertyUnknown4Entry.pack()

propertyUnknown5Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown5Entry.insert(10, "Unknown5")
propertyUnknown5Entry.bind("<Key>", lambda e: "break")
propertyUnknown5Entry.pack()

propertyUnknown6Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown6Entry.insert(11, "Unknown6")
propertyUnknown6Entry.bind("<Key>", lambda e: "break")
propertyUnknown6Entry.pack()

propertyUnknown7Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown7Entry.insert(12, "Unknown7")
propertyUnknown7Entry.bind("<Key>", lambda e: "break")
propertyUnknown7Entry.pack()

propertyUnknown8Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown8Entry.insert(13, "Unknown8")
propertyUnknown8Entry.bind("<Key>", lambda e: "break")
propertyUnknown8Entry.pack()

propertyUnknown9Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown9Entry.insert(14, "Unknown9")
propertyUnknown9Entry.bind("<Key>", lambda e: "break")
propertyUnknown9Entry.pack()

propertyUnknown10Entry = Entry(propertyLabelFrame, width=12)
propertyUnknown10Entry.insert(15, "Unknown10")
propertyUnknown10Entry.bind("<Key>", lambda e: "break")
propertyUnknown10Entry.pack()

propertyHeaderEndEntry = Entry(propertyLabelFrame, width=12)
propertyHeaderEndEntry.insert(16, "HeaderEnd")
propertyHeaderEndEntry.bind("<Key>", lambda e: "break")
propertyHeaderEndEntry.pack()

# Writes any values changed back to the currently-selected entity object
def writeValue(property, value):
        global currentEntity
        if (property == "type" and len(value) and int(value, 16)) == 16 or property != "name" and len(value) == 8 and int(value, 16):
            for key in currentEntity.__dict__.keys():
                if key == property:
                    if currentEntity.__dict__.get(key) != value:
                        print(key)
                        print(currentEntity.__dict__.get(key))
                        print(value)
                        currentEntity.__dict__.update({key : value})
                        if len(fileChanges) == 0:
                            fileChanges.append(currentEntity)
                        else:
                            for entity in fileChanges:
                                if entity != currentEntity:
                                    fileChanges.append(currentEntity)
                        print(fileChanges)
        else:
            print("User will be prompted with error message and value will not be changed")
        entityListRefresh()

# List of Entries for viewing and modifying entity properties. This is also messy like the property Entries but maybe I'll fix it when Nova yells at me later about it. (Hi Nova :3)
# Also the Entries with the events commented out are not editable. Name and Index may be editable one day, but Type and Header End will not be.
valueLabel = Label(propertyFrame, text="Value")
valueLabel.grid(row=0, column=1)
valueFrame = LabelFrame(propertyFrame)
valueFrame.grid(row=1, column=1, sticky="NSW")

valueNameEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
#valueNameEntry.bind("<FocusOut>", lambda e: writeValue("name", bytes(valueNameEntry.get(), "utf-8")))
#valueNameEntry.bind("<Return>", lambda e: writeValue("name", bytes(valueNameEntry.get(), "utf-8")))
valueNameEntry.bind("<Key>", lambda e: "break")
valueNameEntry.pack()

valueTypeEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
#valueTypeEntry.bind("<FocusOut>", lambda e: writeValue("type", valueTypeEntry.get()))
#valueTypeEntry.bind("<Return>", lambda e: writeValue("type", valueTypeEntry.get()))
valueTypeEntry.bind("<Key>", lambda e: "break")
valueTypeEntry.pack()

valueUnknown1Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown1Entry.bind("<FocusOut>", lambda e: writeValue("unknown1", valueUnknown1Entry.get()))
valueUnknown1Entry.bind("<Return>", lambda e: writeValue("unknown1", valueUnknown1Entry.get()))
valueUnknown1Entry.pack()

valueIndexEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
#valueIndexEntry.bind("<FocusOut>", lambda e: writeValue("index", valueIndexEntry.get()))
#valueIndexEntry.bind("<Return>", lambda e: writeValue("index", valueIndexEntry.get()))
valueIndexEntry.bind("<Key>", lambda e: "break")
valueIndexEntry.pack()

valueUnknown2Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown2Entry.bind("<FocusOut>", lambda e: writeValue("unknown2", valueUnknown2Entry.get()))
valueUnknown2Entry.bind("<Return>", lambda e: writeValue("unknown2", valueUnknown2Entry.get()))
valueUnknown2Entry.pack()

valuePosXEntry = Entry(valueFrame, width=30, state=DISABLED)
valuePosXEntry.bind("<FocusOut>", lambda e: writeValue("posX", valuePosXEntry.get()))
valuePosXEntry.bind("<Return>", lambda e: writeValue("posX", valuePosXEntry.get()))
valuePosXEntry.pack()

valuePosYEntry = Entry(valueFrame, width=30, state=DISABLED)
valuePosYEntry.bind("<FocusOut>", lambda e: writeValue("posY", valuePosYEntry.get()))
valuePosYEntry.bind("<Return>", lambda e: writeValue("posY", valuePosYEntry.get()))
valuePosYEntry.pack()

valuePosZEntry = Entry(valueFrame, width=30, state=DISABLED)
valuePosZEntry.bind("<FocusOut>", lambda e: writeValue("posZ", valuePosZEntry.get()))
valuePosZEntry.bind("<Return>", lambda e: writeValue("posZ", valuePosZEntry.get()))
valuePosZEntry.pack()

valueStretchXEntry = Entry(valueFrame, width=30, state=DISABLED)
valueStretchXEntry.bind("<FocusOut>", lambda e: writeValue("stretchX", valueStretchXEntry.get()))
valueStretchXEntry.bind("<Return>", lambda e: writeValue("stretchX", valueStretchXEntry.get()))
valueStretchXEntry.pack()

valueUnknown4Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown4Entry.bind("<FocusOut>", lambda e: writeValue("unknown4", valueUnknown4Entry.get()))
valueUnknown4Entry.bind("<Return>", lambda e: writeValue("unknown4", valueUnknown4Entry.get()))
valueUnknown4Entry.pack()

valueUnknown5Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown5Entry.bind("<FocusOut>", lambda e: writeValue("unknown5", valueUnknown5Entry.get()))
valueUnknown5Entry.bind("<Return>", lambda e: writeValue("unknown5", valueUnknown5Entry.get()))
valueUnknown5Entry.pack()

valueUnknown6Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown6Entry.bind("<FocusOut>", lambda e: writeValue("unknown6", valueUnknown6Entry.get()))
valueUnknown6Entry.bind("<Return>", lambda e: writeValue("unknown6", valueUnknown6Entry.get()))
valueUnknown6Entry.pack()

valueUnknown7Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown7Entry.bind("<FocusOut>", lambda e: writeValue("unknown7", valueUnknown7Entry.get()))
valueUnknown7Entry.bind("<Return>", lambda e: writeValue("unknown7", valueUnknown7Entry.get()))
valueUnknown7Entry.pack()

valueUnknown8Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown8Entry.bind("<FocusOut>", lambda e: writeValue("unknown8", valueUnknown8Entry.get()))
valueUnknown8Entry.bind("<Return>", lambda e: writeValue("unknown8", valueUnknown8Entry.get()))
valueUnknown8Entry.pack()

valueUnknown9Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown9Entry.bind("<FocusOut>", lambda e: writeValue("unknown9", valueUnknown9Entry.get()))
valueUnknown9Entry.bind("<Return>", lambda e: writeValue("unknown9", valueUnknown9Entry.get()))
valueUnknown9Entry.pack()

valueUnknown10Entry = Entry(valueFrame, width=30, state=DISABLED)
valueUnknown10Entry.bind("<FocusOut>", lambda e: writeValue("unknown10", valueUnknown10Entry.get()))
valueUnknown10Entry.bind("<Return>", lambda e: writeValue("unknown10", valueUnknown10Entry.get()))
valueUnknown10Entry.pack()

valueHeaderEndEntry = Entry(valueFrame, width=30, state=DISABLED, bg='#f0f0f0')
#valueHeaderEndEntry.bind("<FocusOut>", lambda e: writeValue("headerEnd", valueHeaderEndEntry.get()))
#valueHeaderEndEntry.bind("<Return>", lambda e: writeValue("headerEnd", valueHeaderEndEntry.get()))
valueHeaderEndEntry.bind("<Key>", lambda e: "break")
valueHeaderEndEntry.pack()

# Main loop of program
root.mainloop()
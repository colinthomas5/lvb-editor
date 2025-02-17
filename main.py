import os
import fileHandler
from tkinter import *
from tkinter import filedialog

# Creating root window
root = Tk()
root.title("LVB-Edit: No File")
layerList = []

# Command for opening a .lvb file
def openFile():
    filePath = filedialog.askopenfilename(title="Select .lvb file", filetypes=[("*.lvb", ".lvb")])
    fileName = os.path.split(filePath)[1]
    global file
    file = open(filePath, 'rb')
    layerListbox.delete(0, END)
    entityListbox.delete(0, END)
    global layerList
    layerList = fileHandler.openLVBFile(file)
    layerNumber=1
    for Layer in layerList:
        layerListbox.insert(END, "Layer "+str(layerNumber))
        layerNumber+=1
    layerListbox.select_set(0)
    layerListbox.event_generate("<<ListboxSelect>>")
    root.title("LVB-Edit: "+fileName)
    #currentFileLabel.config(text="Current file: "+fileName)

# Command for closing the currently-open .lvb file
def closeFile():
    global file
    file.close()
    layerListbox.delete(0, END)
    entityListbox.delete(0, END)
    root.title("LVB-Edit: No File")
    #currentFileLabel.config(text="Current file: ")

# Frame that holds open and close file buttons
fileButtonFrame = LabelFrame(root, padx=5, pady=5)
fileButtonFrame.grid(row=0, column=1, sticky="W")

# Button to open a .lvb file
openFileButton = Button(fileButtonFrame, text="Open File", state=NORMAL, padx=30, pady=10, command=openFile)
openFileButton.grid(row=0, column=0)

# Button to close a .lvb file
closeFileButton = Button(fileButtonFrame, text="Close File", state=NORMAL, padx=30, pady=10, command=closeFile)
closeFileButton.grid(row=0, column=1)

# Text that reads what file is currently open. Deprecated in favor of showing currently-open file in window name
#currentFileLabel = Label(root, text="Current file: ")
#currentFileLabel.grid(row=1, column=1, sticky="W")

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
    for selection in entityListbox.curselection():
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
entityListbox = Listbox(entityFrame, width=40, height=20)
entityListbox.grid(row=0, column=1, sticky="W")
entityListbox.bind("<<ListboxSelect>>", onEntitySelect)

entityScrollbar = Scrollbar(entityFrame, orient="vertical", command=entityListbox.yview)
entityScrollbar.grid(row=0, column=0, sticky="NS")
entityListbox.configure(yscrollcommand=entityScrollbar.set)

# Causes the Entity listbox to populate with entities from a given layer when a layer is selected in the Layer listbox
def onLayerSelect(self):
    global layerList
    if layerListbox.curselection():
        entityListbox.delete(0, END)
        for selection in layerListbox.curselection():
            currentLayer = int(selection)
            global selectedLayer
            selectedLayer = layerList[currentLayer]
            for Entity in selectedLayer.entityList:
                entityListbox.insert(END, Entity.name)

# Listbox that shows all entity layers
layerListbox = Listbox(layerFrame, width=10, height=20)
layerListbox.grid(row=0, column=0, sticky="W")
layerListbox.bind("<<ListboxSelect>>", onLayerSelect)

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
propertyPosXEntry.insert(5, "PosX")
propertyPosXEntry.bind("<Key>", lambda e: "break")
propertyPosXEntry.pack()

propertyPosYEntry = Entry(propertyLabelFrame, width=12)
propertyPosYEntry.insert(6, "PosY")
propertyPosYEntry.bind("<Key>", lambda e: "break")
propertyPosYEntry.pack()

propertyPosZEntry = Entry(propertyLabelFrame, width=12)
propertyPosZEntry.insert(7, "PosZ")
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


'''# Listbox that shows all properties that are applicable to all entities, regardles of type
propertyListbox = Listbox(propertyFrame, width=20, height=19)
propertyListbox.insert(0, "Name")
propertyListbox.insert(1, "Type")
propertyListbox.insert(2, "Unknown1")
propertyListbox.insert(3, "Index")
propertyListbox.insert(4, "Unknown2")
propertyListbox.insert(5, "PositionX")
propertyListbox.insert(6, "PositionY")
propertyListbox.insert(7, "PositionZ")
propertyListbox.insert(8, "StretchX")
propertyListbox.insert(9, "Unknown4")
propertyListbox.insert(10, "Unknown5")
propertyListbox.insert(11, "Unknown6")
propertyListbox.insert(12, "Unknown7")
propertyListbox.insert(13, "Unknown8")
propertyListbox.insert(14, "Unknown9")
propertyListbox.insert(15, "Unknown10")
propertyListbox.insert(16, "HeaderEnd")
propertyListbox.grid(row=1, column=0, sticky="W")'''

# List of Entries for viewing and modifying entity properties. This is also messy like the property Entries but maybe I'll fix it when Nova yells at me later about it. (Hi Nova :3)
valueLabel = Label(propertyFrame, text="Value")
valueLabel.grid(row=0, column=1)
valueFrame = LabelFrame(propertyFrame)
valueFrame.grid(row=1, column=1, sticky="NSW")
valueNameEntry = Entry(valueFrame, width=30)
valueNameEntry.pack()
valueTypeEntry = Entry(valueFrame, width=30)
valueTypeEntry.pack()
valueUnknown1Entry = Entry(valueFrame, width=30)
valueUnknown1Entry.pack()
valueIndexEntry = Entry(valueFrame, width=30)
valueIndexEntry.pack()
valueUnknown2Entry = Entry(valueFrame, width=30)
valueUnknown2Entry.pack()
valuePosXEntry = Entry(valueFrame, width=30)
valuePosXEntry.pack()
valuePosYEntry = Entry(valueFrame, width=30)
valuePosYEntry.pack()
valuePosZEntry = Entry(valueFrame, width=30)
valuePosZEntry.pack()
valueStretchXEntry = Entry(valueFrame, width=30)
valueStretchXEntry.pack()
valueUnknown4Entry = Entry(valueFrame, width=30)
valueUnknown4Entry.pack()
valueUnknown5Entry = Entry(valueFrame, width=30)
valueUnknown5Entry.pack()
valueUnknown6Entry = Entry(valueFrame, width=30)
valueUnknown6Entry.pack()
valueUnknown7Entry = Entry(valueFrame, width=30)
valueUnknown7Entry.pack()
valueUnknown8Entry = Entry(valueFrame, width=30)
valueUnknown8Entry.pack()
valueUnknown9Entry = Entry(valueFrame, width=30)
valueUnknown9Entry.pack()
valueUnknown10Entry = Entry(valueFrame, width=30)
valueUnknown10Entry.pack()
valueHeaderEndEntry = Entry(valueFrame, width=30)
valueHeaderEndEntry.pack()

#valueListbox = Listbox(propertyFrame, width=20, height=19)
#valueListbox.insert(0, "Name")
#valueListbox.grid(row=1, column=1, sticky="W")

# Main loop of program
root.mainloop()
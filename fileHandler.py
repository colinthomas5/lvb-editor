import os
# User is prompted to choose the .lvb file to open
# filePath = input("Enter file directory: ")
# file = open(filePath, 'rb')

def openLevelFile(levelFile, fileExtension):

    global file
    file = levelFile

    global fileOffset
    if fileExtension == "lvb":
        fileOffset = 0

    # Since the .lvb file is embedded in the .pak file, we must determine the offset of the .lvb file within the .pak file and .seek() to it
    elif fileExtension == "pak":
        headerSize = int.from_bytes(file.read(4), "little")
        bytesToFind = b'.lvb'
        file.seek(0)
        fileString = file.read()
        extensionLocation = fileString.find(bytesToFind)
        nextFileOffsetLocation = fileString.find(b'END', extensionLocation)
        file.seek(nextFileOffsetLocation+3)
        nextFileOffset = int.from_bytes(file.read(4), "little")
        file.seek(extensionLocation, 0)

        while file.read(3) != b'END':
            file.seek(-4, 1)
        fileOffsetFromHeader = int.from_bytes(file.read(4), "little")
        fileOffset = headerSize + fileOffsetFromHeader + 64
        file.seek(fileOffset)

    # Header of .lvb file is separated and lvb type is determined.
    global header
    global lvbType
    file.seek(8, 1)
    headerSize = int.from_bytes(file.read(4), "little")
    if headerSize == 64:
        lvbType = 1 # Type 1 has four layers (in every observed instance), with the names of entities stored alongside the rest of the entity information
    elif headerSize == 128:
        lvbType = 2 # Type 2 has five layers (in every observed instance), with the first four layers being entities and the fifth layer existing exclusively to store the names of the entities in layers 1-4
    else:
        print("Error: LVB type not identified. The LVB file was not opened.")
    file.seek(fileOffset)
    header = file.read(headerSize)
    
    # Number of layers is determined based on the contents of the header
    layerNumberOfEntities = int.from_bytes(header[4:8], "little")
    layerOffset = int.from_bytes(header[8:12], "little")
    headerSeek = 16
    global layerList
    layerList = []

    # For each defined layer in the header, a list of entities is created and appended to layerList
    while headerSeek < headerSize:
        nextLayerOffset = int.from_bytes(header[headerSeek+8: headerSeek+12], "little")
        if nextLayerOffset == 0:
            nextLayerOffset = None
        if layerOffset != None:
            layer = Layer(layerOffset, nextLayerOffset, layerNumberOfEntities)
            layerNumberOfEntities = int.from_bytes(header[headerSeek: headerSeek+4], "little")
            layerOffset = nextLayerOffset
            layerList.append(layer)
        headerSeek+=16

    return lvbType, layerList, fileOffset

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class Entity1:
    def __init__(self, layer, offset, nextOffset):
        self.offset = hex(offset)
        self.layer = layer
        file.seek(offset + fileOffset, 0)
        self.type = file.read(8).hex()
        self.unknown1 = file.read(4).hex()
        index = file.read(4)
        self.index = index
        self.unknown2 = file.read(4).hex()
        self.posX = file.read(4).hex()
        self.posY = file.read(4).hex()
        self.posZ = file.read(4).hex()
        self.unknown3 = file.read(4).hex()
        self.unknown4 = file.read(4).hex()
        self.unknown5 = file.read(4).hex()
        self.unknown6 = file.read(4).hex()
        self.unknown7 = file.read(4).hex()
        self.unknown8 = file.read(4).hex()
        self.unknown9 = file.read(4).hex()
        self.unknown10 = file.read(4).hex()
        self.headerEnd = file.read(4).hex()
        self.typeProperties = ''
        while file.tell() < (nextOffset + fileOffset):
            self.typeProperties = self.typeProperties + file.read(4).hex()
        nameLocation = int.from_bytes(header[72:76], "little")+((int.from_bytes(index, "little"))*8)
        self.nameLocation = hex(nameLocation)
        file.seek(nameLocation+fileOffset, 0)
        nameOffset = int.from_bytes(file.read(8), "little")
        self.nameOffset = hex(nameOffset)
        file.seek(nameOffset+fileOffset, 0)
        nameLength = int.from_bytes(file.read(4), "little")
        self.nameLength = hex(nameLength)
        self.name = file.read(nameLength)

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class Entity2:
    def __init__(self, layer, offset, nextOffset):
        self.offset = hex(offset)
        self.layer = layer
        file.seek(offset + fileOffset, 0)
        self.type = file.read(8).hex()
        self.unknown1 = file.read(4).hex()
        self.index = int.from_bytes(file.read(4), "little")
        self.unknown2 = file.read(4).hex()
        self.posX = file.read(4).hex()
        self.posY = file.read(4).hex()
        self.posZ = file.read(4).hex()
        self.unknown3 = file.read(4).hex()
        self.unknown4 = file.read(4).hex()
        self.unknown5 = file.read(4).hex()
        self.unknown6 = file.read(4).hex()
        self.unknown7 = file.read(4).hex()
        self.unknown8 = file.read(4).hex()
        self.unknown9 = file.read(4).hex()
        self.unknown10 = file.read(4).hex()
        self.headerEnd = file.read(4).hex()
        self.typeProperties = ''
        while file.tell() < (nextOffset + fileOffset):
            self.typeProperties = self.typeProperties + file.read(4).hex()
        nameLocation = int.from_bytes(header[72:76], "little")+(self.index*8)
        self.nameLocation = hex(nameLocation)
        file.seek(nameLocation+fileOffset, 0)
        nameOffset = int.from_bytes(file.read(8), "little")
        self.nameOffset = hex(nameOffset)
        file.seek(nameOffset+fileOffset, 0)
        nameLength = int.from_bytes(file.read(4), "little")
        self.nameLength = hex(nameLength)
        self.name = file.read(nameLength)

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class EntityN: # LVB Type 2-exclusive entity type
    def __init__(self, layer, offset):
        self.offset = hex(offset)
        self.layer = layer
        file.seek(offset+fileOffset, 0)
        self.length = int.from_bytes(file.read(4), "little")
        self.entry = file.read(self.length).hex()

# Entities are sorted into Layers within .lvb files. Layers start with a table that lists all hex offsets of entities within that layer, followed by the entities. When parsing a layer, the layer object fills a list with all of the entities in that layer while populating all of the information about the entities.
class Layer:
    def __init__(self, offset, nextOffset, numberOfEntities):
        self.offset = offset
        self.numberOfEntities = numberOfEntities
        entityList = []
        self.entityList = entityList
        entityNumber=0
        if nextOffset != None or lvbType == 0:
            self.type = "entity"
            while(entityNumber < numberOfEntities):
                entityLocation = offset + (entityNumber*8) + fileOffset
                file.seek(entityLocation, 0)
                entityOffset = int.from_bytes(file.read(8), "little")
                if entityNumber+1 != numberOfEntities:
                    nextEntityOffset = int.from_bytes(file.read(8), "little")
                else:
                    nextEntityOffset = nextOffset
                if lvbType == 1:
                    entity = Entity1(self, entityOffset, nextEntityOffset)
                elif lvbType == 2:
                    entity = Entity2(self, entityOffset, nextEntityOffset)
                entityList.append(entity)
                entityNumber+=1
        else:
            self.type = "name"
            entityList.clear()
            while(entityNumber < numberOfEntities):
                entityLocation = offset + (entityNumber*8) + fileOffset
                file.seek(entityLocation, 0)
                nameEntityOffset = int.from_bytes(file.read(8), "little")
                nameEntity = EntityN(self, nameEntityOffset)
                entityList.append(nameEntity)
                entityNumber+=1
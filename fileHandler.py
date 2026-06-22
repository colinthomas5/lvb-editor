import os

#Class to store .lvb file. Includes file offset from which to start reading for .lvb data, header information, layers, and the .lvb type (based on game of .lvb origin)
class LVBFile:
    def __init__(self):
        self.file = None
        self.offset = 0
        self.header = None
        self.layers = []
        self.type = None

    #Method to open a .lvb file
    @classmethod
    def open(LVBFile, inputFile):
        lvb = LVBFile()
        lvb.file = open(inputFile, "rb")

        #Library can open .lvb files, or .lvb files nested within .pak archives. The difference in file type determines the offset within the file where the .lvb data starts
        #.LVB file has no offset
        fileExtension = inputFile.split(".", 1)[1]
        if fileExtension == "lvb":
            lvb.offset = 0
        #LVBFile object has a variable offset depending on where the .lvb file is within the .pak archive
        elif fileExtension == "pak":
            headerSize = int.from_bytes(lvb.file.read(4), "little")
            bytesToFind = b'.lvb'
            lvb.file.seek(0)
            fileString = lvb.file.read()
            #Searching for ".lvb" within .pak archive to determine where the .lvb file is within the .pak archive
            extensionLocation = fileString.find(bytesToFind)
            lvb.file.seek(extensionLocation, 0)

            #The .lvb file within the .pak file is .seek()ed to for purposes of constructing header, type, and layer information
            while lvb.file.read(3) != b'END':
                lvb.file.seek(-4, 1)
            offsetFromHeader = int.from_bytes(lvb.file.read(4), "little")
            lvb.offset = headerSize + offsetFromHeader + 64
            lvb.file.seek(lvb.offset)

        #Header contains information regarding the number, location, and number of contents of each layer. Based on the number of layers, the header size changes, which is used to determine the type.
        lvb.header = lvb.readHeader()
        headerSize = len(lvb.header)
        if headerSize == 64:
            lvb.type = 1 # Type 1 has four layers (in every observed instance), with the names of entities stored alongside the rest of the entity information
        elif headerSize == 128:
            lvb.type = 2 # Type 2 has five layers (in every observed instance), with the first four layers being entities and the fifth layer existing exclusively to store the names of the entities in layers 1-4

        lvb.layers = lvb.readLayers()

        return lvb

    def read(self):
        return self

    def readHeader(self):
        file = self.file
        file.seek(self.offset)
        file.seek(8, 1)
        headerSize = int.from_bytes(file.read(4), "little")
        file.seek(self.offset)
        return file.read(headerSize)
        
    def readLayers(self):
        layers = []
        #Number of layers is determined based on the contents of the header
        layerNumberOfEntities = int.from_bytes(self.header[4:8], "little")
        layerOffset = int.from_bytes(self.header[8:12], "little")
        headerSeek = 16

        # For each defined layer in the header, a list of entities is created and appended to the layer list within the LVBFile object
        while headerSeek <= len(self.header):
            nextLayerOffset = int.from_bytes(self.header[headerSeek+8: headerSeek+12], "little")
            if nextLayerOffset == 0:
                nextLayerOffset = None
            if layerOffset != None:
                layer = Layer().read(self, layerOffset, nextLayerOffset, layerNumberOfEntities)
                layerNumberOfEntities = int.from_bytes(self.header[headerSeek: headerSeek+4], "little")
                layerOffset = nextLayerOffset
                layers.append(layer)
            headerSeek+=16

        return layers

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class Entity1:
    def __init__(self, lvb, layer, offset, nextOffset):
        file = lvb.file
        self.offset = hex(offset)
        self.layer = layer
        file.seek(offset + lvb.offset, 0)
        self.type = file.read(4).hex()
        #index = file.read(4)
        #self.index = index
        self.posX = file.read(4).hex()
        self.posY = file.read(4).hex()
        self.posZ = file.read(4).hex()
        self.unknown1 = file.read(4).hex()
        self.unknown2 = file.read(4).hex()
        self.unknown3 = file.read(4).hex()
        self.unknown4 = file.read(4).hex()
        self.unknown5 = file.read(4).hex()
        self.unknown6 = file.read(4).hex()
        self.unknown7 = file.read(4).hex()
        self.name = file.read(32).rstrip(b'\x00')
        self.headerEnd = file.read(4).hex() #always 000080bf
        self.typeProperties = ''
        if nextOffset != None:
            while file.tell() < (nextOffset + lvb.offset):
                self.typeProperties = self.typeProperties + file.read(4).hex()
        else:
            while file.read(16).hex() != '3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f':
                file.seek(-16, 1)
                doge = file.read(16).hex()
                file.seek(-16, 1)
                self.typeProperties = self.typeProperties + file.read(4).hex()

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class Entity2:
    def __init__(self, lvb, layer, offset, nextOffset):
        file = lvb.file
        self.offset = hex(offset)
        self.layer = layer
        file.seek(offset + lvb.offset, 0)
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
        self.headerEnd = file.read(4).hex() #always ffffffff
        self.typeProperties = ''
        while file.tell() < (nextOffset + lvb.offset):
            self.typeProperties = self.typeProperties + file.read(4).hex()
        nameLocation = int.from_bytes(lvb.header[72:76], "little") + (self.index*8)
        self.nameLocation = hex(nameLocation)
        file.seek(nameLocation + lvb.offset, 0)
        nameOffset = int.from_bytes(file.read(8), "little")
        self.nameOffset = hex(nameOffset)
        file.seek(nameOffset + lvb.offset, 0)
        nameLength = int.from_bytes(file.read(4), "little")
        self.nameLength = hex(nameLength)
        self.name = file.read(nameLength)

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class EntityName: # LVB Type 2-exclusive entity type
    def __init__(self, lvb, layer, offset):
        file = lvb.file
        self.offset = hex(offset)
        self.layer = layer
        file.seek(offset + lvb.offset, 0)
        self.length = int.from_bytes(file.read(4), "little")
        self.entry = file.read(self.length).hex()

#Entities are sorted into Layers within .lvb files. Layers start with a table that lists all hex offsets of entities within that layer, followed by the entities within that layer.
class Layer:
    def __init__(self):
        self.offset = 0
        self.entities = []
        self.type = type

    #When parsing a layer, the layer object fills a list with all of the entities in that layer while populating all of the information about the entities.
    def read(self, lvb, offset, nextOffset, numberOfEntities):
        file = lvb.file
        layer = Layer()
        layer.offset = offset
        entityNumber = 0
        if lvb.type == 1 or nextOffset != None:
            layer.type = "entity"
            while(len(layer.entities) < numberOfEntities):
                entityLocation = layer.offset + (entityNumber*8) + lvb.offset
                file.seek(entityLocation, 0)
                entityOffset = int.from_bytes(file.read(8), "little")
                if entityNumber+1 != numberOfEntities:
                    nextEntityOffset = int.from_bytes(file.read(8), "little")
                else:
                    nextEntityOffset = nextOffset
                if lvb.type == 1:
                    entity = Entity1(lvb, self, entityOffset, nextEntityOffset)
                elif lvb.type == 2:
                    entity = Entity2(lvb, self, entityOffset, nextEntityOffset)
                layer.entities.append(entity)
                entityNumber+=1
        elif lvb.type  == 2 and nextOffset == None:
            layer.type = "name"
            layer.entities.clear()
            while(entityNumber < numberOfEntities):
                entityLocation = layer.offset + (entityNumber*8) + lvb.offset
                file.seek(entityLocation, 0)
                nameEntityOffset = int.from_bytes(file.read(8), "little")
                nameEntity = EntityName(lvb, self, nameEntityOffset)
                layer.entities.append(nameEntity)
                entityNumber+=1
        return layer


#  Entities are sorted into Layers within .lvb files. Layers start with a table that lists all hex offsets of entities within that layer, followed by the entities. When parsing a layer, the layer object fills a list with all of the entities in that layer while populating all of the information about the entities.
#class Layer:
#    def __init__(self, offset, nextOffset, numberOfEntities):
#        self.offset = offset
#        self.numberOfEntities = numberOfEntities
#        entityList = []
#        self.entityList = entityList
#        entityNumber=0
#        if nextOffset != None or lvbType == 1:
#           self.type = "entity"
#            while(entityNumber < numberOfEntities):
#                entityLocation = offset + (entityNumber*8) + fileOffset
#                file.seek(entityLocation, 0)
#                entityOffset = int.from_bytes(file.read(8), "little")
#                if entityNumber+1 != numberOfEntities:
#                    nextEntityOffset = int.from_bytes(file.read(8), "little")
#                else:
#                    nextEntityOffset = nextOffset
#                if lvbType == 1:
#                    entity = Entity1(self, entityOffset, nextEntityOffset)
#                elif lvbType == 2:
#                    entity = Entity2(self, entityOffset, nextEntityOffset)
#                entityList.append(entity)
#                entityNumber+=1
#        else:
#            self.type = "name"
#            entityList.clear()
#            while(entityNumber < numberOfEntities):
#                entityLocation = offset + (entityNumber*8) + fileOffset
#                file.seek(entityLocation, 0)
#                nameEntityOffset = int.from_bytes(file.read(8), "little")
#                nameEntity = EntityName(self, nameEntityOffset)
#                entityList.append(nameEntity)
#                entityNumber+=1]

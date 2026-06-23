import os

#Class to store .lvb file. Includes file offset from which to start reading for .lvb data, header information, layers, and the .lvb type (based on game of .lvb origin)
class LVBFile:
    def __init__(self, inputFile=None):
        self.file = None
        self.offset = 0
        self.header = None
        self.layers = []
        self.type = None

    #Method to open a .lvb file
    @classmethod
    def open(cls, inputFile):
        lvb = cls()
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
        lvb.readHeader()
        lvb.readType()
        lvb.readLayers()
        return lvb

    #Based on the number of layers, the header size changes, which is used to determine the type. Type 1 .lvb files only have 4 layers, while Type 2 .lvb files have 5 layers, which requires a larger header size. I should definitely find a better system to determine .lvb type/version, so maybe future me will find one. Or nova will kill me. Either or.
    def readType(self):
        headerSize = len(self.header)
        if headerSize == 64:
            self.type = 1 # Type 1 has four layers (in every observed instance), with the names of entities stored alongside the rest of the entity information
        elif headerSize == 128:
            self.type = 2 # Type 2 has five layers (in every observed instance), with the first four layers being entities and the fifth layer existing exclusively to store the names of the entities in layers 1-4

    #Header contains information regarding the number, location, and number of contents of each layer.
    def readHeader(self):
        file = self.file
        file.seek(self.offset)
        file.seek(8, 1)
        headerSize = int.from_bytes(file.read(4), "little")
        file.seek(self.offset)
        self.header =  file.read(headerSize)
        
    def writeHeader(self):
        header = bytearray()
        header+=(b'\x00\x00\x00\x00')
        header+=(len(self.layers[0].entites).to_bytes(4, "little"))
        header+=(self.layers[0].offset.to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        header+=(len(self.layers[1].entites).to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        header+=(self.layers[1].offset.to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        header+=(len(self.layers[2].entites).to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        header+=(self.layers[2].offset.to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        header+=(len(self.layers[3].entites).to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        header+=(self.layers[3].offset.to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        if self.type == 2:
            header+=(len(self.layers[4].entites).to_bytes(4, "little"))
            header+=(b'\x00\x00\x00\x00')
            header+=(self.layers[4].offset.to_bytes(4, "little"))
            header+=(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        self.header = header

    def readLayers(self):
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
                layer = Layer()
                layer.offset = layerOffset
                layer.read(self, nextLayerOffset, layerNumberOfEntities)
                layerNumberOfEntities = int.from_bytes(self.header[headerSeek: headerSeek+4], "little")
                layerOffset = nextLayerOffset
                self.layers.append(layer)
            headerSeek+=16
    

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class Entity1:
    def __init__(self):
        self.offset = 0
        self.type = None
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        self.unknown1 = 0
        self.unknown2 = 0
        self.unknown3 = 0
        self.unknown4 = 0
        self.unknown5 = 0
        self.unknown6 = 0
        self.unknown7 = 0
        self.name = ''
        self.headerEnd = 0
        self.typeProperties = ''

    def read(self, lvb, offset, nextOffset):
        file = lvb.file
        self.offset = hex(offset)
        file.seek(offset + lvb.offset, 0)
        self.type = file.read(4).hex()
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
                self.typeProperties = self.typeProperties + file.read(4).hex()


# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class Entity2:
    def __init__(self):
        self.offset = 0
        self.layer = None
        self.type = None
        self.unknown1 = 0
        self.index = 0
        self.unknown2 = 0
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        self.unknown3 = 0
        self.unknown4 = 0
        self.unknown5 = 0
        self.unknown6 = 0
        self.unknown7 = 0
        self.unknown8 = 0
        self.unknown9 = 0
        self.unknown10 = 0
        self.headerEnd = 0
        self.typeProperties = ''
        self.name = ''
        
    def read(self, lvb, offset, nextOffset):
        file = lvb.file
        self.offset = hex(offset)
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
    def __init__(self):
        self.offset = 0
        self.layer = 0
        self.length = 0
        self.entry = None
    
    def read(self, lvb, offset):
        file = lvb.file
        self.offset = hex(offset)
        file.seek(offset + lvb.offset, 0)
        self.length = int.from_bytes(file.read(4), "little")
        self.entry = file.read(self.length).hex()

#Entities are sorted into Layers within .lvb files. Layers start with a table that lists all hex offsets of entities within that layer, followed by the entities within that layer.
class Layer:
    def __init__(self):
        self.offset = 0
        self.entities = []
        self.type = None

    #When parsing a layer, the layer object fills a list with all of the entities in that layer while populating all of the information about the entities.
    def read(self, lvb, nextOffset, numberOfEntities):
        file = lvb.file
        offset = self.offset
        entityNumber = 0
        if lvb.type == 1 or nextOffset != None:
            self.type = "entity"
            while(len(self.entities) < numberOfEntities):
                entityLocation = offset + (entityNumber*8) + lvb.offset
                file.seek(entityLocation, 0)
                entityOffset = int.from_bytes(file.read(8), "little")
                if entityNumber+1 != numberOfEntities:
                    nextEntityOffset = int.from_bytes(file.read(8), "little")
                else:
                    nextEntityOffset = nextOffset
                if lvb.type == 1:
                    entity = Entity1()
                    entity.read(lvb, entityOffset, nextEntityOffset)
                elif lvb.type == 2:
                    entity = Entity2()
                    entity.read(lvb, entityOffset, nextEntityOffset)
                self.entities.append(entity)
                entityNumber+=1
        elif lvb.type  == 2 and nextOffset == None:
            self.type = "name"
            self.entities.clear()
            while(entityNumber < numberOfEntities):
                entityLocation = self.offset + (entityNumber*8) + lvb.offset
                file.seek(entityLocation, 0)
                nameEntityOffset = int.from_bytes(file.read(8), "little")
                nameEntity = EntityName()
                nameEntity.read(lvb, nameEntityOffset)
                self.entities.append(nameEntity)
                entityNumber+=1
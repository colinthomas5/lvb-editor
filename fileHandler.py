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

    def readHeader(self):
        file = self.file
        file.seek(self.offset)
        file.seek(8, 1)
        headerSize = int.from_bytes(file.read(4), "little")
        file.seek(self.offset)
        return file.read(headerSize)
        
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

    def read(entity, lvb, offset, nextOffset):
        file = lvb.file
        entity.offset = hex(offset)
        file.seek(offset + lvb.offset, 0)
        entity.type = file.read(4).hex()
        entity.posX = file.read(4).hex()
        entity.posY = file.read(4).hex()
        entity.posZ = file.read(4).hex()
        entity.unknown1 = file.read(4).hex()
        entity.unknown2 = file.read(4).hex()
        entity.unknown3 = file.read(4).hex()
        entity.unknown4 = file.read(4).hex()
        entity.unknown5 = file.read(4).hex()
        entity.unknown6 = file.read(4).hex()
        entity.unknown7 = file.read(4).hex()
        entity.name = file.read(32).rstrip(b'\x00')
        entity.headerEnd = file.read(4).hex() #always 000080bf
        entity.typeProperties = ''
        if nextOffset != None:
            while file.tell() < (nextOffset + lvb.offset):
                entity.typeProperties = entity.typeProperties + file.read(4).hex()
        else:
            while file.read(16).hex() != '3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f':
                file.seek(-16, 1)
                entity.typeProperties = entity.typeProperties + file.read(4).hex()
        return entity

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
        
    def read(entity, lvb, offset, nextOffset):
        file = lvb.file
        entity.offset = hex(offset)
        file.seek(offset + lvb.offset, 0)
        entity.type = file.read(8).hex()
        entity.unknown1 = file.read(4).hex()
        entity.index = int.from_bytes(file.read(4), "little")
        entity.unknown2 = file.read(4).hex()
        entity.posX = file.read(4).hex()
        entity.posY = file.read(4).hex()
        entity.posZ = file.read(4).hex()
        entity.unknown3 = file.read(4).hex()
        entity.unknown4 = file.read(4).hex()
        entity.unknown5 = file.read(4).hex()
        entity.unknown6 = file.read(4).hex()
        entity.unknown7 = file.read(4).hex()
        entity.unknown8 = file.read(4).hex()
        entity.unknown9 = file.read(4).hex()
        entity.unknown10 = file.read(4).hex()
        entity.headerEnd = file.read(4).hex() #always ffffffff
        entity.typeProperties = ''
        while file.tell() < (nextOffset + lvb.offset):
            entity.typeProperties = entity.typeProperties + file.read(4).hex()
        nameLocation = int.from_bytes(lvb.header[72:76], "little") + (entity.index*8)
        entity.nameLocation = hex(nameLocation)
        file.seek(nameLocation + lvb.offset, 0)
        nameOffset = int.from_bytes(file.read(8), "little")
        entity.nameOffset = hex(nameOffset)
        file.seek(nameOffset + lvb.offset, 0)
        nameLength = int.from_bytes(file.read(4), "little")
        entity.nameLength = hex(nameLength)
        entity.name = file.read(nameLength)
        return entity

# Entity objects represent all of the entities that are within the .lvb files. Regardless of type, entities all share the same header format. Different entity types will have different data following their "headerEnd", which should always be "FFFFFFFF"
class EntityName: # LVB Type 2-exclusive entity type
    def __init__(self):
        self.offset = 0
        self.layer = 0
        self.length = 0
        self.entry = None
    
    def read(entity, lvb, offset):
        file = lvb.file
        entity.offset = hex(offset)
        file.seek(offset + lvb.offset, 0)
        entity.length = int.from_bytes(file.read(4), "little")
        entity.entry = file.read(entity.length).hex()
        return entity

#Entities are sorted into Layers within .lvb files. Layers start with a table that lists all hex offsets of entities within that layer, followed by the entities within that layer.
class Layer:
    def __init__(self):
        self.offset = 0
        self.entities = []
        self.type = None

    #When parsing a layer, the layer object fills a list with all of the entities in that layer while populating all of the information about the entities.
    def read(layer, lvb, offset, nextOffset, numberOfEntities):
        file = lvb.file
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
                    entity = Entity1()
                    entity = Entity1.read(entity, lvb, entityOffset, nextEntityOffset)
                elif lvb.type == 2:
                    entity = Entity2()
                    entity = Entity2.read(entity, lvb, entityOffset, nextEntityOffset)
                layer.entities.append(entity)
                entityNumber+=1
        elif lvb.type  == 2 and nextOffset == None:
            layer.type = "name"
            layer.entities.clear()
            while(entityNumber < numberOfEntities):
                entityLocation = layer.offset + (entityNumber*8) + lvb.offset
                file.seek(entityLocation, 0)
                nameEntityOffset = int.from_bytes(file.read(8), "little")
                nameEntity = EntityName()
                nameEntity = EntityName.read(nameEntity, lvb, nameEntityOffset)
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

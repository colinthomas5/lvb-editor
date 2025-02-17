filePath = input("Enter file directory: ")
file = open(filePath, 'rb')

header = file.read(128)

class Entity:
    def __init__(self, layer, offset):
        self.offset = hex(offset)
        self.layer = layer
        file.seek(offset, 0)
        self.type = file.read(8).hex()
        self.unknown1 = file.read(4).hex()
        index = file.read(4)
        self.index = index.hex
        self.unknown2 = file.read(4).hex()
        self.posX = file.read(4).hex()
        self.posY = file.read(4).hex()
        self.posZ = file.read(4).hex()
        self.stretchX = file.read(4).hex()
        self.unknown4 = file.read(4).hex()
        self.unknown5 = file.read(4).hex()
        self.unknown6 = file.read(4).hex()
        self.unknown7 = file.read(4).hex()
        self.unknown8 = file.read(4).hex()
        self.unknown9 = file.read(4).hex()
        self.unknown10 = file.read(4).hex()
        self.headerEnd = file.read(4).hex()
        nameLocation = int.from_bytes(header[72:76], "little")+((int.from_bytes(index, "little"))*8)
        self.nameLocation = hex(nameLocation)
        file.seek(nameLocation, 0)
        nameOffset = int.from_bytes(file.read(8), "little")
        self.nameOffset = hex(nameOffset)
        file.seek(nameOffset, 0)
        nameLength = int.from_bytes(file.read(4), "little")
        self.nameLength = hex(nameLength)
        self.name = file.read(nameLength)

class Layer:
    def __init__(self, offset, numberOfEntities, entityList):
        self.offset = hex(offset)
        self.numberOfEntities = numberOfEntities
        self.entityList = entityList
        entityNumber=0
        while(entityNumber < numberOfEntities):
            entityLocation = offset+(entityNumber*8)
            file.seek(entityLocation, 0)
            entityOffset = int.from_bytes(file.read(8), "little")
            entity = Entity(self, entityOffset)
            entityList.append(entity)
            entityNumber+=1

entityList1 = []
entityList2 = []
entityList3 = []
entityList4 = []
# entityList5 = []

layer1 = Layer(int.from_bytes(header[8:12], "little"), int.from_bytes(header[4:8], "little"), entityList1)
layer2 = Layer(int.from_bytes(header[24:28], "little"), int.from_bytes(header[16:20], "little"), entityList2)
layer3 = Layer(int.from_bytes(header[40:44], "little"), int.from_bytes(header[32:36], "little"), entityList3)
layer4 = Layer(int.from_bytes(header[56:60], "little"), int.from_bytes(header[48:52], "little"), entityList4)
# layer5 = Layer(int.from_bytes(header[72:76], "little"), int.from_bytes(header[64:68], "little"), entityList5)
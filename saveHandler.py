import fileHandler

def saveLevelFile(layerList, fileChanges, file, fileOffset, lvbType):
    writeFileHeader(layerList, file, fileOffset, lvbType)
    for change in fileChanges:
        writeEntity(change, file, fileOffset, lvbType)

def writeFileHeader(layerList, file, fileOffset, lvbType):
    header = bytearray()
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[0].numberOfEntities.to_bytes(4, "little"))
    header+=(layerList[0].offset.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[1].numberOfEntities.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[1].offset.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[2].numberOfEntities.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[2].offset.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[3].numberOfEntities.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[3].offset.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    if lvbType == 2:
        header+=(layerList[4].numberOfEntities.to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00')
        header+=(layerList[4].offset.to_bytes(4, "little"))
        header+=(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    file.seek(fileOffset)
    file.write(header)

def writeEntity(entity, file, fileOffset, lvbType):
    entityString = ""
    if lvbType == 1:
        entityString+=entity.type
        entityString+=entity.posX
        entityString+=entity.posY
        entityString+=entity.posZ
        entityString+=entity.unknown1
        entityString+=entity.unknown2
        entityString+=entity.unknown3
        entityString+=entity.unknown4
        entityString+=entity.unknown5
        entityString+=entity.unknown6
        entityString+=entity.unknown7
        while len(entity.name) < 32:
            entity.name+=b'\x00'
        entityString+=entity.name.hex()
        entityString+=entity.headerEnd
        entityString+=entity.typeProperties
    if lvbType == 2:
        entityString+=entity.type
        entityString+=entity.unknown1
        entityString+=(entity.index).to_bytes(4, "little").hex()
        entityString+=entity.unknown2
        entityString+=entity.posX
        entityString+=entity.posY
        entityString+=entity.posZ
        entityString+=entity.unknown3
        entityString+=entity.unknown4
        entityString+=entity.unknown5
        entityString+=entity.unknown6
        entityString+=entity.unknown7
        entityString+=entity.unknown8
        entityString+=entity.unknown9
        entityString+=entity.unknown10
        entityString+=entity.headerEnd
        entityString+=entity.typeProperties
    entityHeader = bytearray.fromhex(entityString)
    file.seek(int(entity.offset, 16)+fileOffset)
    file.write(entityHeader)
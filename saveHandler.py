import fileHandler

def saveLevelFile(layerList, fileChanges, file, fileOffset):
    writeFileHeader(layerList, file, fileOffset)
    for change in fileChanges:
        writeEntityHeader(change, file, fileOffset)

def writeFileHeader(layerList, file, fileOffset):
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
    header+=(layerList[4].numberOfEntities.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00')
    header+=(layerList[4].offset.to_bytes(4, "little"))
    header+=(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    #print(header.hex())
    file.seek(fileOffset)
    file.write(header)

def writeEntityHeader(entity, file, fileOffset):
    entityHeaderString = ""
    entityHeaderString+=entity.type
    entityHeaderString+=entity.unknown1
    entityHeaderString+=entity.index
    entityHeaderString+=entity.unknown2
    entityHeaderString+=entity.posX
    entityHeaderString+=entity.posY
    entityHeaderString+=entity.posZ
    entityHeaderString+=entity.stretchX
    entityHeaderString+=entity.unknown4
    entityHeaderString+=entity.unknown5
    entityHeaderString+=entity.unknown6
    entityHeaderString+=entity.unknown7
    entityHeaderString+=entity.unknown8
    entityHeaderString+=entity.unknown9
    entityHeaderString+=entity.unknown10
    entityHeaderString+=entity.headerEnd
    entityHeader = bytearray.fromhex(entityHeaderString)
    #print(entityHeader.hex())
    file.seek(int(entity.offset, 16)+fileOffset)
    file.write(entityHeader)
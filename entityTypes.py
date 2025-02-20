
# List of all entity types that I have written down in a google doc somewhere
entityTypeHex = ["57000000f2be8779", "c50000007a19ccca", "d90000001ef5b4f9", "02000000aff06be1", "d800000010e0391a", "610000007938ef87", "80000000b3287757", "a10000001d3c7cbc", "89000000e5c2e510", "e100000019712817", "8600000083d9ae32", "5e000000a0a3be1d", "b300000001dd294c", "e000000016b7b242", "a7000000018dafee", "9d000000d39d7e5e", "4d00000002b40dbc", "ac00000076248a86", "740000007da56148", "3c0000004ec4a505", "d1000000672abae4", "af000000a891da7d", "b9000000048cbf5b", "5a000000cb4fe297", "e6000000f7e2871e", "bb00000008d6ef2c", "b50000004d43a5be", "c20000009a3c03eb", "30000000de18cc0c", "65000000a0dfba27", "c9000000c8e627c7", "fe000000f0c2c837", "db0000007b26506e", "580000004d57201a", "7e000000328a60a9", "970000003101034c", "f00000003f41235f", "d200000060c69d30", "f30000007d89af01", "a30000006ab129f4", "640000006a8735d2", "6c00000097dbe585", "ad000000fbfdab1d", "790000003ef00c43", "6d000000c75dee4f", "fb00000006a1cf299", "ef00000096f4de59", "51000000ee12ac71", "ea00000075c009ff", "5f000000384302d5", "fc000000968baca8", "d40000000867b27e", "7c0000001b65c162", "590000002e19fc5a", "2b00000016d65c93"]

# List of names of entity types that I have named based on the entities that I saw them on (TL;DR I made them up)
entityTypeNames = ["Room", "StartSpot", "Stairs", "LightManager", "LoadingDoor", "Ledge", "Spawner", "Carryable", "OverworldInfo", "FloorStairs", "Fountain", "Chest", "CutsceneTrigger", "DryTree", "Pickup", "BombableDoor", "PieFairy", "Torch", "WoodenPost", "PointLight", "HiddenStairs", "GateTorch", "Rain", "TempleDoor", "TabletSwitch", "Door", "SpawnPoint", "Floor", "ShopItem/NightmareWaypoint", "ShopSpawner", "Castle", "VideoShelf", "CarryableWithItem", "Barrier", "Door", "FloorSpikes", "FireballShooter", "BarrierSwitch", "RubyTower", "RotatingBridge", "HeavyBlock", "PressurePlate", "BridgeConnector", "LockedDoor", "SlidingTrap", "HitMeSwitch", "GrabbyHandSwitch", "TriggerShutter", "Surface", "BossDoor", "EnemyShutter", "Teleporter", "OneWayDoor", "SpikeNode", "Wall"]

# Function takes the hex value of the type and returns the name of the type
def getTypeName(typeHex):
    for string in entityTypeHex:
        if typeHex == string:
            entityTypeIndex = entityTypeHex.index(typeHex)
            return entityTypeNames[entityTypeIndex]
    return(typeHex)
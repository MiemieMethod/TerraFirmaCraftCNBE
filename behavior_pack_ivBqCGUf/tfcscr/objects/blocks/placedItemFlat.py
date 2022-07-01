# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.minecraftEnum as MinecraftEnum

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

import tfcscr.utils.itemHelper as ItemHelper

# 共用
def get_item_by_identifier(id):
    item_mapping = {
        "tfc:placed_item_flat_stick": ("tfc:stick", 0)
    }
    if id in item_mapping:
        return item_mapping[id]
    else:
        return False

# 服务端
def on_use(data):
    if ServerCompFactory.CreatePlayer(data["playerId"]).IsSneaking() == False:
        if not ServerCompFactory.CreateItem(data["playerId"]).GetPlayerItem(MinecraftEnum.ItemPosType.CARRIED) and ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).SetBlockNew((data["x"], data["y"], data["z"]), {"name": "minecraft:air"}, 0, data["dimensionId"]) == True:
            item = get_item_by_identifier(data["blockName"])
            if item:
                item_to_add_to_inv = {"newItemName": item[0], "newAuxValue": item[1], "count": 1}
                item_to_add_to_inv = ItemHelper.set_temperature(item_to_add_to_inv, 1600)
                print("===== placed_item_flat on_use item_to_add_to_inv =====", item_to_add_to_inv)
                if ServerCompFactory.CreateItem(data["playerId"]).SpawnItemToPlayerInv(ItemHelper.update_custom_tips(item_to_add_to_inv), data["playerId"]) == True:
                    return True
            else:
                print("===== placed_item_flat on_use Give Failed =====")
        else:
            print("===== placed_item_flat on_use Destroy Failed =====")
    else:
        print("===== placed_item_flat on_use Player Sneaking =====")

# 客户端
def on_use_client(data):
    if ClientCompFactory.CreatePlayer(data["playerId"]).isSneaking() == False:
        return True
    else:
        print("===== placed_item_flat on_use_client Player Sneaking =====")


# 服务端
def on_use_on(data):
    if ServerCompFactory.CreatePlayer(data["entityId"]).IsSneaking() == False:
        if not ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).GetBlockBasicInfo(data["itemDict"]["newItemName"]) and ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).SetBlockNew((data["x"], data["y"], data["z"]), {"name": "minecraft:air"}, 0, data["dimensionId"]) == True:
            if get_item_by_identifier(data["blockName"]) and ServerCompFactory.CreateItem(data["entityId"]).SpawnItemToPlayerInv({"newItemName": get_item_by_identifier(data["blockName"])[0], "newAuxValue": get_item_by_identifier(data["blockName"])[1], "count": 1}, data["entityId"]) == True:
                return True
            else:
                print("===== placed_item_flat on_use_on Give Failed =====")
        elif ServerCompFactory.CreateBlockEntityData(serverApi.GetLevelId()).GetBlockEntityData(data["dimensionId"], (data["x"], data["y"], data["z"])):
            block_actor_data = ServerCompFactory.CreateBlockEntityData(serverApi.GetLevelId()).GetBlockEntityData(data["dimensionId"], (data["x"], data["y"], data["z"]))
            block_actor_data["PendingRemove"] = True
            block_actor_data["ReplaceBlock"] = {"name": data["itemDict"]["newItemName"], "aux": data["itemDict"]["newAuxValue"], "entityId": data["entityId"]}
            print("===== placed_item_flat on_use_on Replaced =====", {"name": data["itemDict"]["newItemName"], "aux": data["itemDict"]["newAuxValue"], "entityId": data["entityId"]})
            return True
        else:
            print("===== placed_item_flat on_use_on Destroy Failed =====")
    else:
        print("===== placed_item_flat on_use_on Player Sneaking =====")

# 客户端
def on_use_on_client(data):
    if ClientCompFactory.CreatePlayer(data["entityId"]).isSneaking() == False:
        return True
    else:
        print("===== placed_item_flat on_use_on_client Player Sneaking =====")


# 服务端
def on_place(data, relative):
    solid = ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).GetBlockBasicInfo(relative["name"])["solid"]
    print("===== placed_item_flat on_place =====")
    return data["face"] == MinecraftEnum.Facing.Up and not solid

# 服务端
def on_place_on(data, relative):
    pass

# 服务端
def on_neighbor_changed(data):
    solid = ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).GetBlockBasicInfo(data["toBlockName"])["solid"]
    if data["neighborPosY"] == data["posY"] - 1 and data["neighborPosX"] == data["posX"] and data["neighborPosZ"] == data["posZ"] and not solid:
        ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).SetBlockNew((data["posX"], data["posY"], data["posZ"]), {"name": "minecraft:air"}, 0, data["dimensionId"])

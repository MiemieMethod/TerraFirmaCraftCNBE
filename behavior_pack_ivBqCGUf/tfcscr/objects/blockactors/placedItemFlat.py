# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.minecraftEnum as MinecraftEnum

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

from tfcscr.objects.blocks.placedItemFlat import get_item_by_identifier as get_item_by_identifier

# 服务端
def on_block_actor_tick(data):
    block_actor_data = ServerCompFactory.CreateBlockEntityData(serverApi.GetLevelId()).GetBlockEntityData(data["dimension"], (data["posX"], data["posY"], data["posZ"]))
    if block_actor_data["PendingRemove"] == True:
        replace_info = block_actor_data["ReplaceBlock"]
        if data["blockName"] == replace_info["name"]:
            block_actor_data["PendingRemove"] = False
        elif ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).SetBlockNew((data["posX"], data["posY"], data["posZ"]), replace_info, 0, data["dimension"]):
            item_comp = ServerCompFactory.CreateItem(replace_info["entityId"])
            item_instance = item_comp.GetPlayerItem(MinecraftEnum.ItemPosType.CARRIED)
            item_comp.SetInvItemNum(item_comp.GetSelectSlotId(), item_instance["count"] and item_instance["count"] - 1 or 0)
            print("===== placed_item_flat on_block_actor_tick Replaced =====", replace_info)
        else:
            print("===== placed_item_flat on_block_actor_tick Replace Failed =====", data["posX"], data["posY"], data["posZ"])

# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.utils.moduleUtil as ModuleUtil

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

block_actor_class_mapping = {
    "tfc:placed_item_flat_stick": "tfcscr.objects.blockactors.placedItemFlat"
}

def get_block_actor_class(full_name):
    # print("===== blockActorFactory get_block_actor_class =====", full_name)
    if full_name in block_actor_class_mapping:
        return ModuleUtil.GetModuleByName(block_actor_class_mapping[full_name])
    else:
        return False
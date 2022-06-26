# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.utils.moduleUtil as ModuleUtil

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

block_class_mapping = {
    "tfc:placed_item_flat_stick": "tfcscr.objects.blocks.placedItemFlat"
}

def get_block_class(full_name):
    print("===== blockFactory get_block_class =====", full_name)
    if full_name in block_class_mapping:
        return ModuleUtil.GetModuleByName(block_class_mapping[full_name])
    else:
        return False
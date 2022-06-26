# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.utils.moduleUtil as ModuleUtil

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

item_class_mapping = {
    
}

def get_item_class(full_name):
    print("===== itemFactory get_item_class =====", full_name)
    if full_name in item_class_mapping:
        return ModuleUtil.GetModuleByName(item_class_mapping[full_name])
    else:
        return False
# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.common.minecraftEnum as MinecraftEnum

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()

from tfcscr.config.enums import size_enum as size_enum
from tfcscr.config.enums import weight_enum as weight_enum
import tfcscr.config.configs as Configs

import tfcscr.utils.commonUtils as CommonUtils

class Size:
    TINY = "TINY"
    VERY_SMALL = "VERY_SMALL"
    SMALL = "SMALL"
    NORMAL = "NORMAL"
    VERY_LARGE = "VERY_LARGE"
    HUGE = "HUGE"

class Weight:
    VERY_LIGHT = "VERY_LIGHT"
    LIGHT = "LIGHT"
    MEDIUM = "MEDIUM"
    HEAVY = "HEAVY"
    VERY_HEAVY = "VERY_HEAVY"

sizable_info = {
    "tfc:stick": (Size.SMALL, Weight.VERY_LIGHT, True)
}

def register_sizable(item_id, size = Size.SMALL, weight = Weight.LIGHT, can_stack = True):
    if item_id:
        sizable_info[item_id] = (size, weight, can_stack)
        ServerCompFactory.CreateItem(serverApi.GetLevelId()).SetMaxStackSize(get_stack_size(item_id))
    else:
        print("===== ItemSizeHandler register_sizable wrong item id, register failed =====")

def get_size(item_id):
    return item_id in sizable_info and sizable_info[item_id][0] or Size.SMALL

def get_weight(item_id):
    return item_id in sizable_info and sizable_info[item_id][1] or Weight.LIGHT

def can_stack(item_id):
    return item_id in sizable_info and sizable_info[item_id][2] or True

def get_stack_size(item_id):
    return can_stack(item_id) and weight_enum[get_weight(item_id)]["stack_size"] or 1

def get_item_size(item_id):
    if item_id in sizable_info:
        return sizable_info[item_id]
    else:
        return False

def get_item_size_by_dict(item_dict):
    return get_item_size(item_dict["newItemName"])

def add_size_info(item_dict, text):
    item_size = get_item_size_by_dict(item_dict)
    # print("===== ItemSizeHandler add_size_info item_size =====", item_dict["newItemName"], item_size)
    if item_size:
        tooltip = "⚖ " + CommonUtils.i18n(CommonUtils.get_enum_name(item_size[1], "weight")) + " ⇲ " + CommonUtils.i18n(CommonUtils.get_enum_name(item_size[0], "size"))
        return text + "\n\n" + tooltip
    else:
        register_sizable(item_dict["newItemName"])
        return add_size_info(item_dict, text)
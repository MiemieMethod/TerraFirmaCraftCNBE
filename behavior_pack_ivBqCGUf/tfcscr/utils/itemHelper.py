# coding=utf-8

from mod_log import logger as logger
import item
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.minecraftEnum as MinecraftEnum

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

import tfcscr.utils.blockFactory as BlockFactory
import tfcscr.utils.commonUtils as CommonUtils
import tfcscr.utils.api.itemHeatHandler as ItemHeatHandler

class ContainerType:
    INV = 0
    ARMOR = 1
    OFFHAND = 2
    VANILLA_CHEST = 3
    VANILLA_MISC = 4
    OPEN_CONTAINER = 5
    MODDED_CONTAINER = 6

# 服务端
# todo
def get_custom_tips(item_dict):
    user_data = "userData" in item_dict and item_dict["userData"] or None
    extra_id = "extraId" in item_dict and item_dict["extraId"] or None
    tooltip = "%name%%category%%enchanting%%attack_damage%"
    tooltip = ItemHeatHandler.add_heat_info(item_dict, tooltip)
    # print(user_data, extra_id)
    return tooltip

# 服务端
def update_custom_tips(item_dict):
    custom_tips = get_custom_tips(item_dict)
    item_dict["customTips"] = custom_tips
    return item_dict

# 服务端
# todo
def update_custom_tips_by_container(item_instance, container_type, slot, player, player_container_info, current_tick):
    item_comp = ServerCompFactory.CreateItem(player)
    item_instance["userData"] = CommonUtils.refact_user_data(item_instance["userData"])
    if container_type == ContainerType.INV:
        item_comp.ChangePlayerItemTipsAndExtraId(MinecraftEnum.ItemPosType.INVENTORY, slot, get_custom_tips(item_instance))
        if current_tick % 30 == 0:
            item_instance = update_custom_tips(set_temperature(item_instance, ItemHeatHandler.get_temperature_by_dict(item_instance)))
            item.change_item_in_inventory_with_slot(player, slot, item_instance)
    elif container_type == ContainerType.ARMOR:
        item_instance['customTips'] = get_custom_tips(item_instance)
        item.change_item_in_armor_with_slot(player, slot, item_instance)
        if current_tick % 30 == 0:
            item_instance = update_custom_tips(set_temperature(item_instance, ItemHeatHandler.get_temperature_by_dict(item_instance)))
            item.change_item_in_armor_with_slot(player, slot, item_instance)
    elif container_type == ContainerType.OFFHAND:
        item_comp.ChangePlayerItemTipsAndExtraId(MinecraftEnum.ItemPosType.OFFHAND, slot, get_custom_tips(item_instance))
        if current_tick % 30 == 0:
            item_instance = update_custom_tips(set_temperature(item_instance, ItemHeatHandler.get_temperature_by_dict(item_instance)))
            item.change_item_off_hand(player, item_instance)
    elif container_type == ContainerType.OPEN_CONTAINER:
        item_instance['customTips'] = get_custom_tips(item_instance)
        item_comp.SetPlayerUIItem(item_instance, player, slot)
        if current_tick % 30 == 0:
            item_instance = update_custom_tips(set_temperature(item_instance, ItemHeatHandler.get_temperature_by_dict(item_instance)))
            item_comp.SetPlayerUIItem(item_instance, player, slot)
    return item_instance

# 服务端
def set_temperature(item_dict, temp):
    return ItemHeatHandler.set_temperature(item_dict, temp)

# 服务端
# todo
def item_container_ticking(player_container_info, current_tick):
    players = serverApi.GetPlayerList()
    for player in players:
        item_comp = ServerCompFactory.CreateItem(player)
        if player in player_container_info:
            print("===== itemHelper item_container_ticking Container =====", player, player_container_info[player])
        for i in range(36):
            item_instance = item_comp.GetPlayerItem(MinecraftEnum.ItemPosType.INVENTORY, i, True)
            if item_instance:
                item_instance = update_custom_tips_by_container(item_instance, ContainerType.INV, i, player, player_container_info, current_tick)
        for i in range(4):
            item_instance = item_comp.GetPlayerItem(MinecraftEnum.ItemPosType.ARMOR, i, True)
            if item_instance:
                item_instance = update_custom_tips_by_container(item_instance, ContainerType.ARMOR, i, player, player_container_info, current_tick)
        for i in range(1):
            item_instance = item_comp.GetPlayerItem(MinecraftEnum.ItemPosType.OFFHAND, i, True)
            if item_instance:
                item_instance = update_custom_tips_by_container(item_instance, ContainerType.OFFHAND, i, player, player_container_info, current_tick)
        for i in range(100):
            item_instance = item_comp.GetPlayerUIItem(player, i, True)
            if item_instance:
                # item_instance = update_custom_tips_by_container(item_instance, ContainerType.OPEN_CONTAINER, i, player, player_container_info, current_tick)
                "todo"

# 服务端
def on_use_on(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and hasattr(block_cls, "on_use_on") and block_cls.on_use_on(data) or cancel
    print("===== itemHelper on_use_on =====", cancel)
    return cancel

# 客户端
def on_use_on_client(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and hasattr(block_cls, "on_use_on_client") and block_cls.on_use_on_client(data) or cancel
    print("===== itemHelper on_use_on_client =====", cancel)
    return cancel
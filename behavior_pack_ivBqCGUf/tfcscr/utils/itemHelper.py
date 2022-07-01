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
import tfcscr.utils.api.itemSizeHandler as ItemSizeHandler

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
    tooltip = ItemSizeHandler.add_size_info(item_dict, tooltip)
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
def update_custom_tips_by_container(item_instance, container_type, slot, player, container_info, current_tick):
    item_comp = ServerCompFactory.CreateItem(player)
    item_instance["userData"] = CommonUtils.refact_user_data(item_instance["userData"])
    item_temp = ItemHeatHandler.get_temperature_by_dict(item_instance)
    if container_type == ContainerType.INV:
        tooltip_old = "customTips" in item_instance and item_instance["customTips"] or ""
        tooltip = get_custom_tips(item_instance)
        item_comp.ChangePlayerItemTipsAndExtraId(MinecraftEnum.ItemPosType.INVENTORY, slot, tooltip)
        if tooltip_old != tooltip or item_temp < 1:
            item_instance = update_custom_tips(set_temperature(item_instance, item_temp))
            item.change_item_in_inventory_with_slot(player, slot, item_instance)
    elif container_type == ContainerType.ARMOR:
        tooltip_old = "customTips" in item_instance and item_instance["customTips"] or ""
        tooltip = get_custom_tips(item_instance)
        item_instance['customTips'] = tooltip
        item.change_item_in_armor_with_slot(player, slot, item_instance)
        if tooltip_old != tooltip or item_temp < 1:
            item_instance = update_custom_tips(set_temperature(item_instance, item_temp))
            item.change_item_in_armor_with_slot(player, slot, item_instance)
    elif container_type == ContainerType.OFFHAND:
        tooltip_old = "customTips" in item_instance and item_instance["customTips"] or ""
        tooltip = get_custom_tips(item_instance)
        item_comp.ChangePlayerItemTipsAndExtraId(MinecraftEnum.ItemPosType.OFFHAND, slot, tooltip)
        if tooltip_old != tooltip or item_temp < 1:
            item_instance = update_custom_tips(set_temperature(item_instance, item_temp))
            item.change_item_off_hand(player, item_instance)
    elif container_type == ContainerType.OPEN_CONTAINER:
        tooltip_old = "customTips" in item_instance and item_instance["customTips"] or ""
        tooltip = get_custom_tips(item_instance)
        item_instance['customTips'] = tooltip
        # todo
        # item_comp.SetPlayerUIItem(item_instance, player, slot)
        # if tooltip_old != tooltip or item_temp < 1:
        #     item_instance = update_custom_tips(set_temperature(item_instance, item_temp))
        #     item_comp.SetPlayerUIItem(item_instance, player, slot)
    elif container_type == ContainerType.VANILLA_CHEST:
        tooltip_old = "customTips" in item_instance and item_instance["customTips"] or ""
        tooltip = get_custom_tips(item_instance)
        item_instance['customTips'] = tooltip
        # todo
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
            info = player_container_info[player]
            container_info = ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((info[0], info[1], info[2]), info[3])
            print("===== itemHelper item_container_ticking Container =====", player, info)
            if container_info:
                container_info["pos"] = (info[0], info[1], info[2])
                container_info["dim"] = info[3]
                for i in range(item_comp.GetContainerSize(container_info["pos"], container_info["dim"])):
                    item_instance = item_comp.GetContainerItem(container_info["pos"], i, container_info["dim"], True)
                    if item_instance:
                        item_instance = update_custom_tips_by_container(item_instance, ContainerType.VANILLA_CHEST, i, player, container_info, current_tick)
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
                item_instance = update_custom_tips_by_container(item_instance, ContainerType.OPEN_CONTAINER, i, player, player_container_info, current_tick)

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
# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.common.minecraftEnum as MinecraftEnum

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()

from tfcscr.config.enums import heat_enum as heat_enum
from tfcscr.config.enums import ore_tooltip_mode as ore_tooltip_mode
import tfcscr.config.configs as Configs

import tfcscr.utils.commonUtils as CommonUtils

heatable_info = {}

def register_heatable(item_id, heat_capacity = 1, melt_temp = 1601):
    if item_id:
        heatable_info[item_id] = (heat_capacity, melt_temp)
    else:
        print("===== ItemHeatHandler register_heatable wrong item id, register failed =====")

def get_heat_capacity(item_id):
    return item_id in heatable_info and heatable_info[item_id][0] or 1

def get_melt_temp(item_id):
    return item_id in heatable_info and heatable_info[item_id][1] or 1601

def get_temperature(item_id, last_update_temp, last_update_tick):
    return adjust_temp(last_update_temp, get_heat_capacity(item_id), ServerCompFactory.CreateTime(serverApi.GetLevelId()).GetTime() - last_update_tick)

def get_temperature_by_dict(item_dict):
    user_data = "userData" in item_dict and item_dict["userData"] or {}
    if "tfc" in user_data and "Heatable" in user_data["tfc"]:
        return get_temperature(item_dict["newItemName"], user_data["tfc"]["Heatable"]["heat"], user_data["tfc"]["Heatable"]["ticks"])
    else:
        item_dict = set_temperature(item_dict, 0)
        return 0

def set_temperature(item_dict, temp):
    user_data = "userData" in item_dict and item_dict["userData"] or {}
    if "tfc" in user_data:
        if "Heatable" in user_data["tfc"]:
            user_data["tfc"]["Heatable"]["heat"] = temp > 0 and temp or 0
            user_data["tfc"]["Heatable"]["ticks"] = temp > 0 and ServerCompFactory.CreateTime(serverApi.GetLevelId()).GetTime() or -1
        else:
            user_data["tfc"]["Heatable"] = {
                "heat": temp > 0 and temp or 0,
                "ticks": temp > 0 and ServerCompFactory.CreateTime(serverApi.GetLevelId()).GetTime() or -1
            }
    else:
        user_data["tfc"] = {
            "Heatable": {
                "heat": temp > 0 and temp or 0,
                "ticks": temp > 0 and ServerCompFactory.CreateTime(serverApi.GetLevelId()).GetTime() or -1
            }
        }
    item_dict["userData"] = user_data
    return item_dict

def adjust_temp(temp, heat_capacity, ticks_since_update):
    if ticks_since_update <= 0:
        return temp
    new_temp = temp - heat_capacity * ticks_since_update * Configs.Devices.TemperatureCFG.globalModifier
    return new_temp < 0 and 0 or new_temp

def get_heat(temp):
    for heat in heat_enum:
        if temp >= heat_enum[heat]["min"] and temp < heat_enum[heat]["max"]:
            return heat
    if temp > heat_enum["BRILLIANT_WHITE"]["max"]:
        return "BRILLIANT_WHITE"
    return None

def get_tooltip_colorless(temp):
    heat = get_heat(temp)
    if heat:
        tooltip = CommonUtils.i18n(CommonUtils.get_enum_name(heat, "heat"))
        if heat != "BRILLIANT_WHITE":
            for i in range(1, 5):
                if temp <= heat_enum[heat]["min"] + i * 0.2 * (heat_enum[heat]["max"] - heat_enum[heat]["min"]):
                    continue
                tooltip = tooltip + "★"
        return tooltip
    return None

def get_tooltip(temp):
    heat = get_heat(temp)
    tooltip = get_tooltip_colorless(temp)
    if heat and tooltip:
        tooltip = heat_enum[heat]["format"] + tooltip
        if Configs.Client.TooltipCFG.oreTooltipMode == ore_tooltip_mode["ADVANCED"]["index"]:
            tooltip = tooltip + " : " + round(temp) + CommonUtils.i18n("tfc.tooltip.melttemp")
    return tooltip

# todo
def add_heat_info(item_dict, text):
    user_data = "userData" in item_dict and item_dict["userData"] or {}
    # print("===== ItemHeatHandler add_heat_info user_data =====", user_data, "userData" in item_dict)
    if "tfc" in user_data and "Heatable" in user_data["tfc"]:
        temp = get_temperature(item_dict["newItemName"], user_data["tfc"]["Heatable"]["heat"], user_data["tfc"]["Heatable"]["ticks"])
        tooltip = get_tooltip(temp)
        if tooltip:
            return text + "\n" + tooltip
        else:
            return text
    else:
        item_dict = set_temperature(item_dict, 0)
        return add_heat_info(item_dict, text)
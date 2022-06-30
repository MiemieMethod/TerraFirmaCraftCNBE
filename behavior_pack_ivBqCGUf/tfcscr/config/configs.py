# coding=utf-8

import tfcscr.config.enums as Enums

class Devices:
    class TemperatureCFG:
        globalModifier = 0.5
        heatingModifier = 1
        coolHeatablesInWorld = True
        ticksBeforeAttemptToCool = 10

class Client:
    class TooltipCFG:
        showToolClassTooltip = True
        showOreDictionaryTooltip = True
        showNBTTooltip = False
        propickOutputToActionBar = True
        anvilWeldOutputToActionBar = True
        vesselOutputToActionBar = True
        animalsOutputToActionBar = True
        oreTooltipMode = Enums.ore_tooltip_mode["ALL_INFO"]["index"]
        decayTooltipMode = Enums.decay_tooltip_mode["ALL_INFO"]["index"]
        timeTooltipMode = Enums.time_tooltip_mode["MINECRAFT_HOURS"]["index"]
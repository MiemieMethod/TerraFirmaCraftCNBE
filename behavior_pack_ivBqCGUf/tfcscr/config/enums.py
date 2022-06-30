# coding=utf-8

import mod.common.minecraftEnum as MinecraftEnum

heat_enum = {
    "WARMING": {
        "index": 0,
        "min": 1,
        "max": 80,
        "format": MinecraftEnum.ColorCode.GRAY,
        "alt": MinecraftEnum.ColorCode.DARK_GRAY
    },
    "HOT": {
        "index": 1,
        "min": 80,
        "max": 210,
        "format": MinecraftEnum.ColorCode.GRAY,
        "alt": MinecraftEnum.ColorCode.DARK_GRAY
    },
    "VERY_HOT": {
        "index": 2,
        "min": 210,
        "max": 480,
        "format": MinecraftEnum.ColorCode.GRAY,
        "alt": MinecraftEnum.ColorCode.DARK_GRAY
    },
    "FAINT_RED": {
        "index": 3,
        "min": 480,
        "max": 580,
        "format": MinecraftEnum.ColorCode.DARK_RED
    },
    "DARK_RED": {
        "index": 4,
        "min": 580,
        "max": 730,
        "format": MinecraftEnum.ColorCode.DARK_RED
    },
    "BRIGHT_RED": {
        "index": 5,
        "min": 730,
        "max": 930,
        "format": MinecraftEnum.ColorCode.RED
    },
    "ORANGE": {
        "index": 6,
        "min": 930,
        "max": 1100,
        "format": MinecraftEnum.ColorCode.GOLD
    },
    "YELLOW": {
        "index": 7,
        "min": 1100,
        "max": 1300,
        "format": MinecraftEnum.ColorCode.YELLOW
    },
    "YELLOW_WHITE": {
        "index": 8,
        "min": 1300,
        "max": 1400,
        "format": MinecraftEnum.ColorCode.YELLOW
    },
    "WHITE": {
        "index": 9,
        "min": 1400,
        "max": 1500,
        "format": MinecraftEnum.ColorCode.WHITE
    },
    "BRILLIANT_WHITE": {
        "index": 10,
        "min": 1500,
        "max": 1601,
        "format": MinecraftEnum.ColorCode.WHITE
    }
}


ore_tooltip_mode = {
    "HIDE": {
        "index": 0,
        "name": "Hide ore information"
    },
    "UNIT_ONLY": {
        "index": 1,
        "name": "Show only the ore units"
    },
    "TOTAL_ONLY": {
        "index": 2,
        "name": "Show only the stack total units"
    },
    "ALL_INFO": {
        "index": 3,
        "name": "Show All"
    },
    "ADVANCED": {
        "index": 4,
        "name": "Show numeric heat/melt data"
    }
}

decay_tooltip_mode = {
    "HIDE": {
        "index": 0,
        "name": "Hide decay information"
    },
    "EXPIRATION_ONLY": {
        "index": 1,
        "name": "Show only the expiration date"
    },
    "TIME_REMAINING_ONLY": {
        "index": 2,
        "name": "Show only the time remaining to expire"
    },
    "ALL_INFO": {
        "index": 3,
        "name": "Show All"
    }
}

time_tooltip_mode = {
    "NONE": {
        "index": 0,
        "name": "None"
    },
    "TICKS": {
        "index": 1,
        "name": "Ticks"
    },
    "MINECRAFT_HOURS": {
        "index": 2,
        "name": "Minecraft Hours"
    },
    "REAL_MINUTES": {
        "index": 3,
        "name": "Real Minutes"
    }
}
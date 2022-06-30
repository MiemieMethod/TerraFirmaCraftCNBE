# coding=utf-8

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.minecraftEnum as MinecraftEnum

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

import tfcscr.utils.blockFactory as BlockFactory
import tfcscr.utils.commonUtils as CommonUtils

# 服务端
def on_use(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and hasattr(block_cls, "on_use") and block_cls.on_use(data) or cancel
    print("===== blockHelper on_use =====", cancel)
    return cancel

# 客户端
def on_use_client(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and hasattr(block_cls, "on_use_client") and block_cls.on_use_client(data) or cancel
    print("===== blockHelper on_use_client =====", cancel)
    return cancel

# 服务端
def on_place(data):
    cancel = False
    relative = CommonUtils.get_relative(data["face"], data["x"], data["y"], data["z"], data["dimensionId"])
    print("===== blockHelper on_place =====", relative)
    block_cls = BlockFactory.get_block_class(data["fullName"])
    cancel = block_cls and hasattr(block_cls, "on_place") and block_cls.on_place(data, relative) or cancel
    relative_block_cls = BlockFactory.get_block_class(relative["name"])
    cancel = relative_block_cls and hasattr(relative_block_cls, "on_place_on") and relative_block_cls.on_place_on(data, relative) or cancel
    print("===== blockHelper on_place =====", cancel)
    return cancel

# 服务端
def on_neighbor_changed(data):
    block_cls = BlockFactory.get_block_class(data["blockName"])
    block_cls and hasattr(block_cls, "on_neighbor_changed") and block_cls.on_neighbor_changed(data)
    print("===== blockHelper on_neighbor_changed =====")

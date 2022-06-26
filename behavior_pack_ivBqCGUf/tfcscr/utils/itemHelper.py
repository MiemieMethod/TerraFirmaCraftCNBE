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

# 服务端
def get_relative(side, x, y, z, dim):
    if side == MinecraftEnum.Facing.Down:
        y = y + 1
    elif side == MinecraftEnum.Facing.Up:
        y = y - 1
    elif side == MinecraftEnum.Facing.North:
        z = z + 1
    elif side == MinecraftEnum.Facing.South:
        z = z - 1
    elif side == MinecraftEnum.Facing.West:
        x = x + 1
    elif side == MinecraftEnum.Facing.East:
        x = x - 1
    print("===== itemHelper get_relative =====", x, y, z, side, dim)
    return ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((x, y, z), dim).update({"x": x, "y": y, "z": z})

# 客户端
def get_relative_client(side, x, y, z):
    if side == MinecraftEnum.Facing.Down:
        y = y + 1
    elif side == MinecraftEnum.Facing.Up:
        y = y - 1
    elif side == MinecraftEnum.Facing.North:
        z = z + 1
    elif side == MinecraftEnum.Facing.South:
        z = z - 1
    elif side == MinecraftEnum.Facing.West:
        x = x + 1
    elif side == MinecraftEnum.Facing.East:
        x = x - 1
    print("===== itemHelper get_relative_client =====", x, y, z, side)
    return ClientCompFactory.CreateBlockInfo(clientApi.GetLevelId()).GetBlock((x, y, z)).update({"x": x, "y": y, "z": z})

# 服务端
def on_use_on(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and block_cls.on_use_on(data) or cancel
    print("===== itemHelper on_use_on =====", cancel)
    return cancel

# 客户端
def on_use_on_client(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and block_cls.on_use_on_client(data) or cancel
    print("===== itemHelper on_use_on_client =====", cancel)
    return cancel
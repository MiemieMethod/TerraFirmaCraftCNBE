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
    print("===== blockHelper get_relative =====", x, y, z, side, dim)
    return ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((x, y, z), dim)

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
    print("===== blockHelper get_relative_client =====", x, y, z, side)
    return ClientCompFactory.CreateBlockInfo(clientApi.GetLevelId()).GetBlock((x, y, z)).update({"x": x, "y": y, "z": z})

# 服务端
def on_use(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and block_cls.on_use(data) or cancel
    print("===== blockHelper on_use =====", cancel)
    return cancel

# 客户端
def on_use_client(data):
    cancel = False
    block_cls = BlockFactory.get_block_class(data["blockName"])
    cancel = block_cls and block_cls.on_use_client(data) or cancel
    print("===== blockHelper on_use_client =====", cancel)
    return cancel

# 服务端
def on_place(data):
    cancel = False
    relative = get_relative(data["face"], data["x"], data["y"], data["z"], data["dimensionId"])
    print("===== blockHelper on_place =====", relative)
    block_cls = BlockFactory.get_block_class(data["fullName"])
    cancel = block_cls and block_cls.on_place(data, relative) or cancel
    relative_block_cls = BlockFactory.get_block_class(relative["name"])
    cancel = relative_block_cls and relative_block_cls.on_place_on(data, relative) or cancel
    print("===== blockHelper on_place =====", cancel)
    return cancel

# 服务端
def on_neighbor_changed(data):
    block_cls = BlockFactory.get_block_class(data["blockName"])
    block_cls and block_cls.on_neighbor_changed(data)
    print("===== blockHelper on_neighbor_changed =====")

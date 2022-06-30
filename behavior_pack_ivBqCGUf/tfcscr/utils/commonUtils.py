
from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import mod.common.minecraftEnum as MinecraftEnum

ServerSystem = serverApi.GetServerSystemCls()
ServerCompFactory = serverApi.GetEngineCompFactory()
ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

game_comp = ServerCompFactory.CreateGame(serverApi.GetLevelId())
game_comp_client = ClientCompFactory.CreateGame(clientApi.GetLevelId())

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
    new_block = ServerCompFactory.CreateBlockInfo(serverApi.GetLevelId()).GetBlockNew((x, y, z), dim)
    new_block["x"] = x
    new_block["y"] = y
    new_block["z"] = z
    print("===== itemHelper get_relative =====", x, y, z, side, dim, new_block)
    return new_block

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
    return ClientCompFactory.CreateBlockInfo(clientApi.GetLevelId()).GetBlock((x, y, z)) + (x, y, z)

# 共用
def get_enum_name(key = "", enum = ""):
    return "tfc.enum." + enum + "." + key.lower()

# 服务端
def i18n(key):
    return game_comp.GetChinese(key)

# 客户端
def i18n_client(key):
    return game_comp_client.GetChinese(key)

# 共用
def refact_user_data(dirty):
    clean = {}
    if dirty == None:
        return None
    for item in dirty:
        if not "__type__" in dirty[item] and isinstance(dirty[item], dict):
            clean[item] = refact_user_data(dirty[item])
        elif isinstance(dirty[item], list):
            for index in range(len(dirty[item])):
                clean[item][index] = refact_user_data(dirty[item])
        elif dirty[item] == None:
            clean[item] = None
        elif "__type__" in dirty[item]:
            clean[item] = dirty[item]["__value__"]
        else:
            clean[item] = dirty[item]
    return clean
            
    
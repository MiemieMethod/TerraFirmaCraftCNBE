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
import tfcscr.utils.blockActorFactory as BlockActorFactory

# 服务端
def on_block_actor_tick(data):
    block_actor_cls = BlockActorFactory.get_block_actor_class(data["blockName"])
    block_actor_cls and block_actor_cls.on_block_actor_tick(data)
    # print("===== blockActorHelper on_block_actor_tick =====")

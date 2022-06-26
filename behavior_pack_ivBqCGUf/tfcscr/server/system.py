# -*- coding: utf-8 -*-

from mod_log import logger as logger
import mod.server.extraServerApi as serverApi
import tfcscr.utils.blockHelper as BlockHelper
import tfcscr.utils.itemHelper as ItemHelper
import tfcscr.utils.blockActorHelper as BlockActorHelper

ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

class TerraFirmaCraftServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        super(TerraFirmaCraftServerSystem, self).__init__(namespace, systemName)
        print("===== TerraFirmaCraft ServerSystem init =====")
        self.ListenEvent()

    def Destroy(self):
        print("===== TerraFirmaCraft ServerSystem Destroy =====")
        self.UnListenEvent()

    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerEntityTryPlaceBlockEvent", self, self.ServerEntityTryPlaceBlock)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerBlockUseEvent", self, self.ServerBlockUse)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerItemUseOnEvent", self, self.ServerItemUseOn)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerBlockEntityTickEvent", self, self.ServerBlockEntityTick)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "BlockNeighborChangedServerEvent", self, self.BlockNeighborChanged)

    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerEntityTryPlaceBlockEvent", self, self.ServerEntityTryPlaceBlock)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerBlockUseEvent", self, self.ServerBlockUse)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerItemUseOnEvent", self, self.ServerItemUseOn)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerBlockEntityTickEvent", self, self.ServerBlockEntityTick)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "BlockNeighborChangedServerEvent", self, self.BlockNeighborChanged)

    def ServerEntityTryPlaceBlock(self, args):
        print("==== ServerEntityTryPlaceBlockEvent ====", args)
        args["cancel"] = BlockHelper.on_place(args)

    def ServerBlockUse(self, args):
        print("==== ServerBlockUse ====", args)
        args["cancel"] = BlockHelper.on_use(args)

    def ServerItemUseOn(self, args):
        print("==== ServerItemUseOn ====", args)
        args["ret"] = ItemHelper.on_use_on(args)

    def ServerBlockEntityTick(self, args):
        # print("==== ServerBlockEntityTick ====", args)
        BlockActorHelper.on_block_actor_tick(args)

    def BlockNeighborChanged(self, args):
        # print("==== BlockNeighborChanged ====", args)
        BlockHelper.on_neighbor_changed(args)

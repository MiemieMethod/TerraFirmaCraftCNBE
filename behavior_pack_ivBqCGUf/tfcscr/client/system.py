# -*- coding: utf-8 -*-

from mod_log import logger as logger
import mod.client.extraClientApi as clientApi
import tfcscr.utils.blockHelper as BlockHelper
import tfcscr.utils.itemHelper as ItemHelper

ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

class TerraFirmaCraftClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        super(TerraFirmaCraftClientSystem, self).__init__(namespace, systemName)
        print("===== TerraFirmaCraft ClientSystem init =====")
        self.player_container_info = {}
        self.tick_count = 0
        self.ListenEngineEvent()

    def Destroy(self):
        print("===== TerraFirmaCraft ClientSystem Destroy =====")
        self.UnListenEngineEvent()

    def ListenEngineEvent(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientBlockUseEvent", self, self.ClientBlockUse)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientItemUseOnEvent", self, self.ClientItemUseOn)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestOpenEvent", self, self.ClientChestOpen)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestCloseEvent", self, self.ClientChestClose)

    def UnListenEngineEvent(self):
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientBlockUseEvent", self, self.ClientBlockUse)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientItemUseOnEvent", self, self.ClientItemUseOn)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestOpenEvent", self, self.ClientChestOpen)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestCloseEvent", self, self.ClientChestClose)

    def Update(self):
        self.tick_count = self.tick_count + 1
        # print("===== TerraFirmaCraft ClientSystem Update =====")

    def ClientBlockUse(self, args):
        print("==== ClientBlockUse ====", args)
        args["cancel"] = BlockHelper.on_use_client(args)

    def ClientItemUseOn(self, args):
        print("==== ClientItemUseOn ====", args)
        args["ret"] = ItemHelper.on_use_on_client(args)

    def ClientChestOpen(self, args):
        self.player_container_info[args["playerId"]] = (args["x"], args["y"], args["z"])
        self.NotifyToServer("ServerChestOpenEvent", args)
        print("==== ClientChestOpen ====", args)

    def ClientChestClose(self, args):
        self.NotifyToServer("ServerChestCloseEvent", {"playerId": clientApi.GetLocalPlayerId()})
        del self.player_container_info[clientApi.GetLocalPlayerId()]
        print("==== ClientChestClose ====", args, clientApi.GetLocalPlayerId())

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
        self.ListenEvent()

    def Destroy(self):
        print("===== TerraFirmaCraft ClientSystem Destroy =====")
        self.UnListenEvent()

    def ListenEvent(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientBlockUseEvent", self, self.ClientBlockUse)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientItemUseOnEvent", self, self.ClientItemUseOn)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestOpenEvent", self, self.ClientChestOpen)

    def UnListenEvent(self):
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientBlockUseEvent", self, self.ClientBlockUse)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientItemUseOnEvent", self, self.ClientItemUseOn)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestOpenEvent", self, self.ClientChestOpen)

    def ClientBlockUse(self, args):
        print("==== ClientBlockUse ====", args)
        args["cancel"] = BlockHelper.on_use_client(args)

    def ClientItemUseOn(self, args):
        print("==== ClientItemUseOn ====", args)
        args["ret"] = ItemHelper.on_use_on_client(args)

    def ClientChestOpen(self, args):
        print("==== ClientChestOpen ====", args)

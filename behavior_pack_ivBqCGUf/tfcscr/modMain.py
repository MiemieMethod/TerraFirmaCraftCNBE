# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="TerraFirmaCraft", version="0.0.1")
class TerraFirmaCraft(object):

    def __init__(self):
        print("===== TerraFirmaCraft init =====")

    @Mod.InitServer()
    def TerraFirmaCraftServerInit(self):
        print("===== TerraFirmaCraft ServerSystem register =====")
        serverApi.RegisterSystem("TerraFirmaCraft", "ServerSystem", "tfcscr.server.system.TerraFirmaCraftServerSystem")

    @Mod.DestroyServer()
    def TerraFirmaCraftServerDestroy(self):
        print("===== TerraFirmaCraft ServerSystem destroy =====")

    @Mod.InitClient()
    def TerraFirmaCraftClientInit(self):
        print("===== TerraFirmaCraft ClientSystem register =====")
        clientApi.RegisterSystem("TerraFirmaCraft", "ClientSystem", "tfcscr.client.system.TerraFirmaCraftClientSystem")

    @Mod.DestroyClient()
    def TerraFirmaCraftClientDestroy(self):
        print("===== TerraFirmaCraft ClientSystem destroy =====")
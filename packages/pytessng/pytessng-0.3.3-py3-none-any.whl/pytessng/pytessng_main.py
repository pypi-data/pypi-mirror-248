import os
import sys
from PySide2.QtWidgets import QApplication

from pytessng.DLLs.Tessng import TessngFactory
from pytessng.Tessng.MyPlugin import MyPlugin


class TessngObject:
    def __init__(self, extension=False):
        # 工作空间是本进程所在的路径
        workspace_path = os.path.join(os.getcwd(), "WorkSpace")
        # 创建文件夹
        os.makedirs(workspace_path, exist_ok=True)

        self.app = QApplication()
        self.workspace = workspace_path
        self.config = {
            '__workspace': self.workspace, # 工作空间
            '__simuafterload': False, # 加载路网后是否自动启动仿真
            '__custsimubysteps': False, # 是否自定义仿真调用频率
            '__allowspopup': False, # 禁止弹窗
            '__cacheid': True, # 快速创建路段
        }
        self.plugin = MyPlugin(extension)
        self.factory = TessngFactory()
        self.tessng = self.factory.build(self.plugin, self.config)

        # 启动
        self.run()

    def run(self, ):
        if self.tessng is not None:
            sys.exit(self.app.exec_())
        else:
            sys.exit()

import os
import subprocess
import traceback
from functools import partial, reduce
from pathlib import Path
from ipaddress import ip_address
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyautogui
import webbrowser
from kafka import KafkaConsumer

from pytessng.DLLs.Tessng import tessngIFace
from pytessng.Toolbox.other2tess.other2tess import other2tess
from pytessng.Toolbox.tess2other.tess2other import tess2other
from pytessng.Toolbox.link_processing import link_processing


# 全局变量类
class GlobalVar():
    # 是否需要打断路段
    is_need_split_link = False
    # 打断路段的action
    action_split_link = None

    # 车辆轨迹的投影
    traj_proj = None
    # 车辆轨迹保存为JSON文件路径
    traj_json_config = None
    # 车辆轨迹上传至kafka的配置
    traj_kafka_config = None


# 通用函数类
class Tools():
    # 获取电脑屏幕的尺寸
    screen_width, screen_height = pyautogui.size()

    # 默认打开和保存的位置
    default_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # 设置面板的各属性
    @staticmethod
    def set_attribution(widget):
        # 设置名称
        widget.setWindowTitle(widget.name)
        # 设置图标
        widget.setWindowIcon(QIcon("pytessng/Files/ico/TESSNG.ico"))
        # 设置位置和尺寸
        x = (Tools.screen_width - widget.size().width()) // 2
        y = (Tools.screen_height - widget.size().height()) // 2
        widget.setGeometry(x, y, widget.width, widget.height)
        # 设置尺寸固定
        # widget.setFixedSize(widget.width, widget.height)
        # 设置窗口标志位，使其永远在最前面
        widget.setWindowFlags(widget.windowFlags() | Qt.WindowStaysOnTopHint)

    # 读取.tess文件的属性
    @staticmethod
    def read_file_proj():
        iface = tessngIFace()
        netiface = iface.netInterface()
        attrs = netiface.netAttrs().otherAttrs()
        if attrs.get("proj_center_coord"):
            proj = attrs["proj_center_coord"]
            info = f"lon_0 = {proj['lon_0']}  lat_0 = {proj['lat_0']}"
        else:
            proj = {"lon_0": None, "lat_0": None}
            info = "（未在TESS文件中读取到投影信息）"
        return proj, info

    # 读取.tess文件的名称
    @staticmethod
    def read_file_name():
        iface = tessngIFace()
        tmpNetPath = iface.netInterface().netFilePath()
        base_name = os.path.basename(tmpNetPath)
        file_name, _ = os.path.splitext(base_name)
        return file_name

    # 获取打开文件的路径
    @staticmethod
    def open_file(formats):
        # 指定文件后缀
        xodrSuffix = ";;".join([f"{format} Files (*.{suffix})" for format, suffix in formats])
        # 默认读取位置是电脑桌
        dbDir = Tools.default_path
        # 弹出文件选择框
        file_path, filtr = QFileDialog.getOpenFileName(None, "打开文件", dbDir, xodrSuffix)
        return file_path

    # 获取打开文件夹的路径
    @staticmethod
    def open_folder():
        # 默认读取位置是电脑桌面
        dbDir = Tools.default_path
        # 弹出文件选择框
        folder_path = QFileDialog.getExistingDirectory(None, "打开文件夹", dbDir)
        return folder_path

    # 选择保存文件路径
    @staticmethod
    def save_file(format):
        # 指定文件后缀
        xodrSuffix = f"{format[0]} Files (*.{format[1]})"
        # 默认保存位置是电脑桌面+文件名称
        dbDir = os.path.join(Tools.default_path, Tools.read_file_name())
        # 弹出文件选择框
        file_path, filtr = QFileDialog.getSaveFileName(None, "保存文件", dbDir, xodrSuffix)
        return file_path

    # 弹出警告或提示提示框
    @staticmethod
    def show_info_box(content, mode="info"):
        msg_box = QMessageBox()
        if mode == "warning":
            msg_box.setWindowTitle("警告")
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setWindowTitle("提示")
            msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(content)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)  # 设置窗口标志，使其显示在最前面
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    # 确认弹窗
    @staticmethod
    def show_confirm_dialog(messages):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("确认框")
        msg_box.setText(messages["content"])

        # 设置按钮
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        # 设置默认选项
        msg_box.setDefaultButton(QMessageBox.Cancel)
        # 修改按钮上的文本
        msg_box.button(QMessageBox.Yes).setText(messages["yes"])
        msg_box.button(QMessageBox.Cancel).setText("取消")
        # 获取选择结果
        result = msg_box.exec_()

        return result

    # 路网创建
    @staticmethod
    def network_import(widget, params):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.正在仿真中无法导入
        if iface.simuInterface().isRunning() or iface.simuInterface().isPausing():
            Tools.show_info_box("请先停止仿真！", "warning")
            return

        # 2.关闭窗口
        widget.close()

        # 3.执行转换
        try:
            error_message = other2tess(netiface, params, widget.mode)
            Tools.show_info_box("导入成功")
        except:
            error_message = str(traceback.format_exc())
            Tools.show_info_box("导入失败", "warning")
        print(error_message)

    # 路网导出
    @staticmethod
    def network_export(widget):
        iface = tessngIFace()
        netiface = iface.netInterface()

        # 1.检查路网上是否有路段
        if netiface.linkCount() == 0:
            Tools.show_info_box("当前路网没有路段 !", "warning")
            return

        # 2.获取投影
        if widget.checkBox.isChecked() and widget.radio_proj_custom.isChecked():
            lon_0 = float(widget.lineEdit_proj_custom_lon.text())
            lat_0 = float(widget.lineEdit_proj_custom_lat.text())
            proj = {"lon_0": lon_0, "lat_0": lat_0}
        else:
            proj = widget.file_proj

        # 3.获取保存路径
        file_path = Tools.save_file(widget.format)
        if not file_path:
            return

        # 4.执行转换
        parms = {**proj, "file_path": file_path}
        tess2other(netiface, parms, widget.mode)

        # 5.关闭窗口
        widget.close()

        # 6.提示信息
        Tools.show_info_box("导出成功！")


# 菜单栏类
class MyMenu(QMenu):
    def __init__(self, *args):
        super().__init__(*args)
        # 文件路径
        self.instruction_path = Path(__file__).resolve().parent / ".." / "Files" / "Doc" / "PyTessng Instruction.pdf"
        self.examples_path = "file:\\" + str(Path(__file__).resolve().parent.parent / "Files" / "Examples")

        # 初始化
        self.init()

    def init(self):
        self.setObjectName("PyTessng")
        self.setTitle("PyTessng")

        # 1.路网创建
        self.menu_network_import = self.addMenu('路网创建')
        # 1.1.导入OpenDrive
        self.action_network_import_opendrive = self.menu_network_import.addAction('导入OpenDrive')
        self.action_network_import_opendrive.triggered.connect(self.network_import_opendrive)
        # 1.2.导入Shape
        self.action_network_import_shape = self.menu_network_import.addAction('导入Shape')
        self.action_network_import_shape.triggered.connect(self.network_import_shape)
        # 1.3.导入OpenStreetMap
        self.action_network_import_openstreetmap = self.menu_network_import.addAction('导入OpenStreetMap')
        self.action_network_import_openstreetmap.triggered.connect(self.network_import_openstreetmap)
        # 1.4.导入Excel
        self.action_network_import_excel = self.menu_network_import.addAction('导入Excel')
        self.action_network_import_excel.triggered.connect(self.network_import_excel)

        # 2.路网数据导出
        self.menu_network_export = self.addMenu('路网数据导出')
        # 2.1.导出OpenDrive
        self.action_network_export_opendrive = self.menu_network_export.addAction('导出为OpenDrive')
        self.action_network_export_opendrive.triggered.connect(self.network_export_opendrive)
        # 2.2.导出Shape
        self.action_network_export_shape = self.menu_network_export.addAction('导出为Shape')
        self.action_network_export_shape.triggered.connect(self.network_export_shape)
        # 2.3.导出GeoJson
        self.action_network_export_geojson = self.menu_network_export.addAction('导出为GeoJson')
        self.action_network_export_geojson.triggered.connect(self.network_export_geojson)
        # 2.4.导出Unity
        self.action_network_export_unity = self.menu_network_export.addAction('导出为Unity')
        self.action_network_export_unity.triggered.connect(self.network_export_unity)
        # 2.5.导出Json
        self.action_network_export_json = self.menu_network_export.addAction('导出为Json')
        self.action_network_export_json.triggered.connect(self.network_export_json)

        # 3.路网编辑
        self.menu_network_edit = self.addMenu('路网编辑')
        # 3.1.创建路段
        self.action_network_edit_create = self.menu_network_edit.addAction('创建路段')
        self.action_network_edit_create.triggered.connect(self.network_edit_create)
        # 3.2.打断路段
        self.action_network_edit_split = QAction("打断路段")
        self.action_network_edit_split.setCheckable(True)
        self.menu_network_edit.addAction(self.action_network_edit_split)
        self.action_network_edit_split.triggered.connect(self.network_edit_split)
        GlobalVar.action_split_link = self.action_network_edit_split
        # 3.3.合并路段
        self.action_network_edit_connect = self.menu_network_edit.addAction('合并路段')
        self.action_network_edit_connect.triggered.connect(self.network_edit_connect)
        # 3.4.简化路网
        self.action_network_edit_simplify = self.menu_network_edit.addAction('简化路网')
        self.action_network_edit_simplify.triggered.connect(self.network_edit_simplify)

        # 4.轨迹导出
        self.action_trajectory_export = self.addAction('轨迹数据输出')
        self.action_trajectory_export.triggered.connect(self.trajectory_export)

        # 5.更多
        self.menu_more = self.addMenu('更多')
        # 5.1.打开说明书
        self.action_open_instruction = self.menu_more.addAction("打开说明书")
        self.action_open_instruction.triggered.connect(partial(self.open_instruction))
        # 5.2.打开样例
        self.action_open_examples = self.menu_more.addAction("打开路网创建样例")
        self.action_open_examples.triggered.connect(partial(self.open_examples))

    # 1.1.导入OpenDrive
    def network_import_opendrive(self):
        self.dialog_network_import_opendrive = NetworkImportOpendrive()
        self.dialog_network_import_opendrive.show()

    # 1.2.导入Shape
    def network_import_shape(self):
        self.dialog_network_import_shape = NetworkImportShape()
        self.dialog_network_import_shape.show()

    # 1.3.导入OpenStreetMap
    def network_import_openstreetmap(self):
        self.dialog_network_import_openstreetmap = NetworkImportOpenstreetmap()
        self.dialog_network_import_openstreetmap.show()

    # 1.4.导入Excel
    def network_import_excel(self):
        self.dialog_network_import_excel = NetworkImportExcel()
        self.dialog_network_import_excel.show()

    # 2.1.导出为OpenDrive
    def network_export_opendrive(self):
        self.dialog_network_export_opendrive = NetworkExportOpendrive()
        self.dialog_network_export_opendrive.show()

    # 2.2.导出为Shape
    def network_export_shape(self):
        self.dialog_network_export_shape = NetworkExportShape()
        self.dialog_network_export_shape.show()

    # 2.3.导出为GeoJson
    def network_export_geojson(self):
        self.dialog_network_export_geojson = NetworkExportGeojson()
        self.dialog_network_export_geojson.show()

    # 2.4.导出为Unity
    def network_export_unity(self):
        self.dialog_network_export_unity = NetworkExportUnity()

    # 2.5.导出为Json
    def network_export_json(self):
        self.dialog_network_export_json = NetworkExportJson()
        self.dialog_network_export_json.show()

    # 3.1.创建路段
    def network_edit_create(self):
        iface = tessngIFace()
        guiiface = iface.guiInterface()
        # 将按钮修改成【取消工具】
        guiiface.actionNullGMapTool().trigger()
        #
        self.dialog_network_edit_create = NetworkEditCreate()
        self.dialog_network_edit_create.show()

    # 3.2.打断路段
    def network_edit_split(self):
        iface = tessngIFace()
        guiiface = iface.guiInterface()
        # 将按钮修改成【取消工具】
        guiiface.actionNullGMapTool().trigger()
        # 获取按钮状态
        action = self.action_network_edit_split
        if action.isChecked():
            GlobalVar.is_need_split_link = True
            action.setText("取消选中打断路段")
        else:
            GlobalVar.is_need_split_link = False
            action.setText("打断路段")

    # 3.3.合并路段
    def network_edit_connect(self):
        iface = tessngIFace()
        netiface = iface.netInterface()
        # 1.执行连接
        state, message = link_processing.joinLink(netiface)
        # 2.显示信息
        if state:
            Tools.show_info_box("路段合并完成")
            print(message)
        else:
            Tools.show_info_box(message, "warning")

    # 3.4.简化路网
    def network_edit_simplify(self):
        confirm = Tools.show_confirm_dialog({"content": "简化路网前需要先保存路网", "yes": "保存并简化路网"})
        if confirm != QMessageBox.Yes:
            return

        iface = tessngIFace()
        netiface = iface.netInterface()
        # 1.执行简化
        state, message = link_processing.simplifyTessngFile(netiface)
        # 2.显示信息
        if state:
            Tools.show_info_box("已经在同一目录下生成简化版路网，且当前已经打开！")
            print(message)
        else:
            Tools.show_info_box(message, "warning")

    # 4.导出轨迹
    def trajectory_export(self):
        self.dialog_trajectory_export = TrajectoryExport()
        self.dialog_trajectory_export.show()

    # 5.1.打开说明书
    def open_instruction(self):
        webbrowser.open(self.instruction_path, new=2)

    # 5.2.打开样例
    def open_examples(self):
        subprocess.Popen(['explorer', self.examples_path], shell=True)


# 1.1.导入OpenDrive
class NetworkImportOpendrive(QWidget):
    # 用类变量记住之前的选择
    file_path = None

    def __init__(self):
        super().__init__()
        self.name = "导入OpenDrive"
        self.width = 300
        self.height = 200
        self.format = [("OpenDrive", "xodr")]
        self.mode = "opendrive"

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        # 第一行：文本框和按钮
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(500)
        self.button_select_file = QPushButton('文件选择')
        horizontal_layout_1 = QHBoxLayout()
        horizontal_layout_1.addWidget(self.lineEdit)
        horizontal_layout_1.addWidget(self.button_select_file)
        # 第二行：文本和下拉框
        self.label_select_length = QLabel("路段最小分段长度：")
        self.combo = QComboBox()
        self.combo.addItems(("0.5 m", "1 m", "5 m", "10 m", "20 m"))
        horizontal_layout_2 = QHBoxLayout()
        horizontal_layout_2.addWidget(self.label_select_length)
        horizontal_layout_2.addWidget(self.combo)
        # 第三行：文本框
        self.label_select_type = QLabel("生成车道类型选择：")
        # 第四行：多选栏
        self.checkBox_1 = QCheckBox('机动车道')
        self.checkBox_2 = QCheckBox('非机动车道')
        self.checkBox_3 = QCheckBox('人行道')
        self.checkBox_4 = QCheckBox('应急车道')
        self.checkBoxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4]
        horizontal_layout_3 = QHBoxLayout()
        for checkBox in self.checkBoxes:
            horizontal_layout_3.addWidget(checkBox)
        # 第五行：按钮
        self.button = QPushButton('生成路网文件')

        # 总体布局
        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout_1)
        layout.addLayout(horizontal_layout_2)
        layout.addWidget(self.label_select_type)
        layout.addLayout(horizontal_layout_3)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.lineEdit.textChanged.connect(self.monitor_state)
        for checkBox in self.checkBoxes:
            checkBox.stateChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button_select_file.clicked.connect(self.select_file)
        self.button.clicked.connect(self.create_network)

        # 设置默认模式和初始状态
        if NetworkImportOpendrive.file_path:
            self.lineEdit.setText(NetworkImportOpendrive.file_path)
        self.combo.setCurrentIndex(1)
        for checkBox in self.checkBoxes:
            checkBox.setCheckState(Qt.Checked)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 获取状态
        file_path = self.lineEdit.text()
        isfile = os.path.isfile(file_path)
        checkbox_isChecked = any(checkbox.isChecked() for checkbox in self.checkBoxes)
        enabled = isfile and checkbox_isChecked

        # 设置可用状态
        self.button.setEnabled(enabled)

    # 选择文件
    def select_file(self):
        file_path = Tools.open_file(self.format)
        if file_path:
            # 显示文件路径在LineEdit中
            self.lineEdit.setText(file_path)

            NetworkImportOpendrive.file_path = file_path

    # 创建路网
    def create_network(self):
        # 获取路径
        file_path = self.lineEdit.text()
        # 获取分段长度
        step_length = float(self.combo.currentText().split()[0])
        # 获取车道类型
        lane_types = [checkbox.text() for checkbox in self.checkBoxes if checkbox.isChecked()]
        # 构建参数
        params = {
            "file_path": file_path,
            "step_length": step_length,
            "lane_types": lane_types
        }
        # 执行创建
        Tools.network_import(self, params)


# 1.2.导入Shape
class NetworkImportShape(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "导入Shape"
        self.width = 300
        self.height = 200
        self.format = None
        self.mode = "shape"

        # 标签信息
        self.info_need_file = "待选择文件"
        self.info_no_file = "该路径下无合法文件"
        self.info_not_need_file = "不选择文件"

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        # 第一行：文本框和按钮
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(500)
        self.button_select_folder = QPushButton('文件夹选择')
        horizontal_layout_1 = QHBoxLayout()
        horizontal_layout_1.addWidget(self.lineEdit)
        horizontal_layout_1.addWidget(self.button_select_folder)
        # 第二行：单选框
        self.label_select_coordType = QLabel("读取坐标类型：")
        self.radio_coordType_dke = QRadioButton('笛卡尔坐标')
        self.radio_coordType_jwd = QRadioButton('经纬度坐标')
        self.radio_group_coordType = QButtonGroup(self)
        self.radio_group_coordType.addButton(self.radio_coordType_dke)
        self.radio_group_coordType.addButton(self.radio_coordType_jwd)
        horizontal_layout_2 = QHBoxLayout()
        horizontal_layout_2.addWidget(self.label_select_coordType)
        horizontal_layout_2.addWidget(self.radio_coordType_dke)
        horizontal_layout_2.addWidget(self.radio_coordType_jwd)
        # 第三行：单选框
        self.label_select_laneDataType = QLabel("导入车道数据类型：")
        self.radio_laneDataType_center = QRadioButton('车道中心线')
        self.radio_laneDataType_boundary = QRadioButton('车道边界线')
        self.radio_group_laneDataType = QButtonGroup(self)
        self.radio_group_laneDataType.addButton(self.radio_laneDataType_center)
        self.radio_group_laneDataType.addButton(self.radio_laneDataType_boundary)
        horizontal_layout_3 = QHBoxLayout()
        horizontal_layout_3.addWidget(self.label_select_laneDataType)
        horizontal_layout_3.addWidget(self.radio_laneDataType_center)
        horizontal_layout_3.addWidget(self.radio_laneDataType_boundary)
        # 第四行：下拉框
        self.label_selcet_laneFileName = QLabel("路段车道文件名称：")
        self.combo_laneFileName = QComboBox()
        self.combo_laneFileName.addItems((self.info_need_file,))
        horizontal_layout_4 = QHBoxLayout()
        horizontal_layout_4.addWidget(self.label_selcet_laneFileName)
        horizontal_layout_4.addWidget(self.combo_laneFileName)
        # 第五行：下拉框
        self.label_select_laneConnFileName = QLabel("连接段车道文件名称：")
        self.combo_laneConnFileName = QComboBox()
        self.combo_laneConnFileName.addItems((self.info_need_file,))
        horizontal_layout_5 = QHBoxLayout()
        horizontal_layout_5.addWidget(self.label_select_laneConnFileName)
        horizontal_layout_5.addWidget(self.combo_laneConnFileName)
        # 第六行：按钮
        self.button = QPushButton('生成路网文件')

        # 总体布局
        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout_1)
        layout.addLayout(horizontal_layout_2)
        layout.addLayout(horizontal_layout_3)
        layout.addLayout(horizontal_layout_4)
        layout.addLayout(horizontal_layout_5)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.lineEdit.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button_select_folder.clicked.connect(self.select_folder)
        self.button.clicked.connect(self.create_network)

        # 设置默认模式与初始状态
        self.radio_coordType_dke.setChecked(True)
        self.radio_laneDataType_center.setChecked(True)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 获取文件夹路径
        folder_path = self.lineEdit.text()
        # 判断文件夹是否存在
        isdir = os.path.isdir(folder_path)
        # 设置下拉框状态
        self.set_combo(folder_path, isdir)
        # 获取下拉框状态
        combo = all(
            combo_text not in [self.info_need_file, self.info_no_file]
            for combo_text in [self.combo_laneFileName.currentText(), self.combo_laneConnFileName.currentText()]
        )
        enabled = isdir and combo

        # 设置可用状态
        self.button.setEnabled(enabled)

    # 设置下拉框状态
    def set_combo(self, folder_path, isdir):
        if not folder_path:
            new_items_laneFileName = new_items_laneConnFileName = (self.info_need_file,)
        elif isdir:
            public_file = self.read_public_files(folder_path)
            if public_file:
                new_items_laneFileName = tuple(public_file)
                new_items_laneConnFileName = (self.info_not_need_file,) + tuple(public_file)
            else:
                new_items_laneFileName = new_items_laneConnFileName = (self.info_no_file,)
        else:
            new_items_laneFileName = new_items_laneConnFileName = (self.info_no_file,)
        # 重新设置QComboBox
        self.combo_laneFileName.clear()
        self.combo_laneConnFileName.clear()
        self.combo_laneFileName.addItems(new_items_laneFileName)
        self.combo_laneConnFileName.addItems(new_items_laneConnFileName)
        # self.combo_laneFileName.setCurrentIndex(0)
        # self.combo_laneConnFileName.setCurrentIndex(0)

    # 读取文件夹里的公共文件
    def read_public_files(self, folder_path):
        items = os.listdir(folder_path)
        file_dict = {".cpg": [], ".dbf": [], ".shp": [], ".shx": []}
        # 遍历每个文件和文件夹
        for item in items:
            item_path = os.path.join(folder_path, item)
            # 如果是文件
            if os.path.isfile(item_path):
                file_name, extension = os.path.splitext(item)
                if extension in file_dict:
                    file_dict[extension].append(file_name)
        public_file = reduce(set.intersection, map(set, file_dict.values())) or None
        return sorted(public_file)

    # 选择文件夹
    def select_folder(self):
        folder_path = Tools.open_folder()
        if folder_path:
            # 显示文件路径在LineEdit中
            self.lineEdit.setText(folder_path)

    # 创建路网
    def create_network(self):
        # 获取路径
        folder_path = self.lineEdit.text()
        # 获取坐标类型
        is_use_lon_and_lat = self.radio_coordType_jwd.isChecked()
        # 获取车道数据类型
        is_use_center_line = self.radio_laneDataType_center.isChecked()
        # 获取车道文件名称
        laneFileName = self.combo_laneFileName.currentText()
        # 获取车道连接文件名称
        laneConnectorFileName = self.combo_laneConnFileName.currentText()
        # 构建参数
        params = {
            "folder_path": folder_path,
            "is_use_lon_and_lat": is_use_lon_and_lat,
            "is_use_center_line": is_use_center_line,
            "laneFileName": laneFileName,
            "laneConnectorFileName": laneConnectorFileName
        }
        # 执行创建
        Tools.network_import(self, params)


# 1.3.导入OpenStreetMap
class NetworkImportOpenstreetmap(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "导入OpenStreetMap"
        self.width = 300
        self.height = 500
        self.format = [("OpenStreetMap", "osm")]
        self.mode = "osm"

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        # 第一行：单选框
        self.radio_offline = QRadioButton('导入离线文件')
        # 第二行：文本框和按钮
        self.lineEdit_offline_select_file = QLineEdit()
        self.lineEdit_offline_select_file.setFixedWidth(500)
        self.button_offline_select_file = QPushButton('文件选择')
        horizontal_layout_offline = QHBoxLayout()
        horizontal_layout_offline.addWidget(self.lineEdit_offline_select_file)
        horizontal_layout_offline.addWidget(self.button_offline_select_file)
        # 第三行：单选框
        self.radio_online = QRadioButton('网络接口拉取')
        # 第四行：文本和按钮
        self.label_online_network_scope = QLabel('生成路网范围：')
        self.button_online_network_scope = QPushButton('打开在线地图')
        horizontal_layout_online_network_scope = QHBoxLayout()
        horizontal_layout_online_network_scope.addWidget(self.label_online_network_scope)
        horizontal_layout_online_network_scope.addWidget(self.button_online_network_scope)
        # 第五行：文本和输入框
        self.label_online_coord_leftTop = QLabel('左上顶点经纬度：')
        self.lineEdit_online_coord_leftTop_lon = QLineEdit()
        self.lineEdit_online_coord_leftTop_lat = QLineEdit()
        horizontal_layout_online_coord_leftTop = QHBoxLayout()
        horizontal_layout_online_coord_leftTop.addWidget(self.label_online_coord_leftTop)
        horizontal_layout_online_coord_leftTop.addWidget(self.lineEdit_online_coord_leftTop_lon)
        horizontal_layout_online_coord_leftTop.addWidget(self.lineEdit_online_coord_leftTop_lat)
        # 第六行：文本和输入框
        self.label_online_coord_rightBottom = QLabel('右下顶点经纬度：')
        self.lineEdit_online_coord_rightBottom_lon = QLineEdit()
        self.lineEdit_online_coord_rightBottom_lat = QLineEdit()
        horizontal_layout_online_coord_rightBottom = QHBoxLayout()
        horizontal_layout_online_coord_rightBottom.addWidget(self.label_online_coord_rightBottom)
        horizontal_layout_online_coord_rightBottom.addWidget(self.lineEdit_online_coord_rightBottom_lon)
        horizontal_layout_online_coord_rightBottom.addWidget(self.lineEdit_online_coord_rightBottom_lat)
        # 第七行：勾选框
        self.checkBox_online_map_class = QCheckBox('生成路网地图')
        # 第八行：文本和下拉框
        self.label_online_map_class = QLabel("地图级别设置：")
        self.combo_online_map_class = QComboBox()
        self.combo_online_map_class.addItems((str(i) for i in range(15, 21)))
        horizontal_layout_online_map_class = QHBoxLayout()
        horizontal_layout_online_map_class.addWidget(self.label_online_map_class)
        horizontal_layout_online_map_class.addWidget(self.combo_online_map_class)
        # 第九行：按钮
        self.button = QPushButton('生成路网文件')

        # 限制输入框内容
        validator = QDoubleValidator()
        self.lineEdit_online_coord_leftTop_lon.setValidator(validator)
        self.lineEdit_online_coord_leftTop_lat.setValidator(validator)
        self.lineEdit_online_coord_rightBottom_lon.setValidator(validator)
        self.lineEdit_online_coord_rightBottom_lat.setValidator(validator)

        # Box布局 1
        group_box_1 = QGroupBox()
        group_box_1_layout = QVBoxLayout()
        group_box_1_layout.addLayout(horizontal_layout_offline)
        group_box_1.setLayout(group_box_1_layout)

        # Box布局 2.1
        group_box_2_1 = QGroupBox()
        group_box_2_1_layout = QVBoxLayout()
        group_box_2_1_layout.addLayout(horizontal_layout_online_coord_leftTop)
        group_box_2_1_layout.addLayout(horizontal_layout_online_coord_rightBottom)
        group_box_2_1.setLayout(group_box_2_1_layout)

        # Box布局 2.2
        group_box_2_2 = QGroupBox()
        group_box_2_2_layout = QVBoxLayout()
        group_box_2_2_layout.addLayout(horizontal_layout_online_map_class)
        group_box_2_2.setLayout(group_box_2_2_layout)

        # Box布局 2
        group_box_2 = QGroupBox()
        group_box_2_layout = QVBoxLayout()
        group_box_2_layout.addLayout(horizontal_layout_online_network_scope)
        group_box_2_layout.addWidget(group_box_2_1)
        group_box_2_layout.addWidget(self.checkBox_online_map_class)
        group_box_2_layout.addWidget(group_box_2_2)
        group_box_2.setLayout(group_box_2_layout)

        # 总体布局
        layout = QVBoxLayout()
        layout.addWidget(self.radio_offline)
        layout.addWidget(group_box_1)
        layout.addWidget(self.radio_online)
        layout.addWidget(group_box_2)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.radio_offline.toggled.connect(self.monitor_state)
        self.checkBox_online_map_class.stateChanged.connect(self.monitor_state)
        self.lineEdit_offline_select_file.textChanged.connect(self.monitor_state)
        self.lineEdit_online_coord_leftTop_lon.textChanged.connect(self.monitor_state)
        self.lineEdit_online_coord_leftTop_lat.textChanged.connect(self.monitor_state)
        self.lineEdit_online_coord_rightBottom_lon.textChanged.connect(self.monitor_state)
        self.lineEdit_online_coord_rightBottom_lat.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button_offline_select_file.clicked.connect(self.select_file)
        self.button_online_network_scope.clicked.connect(self.open_online_map)
        self.button.clicked.connect(self.create_network)

        # 设置默认模式和初始状态
        self.radio_offline.setChecked(True)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 获取状态
        enabled_offlie = self.radio_offline.isChecked()
        enabled_online_map_class = self.checkBox_online_map_class.isChecked()
        # 按钮状态
        file_path = self.lineEdit_offline_select_file.text()
        isfile = os.path.isfile(file_path)
        leftTop_lon = self.lineEdit_online_coord_leftTop_lon.text()
        leftTop_lat = self.lineEdit_online_coord_leftTop_lat.text()
        rightBottom_lon = self.lineEdit_online_coord_rightBottom_lon.text()
        rightBottom_lat = self.lineEdit_online_coord_rightBottom_lat.text()
        leftTop_is_ok = leftTop_lon and leftTop_lat and -180<float(leftTop_lon)<180 and -90<float(leftTop_lat)<90
        rightBottom_is_ok = rightBottom_lon and rightBottom_lat and -180<float(rightBottom_lon)<180 and -90<float(rightBottom_lat)<90
        enabled = bool(enabled_offlie and isfile) or bool(not enabled_offlie and leftTop_is_ok and rightBottom_is_ok)

        # 设置可用状态
        self.lineEdit_offline_select_file.setEnabled(enabled_offlie)
        self.button_offline_select_file.setEnabled(enabled_offlie)
        self.label_online_network_scope.setEnabled(not enabled_offlie)
        self.button_online_network_scope.setEnabled(not enabled_offlie)
        self.label_online_coord_leftTop.setEnabled(not enabled_offlie)
        self.label_online_coord_rightBottom.setEnabled(not enabled_offlie)
        self.lineEdit_online_coord_leftTop_lon.setEnabled(not enabled_offlie)
        self.lineEdit_online_coord_leftTop_lat.setEnabled(not enabled_offlie)
        self.lineEdit_online_coord_rightBottom_lon.setEnabled(not enabled_offlie)
        self.lineEdit_online_coord_rightBottom_lat.setEnabled(not enabled_offlie)
        self.checkBox_online_map_class.setEnabled(not enabled_offlie)
        self.label_online_map_class.setEnabled(not enabled_offlie and enabled_online_map_class)
        self.combo_online_map_class.setEnabled(not enabled_offlie and enabled_online_map_class)
        self.button.setEnabled(enabled)

    # 选择文件
    def select_file(self):
        file_path = Tools.open_file(self.format)
        if file_path:
            # 显示文件路径在LineEdit中
            self.lineEdit_offline_select_file.setText(file_path)

    # 打开在线地图
    def open_online_map(self):
        # TODO 通过王帅鹏的接口获取
        leftTop_lon, leftTop_lat, rightBottom_lon, rightBottom_lat = 116.397428, 39.90923, 116.401667, 39.913472

        self.lineEdit_online_coord_leftTop_lon.setText(str(leftTop_lon))
        self.lineEdit_online_coord_leftTop_lat.setText(str(leftTop_lat))
        self.lineEdit_online_coord_rightBottom_lon.setText(str(rightBottom_lon))
        self.lineEdit_online_coord_rightBottom_lat.setText(str(rightBottom_lat))

    # 创建路网
    def create_network(self):
        if self.radio_offline.isChecked():
            # 导入文件
            file_path = self.lineEdit_offline_select_file.text()
            # 构建参数
            params = {"osm_file_path": file_path}
        else:
            # 指定范围
            lon_min = float(self.lineEdit_online_coord_leftTop_lon.text())
            lon_max = float(self.lineEdit_online_coord_rightBottom_lon.text())
            lat_min = float(self.lineEdit_online_coord_rightBottom_lat.text())
            lat_max = float(self.lineEdit_online_coord_leftTop_lat.text())
            # 构建参数
            params = {
                "bounding_box": {
                    "lon_min": lon_min,
                    "lon_max": lon_max,
                    "lat_min": lat_min,
                    "lat_max": lat_max,
                }
            }
        # 执行创建
        Tools.network_import(self, params)


# 1.4.导入Excel
class NetworkImportExcel(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "导入Excel"
        self.width = 300
        self.height = 200
        self.format = [("Excel", "xlsx"), ("Excel", "xls"), ("CSV", "csv")]
        self.mode = "excel"

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        # 第一行：文本框和按钮
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(500)
        self.button_select_file = QPushButton('文件选择')
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.lineEdit)
        horizontal_layout.addWidget(self.button_select_file)
        # 第二行：按钮
        self.button = QPushButton('生成路网文件')

        # 总体布局
        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.lineEdit.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button_select_file.clicked.connect(self.select_file)
        self.button.clicked.connect(self.create_network)

        # 设置默认模式和初始状态
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        file_path = self.lineEdit.text()
        enabled = os.path.isfile(file_path)

        # 设置可用状态
        self.button.setEnabled(enabled)

    # 选择文件
    def select_file(self):
        file_path = Tools.open_file(self.format)
        if file_path:
            # 显示文件路径在LineEdit中
            self.lineEdit.setText(file_path)

    # 创建路网
    def create_network(self):
        # 获取路径
        file_path = self.lineEdit.text()
        # 构建参数
        params = {
            "file_path": file_path,
        }
        # 执行创建
        Tools.network_import(self, params)


# 2.1.导出为OpenDrive
class NetworkExportOpendrive(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "导出为OpenDrive"
        self.width = 300
        self.height = 200
        self.format = ("OpenDrive", "xodr")
        self.mode = "opendrive"
        self.proj = None

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        self.file_proj, file_proj_info = Tools.read_file_proj()

        # 第一行：勾选框
        self.checkBox = QCheckBox('将投影中心的经纬度写入文件的header')
        # 第二行：单选框
        self.radio_proj_file = QRadioButton('使用原投影')
        # 第三行：文本
        self.label_proj_file = QLabel(file_proj_info)
        # 第四行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义墨卡托投影')
        # 第五行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.lineEdit_proj_custom_lon = QLineEdit()
        horizontal_layout_lon = QHBoxLayout()
        horizontal_layout_lon.addWidget(self.label_proj_custom_lon)
        horizontal_layout_lon.addWidget(self.lineEdit_proj_custom_lon)
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.lineEdit_proj_custom_lat = QLineEdit()
        horizontal_layout_lat = QHBoxLayout()
        horizontal_layout_lat.addWidget(self.label_proj_custom_lat)
        horizontal_layout_lat.addWidget(self.lineEdit_proj_custom_lat)
        # 第七行：按钮
        self.button = QPushButton('导出')

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.lineEdit_proj_custom_lon.setValidator(validator_coord)
        self.lineEdit_proj_custom_lat.setValidator(validator_coord)

        # Box布局
        group_box = QGroupBox()
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(self.radio_proj_file)
        group_box_layout.addWidget(self.label_proj_file)
        group_box_layout.addWidget(self.radio_proj_custom)
        group_box_layout.addLayout(horizontal_layout_lon)
        group_box_layout.addLayout(horizontal_layout_lat)
        group_box.setLayout(group_box_layout)

        # 总体布局
        layout = QVBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addWidget(group_box)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.checkBox.stateChanged.connect(self.monitor_state)
        self.radio_proj_custom.toggled.connect(self.monitor_state)
        self.lineEdit_proj_custom_lon.textChanged.connect(self.monitor_state)
        self.lineEdit_proj_custom_lat.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button.clicked.connect(partial(Tools.network_export, self))

        # 设置默认模式和初始状态
        if bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"]):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 勾选框的状态
        enabled_checkBox = self.checkBox.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"])
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()
        # 按钮状态
        enabled_button = True
        if enabled_checkBox and enabled_radio_proj:
            lon_0 = self.lineEdit_proj_custom_lon.text()
            lat_0 = self.lineEdit_proj_custom_lat.text()
            if not (lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90):
                enabled_button = False

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_checkBox and enabled_proj_file)
        self.label_proj_file.setEnabled(enabled_checkBox and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_checkBox)
        self.label_proj_custom_lon.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.lineEdit_proj_custom_lon.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.lineEdit_proj_custom_lat.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.button.setEnabled(enabled_button)


# 2.2.导出为Shape
class NetworkExportShape(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "导出为Shape"
        self.width = 300
        self.height = 300
        self.format = ("Shape", "shp")
        self.mode = "shape"
        self.proj = None

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        self.file_proj, file_proj_info = Tools.read_file_proj()

        # 第一行：单选框
        self.radio_coord_1 = QRadioButton('笛卡尔坐标')
        # 第二行：单选框
        self.radio_coord_2 = QRadioButton('经纬度坐标')
        # 第三行：单选框
        self.radio_proj_file = QRadioButton('使用原投影')
        # 第四行：文本
        self.label_proj_file = QLabel(file_proj_info)
        # 第五行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义墨卡托投影')
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.lineEdit_proj_custom_lon = QLineEdit()
        horizontal_layout_lon = QHBoxLayout()
        horizontal_layout_lon.addWidget(self.label_proj_custom_lon)
        horizontal_layout_lon.addWidget(self.lineEdit_proj_custom_lon)
        # 第七行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.lineEdit_proj_custom_lat = QLineEdit()
        horizontal_layout_lat = QHBoxLayout()
        horizontal_layout_lat.addWidget(self.label_proj_custom_lat)
        horizontal_layout_lat.addWidget(self.lineEdit_proj_custom_lat)
        # 第八行：按钮
        self.button = QPushButton('导出')

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.lineEdit_proj_custom_lon.setValidator(validator_coord)
        self.lineEdit_proj_custom_lat.setValidator(validator_coord)

        # Box布局
        group_box = QGroupBox()
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(self.radio_proj_file)
        group_box_layout.addWidget(self.label_proj_file)
        group_box_layout.addWidget(self.radio_proj_custom)
        group_box_layout.addLayout(horizontal_layout_lon)
        group_box_layout.addLayout(horizontal_layout_lat)
        group_box.setLayout(group_box_layout)

        # 总体布局
        layout = QVBoxLayout()
        layout.addWidget(self.radio_coord_1)
        layout.addWidget(self.radio_coord_2)
        layout.addWidget(group_box)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.radio_coord_1.toggled.connect(self.monitor_state)
        self.radio_proj_custom.toggled.connect(self.monitor_state)
        self.lineEdit_proj_custom_lon.textChanged.connect(self.monitor_state)
        self.lineEdit_proj_custom_lat.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button.clicked.connect(partial(Tools.network_export, self))

        # 设置默认模式和初始状态
        self.radio_coord_1.setChecked(True)
        if bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"]):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 勾选框的状态
        enabled_coord = self.radio_coord_2.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"])
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()
        # 按钮状态
        enabled_button = True
        if enabled_coord and enabled_radio_proj:
            lon_0 = self.lineEdit_proj_custom_lon.text()
            lat_0 = self.lineEdit_proj_custom_lat.text()
            if not (lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90):
                enabled_button = False

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_coord and enabled_proj_file)
        self.label_proj_file.setEnabled(enabled_coord and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_coord)
        self.label_proj_custom_lon.setEnabled(enabled_coord and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lon.setEnabled(enabled_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lat.setEnabled(enabled_coord and enabled_radio_proj)
        self.button.setEnabled(enabled_button)


# 2.3.导出为GeoJson
class NetworkExportGeojson(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "导出为GeoJson"
        self.width = 300
        self.height = 300
        self.format = ("GeoJson", "geojson")
        self.mode = "geojson"
        self.proj = None

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        self.file_proj, file_proj_info = Tools.read_file_proj()

        # 第一行：单选框
        self.radio_coord_1 = QRadioButton('笛卡尔坐标')
        # 第二行：单选框
        self.radio_coord_2 = QRadioButton('经纬度坐标')
        # 第三行：单选框
        self.radio_proj_file = QRadioButton('使用原投影')
        # 第四行：文本
        self.label_proj_file = QLabel(file_proj_info)
        # 第五行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义墨卡托投影')
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.lineEdit_proj_custom_lon = QLineEdit()
        horizontal_layout_lon = QHBoxLayout()
        horizontal_layout_lon.addWidget(self.label_proj_custom_lon)
        horizontal_layout_lon.addWidget(self.lineEdit_proj_custom_lon)
        # 第七行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.lineEdit_proj_custom_lat = QLineEdit()
        horizontal_layout_lat = QHBoxLayout()
        horizontal_layout_lat.addWidget(self.label_proj_custom_lat)
        horizontal_layout_lat.addWidget(self.lineEdit_proj_custom_lat)
        # 第八行：按钮
        self.button = QPushButton('导出')

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.lineEdit_proj_custom_lon.setValidator(validator_coord)
        self.lineEdit_proj_custom_lat.setValidator(validator_coord)

        # Box布局
        group_box = QGroupBox()
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(self.radio_proj_file)
        group_box_layout.addWidget(self.label_proj_file)
        group_box_layout.addWidget(self.radio_proj_custom)
        group_box_layout.addLayout(horizontal_layout_lon)
        group_box_layout.addLayout(horizontal_layout_lat)
        group_box.setLayout(group_box_layout)

        # 总体布局
        layout = QVBoxLayout()
        layout.addWidget(self.radio_coord_1)
        layout.addWidget(self.radio_coord_2)
        layout.addWidget(group_box)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.radio_coord_1.toggled.connect(self.monitor_state)
        self.radio_proj_custom.toggled.connect(self.monitor_state)
        self.lineEdit_proj_custom_lon.textChanged.connect(self.monitor_state)
        self.lineEdit_proj_custom_lat.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button.clicked.connect(partial(Tools.network_export, self))

        # 设置默认模式和初始状态
        self.radio_coord_1.setChecked(True)
        if bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"]):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 勾选框的状态
        enabled_coord = self.radio_coord_2.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"])
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()
        # 按钮状态
        enabled_button = True
        if enabled_coord and enabled_radio_proj:
            lon_0 = self.lineEdit_proj_custom_lon.text()
            lat_0 = self.lineEdit_proj_custom_lat.text()
            if not (lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90):
                enabled_button = False

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_coord and enabled_proj_file)
        self.label_proj_file.setEnabled(enabled_coord and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_coord)
        self.label_proj_custom_lon.setEnabled(enabled_coord and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lon.setEnabled(enabled_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lat.setEnabled(enabled_coord and enabled_radio_proj)
        self.button.setEnabled(enabled_button)


# 2.4.导出为Unity
class NetworkExportUnity():
    def __init__(self):
        self.name = "导出为Unity"
        self.format = ("Unity", "json")
        self.mode = "unity"

        Tools.network_export(self)

    def close(self):
        pass


# 2.5.导出为Json
class NetworkExportJson(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "导出为Json"
        self.width = 300
        self.height = 200
        self.format = ("Json", "json")
        self.mode = "json"
        self.proj = None

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        self.file_proj, file_proj_info = Tools.read_file_proj()

        # 第一行：勾选框
        self.checkBox = QCheckBox('写入经纬度坐标')
        # 第二行：单选框
        self.radio_proj_file = QRadioButton('使用原投影')
        # 第三行：文本
        self.label_proj_file = QLabel(file_proj_info)
        # 第四行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义墨卡托投影')
        # 第五行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.lineEdit_proj_custom_lon = QLineEdit()
        horizontal_layout_lon = QHBoxLayout()
        horizontal_layout_lon.addWidget(self.label_proj_custom_lon)
        horizontal_layout_lon.addWidget(self.lineEdit_proj_custom_lon)
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.lineEdit_proj_custom_lat = QLineEdit()
        horizontal_layout_lat = QHBoxLayout()
        horizontal_layout_lat.addWidget(self.label_proj_custom_lat)
        horizontal_layout_lat.addWidget(self.lineEdit_proj_custom_lat)
        # 第七行：按钮
        self.button = QPushButton('导出')

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.lineEdit_proj_custom_lon.setValidator(validator_coord)
        self.lineEdit_proj_custom_lat.setValidator(validator_coord)

        # Box布局
        group_box = QGroupBox()
        group_box_layout = QVBoxLayout()
        group_box_layout.addWidget(self.radio_proj_file)
        group_box_layout.addWidget(self.label_proj_file)
        group_box_layout.addWidget(self.radio_proj_custom)
        group_box_layout.addLayout(horizontal_layout_lon)
        group_box_layout.addLayout(horizontal_layout_lat)
        group_box.setLayout(group_box_layout)

        # 总体布局
        layout = QVBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addWidget(group_box)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.checkBox.stateChanged.connect(self.monitor_state)
        self.radio_proj_custom.toggled.connect(self.monitor_state)
        self.lineEdit_proj_custom_lon.textChanged.connect(self.monitor_state)
        self.lineEdit_proj_custom_lat.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button.clicked.connect(partial(Tools.network_export, self))

        # 设置默认模式和初始状态
        if bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"]):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 勾选框的状态
        enabled_checkBox = self.checkBox.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"])
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()
        # 按钮状态
        enabled_button = True
        if enabled_checkBox and enabled_radio_proj:
            lon_0 = self.lineEdit_proj_custom_lon.text()
            lat_0 = self.lineEdit_proj_custom_lat.text()
            if not (lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90):
                enabled_button = False

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_checkBox and enabled_proj_file)
        self.label_proj_file.setEnabled(enabled_checkBox and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_checkBox)
        self.label_proj_custom_lon.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.lineEdit_proj_custom_lon.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.lineEdit_proj_custom_lat.setEnabled(enabled_checkBox and enabled_radio_proj)
        self.button.setEnabled(enabled_button)


# 3.1.创建路段
class NetworkEditCreate(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "创建路段"
        self.width = 300
        self.height = 150

        # 设置界面属性
        Tools.set_attribution(self)
        self.setGeometry(80, 200, self.width, self.height)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        # 第一行：文本、下拉框、文本、输入框
        self.label_laneCount = QLabel('车道数：')
        self.combo_laneCount = QComboBox()
        self.combo_laneCount.addItems(("1", "2", "3", "4", "5", "6", "7", "8"))
        self.combo_laneCount.setFixedWidth(100)
        self.label_laneWidth = QLabel('    车道宽度：')
        self.lineEdit_laneWidth = QLineEdit()
        self.lineEdit_laneWidth.setFixedWidth(100)
        self.label_laneWidth_meter = QLabel('m')
        horizontal_layout_1 = QHBoxLayout()
        horizontal_layout_1.addWidget(self.label_laneCount)
        horizontal_layout_1.addWidget(self.combo_laneCount)
        horizontal_layout_1.addWidget(self.label_laneWidth)
        horizontal_layout_1.addWidget(self.lineEdit_laneWidth)
        horizontal_layout_1.addWidget(self.label_laneWidth_meter)
        # 第二行：文本、输入框
        self.label_lanePoints = QLabel('路段中心线坐标：')
        self.lineEdit_lanePoints = QLineEdit()
        # self.lineEdit_lanePoints.setFixedWidth(100)
        horizontal_layout_2 = QHBoxLayout()
        horizontal_layout_2.addWidget(self.label_lanePoints)
        horizontal_layout_2.addWidget(self.lineEdit_lanePoints)
        # 第三行：按钮
        self.button = QPushButton('创建路段')

        # 限制输入框内容
        regex = QRegExp("^([0-9](\.[0-9]{0,2})?|10(\.0+)?)$")  # 限制为0~10的浮点数，两位小数
        validator = QRegExpValidator(regex)
        self.lineEdit_laneWidth.setValidator(validator)

        # 总体布局
        layout = QVBoxLayout()
        layout.addLayout(horizontal_layout_1)
        layout.addLayout(horizontal_layout_2)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.lineEdit_laneWidth.textChanged.connect(self.monitor_state)
        self.lineEdit_lanePoints.textChanged.connect(self.monitor_state)
        # 关联按钮与调用函数
        self.button.clicked.connect(self.create_link)

        # 设置默认模式和初始状态
        self.combo_laneCount.setCurrentIndex(2)
        self.lineEdit_laneWidth.setText("3.5")
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        laneWidth = self.lineEdit_laneWidth.text()
        laneWidth = bool(laneWidth) and float(laneWidth)>0
        # 按钮状态
        enabled_button = False
        try:
            lane_points = self.lineEdit_lanePoints.text()
            lane_points = lane_points.replace("，", ",").replace("；", ";").replace(" ", "")
            lane_points = lane_points.split(";")
            num = set([len([float(value) for value in point.split(",")]) for point in lane_points])
            if len(lane_points) >= 2 and (num == {2} or num == {3}) and laneWidth:
                enabled_button = True
        except:
            pass

        # 设置可用状态
        self.button.setEnabled(enabled_button)

    # 创建路段
    def create_link(self):
        iface = tessngIFace()
        netiface = iface.netInterface()

        laneCount = int(self.combo_laneCount.currentText())
        laneWidth = float(self.lineEdit_laneWidth.text())
        lanePoints = self.lineEdit_lanePoints.text()

        link_processing.createLink(netiface, laneCount, laneWidth, lanePoints)


# 4.导出车辆轨迹
class TrajectoryExport(QWidget):
    memory_params = {
        "is_coord": False,
        "is_json": False,
        "is_kafka": False,
        "coord_lon": None,
        "coord_lat": None,
        "json_path": os.getcwd(),
        "kafka_ip": None,
        "kafka_port": None,
        "kafka_topic": None
    }

    def __init__(self):
        super().__init__()
        self.name = "轨迹数据输出"
        self.width = 300
        self.height = 500

        # kafka有无问题
        self.kafka_is_ok = False

        # 设置界面属性
        Tools.set_attribution(self)
        # 设置界面布局
        self.set_layout()

    # 设置界面布局
    def set_layout(self):
        self.file_proj, file_proj_info = Tools.read_file_proj()

        # 第一行：勾选框
        self.checkBox_coord = QCheckBox('写入经纬度坐标')
        # 第二行：单选框
        self.radio_proj_file = QRadioButton('使用原投影')
        # 第三行：文本
        self.label_proj_file = QLabel(file_proj_info)
        # 第四行：单选框
        self.radio_proj_custom = QRadioButton('使用自定义墨卡托投影')
        # 第五行：文本和输入框，使用水平布局
        self.label_proj_custom_lon = QLabel('投影中心经度：')
        self.lineEdit_proj_custom_lon = QLineEdit()
        horizontal_layout_lon = QHBoxLayout()
        horizontal_layout_lon.addWidget(self.label_proj_custom_lon)
        horizontal_layout_lon.addWidget(self.lineEdit_proj_custom_lon)
        # 第六行：文本和输入框，使用水平布局
        self.label_proj_custom_lat = QLabel('投影中心纬度：')
        self.lineEdit_proj_custom_lat = QLineEdit()
        horizontal_layout_lat = QHBoxLayout()
        horizontal_layout_lat.addWidget(self.label_proj_custom_lat)
        horizontal_layout_lat.addWidget(self.lineEdit_proj_custom_lat)
        # 第七行：勾选框
        self.checkBox_json = QCheckBox('保存为JSON文件')
        # 第八行：文本和按钮
        self.lineEdit_json = QLineEdit()
        self.lineEdit_json.setFixedWidth(500)
        self.button_json_save = QPushButton('选择保存位置')
        horizontal_layout_json = QHBoxLayout()
        horizontal_layout_json.addWidget(self.lineEdit_json)
        horizontal_layout_json.addWidget(self.button_json_save)
        # 第九行：勾选框
        self.checkBox_kafka = QCheckBox('上传至kafka')
        # 第十行：文本和输入框
        self.label_kafka_ip = QLabel('IP：')
        self.lineEdit_kafka_ip = QLineEdit()
        self.label_kafka_port = QLabel('端口：')
        self.lineEdit_kafka_port = QLineEdit()
        horizontal_layout_kafka_ip = QHBoxLayout()
        horizontal_layout_kafka_ip.addWidget(self.label_kafka_ip)
        horizontal_layout_kafka_ip.addWidget(self.lineEdit_kafka_ip)
        horizontal_layout_kafka_ip.addWidget(self.label_kafka_port)
        horizontal_layout_kafka_ip.addWidget(self.lineEdit_kafka_port)
        # 第十一行：文本和输入框
        self.label_kafka_topic = QLabel('topic：')
        self.lineEdit_kafka_topic = QLineEdit()
        self.button_check_kafka = QPushButton('核验')
        self.label_check_info = QLabel('待核验')
        horizontal_layout_kafka_topic = QHBoxLayout()
        horizontal_layout_kafka_topic.addWidget(self.label_kafka_topic)
        horizontal_layout_kafka_topic.addWidget(self.lineEdit_kafka_topic)
        horizontal_layout_kafka_topic.addWidget(self.button_check_kafka)
        horizontal_layout_kafka_topic.addWidget(self.label_check_info)
        # 第十二行：按钮
        self.button = QPushButton('确定')

        # 限制输入框内容
        validator_coord = QDoubleValidator()
        self.lineEdit_proj_custom_lon.setValidator(validator_coord)
        self.lineEdit_proj_custom_lat.setValidator(validator_coord)
        validator_kafka_port = QIntValidator()
        self.lineEdit_kafka_port.setValidator(validator_kafka_port)
        regex = QRegExp("^[a-zA-Z][a-zA-Z0-9_]*$")
        validator_kafka_topic = QRegExpValidator(regex)
        self.lineEdit_kafka_topic.setValidator(validator_kafka_topic)

        # Box布局 坐标
        group_box_coord = QGroupBox()
        group_box_coord_layout = QVBoxLayout()
        group_box_coord_layout.addWidget(self.radio_proj_file)
        group_box_coord_layout.addWidget(self.label_proj_file)
        group_box_coord_layout.addWidget(self.radio_proj_custom)
        group_box_coord_layout.addLayout(horizontal_layout_lon)
        group_box_coord_layout.addLayout(horizontal_layout_lat)
        group_box_coord.setLayout(group_box_coord_layout)

        # Box布局 JSON
        group_box_json = QGroupBox()
        group_box_json_layout = QVBoxLayout()
        group_box_json_layout.addLayout(horizontal_layout_json)
        group_box_json.setLayout(group_box_json_layout)

        # Box布局 kafka
        group_box_kafka = QGroupBox()
        group_box_kafka_layout = QVBoxLayout()
        group_box_kafka_layout.addLayout(horizontal_layout_kafka_ip)
        group_box_kafka_layout.addLayout(horizontal_layout_kafka_topic)
        group_box_kafka.setLayout(group_box_kafka_layout)

        # 总体布局
        layout = QVBoxLayout()
        layout.addWidget(self.checkBox_coord)
        layout.addWidget(group_box_coord)
        layout.addWidget(self.checkBox_json)
        layout.addWidget(group_box_json)
        layout.addWidget(self.checkBox_kafka)
        layout.addWidget(group_box_kafka)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 设置关联关系
        # 监测组件变动
        self.checkBox_coord.stateChanged.connect(self.monitor_state)
        self.radio_proj_custom.toggled.connect(self.monitor_state)
        self.lineEdit_proj_custom_lon.textChanged.connect(self.monitor_state)
        self.lineEdit_proj_custom_lat.textChanged.connect(self.monitor_state)
        self.checkBox_json.stateChanged.connect(self.monitor_state)
        self.lineEdit_json.textChanged.connect(self.monitor_state)
        self.checkBox_kafka.stateChanged.connect(self.monitor_state)
        self.lineEdit_kafka_ip.textChanged.connect(self.monitor_state)
        self.lineEdit_kafka_port.textChanged.connect(self.monitor_state)
        self.lineEdit_kafka_topic.textChanged.connect(self.monitor_state)
        self.lineEdit_kafka_ip.textChanged.connect(self.monitor_kafka)
        self.lineEdit_kafka_port.textChanged.connect(self.monitor_kafka)
        self.lineEdit_kafka_topic.textChanged.connect(self.monitor_kafka)
        # 关联按钮与调用函数
        self.button_json_save.clicked.connect(self.select_folder)
        self.button_check_kafka.clicked.connect(self.check_kafka)
        self.button.clicked.connect(self.save_config)

        # 设置默认模式和初始状态
        if TrajectoryExport.memory_params["is_coord"]:
            self.checkBox_coord.setChecked(True)
        if TrajectoryExport.memory_params["is_json"]:
            self.checkBox_json.setChecked(True)
        if TrajectoryExport.memory_params["is_kafka"]:
            self.checkBox_kafka.setChecked(True)
        if TrajectoryExport.memory_params["coord_lon"] is not None:
            self.lineEdit_proj_custom_lon.setText(str(TrajectoryExport.memory_params["coord_lon"]))
            self.lineEdit_proj_custom_lat.setText(str(TrajectoryExport.memory_params["coord_lat"]))
        if TrajectoryExport.memory_params["json_path"] is not None:
            self.lineEdit_json.setText(TrajectoryExport.memory_params["json_path"])
        if TrajectoryExport.memory_params["kafka_ip"] is not None:
            self.lineEdit_kafka_ip.setText(str(TrajectoryExport.memory_params["kafka_ip"]))
            self.lineEdit_kafka_port.setText(str(TrajectoryExport.memory_params["kafka_port"]))
            self.lineEdit_kafka_topic.setText(str(TrajectoryExport.memory_params["kafka_topic"]))
        # 投影
        if bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"]):
            self.radio_proj_file.setChecked(True)
        else:
            self.radio_proj_custom.setChecked(True)
        self.monitor_state()

    # 监测各组件状态，切换控件的可用状态
    def monitor_state(self):
        # 勾选框的状态
        enabled_checkBox_coord = self.checkBox_coord.isChecked()
        # 文件投影的状态
        enabled_proj_file = bool(self.file_proj["lon_0"]) and bool(self.file_proj["lat_0"])
        # 选择投影方式的状态
        enabled_radio_proj = self.radio_proj_custom.isChecked()

        # 设置可用状态
        self.radio_proj_file.setEnabled(enabled_checkBox_coord and enabled_proj_file)
        self.label_proj_file.setEnabled(enabled_checkBox_coord and enabled_proj_file and not enabled_radio_proj)
        self.radio_proj_custom.setEnabled(enabled_checkBox_coord)
        self.label_proj_custom_lon.setEnabled(enabled_checkBox_coord and enabled_radio_proj)
        self.label_proj_custom_lat.setEnabled(enabled_checkBox_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lon.setEnabled(enabled_checkBox_coord and enabled_radio_proj)
        self.lineEdit_proj_custom_lat.setEnabled(enabled_checkBox_coord and enabled_radio_proj)

        ##############################

        # 勾选框的状态
        enabled_checkBox_json = self.checkBox_json.isChecked()

        # 设置可用状态
        self.lineEdit_json.setEnabled(enabled_checkBox_json)
        self.button_json_save.setEnabled(enabled_checkBox_json)

        ##############################

        # 勾选框的状态
        enabled_checkBox_kafka = self.checkBox_kafka.isChecked()

        # 设置可用状态
        self.label_kafka_ip.setEnabled(enabled_checkBox_kafka)
        self.lineEdit_kafka_ip.setEnabled(enabled_checkBox_kafka)
        self.label_kafka_port.setEnabled(enabled_checkBox_kafka)
        self.lineEdit_kafka_port.setEnabled(enabled_checkBox_kafka)
        self.label_kafka_topic.setEnabled(enabled_checkBox_kafka)
        self.lineEdit_kafka_topic.setEnabled(enabled_checkBox_kafka)
        self.button_check_kafka.setEnabled(enabled_checkBox_kafka)
        self.label_check_info.setEnabled(enabled_checkBox_kafka)

        ##############################

        # 设置按钮可用状态
        proj_state = False
        if not enabled_checkBox_coord:
            proj_state = True
        elif enabled_checkBox_coord and not enabled_radio_proj and enabled_proj_file:
            proj_state = True
        elif enabled_checkBox_coord and enabled_radio_proj:
            lon_0 = self.lineEdit_proj_custom_lon.text()
            lat_0 = self.lineEdit_proj_custom_lat.text()
            if lon_0 and lat_0 and -180 < float(lon_0) < 180 and -90 < float(lat_0) < 90:
                proj_state = True

        # json有无问题
        folder_path = self.lineEdit_json.text()
        isdir = os.path.isdir(folder_path)
        json_state = (not enabled_checkBox_json) or (enabled_checkBox_json and isdir)
        if not (enabled_checkBox_json and isdir):
            GlobalVar.traj_json_config = None

        # kafka有无问题
        kafka_state = (not enabled_checkBox_kafka) or (enabled_checkBox_kafka and self.kafka_is_ok)

        # 三个都没问题
        self.button.setEnabled(proj_state and json_state and kafka_state)

    # 监测各组件状态，切换控件的可用状态
    def monitor_kafka(self):
        self.kafka_is_ok = False
        self.label_check_info.setText("待核验")
        # 更新状态
        self.monitor_state()

    # 选择JSON保存文件夹
    def select_folder(self):
        folder_path = Tools.open_folder()
        if folder_path:
            # 显示文件路径在LineEdit中
            self.lineEdit_json.setText(folder_path)

    # 核验kafka
    def check_kafka(self):
        self.label_check_info.setText("核验中…")
        # 立刻更新界面
        QCoreApplication.processEvents()

        ip = self.lineEdit_kafka_ip.text()
        port = self.lineEdit_kafka_port.text()
        topic = self.lineEdit_kafka_topic.text()

        # 核验IP
        ip_is_ok = False
        if ip:
            try:
                ip_address(ip)
                ip_is_ok = True
            except:
                Tools.show_info_box("请输入正确的IPv4地址", "warning")
                return
        else:
            Tools.show_info_box("请输入IPv4地址", "warning")
            return
        # 核验端口
        port_is_ok = False
        if port:
            if int(port) > 0:
                port_is_ok = True
            else:
                Tools.show_info_box("请输入大于0的端口号", "warning")
                return
        else:
            Tools.show_info_box("请输入端口号", "warning")
            return
        # 核验topic
        topic_is_ok = False
        if topic:
            topic_is_ok = True
        else:
            Tools.show_info_box("请输入topic", "warning")
            return

        kafka_pull_is_ok = self.check_kafka_pull(ip, port, topic)

        # 如果都没问题
        if ip_is_ok and port_is_ok and topic_is_ok and kafka_pull_is_ok:
            self.kafka_is_ok = True
            self.label_check_info.setText("核验成功")
        else:
            self.kafka_is_ok = False
            self.label_check_info.setText("核验失败")

        # 更新状态
        self.monitor_state()

    # 核查kafka连通性
    def check_kafka_pull(self, ip, port, topic):
        kafka_pull_is_ok = False
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=f'{ip}:{port}',
                group_id='test_group',
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                consumer_timeout_ms=10000  # 设置拉取消息的超时时间为10秒
            )

            # 订阅topic并拉取消息
            messages = consumer.poll()

            if messages:
                kafka_pull_is_ok = True
                Tools.show_info_box("Kafka消息拉取测试成功！")
            else:
                Tools.show_info_box("Kafka消息拉取测试失败：未接收到消息")
        except Exception as e:
            Tools.show_info_box(f"Kafka消息拉取测试失败：{e}")
        try:
            consumer.close()
        except:
            pass

        return kafka_pull_is_ok

    # 确认键
    def save_config(self):
        # 获取投影
        if self.checkBox_coord.isChecked():
            TrajectoryExport.memory_params["is_coord"] = True
            if self.radio_proj_custom.isChecked():
                lon_0 = float(self.lineEdit_proj_custom_lon.text())
                lat_0 = float(self.lineEdit_proj_custom_lat.text())
                traj_proj = {"lon_0": lon_0, "lat_0": lat_0}
            else:
                traj_proj = self.file_proj
            TrajectoryExport.memory_params["coord_lon"] = traj_proj["lon_0"]
            TrajectoryExport.memory_params["coord_lat"] = traj_proj["lat_0"]
        else:
            TrajectoryExport.memory_params["is_coord"] = False
            traj_proj = self.file_proj

        if self.checkBox_json.isChecked():
            TrajectoryExport.memory_params["is_json"] = True
            traj_json_config = self.lineEdit_json.text()
            TrajectoryExport.memory_params["json_path"] = traj_json_config
        else:
            TrajectoryExport.memory_params["is_json"] = False
            traj_json_config = None

        if self.checkBox_kafka.isChecked() and self.kafka_is_ok:
            TrajectoryExport.memory_params["is_kafka"] = True
            ip = self.lineEdit_kafka_ip.text()
            port = self.lineEdit_kafka_port.text()
            topic = self.lineEdit_kafka_topic.text()
            traj_kafka_config = {
                "ip": ip,
                "port": port,
                "topic": topic
            }
            TrajectoryExport.memory_params["kafka_ip"] = ip
            TrajectoryExport.memory_params["kafka_port"] = port
            TrajectoryExport.memory_params["kafka_topic"] = topic
        else:
            TrajectoryExport.memory_params["is_kafka"] = False
            traj_kafka_config = None

        # 配置全局变量
        GlobalVar.traj_proj = traj_proj
        GlobalVar.traj_json_config = traj_json_config
        GlobalVar.traj_kafka_config = traj_kafka_config

        # 关闭窗口
        self.close()


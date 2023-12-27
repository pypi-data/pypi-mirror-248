import os
import json
import threading
from datetime import datetime
from PySide2.QtCore import QObject, Signal

from ..DLLs.Tessng import PyCustomerSimulator, tessngIFace, p2m
from ..Toolbox.traj_output.get_traj_data import get_traj_data
from ..Toolbox.traj_output.kafka_producer import KafkaMessageProducer
from ..Tessng.MyMenu import GlobalVar


class MySimulator(QObject, PyCustomerSimulator):
    signalRunInfo = Signal(str)
    forStopSimu = Signal()
    forReStartSimu = Signal()

    def __init__(self):
        QObject.__init__(self)
        PyCustomerSimulator.__init__(self)

        self.traj_proj = None
        self.json_save_path = None
        self.kafka_producer = None
        self.kafka_send_thread = None

    # 仿真开始前
    def ref_beforeStart(self, ref_keepOn):
        iface = tessngIFace()
        simuiface = iface.simuInterface()

        # # 设置仿真精度
        # simuiface.setSimuAccuracy(5)

        # 投影
        traj_proj = GlobalVar.traj_proj
        if traj_proj and traj_proj["lon_0"] and traj_proj["lat_0"]:
            self.traj_proj = GlobalVar.traj_proj

        # JSON
        traj_json_config = GlobalVar.traj_json_config
        if traj_json_config:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M%S")
            folder_path = os.path.join(traj_json_config, f"标准格式车辆轨迹_{formatted_time}")
            print(folder_path)
            # 创建文件夹
            os.makedirs(folder_path, exist_ok=True)
            self.json_save_path = os.path.join(folder_path, "{}.json")

        # kafka
        traj_kafka_config = GlobalVar.traj_kafka_config
        if traj_kafka_config:
            ip = traj_kafka_config["ip"]
            port = traj_kafka_config["port"]
            topic = traj_kafka_config["topic"]
            self.kafka_producer = KafkaMessageProducer(f"{ip}:{port}", topic)
            # 使用线程来发送，不会阻塞主进程，不知道是否发送成功
            self.kafka_send_thread = threading.Thread(target=self.kafka_producer.send_message, args=())
            self.kafka_send_thread.start()

    # 仿真结束后
    def afterStop(self):
        self.traj_proj = None
        self.json_save_path = None
        if self.kafka_producer:
            if self.kafka_send_thread:
                self.kafka_producer.flag_stop_send = True
                self.kafka_send_thread.join()
                self.kafka_send_thread = None
            self.kafka_producer.close()
            self.kafka_producer = None

    # 每帧仿真后
    def afterOneStep(self):
        iface = tessngIFace()
        simuiface = iface.simuInterface()

        # 如果不需要导出，就不需要计算
        if not self.json_save_path and not self.kafka_producer:
            return

        # 轨迹数据计算和导出
        traj_data = get_traj_data(simuiface, self.traj_proj, p2m)

        # 需要保存为json
        if self.json_save_path:
            # 当前仿真计算批次
            batchNum = simuiface.batchNumber()
            file_path = self.json_save_path.format(batchNum)
            try:
                # 将JSON数据写入文件
                with open(file_path, 'w', encoding="utf-8") as file:
                    json.dump(traj_data, file, indent=4, ensure_ascii=False)
            except:
                pass

        # 需要上传至kafka
        if self.kafka_producer:
            traj_data_json = json.dumps(traj_data)
            self.kafka_producer.put_data(traj_data_json)



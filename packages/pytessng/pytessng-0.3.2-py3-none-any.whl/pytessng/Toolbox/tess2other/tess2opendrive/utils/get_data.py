from xml.dom import minidom
from .node import Doc
from .models import Junction, Connector, Road
try:
    from .....Tessng.MyMenu import ProgressDialog as pgd
except:
    class pgd: progress = lambda values, text="": values


def get_data(netiface, proj_center:tuple):
    # 遍历连接段
    connectors = []
    junctions = []
    areas = netiface.allConnectorArea()
    for ConnectorArea in pgd.progress(areas, '连接段数据保存中（1/2）'):
        junction = Junction(ConnectorArea)
        junctions.append(junction)
        for connector in ConnectorArea.allConnector():
            # 为所有的车道连接创建独立的 road，关联至 junction
            for laneConnector in connector.laneConnectors():
                connectors.append(Connector(laneConnector, junction))

    # 遍历路段
    roads = []
    links = netiface.links()
    for link in pgd.progress(links, '路段数据保存中（2/2）'):
        roads.append(Road(link))

    # 路网绘制成功后，写入xodr文件
    doc = Doc()
    # 如果有投影中心的信息
    if proj_center[0] and proj_center[1]:
        doc.init_doc(proj_center=proj_center)
    else:
        doc.init_doc()
    doc.add_junction(junctions)
    doc.add_road(roads + connectors)

    uglyxml = doc.doc.toxml()
    xml = minidom.parseString(uglyxml)
    xml_pretty_str = xml.toprettyxml()
    
    return xml_pretty_str
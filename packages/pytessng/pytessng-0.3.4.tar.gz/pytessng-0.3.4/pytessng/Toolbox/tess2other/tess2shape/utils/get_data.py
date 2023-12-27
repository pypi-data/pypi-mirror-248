import collections
from pyproj import Proj
from geopandas import GeoDataFrame
from shapely.geometry import LineString
from . import config
from .functions import p2m, qtpoint2point, point2latlon
try:
    from .....Tessng.MyMenu import ProgressDialog as pgd
except:
    class pgd: progress = lambda values, text="": values


def get_info(netiface):
    lane_action_type = config.lane_action_type

    lon_0 = config.lon_0
    lat_0 = config.lat_0
    # 有投影中心经纬度就转为经纬度，否则就用X/Y
    if lon_0 and lat_0:
        projection = Proj(f'+proj=tmerc +lon_0={lon_0} +lat_0={lat_0} +ellps=WGS84')
        isUseRealLoc = True
    else:
        isUseRealLoc = False

    # 创建路段的 GeoDataFrame 保存路段信息
    links = netiface.links()
    lane_features = []
    for link in pgd.progress(links, '路段数据保存中（1/2）'):
        link_id = link.id()
        for lane in link.lanes():
            lane_id = lane.id()
            lane_number = lane.number() + 1
            lane_type = lane_action_type.get(lane.actionType(), lane.actionType())
            lane_width = p2m(lane.width())
            lane_points = qtpoint2point(lane.centerBreakPoint3Ds())
            if isUseRealLoc:
                lane_points = point2latlon(lane_points, projection)
            feature = {
                'id': lane_id,
                'roadId': link_id,
                'laneNumber': lane_number,
                'type': lane_type,
                'width': lane_width,
                'geometry': LineString(lane_points)
            }
            lane_features.append(feature)
    lane_gdf = GeoDataFrame(lane_features, crs="EPSG:4326")

    # 创建连接段的 GeoDataFrame 保存连接段信息
    connectors = netiface.connectors()
    if connectors:
        connector_features = []
        for connector in pgd.progress(connectors, '连接段数据保存中（2/2）'):
            for lane_connector in connector.laneConnectors():
                from_lane_id = lane_connector.fromLane().id()
                to_lane_id = lane_connector.toLane().id()
                lane_points = qtpoint2point(lane_connector.centerBreakPoint3Ds())
                if isUseRealLoc:
                    lane_points = point2latlon(lane_points, projection)
                feature = {
                    'preLaneId': from_lane_id,
                    'sucLaneId': to_lane_id,
                    'geometry': LineString(lane_points)
                }
                connector_features.append(feature)
        connector_gdf = GeoDataFrame(connector_features, crs="EPSG:4326")
    else:
        connector_gdf = None
    
    return lane_gdf, connector_gdf

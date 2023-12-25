from .utils.my_class import OSMData, Network, NetworkCreator


def osm2tess(netiface, params):
    # params:
    # - osm_file_path
    # - bounding_box
    # - center_point

    # osm_file_path = "nanjing.osm"
    # bounding_box = {
    #     "lon_min": 113.80543,
    #     "lon_max": 114.34284,
    #     "lat_min": 29.69543,
    #     "lat_max": 31.84852,
    # }
    # center_point = {
    #     "lon_0": lon_0,
    #     "lat_0": lat_0,
    #     "distance": distance,
    # }

    osm_params = {
        "osm_file_path": params.get("osm_file_path"),
        "bounding_box": params.get("bounding_box"),
        "center_point": params.get("center_point"),
        "road_type": ["高速公路", "城市道路"],
        "projection": None,
    }
    # print(osm_params)

    # 获取数据
    osm_data = OSMData(osm_params).get_osm_data()
    # print(osm_data)
    # 解析数据
    network = Network(**osm_data)
    # network.draw()
    # 创建路网
    network_creator = NetworkCreator(netiface, network)
    
    return network_creator.error_message


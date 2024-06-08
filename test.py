import folium
from matplotlib import colormaps, pyplot as plt


def getmap(provinces, values):
    dict = [
        {"province": "上海", "lats": 31.230416, "lons": 121.473701},
        {"province": "云南", "lats": 24.679438, "lons": 102.832891},
        {"province": "内蒙古", "lats": 44.09333, "lons": 111.670801},
        {"province": "北京", "lats": 39.5424, "lons": 116.2351},
        {"province": "台湾", "lats": 23.69781, "lons": 120.960515},
        {"province": "吉林", "lats": 43.666368, "lons": 126.192314},
        {"province": "四川", "lats": 30.572269, "lons": 104.066541},
        {"province": "天津", "lats": 39.085111, "lons": 117.200983},
        {"province": "宁夏", "lats": 37.264608, "lons": 106.165917},
        {"province": "安徽", "lats": 31.861184, "lons": 117.284923},
        {"province": "山东", "lats": 36.682785, "lons": 117.020359},
        {"province": "山西", "lats": 37.877826, "lons": 112.562398},
        {"province": "广东", "lats": 23.132278, "lons": 113.266531},
        {"province": "广西", "lats": 22.815478, "lons": 108.327546},
        {"province": "新疆", "lats": 43.793026, "lons": 87.627704},
        {"province": "江苏", "lats": 32.061707, "lons": 118.767413},
        {"province": "江西", "lats": 28.676493, "lons": 115.892151},
        {"province": "河北", "lats": 38.045475, "lons": 114.502461},
        {"province": "河南", "lats": 34.757977, "lons": 113.665412},
        {"province": "浙江", "lats": 30.26555, "lons": 120.153576},
        {"province": "海南", "lats": 19.197625, "lons": 109.724438},
        {"province": "湖北", "lats": 30.584355, "lons": 114.298572},
        {"province": "湖南", "lats": 28.19409, "lons": 112.982279},
        {"province": "甘肃", "lats": 36.059089, "lons": 103.826308},
        {"province": "福建", "lats": 26.078498, "lons": 119.306239},
        {"province": "贵州", "lats": 26.647661, "lons": 106.630154},
        {"province": "辽宁", "lats": 41.835558, "lons": 123.429096},
        {"province": "重庆", "lats": 29.56301, "lons": 106.551556},
        {"province": "陕西", "lats": 34.265472, "lons": 108.954239},
        {"province": "青海", "lats": 36.625657, "lons": 101.780199},
        {"province": "黑龙江", "lats": 45.742347, "lons": 126.661669}
    ]

    # 从字典中提取经纬度
    lats = [d['lats'] for d in dict]
    lons = [d['lons'] for d in dict]

    # 创建地图对象
    map = folium.Map(location=[35, 105], zoom_start=4)

    # 使用matplotlib colormap生成颜色序列
    cmap = colormaps['viridis']  # 使用新方法访问colormap
    norm = plt.Normalize(min(values), max(values))  # 归一化values以便映射到颜色序列

    # 在地图上添加每个省份的标记
    for i, (province, value) in enumerate(zip(provinces, values)):
        province_data = next((d for d in dict if d["province"] == province), None)
        if province_data:
            lat, lon = province_data["lats"], province_data["lons"]
            # 根据value映射颜色
            color = cmap(norm(value))
            hex_color = '#{0:02x}{1:02x}{2:02x}'.format(*[int(c * 255) for c in color[:3]])

            folium.Circle(
                location=[lat, lon],
                radius=value * 1000,  # 根据数值调整半径大小
                color=hex_color,
                fill=True,
                fill_color=hex_color,
                fill_opacity=0.5
            ).add_child(folium.Popup(province + ': ' + str(value))).add_to(map)
        else:
            print(f"未找到省份 '{province}' 的经纬度数据")

    # 保存地图为HTML文件
    map.save('map.html')


# 示例用法
provinces = ['上海', '云南', '北京', '海南','贵州']
values = [500, 200, 200, 300,700]
getmap(provinces, values)

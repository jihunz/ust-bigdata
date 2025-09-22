import folium

# 안산 시청 중심 지도 생성
map = folium.Map(location=[37.322232, 126.830899], zoom_start=14)

# 마커 추가 - 안산 시청
folium.Marker(
    [37.322232, 126.830899],
    popup='안산 시청'
).add_to(map)

# 마커 추가 - 힐링저수지 (아이콘 변경 예시)
folium.Marker(
    [37.325571, 126.816793],
    popup='힐링저수지',
    icon=folium.Icon(icon='info-sign')
).add_to(map)


print(map)

map.save('folium_test.html')
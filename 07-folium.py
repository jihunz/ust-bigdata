import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import folium

try:
    plt.rc('font', family='NanumBarunGothic')
except Exception:
    pass

data = pd.read_csv('data/도로교통공단_전국사망교통사고.csv', encoding='euc-kr')  # csv 저장된 경로 기입
ansan = data[data['발생지시군구'] == '안산시']
split = data[['사고유형', '경도', '위도']]

accident_type = split['사고유형']
longitude = split['경도']
latitude = split['위도']

# for i in range(len(split)):
#     accident_type = split['사고유형']
#     longitude = split['경도']
#     latitude = split['위도']
#     print('{0} - {1} : {2}'.format(accident_type.iloc[i], longitude.iloc[i], latitude.iloc[i]))


folium_map = folium.Map(location=[37.322821, 126.830799], zoom_start=13)

for i in range(0, 42):
    location = [latitude.iloc[i], longitude.iloc[i]]
    folium.Marker(location, popup=accident_type.iloc[i], icon=folium.Icon(icon='glyphicon glyphicon-remove-sign')).add_to(folium_map)

folium_map.show_in_browser()

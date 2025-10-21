import pandas as pd
import matplotlib.pyplot as plt

try:
    plt.rc('font', family='NanumBarunGothic')
except Exception:
    pass

data = pd.read_csv('도로교통공단_시도_시군구별_교통사고.csv', encoding='euc-kr')  # csv 저장된 경로 기입

data_ac = data.sort_values(by=['발생건수'], ascending=False).iloc[:10]

fig, ax = plt.subplots()
x_value = data_ac['시군구']
y_value = data_ac['사망자수']

ax.bar(x_value, y_value)
ax.set_xlabel('사망자수')
ax.set_title('시군구별 사망자수')

plt.show()

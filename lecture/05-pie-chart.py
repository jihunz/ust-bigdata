import pandas as pd
import matplotlib.pyplot as plt

try:
    plt.rc('font', family='NanumBarunGothic')
except Exception:
    pass

data = pd.read_csv('도로교통공단_시도_시군구별_교통사고.csv', encoding='euc-kr')  # csv 저장된 경로 기입

data_bc = data.groupby(['시도'], as_index=False).sum()
data_cc = data_bc.sort_values(by=['사망자수'], ascending=False)[:5]

labels = data['시도']
sizes = data['사망자수']

fig, ax = plt.subplots()
explode = (0.1,) + (0,) * (len(sizes) - 1)
print(explode)

ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)

plt.show()

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

try:
    plt.rc('font', family='AppleGothic')
except Exception:
    pass

df = pd.read_csv('/Users/jihunjang/Downloads/ust/강의/bigdata/중간고사/도로교통공단_전국_사망교통사고정보(2018).csv',
                 encoding='euc-kr')
filter = ['차대차']
df_filtered = df[df['사고유형_대분류'].isin(filter)]
grouped = (df_filtered.groupby('발생지시도', as_index=False)['사망자수'].sum().sort_values('사망자수', ascending=False))

result = grouped.head(5)

plt.figure()
plt.bar(result['발생지시도'], result['사망자수'])
plt.title('차대차 사망자수 Top 5 시도')
plt.xlabel('발생지시도')
plt.ylabel('사망자수')
plt.tight_layout()
plt.show()

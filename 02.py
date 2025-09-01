# 활용실습 1
num1 = [33 if i == 3 else i for i in range(1,11)]
num2 = [v for v in num1 if 6 <= v <= 10]
print(num2)

# 활용실습 2
sum = 0
for i in range(1, 101):
    if i % 3 == 0:
        sum += i
print(sum)

# 활용실습 3
for i in range(1, 11):
    for k in range(1, 11):
        equation = (4*i) + (5*k)
        if equation == 60:
            print(i , k)
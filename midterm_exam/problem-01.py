if __name__ == '__main__':
    width = 7
    for i in range(1, width + 1, 2):
        star = '*'
        print(f'{star * i:^{width}}')
        print('\n')

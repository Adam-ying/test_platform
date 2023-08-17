import os
import time


def t():
    if True:
        pass
    else:
        print('dasdasda')

    print('dasdasd1111')


def k(path):
    file_list = os.listdir(path)
    print(file_list[-1])

if __name__ == '__main__':
    print(time.time())
    time.sleep(1)
    print(time.time())

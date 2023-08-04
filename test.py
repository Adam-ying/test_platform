import os
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
    t()
    k('/Users/edz/PycharmProjects/test_platform/Proj/my_proj/Reports')
# 此文件用来测试每个功能模块
# 为防止文件路径以及其它问题，请在此文件内测试您的功能模块
from AIR.SM_load import GCS


if __name__ == '__main__':
    print('正在运行功能测试，注意不要使用在正式环境中')
    with open('AIR/HDF5/selfPIC.jpg', 'rb') as f:
        print(GCS().predict(f))


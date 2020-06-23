# *将图片转化为字符画并保存在txt文档中

from PIL import Image, ImageFilter
import numpy as np
import math
import time
import getpass


class NegativeError(Exception):
    pass


class NumError(Exception):
    pass


def imgConvert():
    #输入
    while True:
        try:
            filename = input('请输入文件名：')
            img = Image.open(filename)
            break
        except FileNotFoundError:
            print('文件未找到')
        except SyntaxError:
            print('文件类型错误')

    while True:
        try:
            times = float(input('请输入缩放倍数(缩小时倍数小于1，放大时倍数大于1):'))
            if times <= 0:
                raise NegativeError
            break
        except ValueError:
            print('缩放倍数不能有非数字符')
        except NegativeError:
            print('缩放倍数必须为一正实数')

    while True:
        try:
            enhance = int(input('请输入对比度增强等级（0~20）：'))
            if enhance < 0 or enhance > 20:
                raise NumError
            break
        except ValueError:
            print('对比度增强等级不能有非数字符')
        except NumError:
            print('对比度增强等级只能为0~20')

    while True:
        try:
            adjust = int(input('请输入亮度调整等级（-10~10）：'))
            if adjust < -10 or adjust > 10:
                raise NumError
            break
        except ValueError:
            print('亮度调整等级不能有非数字符')
        except NumError:
            print('等级范围错误')

    while True:
        try:
            sharpen = int(input('请输入锐化等级（0~10）：'))
            if sharpen < 0 or sharpen > 10:
                raise NumError
            break
        except ValueError:
            print('锐化等级不能有非数字符')
        except NumError:
            print('等级范围错误')

    str1 = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''
    
    #缩放
    print('缩放中')
    w = img.width
    h = img.height
    new_size = (int(w*times), int(h*times))
    img = img.resize(new_size)
    #转灰度图
    print('转换中')
    img_gray = img.convert('L')
    if sharpen > 0:
        for i in range(sharpen):
            img_gray = img_gray.filter(ImageFilter.SHARPEN)
    np_list = np.array(img_gray, 'f')

    txt_name_list = filename.split('.')
    txt_name = txt_name_list[0]+'.txt'
    
    #创建文本文件并打开
    f = open(txt_name, 'w')
    f.close()
    f = open(txt_name, 'a')
    
    #向文件中写入内容
    for line in np_list:
        for i in range(int(w*times*0.2)):
            f.write(' ')
        for num in line:
            #增强对比度
            if enhance != 0:
                grey = contrastEnhancement(num, enhance)
            else:
                grey = num
            #调整亮度
            if adjust == 0:
                pass
            else:
                grey = brightnessAdjustment(grey, adjust)
            #写入文件
            for j in range(2):
                f.write(str1[int((grey/255)*(len(str1)-1))])

        f.write('\n')
    #写入基本信息
    f.write('\n\n\n源文件：'+filename+'\n')
    f.write('缩放倍数：'+str(times)+'\n')
    f.write('对比度增强等级:'+str(enhance)+'\n')
    f.write('亮度调整等级:'+str(adjust)+'\n')
    f.write('锐化等级：'+str(sharpen)+'\n')
    f.write('由'+getpass.getuser()+'编辑于' +
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    f.close()

    print(f'转换结束，结果文件为{txt_name}')
    input('按回车键退出')


#对比度增强
def contrastEnhancement(num, key):
    if num <= 127:
        return int((num**key)/(127.5**(key-1)))
    else:
        return int(((127.5**(key-1))*(num-127.5))**(1/key)+127.5)


#亮度调整
def brightnessAdjustment(num, key):
    if key < 0:
        key = -key
        return int((num**key)/(255**(key-1)))
    else:
        return int(((255**(key-1))*num)**(1/key))


if __name__ == "__main__":
    imgConvert()

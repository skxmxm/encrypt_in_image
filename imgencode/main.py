import cv2 as cv
import matplotlib.image as plt


def img_encode(message, path):
    img = cv.imread(path)
    while img is None:
        path = input("图片不存在，请重新输入(或者请检查后缀名)：\n")
        img = cv.imread(path)
        if not path.endswith('.jpg'):
            path += '.jpg'
    em = message.encode("ascii")
    x, y = img.shape[:2]
    if x * y * 3 / 8 < len(message):
        print("需要加密的数据过大，本图片只能加载%d以下长度的文本，请重试\n" % x * y * 3 / 8)
        return
    now_x = 0
    now_y = 0
    now_c = 0
    for i in em:
        for j in range(8):
            c = int(i % 2)
            i = int(i / 2)
            if c != 0:
                if img[now_x][now_y][now_c] == 255:
                    img[now_x][now_y][now_c] -= 1
                else:
                    img[now_x][now_y][now_c] += 1
            now_c += 1
            if now_c == 3:
                now_y += 1
                now_c = 0
                if now_y == y:
                    now_x += 1
                    now_y = 0
                    if now_x == x:
                        raise "程序出错"
    new_path = ''
    new_path = input("请指定输出位置，直接回车则输出到原路径：\n")
    if new_path == '':
        while not path.endswith('.'):
            path = path[:-1]
        path = path[:-1]
        path = path + '_encrypted' + '.png'
        plt.imsave(path, img[:, :, ::-1])
    else:
        if not new_path.endswith('.png'):
            new_path += '.png'
        plt.imsave(new_path, img[:, :, ::-1])


def img_decode(encrypted, source):
    img1 = cv.imread(encrypted)
    img2 = cv.imread(source)
    if img1 is None or img2 is None:
        print("图片路径出错，请重新输入")
        return

    if img1.shape != img2.shape:
        print("两幅图像大小不一致，请检查是否选择正确\n")
        return
    x, y = img1.shape[:2]
    now_x = 0
    now_y = 0
    now_c = 0
    result = ''
    while True:
        c_int = 0
        for i in range(8):
            if img1[now_x][now_y][now_c] != img2[now_x][now_y][now_c]:
                c_int += 2 ** i
            now_c += 1
            if now_c == 3:
                now_y += 1
                now_c = 0
                if now_y == y:
                    now_x += 1
                    now_y = 0
                    if now_x == x:
                        raise "程序出错"
        if c_int == 0:
            break
        result += bytes([c_int]).decode('ascii')
    print("解密结果为：\n%s" % result)


if __name__ == '__main__':
    print("欢迎使用本程序！")
    while True:
        mode = input('请选择模式(1：加密文本，2：解密图像， q：退出):\n')
        if mode == 'q':
            break
        while mode not in ['1', '2']:
            mode = input("输入错误，请输入正确的模式：\n")
        if mode == '1':
            m = input("请输入想要加密的文本(不支持汉字)：\n")
            p = input("请输入想要承载加密文本的图片名称(jpg格式,请输入后缀名)：\n")
            img_encode(m, p)
        else:
            e = input("请输入想要解密的图像：\n")
            s = input("请输入原图像：\n")
            img_decode(e, s)
